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


def generate_wallet():
    """Generate a new wallet."""
    response = make_authenticated_request("/wallet/generate", method="POST")
    if response:
        print("Wallet Generated:", response)
        return response
    return None

def add_wallet(wallet_data):
    """Add a new wallet."""
    response = make_authenticated_request("/wallet/add", method="POST", data=wallet_data)
    if response:
        print("Wallet Added:", response)
        return response
    return None

def remove_wallet(wallet_id):
    """Remove a wallet."""
    response = make_authenticated_request("/wallet/remove", method="POST", data={"wallet_id": wallet_id})
    if response:
        print("Wallet Removed:", response)
        return response
    return None

def get_default_wallet():
    """Get the default wallet."""
    response = make_authenticated_request("/wallet/default", method="GET")
    if response:
        print("Default Wallet:", response)
        return response
    return None

def get_all_wallets():
    """Get all wallets."""
    response = make_authenticated_request("/wallet/all", method="GET")
    if response:
        print("All Wallets:", response)
        return response
    return None

def get_wallet_balance(wallet_id):
    """Get the balance of a specific wallet."""
    response = make_authenticated_request(f"/wallet/balance?wallet_id={wallet_id}", method="GET")
    if response:
        print("Wallet Balance:", response)
        return response
    return None

def wallet_voice_interaction(command):
    """Handle voice commands related to wallets."""
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
    elif 'default' in command:
        response = get_default_wallet()
        speak_response(response)
    elif 'all' in command:
        response = get_all_wallets()
        speak_response(response)
    elif 'balance' in command:
        speak_response("Which wallet would you like to check the balance of?")
        wallet_id = listen_to_command()
        if wallet_id:
            response = get_wallet_balance(wallet_id)
            speak_response(response)
    else:
        speak_response("I'm not sure how to handle that wallet command.")
