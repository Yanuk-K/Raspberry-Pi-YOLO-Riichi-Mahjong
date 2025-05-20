from tkinter import *
from tkinter import messagebox
from picamera2 import Picamera2, Preview
from libcamera import controls
from ultralytics import YOLO
import time
import sys
import importlib.metadata
from PIL import Image, ImageTk

class YoloGrab:
    def __init__(self, master, model):
        self.new_window = master.TopLevel()
        self.new_window.title("Capture Image")
        self.new_window.geometry("400x300")
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.new_window.resizable(False, False)
        self.master = master
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.align()
        self.picam2.configure("preview")
        self.picam2.start()
        self.model = model
        self.result = None
        self.frame_label = None  # For video preview
        self.current_image = None  # To prevent garbage collection

    def capture_screen(self):
        root = Tk()
        root.geometry("450x350")

        label_picam_ver = Label(root, 
                                text="picamera2 ver: " + importlib.metadata.version('picamera2'),
                                anchor="e",)
        label_picam_ver.pack(fill = "x", padx=(10, 10), pady=10)

        labelframe = LabelFrame(root, text="Click button to capture image")
        labelframe.pack(fill = "both", expand = "yes")
        
        self.frame_label = Label(labelframe)
        self.frame_label.pack()

        capture_button = Button(labelframe, text ="Capture", command = self.capture_button_CallBack)
        capture_button.pack()
        
        self.update_video_stream()
        
    def update_video_stream(self):
        frame = self.picam2.capture_array()
        # Convert to PIL Image, then to ImageTk
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.current_image = imgtk  # Prevent garbage collection
        self.frame_label.config(image=imgtk)
        # Schedule next frame update
        self.frame_label.after(30, self.update_video_stream)

    def capture_button_CallBack(self):
        print("- Capture image -")
        frame = self.picam2.capture_array()
        self.result = self.model(frame)
        self.on_closing()

    def on_closing(self):
    # if preview window cloased before,
    # will raise RuntimeError of No preview specified.
        try:
            self.picam2.stop_preview()
        except RuntimeError as e:
            print(e)
        self.new_window.destroy()
        self.picam2.close()