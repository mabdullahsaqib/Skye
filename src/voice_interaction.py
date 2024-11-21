import pyttsx3
import speech_recognition as sr
from wallet import generate_wallet, add_wallet, remove_wallet
from trade import buy_token, sell_token
from configuration import get_config, update_config
from user import get_user_data, change_username

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
    if 'wallet' in command:
        if 'generate' in command:
            response = generate_wallet()
            speak_response(response)
        elif 'add' in command:
            speak_response("What wallet would you like to add?")
            wallet_data = listen_to_command()
            if wallet_data:
                response = add_wallet(wallet_data)
                speak_response(response)
        elif 'remove' in command:
            speak_response("Which wallet would you like to remove?")
            wallet_id = listen_to_command()
            if wallet_id:
                response = remove_wallet(wallet_id)
                speak_response(response)
        else:
            speak_response("I'm not sure how to handle that command.")

    elif 'trade' in command:
        if 'buy' in command:
            speak_response("What token would you like to buy?")
            token_data = listen_to_command()
            if token_data:
                response = buy_token(token_data)
                speak_response(response)
        elif 'sell' in command:
            speak_response("What token would you like to sell?")
            token_data = listen_to_command()
            if token_data:
                response = sell_token(token_data)
                speak_response(response)
        else:
            speak_response("I'm not sure how to handle that trade command.")

    elif 'config' in command:
        if 'get' in command:
            response = get_config()
            speak_response(response)
        elif 'update' in command:
            speak_response("What configuration would you like to update?")
            config_data = listen_to_command()
            if config_data:
                response = update_config(config_data)
                speak_response(response)
        else:
            speak_response("I'm not sure how to handle that config command.")

    elif 'user' in command:
        if 'get' in command:
            response = get_user_data()
            speak_response(response)
        elif 'change' in command:
            speak_response("What would you like to change your username to?")
            new_username = listen_to_command()
            if new_username:
                response = change_username(new_username)
                speak_response(response)
        else:
            speak_response("I'm not sure how to handle that user command.")

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
