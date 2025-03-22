from naoqi import ALProxy

def connect(NAO_IP, PORT):
    tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
    motion = ALProxy("ALMotion", NAO_IP, PORT)

    motion.wakeUp()
    tts.say("Thera NAO Activate")
    print "Connected"


def disconnect(NAO_IP, PORT):
    tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
    motion = ALProxy("ALMotion", NAO_IP, PORT)

    motion.wakeUp()
    tts.say("Thera NAO Sign Out")
    motion.rest()
    print "Exit Successfully"