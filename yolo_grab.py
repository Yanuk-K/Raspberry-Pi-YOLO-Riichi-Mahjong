from tkinter import *
from tkinter import messagebox
from picamera2 import Picamera2, Preview
from libcamera import controls
from ultralytics import YOLO
import time
import sys
import importlib.metadata

class YoloGrab:
    def __init__(self, master):
        picam2 = Picamera2()
        camera_config = picam2.create_preview_configuration()
        picam2.configure(camera_config)
        picam2.start_preview(Preview.QTGL)
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        picam2.start()

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

        capture_button = Button(labelframe, text ="Capture", command = capture_button_CallBack)
        capture_button.pack()

        AF_button = Button(labelframe, text="Continuous Focus", relief="sunken", command=AF_button_tpggled)
        AF_button.pack()

    def capture_button_CallBack(self, picam2, model):
        print("- Capture image -")
        frame = picam2.capture_array()
        results = model(frame)
        return results

    def AF_button_tpggled(self, AF_button, picam2):
        if AF_button.config('relief')[-1] == 'sunken':
            AF_button.config(relief='raised')
            picam2.set_controls({"AfMode": controls.AfModeEnum.Manual})
        else:
            AF_button.config(relief='sunken')
            picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        
    print(picam2.controls.AfMode)
    


def on_closing(self, root, picam2):
    # if preview window cloased before,
    # will raise RuntimeError of No preview specified.
    try:
        picam2.stop_preview()
    except RuntimeError as e:
        print(e)
    root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)