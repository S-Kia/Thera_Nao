import requests
import json
import main

# Initialize conversation history with the base prompt
conversation_history = [
    "User: Assume you are a physiotherapist, and your name is Thera nao. The conversation must no longer. Start role play now."
]


# Function to send request and get model response using requests.Session for connection pooling
def get_model_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "max_tokens": 50,
        "temperature": 0.7,
        "top_p": 0.9
    }

    # Create a session to reuse the connection and avoid overhead of opening new connections each time
    session = requests.Session()

    try:
        # Make the POST request with streaming enabled
        response = session.post(url, json=data, stream=True)
        # Parse the JSON content
        response_data = response.json()  # Converts the response to a dictionary
        # Print the value of the 'response' key
        return response_data.get("response")
    finally:
        session.close()  # Close the session to release the connection


# Function to update the conversation history
def update_history(user_input, model_response):
    conversation_history.append("User: {}".format(user_input))
    conversation_history.append("Model: {}".format(model_response))


# Function to handle multiple interactions
def chat():
    # Loop for continuous conversation

    while True:
        # Get the user's input
        #user_input = raw_input("You: ")

        user_input = main.listen(main.nao_ip, main.nao_port, listen_duration=30)
        if user_input:
            print("You: {}".format(user_input))
        else:
            print("You: {}".format("No speech detected"))
            return


        # Append the new input to the conversation history
        full_prompt = "\n".join(conversation_history) + "\nUser: {}".format(user_input)

        # Get the model's response
        model_response = get_model_response(full_prompt)

        # Print the response from the model
        print("Model: {}".format(model_response))

        main.speak(model_response)

        # Update the conversation history with the new exchange
        update_history(user_input, model_response)


# Start the chat function
if __name__ == "__main__":
    chat()
