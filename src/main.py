import os
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SKYE_MODEL_CONFIG = os.getenv('SKYE_MODEL_CONFIG')

# Configure the generative model
genai.configure()

# Set up model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SKYE_MODEL_CONFIG,
)

chat_session = model.start_chat(
    history=[]
)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


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


print("Press 'exit' to stop the conversation. (This conversation will not be recorded)")

while True:
    user_input = listen()
    if user_input and "exit" in user_input.lower():
        speak("Goodbye!")
        break
    elif user_input:
        try:
            response = chat_session.send_message(user_input)
            print("Skye:", response.text)
            speak(response.text)
        except Exception as e:
            print("Excuse me? I won't say that :p\n")
            speak("Excuse me? I won't say that.")
