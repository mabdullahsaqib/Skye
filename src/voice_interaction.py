import pyttsx3
import speech_recognition as sr
from auth import logout
from configuration import config_voice_interaction
from trade import trade_voice_interaction
from user import user_voice_interaction
from wallet import wallet_voice_interaction

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to a different voice if needed
engine.setProperty('rate', 150)

# Initialize recognizer for voice input
recognizer = sr.Recognizer()

# commands
wallet_commands = ['generate', 'add', 'remove', 'balance', 'default', 'all', 'list']
trade_commands = ['buy', 'sell', 'order', 'create', 'cancel', 'live', 'past', 'token', 'tokens']
config_commands = ['set', 'get', 'update']
user_commands = ['data', 'username', 'change']


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
    if 'wallet' in command.lower() and any(cmd in command.lower() for cmd in wallet_commands):
        wallet_voice_interaction(command)
    elif 'trade' in command.lower() and any(cmd in command.lower() for cmd in trade_commands):
        trade_voice_interaction(command)
    elif 'configuration' in command.lower() and any(cmd in command.lower() for cmd in config_commands):
        config_voice_interaction(command)
    elif 'user' in command.lower() and any(cmd in command.lower() for cmd in user_commands):
        user_voice_interaction(command)
    elif 'logout' in command.lower() or 'exit' in command.lower():
        logout()
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
