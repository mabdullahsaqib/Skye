import requests
from .auth import get_token

BASE_URL = "http://217.196.51.52:4009"


def make_authenticated_request(endpoint, method="GET", data=None):
    """Makes an authenticated request to the API."""
    token = get_token()

    if not token:
        print("Authentication token not found. Please log in.")
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"{BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed! Error: {response.text}")
        return None