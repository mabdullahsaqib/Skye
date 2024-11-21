from api_requests import make_authenticated_request
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to a different voice if needed
engine.setProperty('rate', 150)

# Initialize recognizer for voice input
recognizer = sr.Recognizer()


def speak_response(text):
    """Speak out the provided text."""
    engine.say(text)
    engine.runAndWait()


def listen_to_command():
    """Listen to the user's voice input and return it as text."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening for your command...")
                audio_data = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio_data)
                print(f"You said: {user_input}")
                return user_input
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
                speak_response("Sorry, I didn't catch that.")
                return None
            except sr.RequestError:
                print("Speech recognition service is unavailable.")
                speak_response("Sorry, there was an issue with the service.")
                return None

def update_config(config_data):
    """Update the configuration."""
    response = make_authenticated_request("/config/update", method="POST", data=config_data)
    if response:
        print("Configuration Updated:", response)
        return response
    return None

def get_config():
    """Get the current configuration."""
    response = make_authenticated_request("/config/get", method="GET")
    if response:
        print("Configuration:", response)
        return response
    return None

def config_voice_interaction(command):
    """Handle the user's command related to configuration."""
    if 'get' in command:
        response = get_config()
        speak_response(response)
    elif 'update' in command:
        speak_response("What configuration data would you like to update?")
        config_data = listen_to_command()
        if config_data:
            response = update_config(config_data)
            speak_response(response)