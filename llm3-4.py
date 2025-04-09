import requests
import json
import sys
import re
import main

# Create a persistent session for better performance
session = requests.Session()
API_URL = "http://localhost:11434/api/generate"  # Update as needed

# Initial prompt
conversation_history = [
    "User: Assume you are a physiotherapist, and your name is Thera nao. The conversation must no longer. Start role play now."
]

def get_model_response(prompt):
    """
    Sends a prompt to the model API and streams the response in real time,
    printing each sentence separately while keeping real-time streaming output.
    """
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": True,
        "max_tokens": 50,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = session.post(API_URL, json=data, stream=True, verify=False)

        if response.status_code != 200:
            print "\nError: Received status code {}".format(response.status_code)
            return None

        sys.stdout.write("Model: ")
        sys.stdout.flush()

        full_response = ""
        sentence = ""

        for chunk in response.iter_lines():
            if chunk:
                try:
                    chunk = chunk.decode('utf-8')  # Python 2 needs decoding
                    chunk_data = json.loads(chunk)
                    text_chunk = chunk_data.get("response", "")

                    sys.stdout.write(text_chunk)
                    sys.stdout.flush()

                    full_response += text_chunk
                    sentence += text_chunk

                    if re.search(r'[.!?]', sentence):
                        sentence = sentence.strip()
                        main.speak(sentence)
                        sentence = ""

                    if chunk_data.get("done"):
                        break
                except ValueError:
                    print "\nError decoding JSON chunk"
                    break

        print ""  # Ensure newline
        return full_response

    except requests.RequestException as e:
        print "\nError communicating with API: {}".format(e)
        return None


def update_history(user_input, model_response):
    conversation_history.append("User: {}".format(user_input))
    conversation_history.append("Model: {}".format(model_response))


def chat():
    print "Thera bot is ready!"

    while True:
        user_input = main.listen(main.nao_ip, main.nao_port, listen_duration=30)
        if user_input:
            print "You: {}".format(user_input)
        else:
            print "You: No speech detected"
            return

        if user_input.strip().lower() == "exit":
            print "Goodbye!"
            break

        model_response = get_model_response(user_input)
        if model_response:
            update_history(user_input, model_response)


if __name__ == "__main__":
    chat()
