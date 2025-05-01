import main
from naoqi import ALProxy
import threading

nao_ip = main.nao_ip
nao_port = main.nao_port

# Connect to the audio player service
audio_player = ALProxy("ALAudioPlayer", nao_ip, nao_port)

# Global variable to store the current sound ID
current_sound = None

def play(file_path):
    def play_in_background():
        global current_sound
        current_sound = audio_player.playFile(file_path)

    thread = threading.Thread(target=play_in_background)
    thread.start()

def pause():
    if current_sound is not None:
        audio_player.stop(current_sound)

def stop_all_sounds():
    audio_player.stopAll()