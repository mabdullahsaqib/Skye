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

def buy_token(token_data):
    """Buy a token."""
    response = make_authenticated_request("/trade/buy-token", method="POST", data=token_data)
    if response:
        print("Token Bought:", response)
        return response
    return None

def sell_token(token_data):
    """Sell a token."""
    response = make_authenticated_request("/trade/sell-token", method="POST", data=token_data)
    if response:
        print("Token Sold:", response)
        return response
    return None

def create_buy_order(order_data):
    """Create a buy order."""
    response = make_authenticated_request("/trade/create-buy-order", method="POST", data=order_data)
    if response:
        print("Buy Order Created:", response)
        return response
    return None

def create_sell_order(order_data):
    """Create a sell order."""
    response = make_authenticated_request("/trade/create-sell-order", method="POST", data=order_data)
    if response:
        print("Sell Order Created:", response)
        return response
    return None

def cancel_order(order_id):
    """Cancel a trade order."""
    response = make_authenticated_request("/trade/cancel-order", method="POST", data={"order_id": order_id})
    if response:
        print("Order Canceled:", response)
        return response
    return None

def get_live_orders():
    """Get live orders."""
    response = make_authenticated_request("/trade/live-orders", method="GET")
    if response:
        print("Live Orders:", response)
        return response
    return None

def get_past_orders():
    """Get past orders."""
    response = make_authenticated_request("/trade/past-orders", method="GET")
    if response:
        print("Past Orders:", response)
        return response
    return None

def get_tracked_tokens():
    """Get all tracked tokens."""
    response = make_authenticated_request("/trade/get-tracked-tokens", method="POST")
    if response:
        print("Tracked Tokens:", response)
        return response
    return None

def get_tracked_token(token_id):
    """Get details of a tracked token."""
    response = make_authenticated_request(f"/trade/get-tracked-token?token_id={token_id}", method="GET")
    if response:
        print("Tracked Token:", response)
        return response
    return None


def trade_voice_interaction(command):
    """Handle trade commands."""
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
    elif 'create buy order' in command:
        speak_response("What order would you like to create?")
        order_data = listen_to_command()
        if order_data:
            response = create_buy_order(order_data)
            speak_response(response)
    elif 'create sell order' in command:
        speak_response("What order would you like to create?")
        order_data = listen_to_command()
        if order_data:
            response = create_sell_order(order_data)
            speak_response(response)
    elif 'cancel order' in command:
        speak_response("What is the order ID?")
        order_id = listen_to_command()
        if order_id:
            response = cancel_order(order_id)
            speak_response(response)
    elif 'live orders' in command:
        response = get_live_orders()
        speak_response(response)
    elif 'past orders' in command:
        response = get_past_orders()
        speak_response(response)
    elif 'tracked tokens' in command:
        response = get_tracked_tokens()
        speak_response(response)
    elif 'tracked token' in command:
        speak_response("What is the token ID?")
        token_id = listen_to_command()
        if token_id:
            response = get_tracked_token(token_id)
            speak_response(response)
    else:
        speak_response("I'm not sure how to handle that trade command.")