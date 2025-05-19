import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# set up camera w/ picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (500, 500)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# load yolov8
model = YOLO("yolov8n.pt")

while True:
    # capture a frame from camera
    frame = picam2.capture_array()
    
    # run yolo on the captured frame and store results
    results = model(frame)
    
    # output visual detection data, will draw on preview window
    annotated_frame = results[0].plot()
    
    # get inference time
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time # convert to milliseconds
    text = f'FPS: {fps:.1f}'
    
    # define font and position
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10 # 10 pixels from right
    text_y = text_size[1] + 10 # 10 pixels from the top
    
    # draw text on the annotated frame
    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # display resulting frame
    cv2.imshow("Camera", annotated_frame)
    
    # exit program if q is pressed
    if cv2.waitKey(1) == ord("q"):
        break
    
# close all windows
cv2.destroyAllWindows()