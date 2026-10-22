"""Validate snippet registration, fields, prefix uniqueness, and Python syntax."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "package.json"
SNIPPET_FIELD = re.compile(r"\$\{\d+:([^}]*)\}|\$\{\d+\}|\$\d+")
PLACEHOLDER = re.compile(r"\$\{(?:\d+|[A-Z_][A-Z0-9_]*)(?::[^{}]*)?\}|\$\d+")


def main() -> int:
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    for json_path in ROOT.rglob("*.json"):
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"{json_path.relative_to(ROOT)}: invalid JSON: {exc}", file=sys.stderr)
            return 1
    registered = {
        (ROOT / item["path"]).resolve()
        for item in package.get("contributes", {}).get("snippets", [])
    }
    registrations = package.get("contributes", {}).get("snippets", [])
    files = sorted((ROOT / "snippets").glob("*.json"))
    errors: list[str] = []
    prefixes: dict[str, Path] = {}
    category_counts: dict[str, int] = {}
    total = 0

    if set(files) != registered:
        errors.append(
            "Registered snippet files do not match snippets/*.json: "
            f"unregistered={sorted(str(p.relative_to(ROOT)) for p in set(files) - registered)}, "
            f"missing={sorted(str(p.relative_to(ROOT)) for p in registered - set(files))}"
        )
    if len(registrations) != len(registered):
        errors.append("package.json contains duplicate snippet file registrations")
    for item in registrations:
        if item.get("language") != "python":
            errors.append(f"Snippet target language must be python: {item}")

    for path in files:
        try:
            snippets = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        category_counts[path.stem] = len(snippets)
        total += len(snippets)
        for title, snippet in snippets.items():
            prefix = snippet.get("prefix")
            description = snippet.get("description")
            if not isinstance(title, str) or not title.strip():
                errors.append(f"{path.name}: snippet title must be non-empty")
            if not isinstance(prefix, str) or not prefix.strip():
                errors.append(f"{path.name}: {title!r} prefix must be non-empty")
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{path.name}: {title!r} missing title, prefix, or description")
                continue
            if prefix in prefixes:
                errors.append(
                    f"duplicate prefix {prefix!r}: {prefixes[prefix].name} and {path.name}"
                )
            prefixes[prefix] = path
            if not isinstance(snippet.get("body"), list) or not snippet["body"] or not all(
                isinstance(line, str) for line in snippet["body"]
            ):
                errors.append(f"{path.name}: {prefix} body must be a non-empty array of strings")
                continue
            if not any(line.strip() for line in snippet["body"]):
                errors.append(f"{path.name}: {prefix} body must contain non-empty text")

            expanded = "\n".join(snippet["body"])
            if PLACEHOLDER.sub("", expanded).find("$") >= 0:
                errors.append(f"{path.name}: {prefix} contains a malformed VS Code placeholder")
            expanded = SNIPPET_FIELD.sub(lambda match: match.group(1) or "", expanded)
            try:
                compile(expanded, f"{path.name}:{prefix}", "exec")
            except SyntaxError as exc:
                errors.append(
                    f"{path.name}: {prefix} is not valid expanded Python at "
                    f"line {exc.lineno}: {exc.msg}"
                )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for path, count in category_counts.items():
        row = re.search(
            rf"`snippets/{re.escape(path)}\.json`\s*\|\s*(\d+)\s*\|", readme
        )
        if row is None or int(row.group(1)) != count:
            errors.append(f"README category count does not match snippets/{path}.json")
    total_row = re.search(r"\| \*\*Total\*\* \|\s*\*{0,2}(\d+)\*{0,2}\s*\|", readme)
    if total_row is None or int(total_row.group(1)) != total:
        errors.append("README total snippet count does not match the library")

    print(f"Snippet total: {total}")
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    print(f"Unique prefixes: {len(prefixes)}")
    if errors:
        print("Validation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("JSON, schema, registration, uniqueness, and expanded Python syntax: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
