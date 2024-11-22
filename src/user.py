from api_requests import make_authenticated_request

def get_user_data():
    """Get the current user's data."""
    response = make_authenticated_request("/user/get-me", method="GET")
    if response:
        print("User Data:", response)
        return response
    return None


def change_username(new_username):
    """Change the username of the current user."""
    response = make_authenticated_request("/user/change-username", method="POST", data={"username": new_username})
    if response:
        print("Username Changed:", response)
        return response
    return None


def user_voice_interaction(command):
    """Handle the user's command and take appropriate action."""
    if 'data' in command or 'get' in command:
        response = get_user_data()
        print(response)
    elif 'change username' in command:
        print("What would you like your new username to be?")
        new_username = input("Enter new username: ")
        if new_username:
            response = change_username(new_username)
            print(response)
    else:
        print("I'm not sure how to handle that command.")
