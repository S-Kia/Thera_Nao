import csv
from naoqi import ALProxy
import main
import math
import time


nao_ip = main.nao_ip
nao_port = main.nao_port


# Create NAOqi proxies with error handling
try:
    motion = ALProxy("ALMotion", nao_ip, nao_port)
    posture_service = ALProxy("ALRobotPosture", nao_ip, nao_port)
except Exception as e:
    print "Error connecting to NAOqi services:", str(e)
    exit(1)  # Exit if connection fails

# Choose between upper body only or full body motion
USE_UPPER_BODY_ONLY = True

# Define NAO's joint names
upper_body_joints = [
    "LShoulderPitch", "LShoulderRoll",
    "LElbowYaw", "LElbowRoll",
    "RShoulderPitch", "RShoulderRoll",
    "RElbowYaw", "RElbowRoll"
]

lower_body_joints = [
    "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch",
    "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch"
]


# Select joints based on user preference
if USE_UPPER_BODY_ONLY:
    joint_names = upper_body_joints
else:
    joint_names = upper_body_joints + lower_body_joints

# Initialize joint angles with default values (0.0)
joint_angles = {jn: 0.0 for jn in joint_names}


# CSV file path
#csv_file = "joint_angles_processed.csv"
csv_file = "joint_angles_all_frame.csv"

# Move NAO to the "Stand" posture
posture_service.goToPosture("Stand", 0.5)


try:
    with open(csv_file, "r") as infile:
        reader = csv.DictReader(infile)  # Read CSV as a dictionary

        for row in reader:
            for joint in joint_names:
                if joint in row and row[joint].strip():  # Ensure the column exists and is not empty
                    try:
                        joint_angles[joint] = float(row[joint])
                    except ValueError:
                        print "Skipping invalid value for", joint, ":", row[joint]

            # Convert dictionary to ordered list of angles
            final_joint_angles = [joint_angles[jn] for jn in joint_names]

            print "Parsed Joint Angles:", final_joint_angles
            final_joint_angles = [round(math.radians(d), 4) for d in final_joint_angles]

            # Set time duration for each motion
            time_lists = [1] * len(joint_names)  # 2 seconds for each joint

            # Execute motion with parsed angles
            motion.angleInterpolation(joint_names, final_joint_angles, time_lists, True)

except IOError:
    print "Error: Cannot open file '{}'.".format(csv_file)
    exit(1)

posture_service.goToPosture("Stand", 1)