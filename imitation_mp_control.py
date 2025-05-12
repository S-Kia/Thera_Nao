import math
import time
from naoqi import ALProxy
import main
import requests

# =============== NAO Setup ================
nao_ip = main.nao_ip
nao_port = main.nao_port

try:
    motion = ALProxy("ALMotion", nao_ip, nao_port)
    posture_service = ALProxy("ALRobotPosture", nao_ip, nao_port)
except Exception as e:
    print("Connection error:", str(e))
    exit(1)

posture_service.goToPosture("Stand", 0.5)
joint_names = ["LShoulderPitch", "LElbowRoll", "RShoulderPitch", "RElbowRoll"]


# =============== Control Loop ================
try:
    while True:
        response = requests.get("http://localhost:8000/pose")
        latest_pose = response.json()

        if latest_pose:
            final_joint_angles = []
            for joint in joint_names:
                deg = float(latest_pose.get(joint, 0.0))
                final_joint_angles.append(round(math.radians(deg), 4))

            print("Moving to:", final_joint_angles)
            motion.angleInterpolation(joint_names, final_joint_angles, [1] * len(joint_names), True)

        time.sleep(1.0)

except KeyboardInterrupt:
    print("Stopped by user")

posture_service.goToPosture("Stand", 1)
