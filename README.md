🧠 Brain Tumor Detection & Analysis

This project is a Brain Tumor Detection and Analysis System that can:

Classify brain tumors into four types.

Identify the tumor stage.

Calculate tumor volume from MRI/NIfTI files.

Provide an interactive GUI for easy use by medical professionals or researchers.

🚀 Features

Tumor Type Classification – Detects whether the tumor is:

Glioma Tumor

Meningioma Tumor

Pituitary Tumor

No Tumor

Stage Prediction – Identifies the stage (Stage 1–4) based on image analysis.

Tumor Volume Estimation – Uses NIfTI MRI scan data to calculate the tumor volume in mm³.

User-Friendly GUI – Built with Tkinter for easy file uploads and prediction without coding knowledge.

Multi-Input Support – Accepts:

Standard MRI image formats (.jpg, .png)

NIfTI files (.nii) for 3D volumetric analysis.

🖥️ Tech Stack

Programming Language: Python

GUI: Tkinter

Machine Learning Framework: TensorFlow/Keras

Image Processing: OpenCV, NumPy, PIL

Medical Imaging: NiBabel (for NIfTI file handling)

📂 Project Structure
.
├── gui1.py                  # Main GUI application
├── braintumor.h5            # Trained classification model weights
├── model.json               # Classification model architecture
├── tumor_volume_model.h5    # Trained tumor volume prediction model weights
├── tumor_volume_model.json  # Volume prediction model architecture
├── Untitled_brain_volume.ipynb   # Notebook for tumor volume estimation
├── Untitled-checkpoint.ipynb     # Training/testing notebook
└── README.md                # Project documentation

⚙️ How It Works

Load Model – The application loads pre-trained deep learning models for tumor classification and volume estimation.

Preprocessing

Images are resized to 150x150 pixels and normalized.

NIfTI files are processed to extract voxel data and dimensions.

Prediction

MRI images → Predict tumor type & stage.

NIfTI files → Calculate tumor volume.

Output – Results are shown in a popup, including:

Patient Name & Age

Tumor Type

Stage

Volume (if available)
