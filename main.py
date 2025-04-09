import time
from naoqi import ALProxy


nao_ip = "127.0.0.1"
nao_port = 9559
"""

nao_ip = "172.18.16.47"
nao_port = 9559
"""

def speak(text):
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
    #tts.say("Hello, virtual world!")
    tts.say(str(text))

def listen(nao_ip, nao_port, listen_duration):
    try:
        # Create proxies for ALDialog and ALMemory
        dialog = ALProxy("ALDialog", nao_ip, nao_port)
        memory = ALProxy("ALMemory", nao_ip, nao_port)

        # Set NAO's listening language
        dialog.setLanguage("English")

        last_speech = ""
        start_time = time.time()
        print("listening...")
        while time.time() - start_time < listen_duration:  # Listen for the specified duration
            recognized_text = memory.getData("Dialog/LastInput")
            if recognized_text and recognized_text != last_speech and last_speech != "":
                #print("NAO Heard:", recognized_text)
                return recognized_text
            last_speech = recognized_text

            time.sleep(0.1)  # Small delay to prevent excessive looping

        return None  # Return None if no speech is detected

    except Exception as e:
        print("Error:", e)
        return None

#listen(nao_ip, nao_port, listen_duration=30)