from api_requests import make_authenticated_request

def update_config(config_data):
    """Update the configuration."""
    response = make_authenticated_request("/config/update", method="POST", data=config_data)
    if response:
        print("Configuration Updated:", response)
        return response
    return None


def get_config():
    """Get the current configuration."""
    response = make_authenticated_request("/config/get", method="GET")
    if response:
        print("Configuration:", response)
        return response
    return None


def config_voice_interaction(command):
    """Handle the user's command related to configuration."""
    if 'get' in command or 'view' in command:
        response = get_config()
        print(response)
    elif 'update' in command or 'set' in command:
        print("What configuration data would you like to update?")
        config_data = input()
        if config_data:
            response = update_config(config_data)
            print(response)
