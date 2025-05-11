# 🤖 NAO Greeting Robot – Patient Interaction Module

This repository enables the **NAO humanoid robot** to engage with patients through voice recognition and greet patients.

## 🧩 Project Purpose

This module allows the **NAO robot** to recognize returning and new patients based on their **patient ID** and engage in structured voice-based conversations. The robot greets the patient and responds according to predefined intents.

---

## 💬 Features

- **Voice Interaction:** NAO uses voice recognition to identify patients and engage in contextual conversations.
- **Greeting:** NAO greets patients based on their patient ID.
- **Keyword-Based Responses:** NAO responds using predefined natural responses based on detected keywords.
- **Patient ID Recognition:** NAO distinguishes between new and returning patients using speech recognition.

---

## ⚙️ System Architecture

### 🧠 High-Level Flow

1. **`nao_greeting.py`**: Handles patient greeting and feedback interaction logic, including speech recognition and response generation.
2. **`connection.py`**: Manages the connection and disconnection to the NAO robot.
3. **`run_nao_greeting.py`**: Starts the NAO greeting session and triggers the entire process.

---

## 📂 Project Structure


---

## 🎙️ Patient Interaction Example

**NAO:** Welcome back! Please tell me your patient ID. <br/>
**Patient:** My ID is 1001. <br/>
**NAO:** Hello, Razu! How are you feeling today? <br/>
**Patient:** I'm feeling better. <br/>
**NAO:** That's great to hear! Keep up the good work! <br/>

---

## 🧠 Intents and Keywords

| Intent              | Keywords                                      |
| ------------------- | --------------------------------------------- |
| greeting            | hello, hi, good morning, good afternoon       |
| feeling             | feeling, sore, pain, tired, better            |
| exercise_difficulty | hard, challenging, balance, squats           |
| thanks              | thank, thanks for the session                 |

---

## 🚀 Getting Started

1. Connect to your NAO robot via `connection.py`.
2. Start the greeting session with:

```bash
python run_nao_greeting.py
```

---

## ✅ Requirements

NAO robot with naoqi SDK (Python 2.7)

Python 2.7 (for NAO)

Python 3.x for development purposes

---

## 🧑‍💻 Maintainer

Module Owner: Meghana Lokesh (st20310192) 
Responsibility: Integrating patients greeting via speech recognition and guiding the interaction flow.
