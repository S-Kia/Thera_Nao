import cv2
import math
import time
import requests
import mediapipe as mp
import numpy as np

# === Joint limit enforcement ===
def clamp(value, low, high):
    return max(min(value, high), low)

nao_joint_limits = {
    "LShoulderPitch": (-119.5, 119.5),
    "RShoulderPitch": (-119.5, 119.5),
    "LShoulderRoll":  (-18.0,   76.0),
    "RShoulderRoll":  (-76.0,   18.0),
    "LElbowRoll":     (-88.5,   -2.0),
    "RElbowRoll":     (  2.0,   88.5),
}

# === Angle calculation functions ===
def angleRShoulderPitch(Rshoulder, Relbow):
    if Rshoulder[1] > Relbow[1]:
        angle = -math.degrees(math.atan(abs(Rshoulder[1] - Relbow[1]) / abs(Rshoulder[2] - Relbow[2])))
        return clamp(angle, *nao_joint_limits["RShoulderPitch"])
    else:
        angle = 90 - math.degrees(math.atan((Rshoulder[2] - Relbow[2]) / (Relbow[1] - Rshoulder[1])))
        return clamp(angle, *nao_joint_limits["RShoulderPitch"])

def angleRShoulderRoll(Rshoulder, Relbow):
    angle = math.degrees(math.atan((Relbow[0] - Rshoulder[0]) / (Rshoulder[2] - Relbow[2] + 1e-6)))
    return clamp(angle, *nao_joint_limits["RShoulderRoll"])

def angleRElbowRoll(Rshoulder, Relbow, Rwrist):
    a = np.linalg.norm(np.array(Rshoulder) - np.array(Relbow))
    b = np.linalg.norm(np.array(Relbow) - np.array(Rwrist))
    c = np.linalg.norm(np.array(Rwrist) - np.array(Rshoulder))
    angle = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
    angle = 180 - angle
    return clamp(angle, *nao_joint_limits["RElbowRoll"])

def angleLShoulderPitch(Lshoulder, Lelbow):
    if Lshoulder[1] > Lelbow[1]:
        angle = -math.degrees(math.atan(abs(Lshoulder[1] - Lelbow[1]) / abs(Lshoulder[2] - Lelbow[2])))
        return clamp(angle, *nao_joint_limits["LShoulderPitch"])
    else:
        angle = 90 - math.degrees(math.atan((Lshoulder[2] - Lelbow[2]) / (Lelbow[1] - Lshoulder[1])))
        return clamp(angle, *nao_joint_limits["LShoulderPitch"])

def angleLShoulderRoll(Lshoulder, Lelbow):
    angle = math.degrees(math.atan((Lelbow[0] - Lshoulder[0]) / (Lshoulder[2] - Lelbow[2] + 1e-6)))
    return clamp(angle, *nao_joint_limits["LShoulderRoll"])

def angleLElbowRoll(Lshoulder, Lelbow, Lwrist):
    a = np.linalg.norm(np.array(Lshoulder) - np.array(Lelbow))
    b = np.linalg.norm(np.array(Lelbow) - np.array(Lwrist))
    c = np.linalg.norm(np.array(Lwrist) - np.array(Lshoulder))
    angle = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
    angle = 180 - angle
    return clamp(angle, *nao_joint_limits["LElbowRoll"])

# === MediaPipe Setup ===
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)

last_post_time = time.time()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            Rshoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                         lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
            Relbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                      lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]
            Rwrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                      lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]

            Lshoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                         lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
            Lelbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                      lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
            Lwrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                      lm[mp_pose.PoseLandmark.LEFT_WRIST.value].z]

            angles = {
                "RShoulderPitch": angleRShoulderPitch(Rshoulder, Relbow),
                "RShoulderRoll":  angleRShoulderRoll(Rshoulder, Relbow),
                "RElbowRoll":     angleRElbowRoll(Rshoulder, Relbow, Rwrist),
                "LShoulderPitch": angleLShoulderPitch(Lshoulder, Lelbow),
                "LShoulderRoll":  angleLShoulderRoll(Lshoulder, Lelbow),
                "LElbowRoll":     angleLElbowRoll(Lshoulder, Lelbow, Lwrist),
            }

            current_time = time.time()
            if current_time - last_post_time >= 1.0:
                try:
                    requests.post("http://localhost:8000/pose", json=angles, timeout=0.2)
                    print("Sent:", angles)
                except Exception as e:
                    print("Failed to send:", e)
                last_post_time = current_time

            # Draw landmarks
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Pose with NAO Angles", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
