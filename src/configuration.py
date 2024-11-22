from api_requests import make_authenticated_request


def update_config(config_data: dict) -> dict:
    """
    Update the configuration settings.

    Args:
        config_data (dict): A dictionary containing configuration fields to update.

    Returns:
        dict: The updated configuration details or an error message.
    """
    response = make_authenticated_request("/config/update", method="POST", data=config_data)
    if response:
        return {"status": "success", "message": "Configuration updated successfully.", "data": response.get("data")}
    return {"status": "error", "message": "Failed to update configuration."}


def get_config() -> dict:
    """
    Retrieve the current configuration settings.

    Returns:
        dict: The current configuration settings or an error message.
    """
    response = make_authenticated_request("/config/get", method="GET")
    if response:
        return {"status": "success", "message": "Configuration retrieved successfully.", "data": response}
    return {"status": "error", "message": "Failed to retrieve configuration."}


def config_voice_interaction(command: str, data=None) -> dict:
    """
    Handle configuration-related commands.

    Args:
        command (str): The command string provided by the user.
        data (dict, optional): Additional data for the command.

    Returns:
        dict: The result of the command execution.
    """
    if 'get' in command or 'view' in command:
        return get_config()
    elif 'update' in command or 'set' in command:
        if not data:
            return {"status": "error", "message": "Configuration data required to update settings."}
        return update_config(data)
    else:
        return {"status": "error", "message": "Unknown configuration command."}
