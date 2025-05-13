# 🤖 Thera NAO – Multimodal AI Physiotherapy Robot System

**Thera NAO** is an intelligent, multimodal physiotherapy robot system consisting of three integrated modules:
- 🤝 **Greeting Module**: Greets and registers patients via voice interaction.
- 💆 **Massage & Exercise Module**: Delivers guided massage and physical therapy routines.
- 💬 **Feedback Module**: Collects patient feedback and provides personalized follow-up.


Patient-driven workflow
![image](https://github.com/user-attachments/assets/2a93a39d-eef4-4b8a-b324-d53a45dffc40)

🎥 **[YouTube Demo Video](https://youtube.com/your_demo_link_here)**
---

🤖 **NAO Greeting Session – Voice-Based Patient Onboarding**  
This module enables a NAO robot to greet patients and register them for physiotherapy sessions using voice interaction. It runs entirely on NAO’s onboard Python 2.7 environment, using keyword-based intent recognition and predefined empathetic responses to collect patient details like ID, reason for visit, pain level, and assigned doctor.

🧩 **Contributor:** Meghana Lokesh (st20310192)

### Modules  
- `nao_greeting.py`: Main script managing voice-based conversation flow.  
- `INTENTS`: Dictionary defining valid user intents and triggers.  
- `RESPONSES`: Dictionary for dynamic and supportive replies.

👉 Visit the `greeting` branch to explore the onboarding workflow.

---

🤖 **Thera NAO – AI-Guided Massage and Exercise Robot**  
This module enables the NAO robot to function as an intelligent physiotherapy assistant. It guides patients through massage and exercise routines using pose detection, joint angle transformation, and LLM-driven natural language interaction via Dify.

🧩 **Contributor:** Suphakris Tanmuk (st20298766)

### Modules  
- `main.py`: Sets up robot IP and basic motion/speech functions.  
- `server.py`: Handles HTTP GET/POST requests to control robot actions.  
- `massage_hand.py`: Detects palm using OpenCV and performs a hand massage.  
- `massage_upper.py`: Detects upper torso and controls upper back massage movement.  
- `imitation_get_angle_vdo.py`: Converts MMPose landmarks into NAO joint angles (CSV).  
- `imitation_control_vdo.py`: Controls NAO motion based on prerecorded pose data.  
- `imitation_mp_pose.py`: Uses MediaPipe to extract live body pose landmarks.  
- `imitation_mp_control.py`: Mirrors user posture in real-time using joint angles.  
- `sounds.py`: Plays ambient music to enhance patient relaxation.  
- `get_camera.py`: Captures image frames from the NAO robot camera.

👉 Visit the `main` branch to explore the full massage and exercise system.

---

🤖 **NAO Physiotherapist Robot – Patient Feedback Interaction**  
This module enables a NAO robot to act as a physiotherapist, collecting verbal feedback from patients after an exercise session. It supports both offline keyword-based interactions and intelligent advice generation via Groq's LLM.

🧩 **Contributor:** Hadayet Ullah Razu (st20313374)

### Modules  
- `feedback_session_llm.py`: Core module for handling patient feedback with dynamic Groq LLM responses.  
- `feedback_session_without_llm.py`: Fallback version using only intent-based keyword recognition without LLM.  
- `groq_wrapper.py`: Bridges Python 2.7 (NAO environment) with Groq's API via a subprocess.  
- `groq_runner.py`: Runs in Python 3.8 Anaconda to fetch Groq LLM responses and return them to the wrapper.  
- `connection.py`: Handles connection and disconnection to the NAO robot.

👉 Go to the `feedback` branch to see more.
