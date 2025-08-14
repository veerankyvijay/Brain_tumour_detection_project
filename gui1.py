import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import nibabel as nib
import cv2

# Load the model and architecture
def load_model(model_file, json_file):
    with open(json_file, 'r') as json_file:
        loaded_model_json = json_file.read()
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights(model_file)
    return loaded_model

# Preprocess the image for model prediction
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (150, 150))  # Resize to match model input size
    img = img.astype('float32') / 255.0  # Normalize
    img = np.expand_dims(img, axis=0)  # Reshape for batch processing
    return img

# Preprocess the NIfTI file for volume calculation
def preprocess_nii(nii_path):
    nii_image = nib.load(nii_path)
    data = nii_image.get_fdata()
    voxel_size = nib.load(nii_path).header.get_zooms()  # Get voxel dimensions
    return data, voxel_size

# Calculate tumor volume from NIfTI data
def calculate_volume(data, voxel_size):
    binary_mask = data > 0.5  # Threshold for tumor segmentation
    volume = np.sum(binary_mask) * np.prod(voxel_size)  # Calculate volume
    return volume

# Predict tumor type, stage, and volume
def predict_tumor():
    if not image_path and not nii_path:
        messagebox.showerror("Error", "Please upload an MRI image or NIfTI file!")
        return
    
    result_text = f"Patient: {saved_patient_name}\nAge: {saved_patient_age}\n"

    # Handle image file prediction
    if image_path:
        img_array = preprocess_image(image_path)
        prediction = tumor_model.predict(img_array)
        predicted_index = np.argmax(prediction)

        # Map prediction index to labels
        tumor_types = ['Glioma Tumor', 'Meningioma Tumor', 'No Tumor', 'Pituitary Tumor']
        tumor_stages = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4']

        tumor_name = tumor_types[predicted_index]
        tumor_stage = tumor_stages[predicted_index]

        result_text += f"Tumor Detected: {tumor_name}\nStage: {tumor_stage}\n"

    # Handle NIfTI file volume calculation
    if nii_path:
        data, voxel_size = preprocess_nii(nii_path)
        tumor_volume = calculate_volume(data, voxel_size)
        result_text += f"Tumor Volume: {tumor_volume:.2f} mm³\n"

    messagebox.showinfo("Prediction Result", result_text)

# Function to upload an MRI image
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if image_path:
        img = Image.open(image_path)
        img = img.resize((200, 200))  # Resize to fit panel
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        panel.image = img

# Function to upload a NIfTI file
def upload_nii():
    global nii_path
    nii_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii")])
    if nii_path:
        messagebox.showinfo("File Uploaded", "NIfTI file uploaded successfully!")

# Welcome screen
def welcome_screen():
    intro_label = tk.Label(window, text="Welcome to Brain Tumor Detection", font=("Arial", 20, "bold"))
    intro_label.pack(pady=50)
    next_button = tk.Button(window, text="Next", font=("Arial", 16), command=patient_details_screen)
    next_button.pack()

# Screen to take patient details
def patient_details_screen():
    for widget in window.winfo_children():
        widget.destroy()
    
    name_label = tk.Label(window, text="Enter Patient's Name:", font=("Arial", 14))
    name_label.pack(pady=10)
    
    global patient_name
    patient_name = tk.Entry(window, font=("Arial", 14))
    patient_name.pack(pady=10)

    age_label = tk.Label(window, text="Enter Patient's Age:", font=("Arial", 14))
    age_label.pack(pady=10)

    global patient_age
    patient_age = tk.Entry(window, font=("Arial", 14))
    patient_age.pack(pady=10)

    next_button = tk.Button(window, text="Next", font=("Arial", 14), command=save_patient_details)
    next_button.pack(pady=20)

# Save the patient details
def save_patient_details():
    global saved_patient_name, saved_patient_age
    saved_patient_name = patient_name.get()
    saved_patient_age = patient_age.get()

    if not saved_patient_name or not saved_patient_age:
        messagebox.showerror("Error", "Please fill in both name and age.")
    else:
        show_upload_screen()

# Screen for uploading files
def show_upload_screen():
    for widget in window.winfo_children():
        widget.destroy()
    
    question_label = tk.Label(window, text="Upload Your MRI Report", font=("Arial", 18, "bold"))
    question_label.pack(pady=20)
    
    # Buttons to upload files
    upload_image_button = tk.Button(window, text="Upload Image File", command=upload_image, font=("Arial", 14))
    upload_image_button.pack(pady=10)

    upload_nii_button = tk.Button(window, text="Upload NIfTI File", command=upload_nii, font=("Arial", 14))
    upload_nii_button.pack(pady=10)

    # Image display panel
    global panel
    panel = tk.Label(window)
    panel.pack(pady=10)

    # Predict button
    detect_button = tk.Button(window, text="Predict", command=predict_tumor, font=("Arial", 14))
    detect_button.pack(pady=20)

# Main window setup
window = tk.Tk()
window.title("Brain Tumor Detection")
window.geometry("500x600")

# Load models
tumor_model = load_model('braintumor.h5', 'model.json')
nii_path = ""
image_path = ""
saved_patient_name = ""
saved_patient_age = ""

# Start with the welcome screen
welcome_screen()

# Start the GUI loop
window.mainloop()
