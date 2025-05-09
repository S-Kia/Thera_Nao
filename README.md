# Thera_Nao


# 🤖 NAO Physiotherapist Robot – Patient Feedback Interaction

This part enables a NAO robot to act as a physiotherapist, collecting verbal feedback from patients after an exercise session. It supports both offline keyword-based interactions and intelligent advice generation via Groq's LLM.

## 🧩 Contributor: Hadayet Ullah Razu (st20313374)

### Modules

- `feedback_session_llm.py`: Core module for handling patient feedback with dynamic Groq LLM responses.
- `feedback_session_without_llm.py`: Fallback version using only intent-based keyword recognition without LLM.
- `groq_wrapper.py`: Bridges Python 2.7 (NAO environment) with Groq's API via a subprocess.
- `groq_runner.py`: Runs in Python 3.8 Anaconda to fetch Groq LLM responses and return them to the wrapper.
- `connection.py`: Handles connection and disconnection to the NAO robot.
