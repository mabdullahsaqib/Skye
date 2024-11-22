from api_requests import make_authenticated_request

def update_config(config_data: dict) -> dict:
    """
    Updates the configuration settings.

    Args:
        config_data (dict): A dictionary containing configuration fields to update.
            Example fields include:
            - amountInSOL: float
            - autoSniping: bool
            - burnLP: bool
            - dexPaid: bool
            - jitoTip: float
            - launchTime: int
            - maxMarketCap: int
            - minMarketCap: int
            - renounced: bool
            - slippage: int
            - top10HP: int

    Returns:
        dict: Updated configuration details or None if the request fails.
    """
    response = make_authenticated_request("/config/update", method="POST", data=config_data)
    if response:
        print("Configuration updated successfully:", response.get("data", {}))
        return response.get("data")
    else:
        print("Failed to update configuration.")
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
