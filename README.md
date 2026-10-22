# TensorFlow Keras Pro Snippets

A VS Code snippet extension for practical Python workflows with TensorFlow, `tf.keras`, standalone Keras, computer vision, NLP, and time-series data. It contains **163 snippets** across seven registered Python snippet files, with **163 unique prefixes**.

The snippets are editable starting points. They do not replace understanding your data, checking installed framework versions, or validating a complete model for your use case.

## Features

- Model building, compile choices, training callbacks, saving, loading, and inference.
- `tf.data` and image-directory input pipelines, dataset inspection, and performance diagnostics.
- Leakage-aware stratified, group-aware, and time-aware splitting patterns.
- Classification and regression evaluation, threshold selection, and residual diagnostics.
- Transfer learning and fine-tuning with MobileNetV2-specific preprocessing.
- TensorFlow debugging, profiling, reproducibility, and device diagnostics.

## Installation

### Install from the Visual Studio Marketplace

After the extension is published, open **Extensions** in VS Code and search for **TensorFlow Keras Pro Snippets**. You can also install it from a terminal:

```powershell
code --install-extension DevManish007.tensorflow-keras-pro-snippets
```

### Install a packaged VSIX

Download the `.vsix` file from the project's GitHub release. In VS Code, open **Extensions**, select **Views and More Actions (…)**, choose **Install from VSIX…**, and select the downloaded file.

You can also install a local VSIX from a terminal:

```powershell
code --install-extension .\tensorflow-keras-pro-snippets-0.1.0.vsix
```

The filename includes the package version; adjust it when installing a later release.

### Run from source

1. Open the project directory in VS Code.
2. Press `F5` to launch the Extension Development Host.
3. Create or open a Python (`.py`) file.
4. Type a prefix and select its completion. Use `Ctrl+Space` if suggestions are not visible.

This declarative snippet extension has no extension runtime or build dependency. Snippet examples may import optional Python packages such as TensorFlow, NumPy, Matplotlib, pandas, or scikit-learn; install those in the Python environment where you run the expanded code.

## Snippet categories

| File | Count | Coverage |
| --- | ---: | --- |
| `snippets/python.json` | 25 | Imports, setup, paths, files, configuration, logging, and experiment helpers |
| `snippets/datasets.json` | 21 | Directory datasets, `tf.data`, leakage-aware splits, preprocessing, and sequence data |
| `snippets/computer-vision.json` | 23 | Image preprocessing, augmentation, CNNs, predictions, and image evaluation |
| `snippets/training.json` | 40 | Keras models, compile and fit choices, evaluation, diagnostics, callbacks, and optimizers |
| `snippets/nlp-time-series.json` | 20 | Text vectorization and models, temporal splits, windows, and forecasting |
| `snippets/advanced.json` | 26 | Custom training, layers, metrics, serialization, profiling, diagnostics, and distribution |
| `snippets/transfer-learning.json` | 8 | MobileNetV2 image data, preprocessing, head training, fine-tuning, and inference |
| **Total** | **163** | |

## Screenshots

Screenshots are not available yet. This section will be updated when real screenshots of the extension in VS Code are ready.

## Example prefixes

These prefixes were checked against their snippet files:

| Prefix | File | Use |
| --- | --- | --- |
| `tf-import` | `python.json` | Import TensorFlow, NumPy, and Matplotlib |
| `sk-stratified-splits` | `datasets.json` | Preserve class ratios across train, validation, and test partitions |
| `cnn-classifier` | `computer-vision.json` | Build a compact multiclass CNN |
| `sk-binary-curves` | `training.json` | Plot binary ROC and precision-recall curves |
| `nlp-text-classifier` | `nlp-time-series.json` | Build a raw-text multiclass classifier |
| `tf-profile-fit` | `advanced.json` | Profile a bounded Keras training run |
| `tl-image-data` | `transfer-learning.json` | Load separate class-folder train, validation, and test datasets |

## Compatibility and data notes

- TensorFlow examples use `import tensorflow as tf` and `tf.keras`. Standalone Keras examples use `import keras`; avoid mixing objects across separate installations unless their selected backend and versions explicitly support it.
- TensorFlow/Keras examples use APIs such as `tf.keras.utils.image_dataset_from_directory` and modern preprocessing layers. Full models use `.keras` files; weights-only examples use `.weights.h5`. Keras 3 SavedModel export is shown separately from model saving.
- Fit normalization and vectorization statistics on training data only. Keep final test data out of model selection and threshold tuning. Group and time splits require IDs or correctly ordered history, respectively; choose a temporal gap appropriate to overlapping windows or the forecast horizon.
- Transfer-learning directory examples expect matching class subdirectories under `data/train`, `data/validation`, and `data/test`. The MobileNetV2 pretrained example can download ImageNet weights when run; the extension itself does not download models or datasets.
- GPU support, determinism, mixed precision, and export behavior depend on TensorFlow/Keras versions, backend, hardware, drivers, and platform. Exact reproducibility is not guaranteed across all environments.

## Validation and contributions

Run the static validator from the project root:

```powershell
python scripts/validate_snippets.py
```

It checks JSON parsing, required snippet fields, registration, unique prefixes, README counts, malformed placeholders, and Python syntax after replacing VS Code placeholders with their defaults. It does not execute every snippet or guarantee compatibility with every TensorFlow/Keras environment.

When contributing, place a distinct snippet in the most relevant file under `snippets/`. Give it a unique prefix, a clear description, and a body made of Python lines. Keep imports and required variables explicit, explain important data or label assumptions, and use VS Code placeholders for editable values. Update the category counts and examples in this README when the library changes. Register any new snippet file in `package.json` with the `python` language, then run the validator and manually check representative expansions in the Extension Development Host.

## License

This project is available under the [MIT License](LICENSE).

## References

- [TensorFlow API](https://www.tensorflow.org/api_docs/python/tf)
- [Keras API](https://keras.io/api/)
- [Keras guides](https://keras.io/guides/)
- [Keras saving and serialization](https://keras.io/guides/serialization_and_saving/)
