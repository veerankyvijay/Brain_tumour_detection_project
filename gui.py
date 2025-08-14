import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import cv2

# Load the model and the architecture
def load_model(model_file, json_file):
    # Load the model architecture
    with open(json_file, 'r') as json_file:
        loaded_model_json = json_file.read()
    # Load model from json file
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights(model_file)
    return loaded_model

# Preprocess the image for model prediction
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (150, 150))  # Resize to match model input size
    img = np.array(img)
    img = img.reshape(1, 150, 150, 3)  # Reshape for batch processing
    return img

# Predict tumor type and stage
def predict_tumor():
    if not image_path:
        messagebox.showerror("Error", "Please upload an MRI image!")
        return
    
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    
    # Map prediction index to labels
    tumor_types = ['Glioma Tumor', 'Meningioma Tumor', 'No Tumor', 'Pituitary Tumor']
    tumor_stages = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4']
    
    tumor_name = tumor_types[predicted_index]
    tumor_stage = tumor_stages[predicted_index]  # Mapping based on label for demonstration
    
    result_text = f"Patient: {saved_patient_name}\nAge: {saved_patient_age}\nTumor Detected: {tumor_name}\nStage: {tumor_stage}"
    messagebox.showinfo("Prediction Result", result_text)

# Function to upload and display the selected image
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    
    if image_path:
        img = Image.open(image_path)
        img = img.resize((200, 200))  # Resize to fit panel
        img = ImageTk.PhotoImage(img)
        
        panel.configure(image=img)
        panel.image = img

# Welcome screen
def welcome_screen():
    intro_label = tk.Label(window, text="Welcome to Vijay's Brain Tumor Detection", font=("Arial", 20, "bold"))
    intro_label.pack(pady=50)
    
    next_button = tk.Button(window, text="Next", font=("Arial", 16), command=patient_details_screen)
    next_button.pack()

# Screen to take patient details
def patient_details_screen():
    for widget in window.winfo_children():
        widget.destroy()  # Clear previous widgets
    
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

# Save the patient details before moving to the next screen
def save_patient_details():
    global saved_patient_name, saved_patient_age
    saved_patient_name = patient_name.get()
    saved_patient_age = patient_age.get()

    if not saved_patient_name or not saved_patient_age:
        messagebox.showerror("Error", "Please fill in both name and age.")
    else:
        show_upload_screen()

# Screen for uploading MRI image
def show_upload_screen():
    for widget in window.winfo_children():
        widget.destroy()  # Clear previous widgets
    
    question_label = tk.Label(window, text="Upload Your MRI Report Photo", font=("Arial", 18, "bold"))
    question_label.pack(pady=20)
    
    # Upload button
    upload_button = tk.Button(window, text="Upload MRI", command=upload_image, font=("Arial", 14))
    upload_button.pack(pady=20)

    # Image display panel
    global panel
    panel = tk.Label(window)
    panel.pack(pady=10)

    # Detect button
    detect_button = tk.Button(window, text="Detect Tumor", command=predict_tumor, font=("Arial", 14))
    detect_button.pack(pady=20)

# Main window setup
window = tk.Tk()
window.title("Brain Tumor Detection")
window.geometry("500x600")

# Load the model and architecture
model_file = 'braintumor.h5'  # Update if path is different
json_file = 'model.json'  # Update if path is different
model = load_model(model_file, json_file)
image_path = ""

saved_patient_name = ""
saved_patient_age = ""

# Start with the welcome screen
welcome_screen()

# Start the GUI loop
window.mainloop()
