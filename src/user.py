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

def user_login():
    """Function to log in a user."""
    speak("Please provide your username.")
    username = input("username : " )

    speak("Please provide your password.")
    password = input("password : ")

    if username and password:
        payload = {"username": username, "password": password}
        response = make_request("POST", "/user/login", data=payload)

        if "error" in response:
            speak(f"Login failed. {response['error']}")
        else:
            token = response.get("token")
            HEADERS["Authorization"] = f"Bearer {token}"
            speak("Login successful. How can I assist you today?")
    else:
        speak("Login canceled. I couldn't understand your credentials.")

def get_user_data():
    """Function to fetch the current user's data."""
    response = make_request("GET", "/user/get-me", auth=True)

    if "error" in response:
        speak(f"Failed to fetch user data. {response['error']}")
    else:
        username = response.get("username", "Unknown")
        email = response.get("email", "Unknown")
        speak(f"Your username is {username} and your email is {email}.")

def change_username():
    """Function to change the username of the user."""
    speak("Please provide your new username.")
    new_username = listen()

    if new_username:
        payload = {"username": new_username}
        response = make_request("POST", "/user/change-username", data=payload, auth=True)

        if "error" in response:
            speak(f"Failed to change username. {response['error']}")
        else:
            speak("Username updated successfully.")
    else:
        speak("I couldn't understand your new username.")

def user_logout():
    """Function to log out the user."""
    response = make_request("POST", "/user/logout", auth=True)

    if "error" in response:
        speak(f"Logout failed. {response['error']}")
    else:
        HEADERS.pop("Authorization", None)  # Remove the token
        speak("You have been logged out successfully.")


print("Say 'login' to log in, 'get user' to fetch your data, 'change username' to update your username, or 'logout' to log out.")

while True:
    user_input = listen()
    if user_input and "exit" in user_input.lower():
        speak("Goodbye!")
        break
    elif user_input and "login" in user_input.lower():
        user_login()
    elif user_input and "get user" in user_input.lower():
        get_user_data()
    elif user_input and "change username" in user_input.lower():
        change_username()
    elif user_input and "logout" in user_input.lower():
        user_logout()
    else:
        speak("I didn't understand that. Try saying 'login', 'get user', 'change username', or 'logout'.")
