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
    response = make_authenticated_request("/user/change-username", method="POST", data={"new_username": new_username})
    if response:
        print("Username Changed:", response)
        return response
    return None
