#-*-coding: uft-8-*-
from naoqi import ALProxy
import time



INTENTS = {
    'patient_id': ['1001', '1002', '1003'],
    'visit_reason': ['backpain', 'neckpain', 'handpain'],
    'pain_level': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    'check_appointment': ['meghna', 'theranao', 'jack'],
    'greet': ['thankyou'],
    'mood_check': ['good', 'okay', 'tired', 'sad', 'happy'],
    'last_session_feedback': ['better', 'same', 'worse'],
    'wellness_goal': ['flexibility', 'strength', 'pain relief', 'relaxation'],
    'exercise_feedback': ['easy', 'hard', 'manageable'],
    'diet_check': ['yes', 'no', 'sometimes']
}

# Define NAO’s extra reaction based on specific keywords
RESPONSES = {
    # patient_id
    '1001': "Hello Razu, welcome back. How are you feeling today?",
    '1002': "Hello Kia, welcome back. How are you feeling today?",
    '1003': "Hello Lily, welcome back. How are you feeling today?",

    # visit_reason
    'backpain': "Back pain can be really uncomfortable. Don't worry — the physiotherapist will help you feel better soon.",
    'neckpain': "Thank you for sharing that. I've noted you're here for neck pain. Please sit comfortably and avoid sudden movements until the physiotherapist sees you.",
    'handpain': "Got it — hand pain. I’ll let the therapist know. Try not to strain your hand while you wait.",

    # pain_level
    '1': "Very mild. That’s a good sign. Let’s keep it that way!",
    '2': "Slight discomfort. Great progress — you're almost pain-free.",
    '3': "Mild pain. You’re managing well. We’ll help you feel even better.",
    '4': "Moderate discomfort. Let’s make sure it doesn’t increase.",
    '5': "Noticeable pain. Thank you for sharing. Your therapist will guide you carefully.",
    '6': "That sounds uncomfortable. We’ll make sure you get the support you need today.",
    '7': "Quite painful. Please be careful with movement until your session.",
    '8': "That’s intense. I’ll alert the physiotherapist so they can attend to you soon.",
    '9': "Severe pain. Please take a seat and relax. Help is on the way.",
    '10': "Extremely painful. I’ll immediately inform the therapist to assist you urgently.",

    # check_appointment
    'meghna': "You have an appointment with Dr. Meghna at 10:00 AM. Please proceed to Room 23.",
    'theranao': "You have an appointment with Dr. Theranao at 10:30 AM. Please go to Room 24.",
    'jack': "You have an appointment with Dr. Jack at 11:00 AM. Please head to Room 25.",

    # greet
    'thankyou': "You're welcome. I hope your session goes well!",
    'thanks': "You're welcome. I hope your session goes well!",

    # mood_check
    'good': "Glad to hear you're feeling good!",
    'okay': "Okay, thank you for letting me know. Let’s aim to make your day even better.",
    'tired': "You seem a bit tired — we’ll try to keep things light for you today.",
    'sad': "I’m here for you. Let’s see if today’s session helps you feel better.",
    'happy': "That’s wonderful! Let’s keep that positive energy going.",

    # last_session_feedback
    'better': "I'm glad to hear you're feeling better since your last session!",
    'same': "Thanks for the update. Staying steady is still progress.",
    'worse': "I'm sorry to hear that. I'll make sure your physiotherapist knows.",

    # wellness_goal
    'flexibility': "Improving flexibility is a great goal. Let’s work toward it together.",
    'strength': "Building strength takes time — you’re on the right path.",
    'pain relief': "Pain relief is a top priority. Let’s focus on that today.",
    'relaxation': "Relaxation is important. We’ll ensure your session helps you unwind.",

    # exercise_feedback
    'easy': "Great! That means your body is adapting well.",
    'hard': "Thanks for the honesty. The therapist will adjust accordingly.",
    'manageable': "That's a good balance. Let’s keep it at a steady pace.",

    # diet_check
    'yes': "Good job staying on track with your diet!",
    'no': "Thanks for being honest. Let’s find ways to support your nutrition goals.",
    'sometimes': "That’s okay — balance is key. We’ll keep working on it together.",
}

#Dialogue steps
   CONVO_FLOW = {
    'start': ("Hello, I am Thera Nao! Welcome to the Physiotherapy Clinic. Please tell me your patient ID.", 'patient_id'),

    'patient_id': ("Welcome back! What brings you to the clinic today?", 'visit_reason'),

    'visit_reason': ("Can you please tell me the pain level out of 10?", 'pain_level'),

    'pain_level': ("You have an appointment with which doctor?", 'check_appointment'),

    'check_appointment': ("Have a great session! You can say 'thank you' to finish or tell me how you're feeling today.", 'greet'),

    'greet': ("You're welcome! By the way, how are you feeling today?", 'mood_check'),

    'mood_check': ("Thanks for sharing. How did your last physiotherapy session go?", 'last_session_feedback'),

    'last_session_feedback': ("Noted. What is your main wellness goal for this therapy?", 'wellness_goal'),

    'wellness_goal': ("Thank you. And how are the exercises feeling so far — are they easy, hard, or manageable?", 'exercise_feedback'),

    'exercise_feedback': ("Good to know. Have you been able to follow your recommended diet?", 'diet_check'),

    'diet_check': ("Thanks for the update. I’ll share this information with your physiotherapist. Have a great session!", None)
}

# Create combined vocabulary for recognition
vocabulary = list(set([word for kw in INTENTS.values() for word in kw]))


def get_voice_input(speech_recog, memory):
    try:
        memory.removeData("WordRecognized")
    except RuntimeError:
        pass  # It may not exist yet

    speech_recog.pause(True)
    speech_recog.setVocabulary(vocabulary, False)
    speech_recog.subscribe("MyApp")
    speech_recog.pause(False)

    print("Listening...")

    for i in range(20):  # max 10 seconds
        time.sleep(0.5)
        try:
            data = memory.getData("WordRecognized")
        except RuntimeError:
            data = None  # If the key doesn't exist yet

        if data and isinstance(data, list) and len(data) > 1 and data[1] > 0.4:
            word = data[0].lower()
            print("Heard:", word)
            speech_recog.unsubscribe("MyApp")
            try:
                memory.removeData("WordRecognized")
            except RuntimeError:
                pass
            return word

    speech_recog.unsubscribe("MyApp")
    return ""

def get_intent(word):
    for intent, keywords in INTENTS.items():
        if word in keywords:
            return intent
    return 'unknown'

def say_reaction(tts, word):
    if word in RESPONSES:
        tts.say(RESPONSES[word])
        print("NAO:", RESPONSES[word])

def initial_feedback_session(IP, PORT):
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    animated_speech = ALProxy("ALAnimatedSpeech", IP, PORT)
    speech_recognition = ALProxy("ALSpeechRecognition", IP, PORT)
    dialog = ALProxy("ALDialog", IP, PORT)

    memory = ALProxy("ALMemory", IP, PORT)

    state = 'start'
    while state:
        prompt, expected_intent = CONVO_FLOW[state]
        tts.say(prompt)
        recognized_word = get_voice_input(speech_recognition, memory)
        print(recognized_word)

        if not recognized_word:
            print("No input detected. Waiting silently.")
            time.sleep(5)
            continue  # skip this iteration and ask again without saying anything

                # React to the word
            say_reaction(tts, recognized_word)

            # Determine intent
            intent = get_intent(recognized_word)
            if intent == expected_intent:
                state = intent

                # Check if this is the end of conversation
                if CONVO_FLOW[state][1] is None:
                    # Speak the final message
                    tts.say(CONVO_FLOW[state][0])
                    break  # Exit the loop
            else:
                tts.say("Sorry, I didn't catch that. Could you repeat?")

        tts.say("Thank you for your feedback.")
if __name__ == "__main__":
    main()




