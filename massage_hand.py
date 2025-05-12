import cv2
import time
import threading    # for run in background
from get_camera import get_nao_camera_frame
import main
import math

# Load Haar cascade for hand detection
hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'palm.xml')

# Choose camera source
source_type = "nao"  # "webcam" or "nao"

cap = None
if source_type == "webcam":
    cap = cv2.VideoCapture(0)

def get_frame(source="webcam"):
    if source == "webcam":
        ret, frame = cap.read()
        return frame if ret else None
    elif source == "nao":
        return get_nao_camera_frame(1)  # lower camera = 1
    return None

# Joint configuration for hand massage (Squeeze and release)
angles_1 = [
    -0.88, 2.28, 49.74, 1.76, -54.23, -55.81, -56.96, 37.65, 0.09, 0.18, -0.17, 0,
    0, 0, 0.09, -0.09, -0.09, -0.17, -0.17, 0, 51.86, 1.67, 58.71, 52.39, 55.55, 37.36
]
angles_2 = [
    -4.4, 2.28, 49.22, 1.49, -54.23, -55.81, -61.88, 15.15, 0.09, 0.09, -0.17, -0.09,
    0, 0, 0.09, -0.09, -0.09, -0.17, -0.17, 0, 51.77, 1.58, 58.53, 52.3, 59.06, 16.41
]
angles_1 = [math.radians(a) for a in angles_1]
angles_2 = [math.radians(a) for a in angles_2]

# Massage 5 time
def move_joint_task():
    for _ in range(5):
        main.move_nao_joints(angles_2)
        main.move_nao_joints(angles_1)

# Starting position
main.move_nao_joints(angles_1)

# Timer
hand_start_time = None
HAND_DETECTION_THRESHOLD = 2  # seconds

while True:
    frame = get_frame(source=source_type)
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands
    hands = hand_cascade.detectMultiScale(
        gray,
        scaleFactor= 1.02,      # lower > sensitive
        minNeighbors= 1,       # lower > sensitive
        minSize = (120, 120)    # min width/height in pixels
    )

    # If detection lasts more than 2 seconds, start massage
    if len(hands) > 0:
        if hand_start_time is None:
            hand_start_time = time.time()
        elif time.time() - hand_start_time >= HAND_DETECTION_THRESHOLD:
            print("Hand detected: starting joint movement")
            joint_thread = threading.Thread(target=move_joint_task)
            joint_thread.start()
    else:
        hand_start_time = None

    # Draw rectangles to highlight the hand
    for (x, y, w, h) in hands:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show frame
    cv2.imshow('Hand Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
if cap:
    cap.release()
cv2.destroyAllWindows()
