import os
import google.generativeai as genai
from dotenv import load_dotenv


# Load the environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SKYE_MODEL_CONFIG = os.getenv('SKYE_MODEL_CONFIG')

genai.configure()

# Create the model
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

print("Press exit to stop conversation. (This conversation will not be recorded)")

while True:
    user_input = input("You: ")
    if "exit" in user_input:
        break
    try:
        response = chat_session.send_message(user_input)
    except Exception as e:
        print("Excuse me? I won't say that :p\n")
        response = None
    if response:
        print("Skye:", response.text)
    else:
        continue
