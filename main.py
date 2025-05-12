import time
import math
from naoqi import ALProxy

# Select local or NAO robot IP address
nao_ip = "127.0.0.1"
nao_port = 9559

"""
nao_ip = "172.18.16.30"
nao_port = 9559
"""

# TTS
def speak(text):
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
    tts.say(str(text))

# Get text input in Choregraphe
def listen(nao_ip, nao_port, listen_duration):
    try:
        # Create proxies for ALDialog and ALMemory
        dialog = ALProxy("ALDialog", nao_ip, nao_port)
        memory = ALProxy("ALMemory", nao_ip, nao_port)

        # Set NAO's listening language
        dialog.setLanguage("English")

        last_speech = ""
        start_time = time.time()
        print("listening...")
        while time.time() - start_time < listen_duration:  # Listen for the specified duration
            recognized_text = memory.getData("Dialog/LastInput")
            if recognized_text and recognized_text != last_speech and last_speech != "":
                #print("NAO Heard:", recognized_text)
                return recognized_text
            last_speech = recognized_text

            time.sleep(0.1)  # Small delay to prevent excessive looping

        return None  # Return None if no speech is detected

    except Exception as e:
        print("Error:", e)
        return None

# Control motion
def move_nao_joints(angles,speed=0.5):

    if len(angles) != 26:
        raise ValueError("Expected 26 joint angles, got {}".format(len(angles)))

    joint_names = [
        "HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowYaw",
        "LElbowRoll", "LWristYaw", "LHand", "LHipYawPitch", "LHipRoll",
        "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", "RHipYawPitch",
        "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"
    ]

    # Connect to NAO
    motion = ALProxy("ALMotion", nao_ip, nao_port)

    # Speed fraction (0.0 to 1.0)
    speed = speed   # 0.2

    # Send the command
    motion.angleInterpolationWithSpeed(joint_names, angles, speed)

# Go behind the user before massaging the upper back
def navigate_square_and_turn():
    # Connect to proxies
    motion = ALProxy("ALMotion", nao_ip, nao_port)
    posture = ALProxy("ALRobotPosture", nao_ip, nao_port)

    # Wake up robot and set to initial posture
    motion.wakeUp()
    posture.goToPosture("StandInit", 0.5)

    # Step 1: Go Left (0.5 m)
    motion.moveTo(0.0, -0.5, 0.0)
    time.sleep(1)

    # Step 2: Go forward (1 m)
    motion.moveTo(1.0, 0.0, 0.0)
    time.sleep(1)

    # Step 3: Turn around to face South (180 degrees)
    motion.moveTo(0.0, 0.0, math.pi)
    time.sleep(1)

    # Step 4: Go Left (0.5 m)
    motion.moveTo(0.0, -0.5, 0.0)
    time.sleep(1)