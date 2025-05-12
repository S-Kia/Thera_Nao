import json
import numpy as np
import pandas as pd
import math
import os

# Load the JSON file
json_file_path = "data/results_Ex1.json"
with open(json_file_path, 'r') as file:
    data = json.load(file)

joint_names = {int(k): v for k, v in data['meta_info']['keypoint_id2name'].items()}
skeleton_links = data['meta_info']['skeleton_links']

# Mapping to correlate names
joint_mapping = {
    "LShoulderPitch": "left_shoulder",
    "LShoulderRoll": "left_shoulder",
    "LElbowRoll": "left_elbow",
    "RElbowRoll": "right_elbow",
    "RShoulderPitch": "right_shoulder",
    "RShoulderRoll": "right_shoulder",
    "LHipRoll": "left_hip",
    "LHipPitch": "left_hip",
    "LKneePitch": "left_knee",
    "RHipRoll": "right_hip",
    "RHipPitch": "right_hip",
    "RKneePitch": "right_knee"
}

# Set joint limits using clamp()
nao_joint_limits = {
    "LShoulderPitch": (-119.5, 119.5),
    "RShoulderPitch": (-119.5, 119.5),
    "LShoulderRoll":  (-18.0,   76.0),
    "RShoulderRoll":  (-76.0,   18.0),
    "LElbowRoll":     (-88.5,   -2.0),
    "RElbowRoll":     (  2.0,   88.5),
    "LHipRoll":       (-21.74,  45.29),
    "RHipRoll":       (-45.29,  21.74),
    "LHipPitch":      (-88.00,  27.73),
    "RHipPitch":      (-88.00,  27.73),
    "LKneePitch":     ( -5.90, 121.47),
    "RKneePitch":     ( -5.90, 121.47),
}

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

# Calculate the angle of the elbow and knee
def calculate_joint_angle(parent, joint, child):
    vec1 = np.array(parent[:3]) - np.array(joint[:3])
    vec2 = np.array(child[:3]) - np.array(joint[:3])
    vec1 /= np.linalg.norm(vec1)
    vec2 /= np.linalg.norm(vec2)
    cos_angle = np.dot(vec1, vec2)
    angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return 180 - np.degrees(angle_rad)

# Calculate the angle of the shoulder and hip
def calculate_pitch_roll(parent, joint, child):
    # Step 1: Convert to float arrays
    parent = np.array(parent, dtype=float)
    joint  = np.array(joint, dtype=float)
    base   = np.array(keypoints[7][:3], dtype=float)
    child  = np.array(child, dtype=float)

    joint = joint - parent
    base = base - parent
    child = child - parent
    parent = parent - parent

    # Step 2: Translate so that joint becomes the origin
    parent_t = parent - joint
    base_t = base - joint
    child_t = child - joint

    # Step 3: Define Z-axis = parent - base
    z_axis = parent_t - base_t
    z_norm = np.linalg.norm(z_axis)
    if z_norm == 0:
        return 0.0, 0.0  # prevent division by zero
    if any(term in joint_name for term in ["Shoulder"]):
        z_axis /= z_norm
    elif any(term in joint_name for term in ["Hip"]):
        z_axis /= -z_norm

    # Step 4: Project joint (origin) onto base–parent line (for Y-axis)
    base_vec = base_t - parent_t
    base_norm = np.linalg.norm(base_vec)
    if base_norm == 0:
        return 0.0, 0.0
    base_vec /= base_norm
    proj_length = -np.dot(parent_t, base_vec)
    proj_point = parent_t + proj_length * base_vec

    # Step 5: Y-axis = from joint (origin) to projection
    if any(term in joint_name for term in ["RShoulder", "RHip"]):
        y_axis = proj_point
    elif any(term in joint_name for term in ["LShoulder", "LHip"]):
        y_axis = -proj_point
    y_norm = np.linalg.norm(y_axis)
    if y_norm == 0:
        return 0.0, 0.0
    y_axis /= y_norm

    # Step 6: X-axis = Y × Z (right-handed system)
    x_axis = np.cross(y_axis, z_axis)
    x_norm = np.linalg.norm(x_axis)
    if x_norm == 0:
        return 0.0, 0.0
    x_axis /= x_norm

    # Step 7: Rotation matrix with local axes as columns
    R = np.stack([x_axis, y_axis, z_axis], axis=1)  # shape (3, 3)

    # Step 8: Rotate child vector into local coordinate frame
    v_local = np.dot(R.T, child_t)

    # Step 9: Normalize vector
    v_norm = np.linalg.norm(v_local)
    if v_norm == 0:
        return 0.0, 0.0
    v_local /= v_norm

    # Step 10: Compute pitch (rotation around X-axis, looking up/down)
    if any(term in joint_name for term in ["Shoulder"]):
        pitch_rad = math.asin(-v_local[2])
    elif any(term in joint_name for term in ["Hip"]):
        pitch_rad = math.atan2(v_local[0], -v_local[2])
    pitch = math.degrees(pitch_rad)

    # Step 11: Compute roll (rotation in XY plane)
    Ry = np.array([[np.cos(pitch_rad), 0, np.sin(pitch_rad)],
                   [0, 1, 0],
                   [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]])
    v_roll = np.dot(Ry.T, v_local)

    proj_xy = np.array([v_roll[0], v_roll[1], 0])
    proj_norm = np.linalg.norm(proj_xy)
    if proj_norm == 0:
        roll = 0.0
    else:
        proj_xy /= proj_norm
        roll_rad = math.atan2(proj_xy[1], proj_xy[0])
        roll = math.degrees(roll_rad)

        if roll > 90:
            roll = 180 - roll
        elif roll < -90:
            roll = -180 - roll

    return round(pitch, 2), round(roll, 2)


# Apply final joint transformation, clamp to NAO range, and return as string
def offset_angle_string(joint_name: str, angle_value: float) -> str:
    # Apply offsets
    a = round(angle_value, 2)

    if joint_name == "LShoulderPitch":
        final_val = a

    elif joint_name == "RShoulderPitch":
        final_val = a

    elif joint_name == "LShoulderRoll":
        final_val = a

    elif joint_name == "RShoulderRoll":
        final_val = a

    elif joint_name == "LElbowRoll":
        final_val = -a

    elif joint_name == "RElbowRoll":
        final_val = a

    elif joint_name == "LHipRoll":
        final_val = a

    elif joint_name == "LHipPitch":
        final_val = a

    elif joint_name == "LKneePitch":
        final_val = a

    elif joint_name == "RHipRoll":
        final_val = a

    elif joint_name == "RHipPitch":
        final_val = a

    elif joint_name == "RKneePitch":
        final_val = a

    else:
        # Default
        final_val = a

    # Now clamp the final_val to the NAO range
    if joint_name in nao_joint_limits:
        min_lim, max_lim = nao_joint_limits[joint_name]
        final_val = clamp(final_val, min_lim, max_lim)

    return f"{joint_name}: {final_val:.2f}"


# Sorted list for consistent output order
joint_list_order = [
    "LShoulderPitch", "LShoulderRoll", "LElbowRoll",
    "RShoulderPitch", "RShoulderRoll", "RElbowRoll",
    "LHipRoll", "LHipPitch", "LKneePitch",
    "RHipRoll", "RHipPitch", "RKneePitch"
]

all_joint_angles = []

for frame_idx, frame in enumerate(data["instance_info"]):
    if not frame["instances"]:
        continue  # Skip if no instances in frame

    keypoints = frame["instances"][0]["keypoints"]
    raw_angles = {}

    # Calculate joint angles but store them in raw_angles
    for joint_name, mapped_name in joint_mapping.items():
        joint_id = next((id for id, name in joint_names.items() if name == mapped_name), None)
        if joint_id is None or joint_id >= len(keypoints):
            continue

        parent_joint = next((link[0] for link in skeleton_links if link[1] == joint_id), None)
        child_joint = next((link[1] for link in skeleton_links if link[0] == joint_id), None)

        if (
                parent_joint is not None and child_joint is not None
                and all(
            isinstance(keypoints[idx], list)
            and len(keypoints[idx]) >= 3
            for idx in [parent_joint, joint_id, child_joint]
        )
        ):
            if any(term in joint_name for term in ["Elbow", "Knee"]):
                angle = calculate_joint_angle(
                    keypoints[parent_joint],
                    keypoints[joint_id],
                    keypoints[child_joint]
                )
                raw_angles[joint_name] = angle
            elif any(term in joint_name for term in ["Shoulder"]):
                pitch, roll = calculate_pitch_roll(
                    keypoints[parent_joint],
                    keypoints[joint_id],
                    keypoints[child_joint]
                )
                if "Pitch" in joint_name:
                    raw_angles[joint_name] = pitch
                elif "Roll" in joint_name:
                    raw_angles[joint_name] = roll


            else:  # Hip
                pitch, roll = calculate_pitch_roll(
                    keypoints[parent_joint],
                    keypoints[joint_id],
                    keypoints[child_joint]
                )
                if "Pitch" in joint_name:
                    raw_angles[joint_name] = pitch
                elif "Roll" in joint_name:
                    raw_angles[joint_name] = roll


    joint_angle_data = {"frame_id": frame.get("frame_id", frame_idx + 1)}
    for jn in joint_list_order:
        if jn in raw_angles:
            angle_str = offset_angle_string(jn, raw_angles[jn]).split(": ")[1]
            joint_angle_data[jn] = angle_str
            print(jn, raw_angles[jn], angle_str)

    all_joint_angles.append(joint_angle_data)

# Export to CSV
df = pd.DataFrame(all_joint_angles)

# Derive CSV filename from JSON filename
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
csv_filename = os.path.join(os.path.dirname(json_file_path), base_name + ".csv")

df.to_csv(csv_filename, index=False)
print(f"\nJoint angles (first instance per frame) exported to {csv_filename}!")