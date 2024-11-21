import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Image Processing")
root.geometry("1420x880")

image_frame = tk.Frame(root)
image_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

image_panel_original = None
image_panel_modified = None
original_image = None

def load_image():
    global original_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        show_original_image()

def show_original_image():
    if original_image is not None:
        show_image(original_image, 'original')

def show_modified_image(image):
    show_image(image, 'modified')

def show_image(image, panel_type):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image)

    aspect_ratio = image_pil.width / image_pil.height
    if aspect_ratio > 1: 
        new_width = 300
        new_height = int(new_width / aspect_ratio)
    else:  
        new_height = 300
        new_width = int(new_height * aspect_ratio)

    image_resized = image_pil.resize((new_width, new_height), Image.ANTIALIAS) 
    image_tk = ImageTk.PhotoImage(image_resized)

    if panel_type == 'original':
        global image_panel_original
        if image_panel_original is None:
            image_panel_original = tk.Label(image_frame, image=image_tk)
            image_panel_original.image = image_tk
            image_panel_original.pack(pady=10)
        else:
            image_panel_original.configure(image=image_tk)
            image_panel_original.image = image_tk
    else:
        global image_panel_modified
        if image_panel_modified is None:
            image_panel_modified = tk.Label(image_frame, image=image_tk)
            image_panel_modified.image = image_tk
            image_panel_modified.pack(pady=10)
        else:
            image_panel_modified.configure(image=image_tk)
            image_panel_modified.image = image_tk

def apply_laplacian_filter():
    if original_image is not None:
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        laplacian_image = cv2.Laplacian(gray_image, cv2.CV_64F)
        laplacian_image = np.uint8(np.abs(laplacian_image))
        show_modified_image(laplacian_image)
    else:
        messagebox.showwarning("Warning", "Please load an image first.")

def local_thresholding():
    if original_image is not None:
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        show_modified_image(adaptive_thresh)
    else:
        messagebox.showwarning("Warning", "Please load an image first.")

def local_thresh():
    if original_image is not None:
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        show_modified_image(adaptive_thresh)
    else:
        messagebox.showwarning("Warning", "Please load an image first.")


upload_button = tk.Button(button_frame, text="Load Image", command=load_image, width=20)
upload_button.pack(pady=5)

laplacian_button = tk.Button(button_frame, text="Apply Laplacian Filter", command=apply_laplacian_filter, width=20)
laplacian_button.pack(pady=5)

threshold_button = tk.Button(button_frame, text="Apply Adaptive Thresholding", command=local_thresholding, width=20)
threshold_button.pack(pady=5)

threshold_button1 = tk.Button(button_frame, text="Apply Gaussian Adaptive Thresholding", command=local_thresh, width=20)
threshold_button1.pack(pady=5)


root.mainloop()