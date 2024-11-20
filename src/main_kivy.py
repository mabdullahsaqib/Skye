import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SKYE_MODEL_CONFIG = os.getenv('SKYE_MODEL_CONFIG')

# Configure the generative model
genai.configure()
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
chat_session = model.start_chat(history=[])

# Text-to-Speech setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 250)

def speak(text):
    """Speak out the provided text."""
    engine.say(text)
    engine.runAndWait()

# Kivy App Layout
class ChatApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")
        self.chat_history = Label(size_hint=(1, 0.8), text="Welcome to Skye!\n")
        self.layout.add_widget(self.chat_history)

        self.listen_button = Button(size_hint=(1, 0.2), text="Tap to Speak")
        self.listen_button.bind(on_press=self.start_listening)
        self.layout.add_widget(self.listen_button)

        return self.layout

    def start_listening(self, instance):
        Clock.schedule_once(self.listen)

    def listen(self, dt):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                speak("Listening...")
                self.chat_history.text += "\nListening..."
                audio_data = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio_data)
                self.chat_history.text += f"\nYou: {user_input}"
                self.get_response(user_input)
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that.")
                self.chat_history.text += "\nSorry, I didn't catch that."
            except sr.RequestError:
                speak("Speech recognition service is unavailable.")
                self.chat_history.text += "\nSpeech recognition service is unavailable."

    def get_response(self, user_input):
        if "exit" in user_input.lower():
            speak("Goodbye!")
            self.stop()
        else:
            try:
                response = chat_session.send_message(user_input)
                bot_response = response.text
                self.chat_history.text += f"\nSkye: {bot_response}"
                speak(bot_response)
            except Exception:
                speak("Excuse me? I won't say that.")
                self.chat_history.text += "\nExcuse me? I won't say that."

if __name__ == "__main__":
    ChatApp().run()
