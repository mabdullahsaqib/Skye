from voice_interaction import start
from auth import login

if __name__ == "__main__":
    # Login the user
    login("user", "password")
    # Start the voice interaction
    start()
