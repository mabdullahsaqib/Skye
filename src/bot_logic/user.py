from .api_requests import make_authenticated_request

def get_user_data():
    """Get the current user's data."""
    response = make_authenticated_request("/user/get-me", method="GET")
    if response:
        return {"status": "success", "data": response}
    return {"status": "error", "message": "Failed to fetch user data."}


def change_username(new_username):
    """Change the username of the current user."""
    response = make_authenticated_request("/user/change-username", method="POST", data={"username": new_username})
    if response:
        return {"status": "success", "message": "Username changed successfully.", "data": response}
    return {"status": "error", "message": "Failed to change username."}


def user_voice_interaction(command, data=None):
    """
    Handle the user's command and take appropriate action.
    :param command: The command issued by the user.
    :param data: Optional data required for specific commands (e.g., new username).
    """
    if 'data' in command or 'get' in command:
        return get_user_data()
    elif 'change username' in command:
        if data and "new_username" in data:
            return change_username(data["new_username"])
        return {"status": "error", "message": "New username is required to change username."}
    else:
        return {"status": "error", "message": "Unknown user command."}
