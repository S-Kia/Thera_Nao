# 🤖 NAO Physiotherapist Robot – Patient Feedback Module

This branch of this repository enables the **NAO humanoid robot** to act as a **physiotherapist**, guiding patients through exercises and collecting their feedback post-session.

## 🧩 Project Purpose

This module focuses on managing post-session feedback from patients using voice interaction, processing their responses, and providing supportive and motivating replies, both prescripted and AI-generated via Groq's LLM API.

---

## 💬 Features

- NAO asks patients how they feel after a physiotherapy session
- Uses **voice recognition** to identify patient responses
- Classifies responses into **intents** (e.g., pain, tiredness, challenge)
- Reacts with:

  - Predefined natural responses
  - **Real-time LLM-generated advice** via Groq API

- Supports hybrid Python environments (Python 2.7 for NAO + Python 3.8+ for Groq API)

---

## ⚙️ System Architecture

### 🧠 High-Level Flow

1. `feedback_session_start.py`: Starts the feedback interaction session.
2. `feedback_session_llm.py`: Handles NAO's dialogue logic, keyword detection, and response generation.
3. `connection.py`: Connects and disconnects to the NAO robot.
4. `groq_wrapper.py`: Acts as a subprocess bridge between Python 2.7 (NAO) and Groq's Python 3.8+ environment.
5. `groq_runner.py`: Executes the Groq API request and returns the generated advice text.

---

## 📂 Project Structure

```
.
├── connection.py              # Connect/disconnect NAO robot
├── feedback_session_start.py  # Entry point for launching feedback session
├── feedback_session_llm.py    # Feedback session using Groq LLM (via wrapper)
├── feedback_session_without_llm.py  # Fallback mode using only keyword-based responses
├── groq_wrapper.py            # Python 2.7 compatible wrapper to run subprocess
├── groq_runner.py             # Python 3.8 script to query Groq API and return result
```

---

## 🎙️ Patient Interaction Example

**NAO:** Great job today! How do you feel after the session? <br/>
**Patient:** I feel a little sore. <br/>
**NAO:** That's normal. Some muscle soreness happens after therapy. <br/>
**NAO:** Please wait a moment while I get some advice... <br/>
**NAO (Groq-generated):** It’s completely normal to feel sore after exercising. Try to rest and stay hydrated, and it should ease by tomorrow. <br/>

---

## 🧠 Intents and Keywords

| Intent              | Keywords                                      |
| ------------------- | --------------------------------------------- |
| report_feeling      | relaxed, sore, better, pain, tired            |
| exercise_difficulty | hard, challenging, stretches, balance, squats |
| request_variation   | yes, variation, try, show                     |
| ask_home_exercise   | home, same, practice                          |
| thanks              | thank, session                                |

---

## 🔁 Multi-Python Compatibility

NAO uses Python 2.7, while Groq's API requires Python 3.7+. To solve this, the project uses:

- `groq_wrapper.py`: A Python 2.7 subprocess script to launch Groq requests
- `groq_runner.py`: Executes in a Python 3.8+ Anaconda environment to query Groq and return results

---

## 🚀 Getting Started

1. Connect to your NAO robot via `connection.py`
2. Start a feedback session with:

```bash
python feedback_session_start.py
```

3. Make sure a Python 3.8+ environment (with Groq API access) is configured correctly for subprocess execution.

---

## ✅ Requirements

- NAO robot with `naoqi` SDK (Python 2.7)
- Anaconda / Python 3.8+ environment with:

  - Access to [Groq API](https://groq.com/)
  - `openai` or `groq`-compatible SDK

---

## 🧑‍💻 Maintainer

**Module Owner:** Hadayet Ullah Razu (st20313374) <br/>
**Responsibility:** Integrating patient feedback via speech recognition and LLM advice using Groq API.
