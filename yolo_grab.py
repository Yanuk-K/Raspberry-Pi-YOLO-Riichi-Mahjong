from tkinter import *
from tkinter import messagebox
from picamera2 import Picamera2, Preview
from libcamera import controls
from ultralytics import YOLO
import time
import sys
import importlib.metadata

class YoloGrab:
    def __init__(self, master, model):
        self.master = master
        self.master.geometry("400x300")
        self.start()
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        self.picam2.start()
        self.model = model
        self.result = None

    def capture_screen(self):
        root = Tk()
        root.title(sys.argv[0])
        root.geometry("450x350")
        # center on screen
        root.eval('tk::PlaceWindow . center')

        label_picam_ver = Label(root, 
                                text="picamera2 ver: " + importlib.metadata.version('picamera2'),
                                anchor="e",)
        label_picam_ver.pack(fill = "x", padx=(10, 10), pady=10)

        labelframe = LabelFrame(root, text="Click button to capture image")
        labelframe.pack(fill = "both", expand = "yes")

        capture_button = Button(labelframe, text ="Capture", command = self.capture_button_CallBack)
        capture_button.pack()

        AF_button = Button(labelframe, text="Continuous Focus", relief="sunken", command=self.AF_button_tpggled)
        AF_button.pack()

    def capture_button_CallBack(self):
        print("- Capture image -")
        frame = self.picam2.capture_array()
        self.result = self.model(frame)

    def AF_button_tpggled(self, AF_button):
        if AF_button.config('relief')[-1] == 'sunken':
            AF_button.config(relief='raised')
            self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual})
        else:
            AF_button.config(relief='sunken')
            self.picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

def on_closing(self, root):
    # if preview window cloased before,
    # will raise RuntimeError of No preview specified.
    try:
        self.picam2.stop_preview()
    except RuntimeError as e:
        print(e)
    root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)