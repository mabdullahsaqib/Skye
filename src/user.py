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


def get_user_data():
    """Get the current user's data."""
    response = make_authenticated_request("/user/get-me", method="GET")
    if response:
        print("User Data:", response)
        return response
    return None

def change_username(new_username):
    """Change the username of the current user."""
    response = make_authenticated_request("/user/change-username", method="POST", data={"new_username": new_username})
    if response:
        print("Username Changed:", response)
        return response
    return None

def user_voice_interaction(command):
    """Handle the user's command and take appropriate action."""
    if 'get data' in command:
        response = get_user_data()
        speak_response(response)
    elif 'change username' in command:
        speak_response("What would you like your new username to be?")
        new_username = listen_to_command()
        if new_username:
            response = change_username(new_username)
            speak_response(response)
    else:
        speak_response("I'm not sure how to handle that command.")

