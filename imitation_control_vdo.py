import csv
from naoqi import ALProxy
import main
import math
import argparse


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

# Parse command-line arguments to run: python3 xxx.py --input <input_directory>
parser = argparse.ArgumentParser(description="Send joint angles to NAO from CSV file")
parser.add_argument('--input', type=str, default="joint_angles_all_frame.csv",
                    help='Path to the input CSV file (default: joint_angles_all_frame.csv)')
args = parser.parse_args()

# CSV file path
csv_file = args.input
# csv_file = "joint_angles_all_frame.csv"   # Manual input

# Move NAO to the "Stand" posture
posture_service.goToPosture("Stand", 0.5)


try:
    with open(csv_file, "r") as infile:
        reader = csv.DictReader(infile)  # Read CSV as a dictionary
        frame_count = 0

        for row in reader:
            # Skip every second frame (process every x frame)
            if frame_count %15  != 0:
                frame_count += 1
                continue

            for joint in joint_names:
                if joint in row and row[joint].strip():  # Ensure the column exists and is not empty
                    try:
                        joint_angles[joint] = float(row[joint])
                    except ValueError:
                        print "Skipping invalid value for", joint, ":", row[joint]

            # Convert dictionary to ordered list of angles
            final_joint_angles = [joint_angles[jn] for jn in joint_names]

            print "Parsed Joint Angles (Frame {}):".format(frame_count), final_joint_angles
            final_joint_angles = [round(math.radians(d), 4) for d in final_joint_angles]

            # Set time duration for each motion
            time_lists = [0.5] * len(joint_names)  # 0.5 seconds for each joint

            # Execute motion with parsed angles
            motion.angleInterpolation(joint_names, final_joint_angles, time_lists, True)

            frame_count += 1

except IOError:
    print "Error: Cannot open file '{}'.".format(csv_file)
    exit(1)

print "Done"