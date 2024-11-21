import os
import requests

# URL of the API
BASE_URL = "http://217.196.51.52:4009"


def login(username, password):
    """Logs in a user and returns the auth token."""
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # Assuming the response contains the token
        token = response.json().get("token")
        print(f"Login successful! Token: {token}")
        os.environ["AUTH_TOKEN"] = token  # Store token in the environment variable
        return token
    else:
        print(f"Login failed! Error: {response.text}")
        return None


def logout():
    """Logs out the user and invalidates the auth token."""
    url = f"{BASE_URL}/user/logout"
    token = os.getenv("AUTH_TOKEN")

    if token:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print("Logged out successfully!")
            os.environ["AUTH_TOKEN"] = ""  # Clear the stored token
        else:
            print(f"Logout failed! Error: {response.text}")
    else:
        print("No token found, cannot log out.")


def get_token():
    """Returns the stored auth token."""
    return os.getenv("AUTH_TOKEN")
