import pyttsx3
import speech_recognition as sr
from wallet import wallet_voice_interaction
from trade import trade_voice_interaction
from configuration import config_voice_interaction
from user import user_voice_interaction

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


def handle_user_command(command):
    """Handle the user's command and take appropriate action."""
    if 'wallet' in command.lower():
        wallet_voice_interaction(command)
    elif 'trade' in command.lower():
        trade_voice_interaction(command)
    elif 'configuration' in command.lower():
        config_voice_interaction(command)
    elif 'user' in command.lower():
        user_voice_interaction(command)
    else:
        speak_response("Sorry, I didn't understand the command. Can you repeat it?")



def start():
    """Start the bot and handle voice interaction."""
    speak_response("Welcome to Skye! How can I assist you today?")

    while True:
        command = listen_to_command()
        if command:
            if 'exit' in command.lower():
                speak_response("Goodbye!")
                break
            handle_user_command(command)
        else:
            speak_response("Sorry, I didn't catch that. Can you say it again?")
