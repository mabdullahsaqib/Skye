import requests
import pyttsx3
import speech_recognition as sr

# Base URL for the API
BASE_URL = "http://217.196.51.52:4009"

# Global headers to store authentication token
HEADERS = {"Content-Type": "application/json"}


# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 250)


def speak(text):
    """Speak out the provided text."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen to the user's voice input and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening...")
                audio_data = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio_data)
                print("You:", user_input)
                return user_input
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                speak("Sorry, I didn't catch that.")
                return None
            except sr.RequestError:
                print("Speech recognition service is unavailable.")
                speak("Speech recognition service is unavailable.")
                return None

def make_request(method, endpoint, data=None, auth=False):
    """Helper function to make API requests."""
    url = f"{BASE_URL}{endpoint}"
    headers = HEADERS if auth else {"Content-Type": "application/json"}

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        else:
            return {"error": "Invalid HTTP method"}

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned {response.status_code}: {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_configuration():
    """Function to fetch the current configuration."""
    response = make_request("GET", "/config/get", auth=True)

    if "error" in response:
        speak(f"Failed to fetch configuration. {response['error']}")
    else:
        config_details = "\n".join([f"{key}: {value}" for key, value in response.items()])
        speak(f"The current configuration is as follows: {config_details}")

def update_configuration():
    """Function to update the configuration."""
    speak("What configuration would you like to update? Say it in the format key equals value.")
    config_update = listen()

    if config_update:
        try:
            # Parse the user input into a key-value pair
            key, value = map(str.strip, config_update.split("=", 1))
            payload = {key: value}
            response = make_request("POST", "/config/update", data=payload, auth=True)

            if "error" in response:
                speak(f"Failed to update configuration. {response['error']}")
            else:
                speak(f"Configuration for {key} has been updated successfully.")
        except ValueError:
            speak("Invalid format. Please say it in the format key equals value.")
    else:
        speak("I couldn't understand your input.")

print("Say 'get config' to fetch the configuration or 'update config' to update a configuration.")

while True:
    user_input = listen()
    if user_input and "exit" in user_input.lower():
        speak("Goodbye!")
        break
    elif user_input and "get config" in user_input.lower():
        get_configuration()
    elif user_input and "update config" in user_input.lower():
        update_configuration()
    else:
        speak("I didn't understand that. Try saying 'get config' or 'update config'.")
