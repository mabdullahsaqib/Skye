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

def generate_wallet():
    """Function to generate a new wallet."""
    response = make_request("POST", "/wallet/generate", auth=True)

    if "error" in response:
        speak(f"Failed to generate a wallet. {response['error']}")
    else:
        wallet_address = response.get("address", "an unknown address")
        speak(f"A new wallet has been successfully generated. The address is {wallet_address}.")

def get_all_wallets():
    """Function to retrieve all wallets."""
    response = make_request("GET", "/wallet/all", auth=True)

    if "error" in response:
        speak(f"Failed to fetch wallets. {response['error']}")
    else:
        wallets = response.get("wallets", [])
        if not wallets:
            speak("No wallets found.")
        else:
            wallet_list = "\n".join(wallets)
            speak(f"The following wallets are available: {wallet_list}")

def get_default_wallet():
    """Function to fetch the default wallet."""
    response = make_request("GET", "/wallet/default", auth=True)

    if "error" in response:
        speak(f"Failed to retrieve the default wallet. {response['error']}")
    else:
        default_wallet = response.get("address", "unknown")
        speak(f"The default wallet address is {default_wallet}.")

def set_default_wallet():
    """Function to set a wallet as the default."""
    speak("Please provide the address of the wallet you'd like to set as default.")
    wallet_address = listen()

    if wallet_address:
        payload = {"address": wallet_address}
        response = make_request("POST", "/wallet/make-default", data=payload, auth=True)

        if "error" in response:
            speak(f"Failed to set the wallet as default. {response['error']}")
        else:
            speak(f"The wallet {wallet_address} has been set as default successfully.")
    else:
        speak("I didn't get any wallet address.")

def get_wallet_balance():
    """Function to fetch the balance of a wallet."""
    speak("Please provide the address of the wallet to check its balance.")
    wallet_address = listen()

    if wallet_address:
        response = make_request("GET", "/wallet/balance", params={"address": wallet_address}, auth=True)

        if "error" in response:
            speak(f"Failed to fetch the balance. {response['error']}")
        else:
            balance = response.get("balance", 0)
            speak(f"The balance of the wallet {wallet_address} is {balance} DOGE.")
    else:
        speak("I didn't get any wallet address.")

def add_wallet():
    """Function to add a new wallet."""
    speak("Please provide the address of the wallet you'd like to add.")
    wallet_address = listen()

    if wallet_address:
        payload = {"address": wallet_address}
        response = make_request("POST", "/wallet/add", data=payload, auth=True)

        if "error" in response:
            speak(f"Failed to add the wallet. {response['error']}")
        else:
            speak(f"The wallet with address {wallet_address} has been added successfully.")
    else:
        speak("I didn't get any wallet address.")

def remove_wallet():
    """Function to remove a wallet."""
    speak("Please provide the address of the wallet you'd like to remove.")
    wallet_address = listen()

    if wallet_address:
        payload = {"address": wallet_address}
        response = make_request("POST", "/wallet/remove", data=payload, auth=True)

        if "error" in response:
            speak(f"Failed to remove the wallet. {response['error']}")
        else:
            speak(f"The wallet with address {wallet_address} has been removed successfully.")
    else:
        speak("I didn't get any wallet address.")

print(
    "Say 'generate wallet' to create a new wallet, 'get wallets' to list all wallets, "
    "'default wallet' to fetch the default wallet, 'set default wallet' to set a wallet as default, "
    "'wallet balance' to check the balance of a wallet, "
    "'add wallet' to add a wallet, or 'remove wallet' to remove a wallet."
)

while True:
    user_input = listen()
    if user_input and "exit" in user_input.lower():
        speak("Goodbye!")
        break
    elif user_input and "generate wallet" in user_input.lower():
        generate_wallet()
    elif user_input and "get wallets" in user_input.lower():
        get_all_wallets()
    elif user_input and "default wallet" in user_input.lower():
        get_default_wallet()
    elif user_input and "set default wallet" in user_input.lower():
        set_default_wallet()
    elif user_input and "wallet balance" in user_input.lower():
        get_wallet_balance()
    elif user_input and "add wallet" in user_input.lower():
        add_wallet()
    elif user_input and "remove wallet" in user_input.lower():
        remove_wallet()
    else:
        speak("I didn't understand that. Try asking about wallets.")
