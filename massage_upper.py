import cv2
import math
import threading
import time

from get_camera import get_nao_camera_frame
from naoqi import ALProxy
import main
import imitation_control_actual

# Load Haar cascade
upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

def get_frame(source="webcam"):
    if source == "webcam":
        ret, frame = cap.read()
        return frame if ret else None
    elif source == "nao":
        return get_nao_camera_frame(0)
    return None

# Go behind the user before massaging the upper back
def navigate_task():
    main.navigate_square_and_turn()

# Move slightly when the user is far from the robot
def move_small_step_task():
    motion = ALProxy("ALMotion", main.nao_ip, main.nao_port)
    motion.moveTo(0.1, 0, 0)

# Massage upper back
def joint_movement_task():
    imitation_control_actual.massageup()

# Choose camera source
source_type = "nao"

cap = None
if source_type == "webcam":
    cap = cv2.VideoCapture(0)

# State tracking
stage = 0
nav_thread = None
higher_start_time = None  # for diagonal > 500
below_start_time = None   # for diagonal < 500

while True:
    frame = get_frame(source=source_type)
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    upper_bodies = upper_body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Measure the diagonal line
    detected_diagonal = None
    for (x, y, w, h) in upper_bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        detected_diagonal = math.sqrt(w ** 2 + h ** 2)
        print("Diagonal length: %.2f" % detected_diagonal)
        break  # use first detected person

    now = time.time()

    # Stage 0: Wait to decide based on diagonal
    if detected_diagonal is not None and stage == 0:
        if detected_diagonal > 500:     # User is near the robot
            higher_start_time = higher_start_time or now
            below_start_time = None
            if now - higher_start_time >= 2.0:  # Detect > 2 sec, perform action
                print("Stage 1: navigating")
                nav_thread = threading.Thread(target=navigate_task)
                nav_thread.start()
                stage = 1
        elif detected_diagonal < 500:   # User is far from the robot
            below_start_time = below_start_time or now
            higher_start_time = None
            if now - below_start_time >= 2.0:
                print("Moving forward 0.1m")    # Move slightly when far from the user
                move_thread = threading.Thread(target=move_small_step_task)
                move_thread.start()
                below_start_time = None
        else:
            higher_start_time = None
            below_start_time = None
    else:
        higher_start_time = None
        below_start_time = None

    # Stage 1 wait for nav thread to finish, then start joint movement
    if stage == 1 and nav_thread is not None and not nav_thread.is_alive():
        print("Stage 2: joint movement sequence")
        joint_thread = threading.Thread(target=joint_movement_task)
        joint_thread.start()
        stage = 2   # Done

    # Show camera
    cv2.imshow('Upper Body Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
if cap:
    cap.release()
cv2.destroyAllWindows()