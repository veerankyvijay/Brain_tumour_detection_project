# Brain tumour detection

A convolutional neural network (CNN) that classifies brain MRI scans into four classes, with a Tkinter desktop app to try it on your own images.

**Classes:** glioma, meningioma, pituitary tumour, no tumour.

## Results

| Measure | Value |
|---|---|
| Training accuracy (epoch 20 of 20) | 97.1% |
| Validation accuracy (epoch 19 / epoch 20) | 90.1% / 88.4% |
| Separate test evaluation in the notebook | 84.0% |

The gap between training and validation accuracy shows some overfitting. Validation loss rose in the last epochs (0.29 to 0.55), so earlier stopping or data augmentation is the next step.

## Dataset

[Brain Tumor Classification (MRI)](https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri) on Kaggle, version 2. Not included in this repo because of its size. Download it with `kagglehub` (see the notebook).

## How it works

1. Images are resized to 150 x 150 pixels and normalised.
2. The CNN (TensorFlow/Keras) predicts the tumour class.
3. For 3D NIfTI (`.nii`) scans, a second model estimates tumour volume in mm³ (experimental).
4. `gui1.py` wraps this in a Tkinter window: pick a file, enter patient name and age, see the result.

## Run it

```bash
pip install tensorflow opencv-python numpy pillow nibabel
python gui1.py
```

You need the trained weights `braintumor.h5` and `tumor_volume_model.h5` next to `model.json` and `tumor_volume_model.json`.

## Files

- `gui1.py`: desktop app
- `Untitled-checkpoint.ipynb`: training and evaluation
- `Untitled_brain_volume.ipynb`: volume estimation
- `Presentation10.pptx`: project slides

## Limits

A student project built during an internship at ICMR-NIRT. It is not a medical device and must not be used for diagnosis. The tumour "stage" output is a model guess from image features, not a clinical staging.
