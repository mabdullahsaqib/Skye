from auth import login
from voice_interaction import start

if __name__ == "__main__":
    # Login the user
    login("user", "password")
    # Start the voice interaction
    start()
