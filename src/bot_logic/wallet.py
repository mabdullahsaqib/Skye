from .api_requests import make_authenticated_request

def generate_wallet(label):
    """Generate a new wallet."""
    response = make_authenticated_request("/wallet/generate", method="POST", data={"label": label})
    if response:
        return {"status": "success", "message": "Wallet generated successfully.", "data": response}
    return {"status": "error", "message": "Failed to generate wallet."}


def add_wallet(privateKey, label):
    """Add a new wallet."""
    response = make_authenticated_request("/wallet/add", method="POST", data={"privateKey": privateKey, "label": label})
    if response:
        return {"status": "success", "message": "Wallet added successfully.", "data": response}
    return {"status": "error", "message": "Failed to add wallet."}


def remove_wallet(wallet_id):
    """Remove a wallet."""
    response = make_authenticated_request("/wallet/remove", method="POST", data={"address": wallet_id})
    if response:
        return {"status": "success", "message": "Wallet removed successfully.", "data": response}
    return {"status": "error", "message": "Failed to remove wallet."}


def get_default_wallet():
    """Get the default wallet."""
    response = make_authenticated_request("/wallet/default", method="GET")
    if response:
        return {"status": "success", "message": "Default wallet retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch default wallet."}


def set_default_wallet(wallet_id):
    """Set the default wallet."""
    response = make_authenticated_request("/wallet/default", method="POST", data={"address": wallet_id})
    if response:
        return {"status": "success", "message": "Default wallet set successfully.", "data": response}
    return {"status": "error", "message": "Failed to set default wallet."}


def get_all_wallets():
    """Get all wallets."""
    response = make_authenticated_request("/wallet/all", method="GET")
    if response:
        return {"status": "success", "message": "All wallets retrieved.", "data": response}
    return {"status": "error", "message": "Failed to retrieve wallets."}


def get_wallet_balance(wallet_id):
    """Get the balance of a specific wallet."""
    response = make_authenticated_request(f"/wallet/balance?address={wallet_id}", method="GET")
    if response:
        return {"status": "success", "message": "Wallet balance retrieved.", "data": response}
    return {"status": "error", "message": "Failed to retrieve wallet balance."}

def rename_wallet(wallet_id, new_label):
    """Rename a wallet."""
    response = make_authenticated_request("/wallet/rename", method="POST", data={"address": wallet_id, "label": new_label})
    if response:
        return {"status": "success", "message": "Wallet renamed successfully.", "data": response}
    return {"status": "error", "message": "Failed to rename wallet."}

def get_wallet_by_label(label):
    """Get wallet by label."""
    response = make_authenticated_request(f"/wallet/by-label?label={label}", method="GET")
    if response:
        return {"status": "success", "message": "Wallet retrieved.", "data": response}
    return {"status": "error", "message": "Failed to retrieve wallet."}


def wallet_voice_interaction(command, data=None):
    """
    Handle wallet-related commands.
    :param command: The command issued by the user.
    :param data: Optional dictionary containing additional data for the command.
    """
    if 'generate' in command or 'create' in command:
        if data and "label" in data:
            return generate_wallet(data["label"])
    elif 'add' in command:
        if data and "privateKey" in data:
            return add_wallet(data["privateKey"], data["label"])
        return {"status": "error", "message": "Private key is required to add a wallet."}
    elif 'remove' in command or 'delete' in command:
        if data and "address" in data:
            return remove_wallet(data["address"])
        return {"status": "error", "message": "Wallet address is required to remove a wallet."}
    elif 'get' in command and 'default' in command:
        return get_default_wallet()
    elif ('set' in command or 'make' in command) and 'default' in command:
        if data and "address" in data:
            return set_default_wallet(data["address"])
        return {"status": "error", "message": "Wallet address is required to set default wallet."}
    elif 'get' in command and  'by' in command and 'label' in command:
        if data and "label" in data:
            return get_wallet_by_label(data["label"])
        return {"status": "error", "message": "Wallet label is required to fetch wallet."}
    elif 'all' in command or 'list' in command:
        return get_all_wallets()
    elif 'rename' in command:
        if data and "address" in data and "label" in data:
            return rename_wallet(data["address"], data["label"])
        return {"status": "error", "message": "Wallet address and new label are required to rename a wallet."}
    elif 'balance' in command:
        if data and "address" in data:
            return get_wallet_balance(data["address"])
        return {"status": "error", "message": "Wallet address is required to fetch balance."}
    else:
        return {"status": "error", "message": "Unknown wallet command."}
