import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Retrieve and print actual settings
actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
actual_fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Resolution: {actual_width}x{actual_height}")
print(f"Frame Rate: {actual_fps} fps")

# Set dimensions of video frames
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
actual_fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Resolution: {actual_width}x{actual_height}")
print(f"Frame Rate: {actual_fps} fps")

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)
    if not ret:
        print("No video frame available")
        break

    # End program when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()