import os
import requests

# URL of the API
BASE_URL = "http://217.196.51.52:4009"


def login(wallet: str, message: str):
    """
    Logs in a user using their wallet address and a message.

    Args:
        wallet (str): Wallet address of the user.
        message (str): Message to authenticate the user.

    Returns:
        dict: A dictionary containing the token and user data if successful.
    """
    url = f"{BASE_URL}/user/login"
    payload = {
        "wallet": wallet,
        "message": message
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json().get("data", {})
        token = data.get("token")
        os.environ["AUTH_TOKEN"] = token  # Store token for subsequent requests
        print(f"Login successful! Token: {token}")
        return data
    else:
        print(f"Login failed! Error: {response.text}")
        return None


def logout():
    """
    Logs out the user and invalidates the auth token.
    """
    url = f"{BASE_URL}/user/logout"
    token = os.getenv("AUTH_TOKEN")

    if token:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print("Logged out successfully!")
            os.environ["AUTH_TOKEN"] = ""  # Clear the token from the environment
            return True
        else:
            print(f"Logout failed! Error: {response.text}")
            return False
    else:
        print("No token found. Cannot log out.")
        return False


def get_token():
    """Returns the stored auth token."""
    return os.getenv("AUTH_TOKEN")
