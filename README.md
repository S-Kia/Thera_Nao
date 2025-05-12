# 🤖 Thera NAO: AI-Assisted Massage and Exercise Robot for Collaborative Rehabilitation


## 📌 Overview

**Thera NAO** is an AI-assisted humanoid robot developed to support physical rehabilitation through interactive massage and guided exercise routines. It combines body detection, pose estimation, and natural language processing to deliver adaptive and engaging therapy sessions.

---

## 🧠 Key Features

- **Human-Robot Interaction (HRI)** using LLMs (LLaMA3) via [Dify](https://docs.dify.ai)
- **Robot Massage** (Hand and Upper Back) using OpenCV and Haar cascades
- **Exercise Demonstration and Mirroring** using pose landmarks (MMPose + MediaPipe)
- **Real-time Robot Control** via HTTP server (Python 2.7 for NAO, Python 3 for AI/vision)
- **Natural Language Dialogue** powered by Retrieval-Augmented Generation (RAG)

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|-------------|
| Robot Platform | NAO (Python 2.7 SDK) |
| Vision & Pose Estimation | OpenCV, MediaPipe, MMPose |
| AI & Workflow | Dify (LLMs, RAG), JSON-based input |
| Backend Server | Python HTTP server (GET/POST for commands) |
| Integration | Multi-threading |

---

## 🔍 Core Functionalities

### Hand Massage
- Detects palm using Haar cascade
- Initiates massage with animated joint sequences

### Upper Back Massage
- Uses upper-body detection to adjust distance and begin massage

### Exercise Demo & Practice
- Uses MMPose for prerecorded postures (high accuracy)
- Uses MediaPipe for real-time mirroring using the robot's camera

### AI Workflow (Dify)
- User input → NLP → Answer generation → Speech/action commands → NAO robot execution

---

## 📂 File Structure

```
Thera_Nao/
├── main.py                     # Set IP address and port, basic NAO functions (e.g., speak, walk)
├── server.py                   # HTTP request handler for robot control
├── get_camera.py               # Fetch image from NAO robot
├── massage_hand.py             # Detect hand via OpenCV and perform hand massage
├── massage_upper.py            # Detect upper body via OpenCV and perform upper back massage
├── sounds.py                   # Play ambient music
├── imitation_get_angle_vdo.py # Convert JSON output from MMPose to joint angles (CSV)
├── imitation_control_vdo.py   # Read angles from CSV file and control robot
├── imitation_control_actual.py# Demo exercise and upper back massage execution
├── imitation_mp_pose.py       # Use MediaPipe to extract landmarks
├── imitation_mp_control.py    # Live pose mirroring via MediaPipe
```

---

## ✅ Requirements
- NAO robot with NAOqi SDK (Python 2.7)
- Python 3.8+ environment with MMPose, MediaPipe, OpenCV
- Docker to run Dify locally ([Docs](https://docs.dify.ai/en/introduction))

---

## 🚀 Getting Started

0. Install all required libraries  
1. Run Dify using Docker and import `Thera_nao.yml`  
2. Select your preferred LLM in Dify  
3. Edit the NAO IP address in `main.py` (Python 2.7)  
4. Copy the contents of `/Lib/site-packages/cv2/data` to your local environment if using OpenCV Haar cascades  
5. Run `server.py` using Python 2.7, or execute it via a Python 3 subprocess wrapper  
6. Interact with the robot through the Dify interface

---

## 🧪 Limitations & Future Work

- Replace NAO with more advanced hardware
- Integrate stereo/depth cameras for better pose accuracy
- Add speech-to-text (STT) and text-to-speech (TTS) for fluid interaction
- Improve motion tracking latency
- Conduct clinical trials for real-world validation

---

## 🧑‍💻 Maintainer
**Module Owner:** Suphakris Tanmuk
