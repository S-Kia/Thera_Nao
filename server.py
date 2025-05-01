import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from naoqi import ALProxy

import imitation_control_actual
import main
import sounds
import subprocess

# NAO Configuration
nao_ip = main.nao_ip
nao_port = 9559

# Initialize Proxies
tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
motion = ALProxy("ALMotion", nao_ip, nao_port)
posture = ALProxy("ALRobotPosture", nao_ip, nao_port)
behavior = ALProxy("ALBehaviorManager", nao_ip, nao_port)

# Global shared states
status_message = "NAO server is running."
latest_pose = {}
massage_hand = None
massage_upper = None
demo = None
imitation_control = None
imitation_pose = None
music = None

class NaoRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global latest_pose
        content_length = int(self.headers.getheader('Content-Length'))
        post_data = self.rfile.read(content_length)

        if self.path == "/pose":
            try:
                latest_pose = json.loads(post_data)
                print(latest_pose)
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Pose received")
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("Invalid JSON: {}".format(str(e)))
            return

        try:
            command = json.loads(post_data)
            response_message = handle_command(command)
        except Exception as e:
            response_message = "Error: {}".format(str(e))
            print(response_message)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_message)

    def do_GET(self):
        if self.path == "/pose":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(latest_pose))
        else:
            message = get_status_message()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(message)

    def do_PUT(self):
        global status_message
        content_length = int(self.headers.getheader('Content-Length'))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            new_message = data.get("message", "").strip()
            if new_message:
                status_message = new_message
                response_message = "Status message updated."
            else:
                response_message = "No valid 'message' provided."
        except Exception as e:
            response_message = "Error: {}".format(str(e))
            print(response_message)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_message)

def get_status_message():
    global status_message
    return status_message

def run(server_class=HTTPServer, handler_class=NaoRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(get_status_message() + " on port {}".format(port))
    httpd.serve_forever()

def handle_command(command):
    global status_message, massage_hand, massage_upper
    global imitation_control, imitation_pose
    global music

    action = command.get("action", "")

    if action == "speak":
        text = command.get("text", "Hello")
        print("NAO Speaking: {}".format(text))
#        tts.say(str(text))
        status_message = "Done"
        return "Spoken: {}".format(text)

    elif action == "walk":
        distance = float(command.get("distance", 0.2))
        print("NAO Walking: {} meters".format(distance))
        motion.moveInit()
        motion.moveTo(distance, 0, 0)
        status_message = "Done"
        return "Walked: {} meters".format(distance)

    elif action == "massage hand":
        if command.get("stage") == "start":
            if massage_hand is None:
#                sounds.play("/home/nao/sounds/Amberlight.wav")
                massage_hand = subprocess.Popen(["python", "massage_hand.py"])
            status_message = "Hand massage started"
        else:
            if massage_hand:
                massage_hand.terminate()
                sounds.stop_all_sounds()
                massage_hand = None
                print("Hand massage stopped")
            status_message = "Hand massage stopped"
        return "Massage hand: updated"

    elif action == "massage upper back":
        if command.get("stage") == "start":
            if massage_upper is None:
#                sounds.play("/home/nao/sounds/Amberlight.wav")
                massage_upper = subprocess.Popen(["python", "massage_upper.py"])
            status_message = "Upper back massage started"
        else:
            if massage_upper:
                massage_upper.terminate()
                sounds.stop_all_sounds()
                massage_upper = None
                print("Upper back massage stopped")
            status_message = "Upper back massage stopped"
        return "Massage upper back: updated"

    elif action == "exercise demo":
        if command.get("stage") == "start":
            for i in range(1):   # 4
                imitation_control_actual.exercise(str(i+1), 0.08)
            status_message = "Started demo"
            return "Exercise demo: updated"

    elif action == "exercise practice":
        if command.get("stage") == "start":
            if imitation_control is None:
                imitation_control = subprocess.Popen(["python", "imitation_mp_control.py"])
            if imitation_pose is None:
                imitation_pose = subprocess.Popen([
                    "C:/Users/supha/Desktop/Coding/Hand_washing_application/.venv/Scripts/python.exe",
                    "imitation_mp_pose.py"
                ])
            status_message = "Started imitation"
        else:
            if imitation_control is not None:
                imitation_control.terminate()
                imitation_control = None
            if imitation_pose is not None:
                imitation_pose.terminate()
                imitation_pose = None
            print("Exercise imitation stopped")
            status_message = "Stopped imitation"
        return "Exercise imitation: updated"

# ================= ADDED POSTURE, GESTURE, EMOTION, CUSTOM BEHAVIOR =================
    elif action == "posture":
        posture_type = command.get("type")
        postures = {
            "stand": "StandInit",
            "sit": "SitRelax",
            "crouch": "Crouch",
            "stand_zero": "StandZero",
            "lying_back": "LyingBack",
            "lying_belly": "LyingBelly"
        }
        if posture_type in postures:
            posture.goToPosture(postures[posture_type], 0.5)
            return "Changed posture to: {}".format(posture_type)
        else:
            return "Unknown posture type"

    elif action == "gesture": # It doesn't work when run on simulator.
        gestures = {
            "wave": "animations/Stand/Gestures/Hey_1",
            "point": "animations/Stand/Gestures/You_1",
            "me": "animations/Stand/Gestures/Me_1",
            "explain": "animations/Stand/Gestures/Explain_1",
            "yes": "animations/Stand/Gestures/Yes_1",
            "no": "animations/Stand/Gestures/No_1",
            "think": "animations/Stand/Gestures/Thinking_1",
            "show_sky": "animations/Stand/Gestures/ShowSky_1",
            "show_floor": "animations/Stand/Gestures/ShowFloor_1",
            "bow": "animations/Stand/Gestures/BowShort_1"
        }
        gesture_type = command.get("type")
        if gesture_type in gestures:
            behavior.runBehavior(gestures[gesture_type])
            return "Gesture performed: {}".format(gesture_type)
        else:
            return "Unknown gesture type"

    elif action == "emotion":
        emotions = {
            "happy": "animations/Stand/Emotions/Positive/Happy_1",
            "sad": "animations/Stand/Emotions/Negative/Sad_1",
            "laugh": "animations/Stand/Emotions/Positive/Laugh_1"
        }
        emotion_type = command.get("type")
        if emotion_type in emotions:
            behavior.runBehavior(emotions[emotion_type])
            return "Emotion shown: {}".format(emotion_type)
        else:
            return "Unknown emotion type"

    elif action == "custom_behavior":
        behavior_name = command.get("behavior_name")
        if behavior_name:
            behavior.runBehavior(behavior_name)
            return "Custom behavior executed: {}".format(behavior_name)
        else:
            return "Missing behavior_name"

    elif action == "wake":
        motion.wakeUp()
        return "Robot awakened"


    elif action == "rest":
        motion.rest()
        return "Robot resting"

    elif action == "ambient music":
        if command.get("stage") == "start":
            if music is None:
                music = sounds.play("/home/nao/sounds/Amberlight.wav")
            status_message = "Started music"
        else:
            sounds.stop_all_sounds()
            music = None
            print("Music stopped")
            status_message = "Stopped music"
        return "Ambient music: updated"

    return "Unknown action"

# Run server
if __name__ == '__main__':
    run()