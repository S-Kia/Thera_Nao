# NAO Robot Patient Greeting and Interaction System

This project is designed to implement a speech-based interaction system for a NAO robot that can recognize patient IDs and engage in a structured conversation with patients. The system aims to enhance the patient's experience during their visit to the physiotherapy clinic by providing voice-based interactions.

## Table of Contents
1. [System Overview](#system-overview)
2. [System Architecture](#system-architecture)
3. [Intents and Keywords](#intents-and-keywords)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributions](#contributions)
7. [License](#license)

## System Overview
The NAO robot serves as an interactive assistant for patients, helping them check-in, provide feedback, and track their visit details (e.g., pain level, visit reason, and wellness goals). The robot uses speech recognition to identify patient IDs and interacts based on predefined intents and keywords. It guides the patient through a series of prompts to collect essential information and then shares responses based on the collected data.

### Features:
- **Patient ID recognition**: The robot identifies whether the patient is returning or new by recognizing their ID.
- **Contextual conversation**: The robot asks questions related to the patient's condition, visit reason, and wellness goals.
- **Feedback system**: The robot allows the patient to rate their pain level and share session feedback.
- **Customized responses**: Based on the recognized keywords, the robot provides relevant responses.

## System Architecture
The system uses several components to achieve the interactive experience:

1. **Speech Recognition (ALSpeechRecognition)**:
   - The robot listens to the patient's spoken responses using the speech recognition module.
   - It converts the spoken input into text and matches it against predefined keywords for determining intents.

2. **Text-to-Speech (ALTextToSpeech)**:
   - The robot provides spoken feedback to the patient based on the recognized keywords and determined intent.
   
3. **Memory Proxy (ALMemory)**:
   - Stores recognized speech input and patient information for processing and context management.
   
4. **Intent Recognition**:
   - The recognized speech is matched with predefined intents (e.g., patient ID, pain level) to guide the flow of the conversation.
   
5. **Conversation Flow**:
   - The robot follows a structured conversation flow, starting with patient ID recognition, then moving to various feedback and interaction prompts.

### Diagram:
