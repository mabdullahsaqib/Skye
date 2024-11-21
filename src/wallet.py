from api_requests import make_authenticated_request

def generate_wallet():
    """Generate a new wallet."""
    response = make_authenticated_request("/wallet/generate", method="POST")
    if response:
        print("Wallet Generated:", response)
        return response
    return None

def add_wallet(wallet_data):
    """Add a new wallet."""
    response = make_authenticated_request("/wallet/add", method="POST", data=wallet_data)
    if response:
        print("Wallet Added:", response)
        return response
    return None

def remove_wallet(wallet_id):
    """Remove a wallet."""
    response = make_authenticated_request("/wallet/remove", method="POST", data={"wallet_id": wallet_id})
    if response:
        print("Wallet Removed:", response)
        return response
    return None

def get_default_wallet():
    """Get the default wallet."""
    response = make_authenticated_request("/wallet/default", method="GET")
    if response:
        print("Default Wallet:", response)
        return response
    return None

def get_all_wallets():
    """Get all wallets."""
    response = make_authenticated_request("/wallet/all", method="GET")
    if response:
        print("All Wallets:", response)
        return response
    return None

def get_wallet_balance(wallet_id):
    """Get the balance of a specific wallet."""
    response = make_authenticated_request(f"/wallet/balance?wallet_id={wallet_id}", method="GET")
    if response:
        print("Wallet Balance:", response)
        return response
    return None
