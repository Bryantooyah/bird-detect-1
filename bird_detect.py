import cv2
import datetime
import os
from ultralytics import YOLO
import serial
import time

# Set up serial communication with Arduino
#arduino = serial.Serial(port = '/dev/cu.usbserial-1120',baudrate = 9600, timeout = 1)  # Adjust the port as needed (MAC)
arduino = serial.Serial(port = 'COM3', baudrate = 9600, timeout = 1)  # Adjust the port as needed (Windows)
time.sleep(0.05)  # Wait for the serial connection to initialize

def send_coordinates(x, y):
    # Send coordinates to Arduino
    data = f"{x},{y}\n"
    arduino.write(data.encode("utf-8"))

# Loading pretrained YOLO model (will be downloaded on first run)
model = YOLO("model/yolov8n.pt", "v8")



# Video source is MP4 file stored locally
#cap = cv2.VideoCapture("source/birds.mp4")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Use webcam as video source
# Only save an image on frame 0
# Retrieve and print actual settings
frame_count = 0

# Set dimensions of video frames
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Cannot open video stream")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("No video frame available")
        break
    
    

    # Do prediction on image, with confidence greater than 80%
    results = model.predict(source=[frame], conf=0.8, save=False)

    DP = results[0].numpy()

    if len(DP) != 0:
        # Process each detection
        for result in results:
            boxes = result.boxes  # Bounding boxes
            for box in boxes:
                cls_id = int(box.cls)  # Class ID
                conf = box.conf.numpy()[0]  # Confidence score
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

                # Get class name
                class_name = model.names[cls_id]
        # If the class name contains the word 'bird', do something with the frame
        if 'bird' in class_name.lower():

            if frame_count == 0:
                current_time = datetime.datetime.now()
                filename = os.path.join("images", current_time.strftime("bird_%Y-%m-%d_%H-%M-%S-%f.jpg"))
                success = cv2.imwrite(filename, frame)

            frame_count = (frame_count + 1) % 11

            # Draw green rectangle around the object
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Add some text labelling to the rectangle
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                frame,
                class_name + " " + str(round(conf, 3)*100) + "%",
                (int(x1), int(y1) - 10),
                font,
                1,
                (255,255,255),
                2,
            )
            # Print coordinates of the bounding box
            Xa = int(x1+x2)/2
            Ya = int(y1+y2)/2
            print(f"Coordinates: ({Xa}, {Ya})")
            # Send coordinates to Arduino
            send_coordinates(Xa, Ya)
            


    # Display the frame onscreen
    cv2.imshow("Object Detection", frame)

    # End program when q is pressed
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
