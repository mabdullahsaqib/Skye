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

def buy_token():
    """Function to buy a token."""
    speak("Please provide the token symbol you'd like to buy.")
    token_symbol = listen()

    if token_symbol:
        speak("How many tokens would you like to buy?")
        token_quantity = listen()

        if token_quantity:
            payload = {
                "token_symbol": token_symbol,
                "quantity": token_quantity
            }
            response = make_request("POST", "/trade/buy-token", data=payload, auth=True)

            if "error" in response:
                speak(f"Failed to buy the token. {response['error']}")
            else:
                speak(f"Successfully bought {token_quantity} of {token_symbol}.")
        else:
            speak("I didn't catch the quantity of tokens.")
    else:
        speak("I didn't catch the token symbol.")

def sell_token():
    """Function to sell a token."""
    speak("Please provide the token symbol you'd like to sell.")
    token_symbol = listen()

    if token_symbol:
        speak("How many tokens would you like to sell?")
        token_quantity = listen()

        if token_quantity:
            payload = {
                "token_symbol": token_symbol,
                "quantity": token_quantity
            }
            response = make_request("POST", "/trade/sell-token", data=payload, auth=True)

            if "error" in response:
                speak(f"Failed to sell the token. {response['error']}")
            else:
                speak(f"Successfully sold {token_quantity} of {token_symbol}.")
        else:
            speak("I didn't catch the quantity of tokens.")
    else:
        speak("I didn't catch the token symbol.")

def create_buy_order():
    """Function to create a buy order."""
    speak("Please provide the token symbol you'd like to buy.")
    token_symbol = listen()

    if token_symbol:
        speak("How much are you willing to spend?")
        amount = listen()

        if amount:
            payload = {
                "token_symbol": token_symbol,
                "amount": amount
            }
            response = make_request("POST", "/trade/create-buy-order", data=payload, auth=True)

            if "error" in response:
                speak(f"Failed to create the buy order. {response['error']}")
            else:
                speak(f"Buy order for {token_symbol} created with {amount} as the spending amount.")
        else:
            speak("I didn't catch the amount you want to spend.")
    else:
        speak("I didn't catch the token symbol.")

def create_sell_order():
    """Function to create a sell order."""
    speak("Please provide the token symbol you'd like to sell.")
    token_symbol = listen()

    if token_symbol:
        speak("How many tokens would you like to sell?")
        quantity = listen()

        if quantity:
            payload = {
                "token_symbol": token_symbol,
                "quantity": quantity
            }
            response = make_request("POST", "/trade/create-sell-order", data=payload, auth=True)

            if "error" in response:
                speak(f"Failed to create the sell order. {response['error']}")
            else:
                speak(f"Sell order for {quantity} of {token_symbol} created.")
        else:
            speak("I didn't catch the quantity you want to sell.")
    else:
        speak("I didn't catch the token symbol.")

def cancel_order():
    """Function to cancel a previously placed order."""
    speak("Please provide the order ID you'd like to cancel.")
    order_id = listen()

    if order_id:
        payload = {
            "order_id": order_id
        }
        response = make_request("POST", "/trade/cancel-order", data=payload, auth=True)

        if "error" in response:
            speak(f"Failed to cancel the order. {response['error']}")
        else:
            speak(f"Order with ID {order_id} has been successfully cancelled.")
    else:
        speak("I didn't catch the order ID.")

def get_live_orders():
    """Function to retrieve live orders."""
    response = make_request("GET", "/trade/live-orders", auth=True)

    if "error" in response:
        speak(f"Failed to retrieve live orders. {response['error']}")
    else:
        speak("Here are your live orders.")
        print(response)  # Assuming the response contains live orders in a readable format.

def get_past_orders():
    """Function to retrieve past orders."""
    response = make_request("GET", "/trade/past-orders", auth=True)

    if "error" in response:
        speak(f"Failed to retrieve past orders. {response['error']}")
    else:
        speak("Here are your past orders.")
        print(response)  # Assuming the response contains past orders.

def get_spl_token():
    """Function to retrieve SPL token details."""
    speak("Please provide the SPL token symbol.")
    token_symbol = listen()

    if token_symbol:
        response = make_request("GET", f"/trade/spl-token?symbol={token_symbol}", auth=True)

        if "error" in response:
            speak(f"Failed to retrieve the SPL token details. {response['error']}")
        else:
            speak(f"Here are the details for SPL token {token_symbol}.")
            print(response)
    else:
        speak("I didn't catch the SPL token symbol.")

def get_tracked_tokens():
    """Function to retrieve all tracked tokens."""
    response = make_request("POST", "/trade/get-tracked-tokens", auth=True)

    if "error" in response:
        speak(f"Failed to retrieve tracked tokens. {response['error']}")
    else:
        speak("Here are your tracked tokens.")
        print(response)

def get_tracked_token():
    """Function to retrieve details of a single tracked token."""
    speak("Please provide the symbol of the tracked token.")
    token_symbol = listen()

    if token_symbol:
        response = make_request("GET", f"/trade/get-tracked-token?symbol={token_symbol}", auth=True)

        if "error" in response:
            speak(f"Failed to retrieve the tracked token details. {response['error']}")
        else:
            speak(f"Here are the details for the tracked token {token_symbol}.")
            print(response)
    else:
        speak("I didn't catch the token symbol.")

print(
    "Say 'buy token' to buy a token, 'sell token' to sell a token, "
    "'create buy order' to place a buy order, 'create sell order' to place a sell order, "
    "'cancel order' to cancel an order, 'live orders' to check live orders, "
    "'past orders' to check past orders, 'spl token' to check an SPL token, "
    "'tracked tokens' to check tracked tokens, or 'tracked token' to check a specific tracked token."
)

while True:
    user_input = listen()
    if user_input and "exit" in user_input.lower():
        speak("Goodbye!")
        break
    elif user_input and "buy token" in user_input.lower():
        buy_token()
    elif user_input and "sell token" in user_input.lower():
        sell_token()
    elif user_input and "create buy order" in user_input.lower():
        create_buy_order()
    elif user_input and "create sell order" in user_input.lower():
        create_sell_order()
    elif user_input and "cancel order" in user_input.lower():
        cancel_order()
    elif user_input and "live orders" in user_input.lower():
        get_live_orders()
    elif user_input and "past orders" in user_input.lower():
        get_past_orders()
    elif user_input and "spl token" in user_input.lower():
        get_spl_token()
    elif user_input and "tracked tokens" in user_input.lower():
        get_tracked_tokens()
    elif user_input and "tracked token" in user_input.lower():
        get_tracked_token()
    else:
        speak("I didn't understand that. Try asking about trade orders.")

