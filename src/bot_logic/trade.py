from .api_requests import make_authenticated_request

def buy_token(token_data):
    """Buy a token."""
    response = make_authenticated_request("/trade/buy-token", method="POST", data=token_data)
    if response:
        return {"status": "success", "message": "Token bought successfully.", "data": response}
    return {"status": "error", "message": "Failed to buy token."}


def sell_token(token_data):
    """Sell a token."""
    response = make_authenticated_request("/trade/sell-token", method="POST", data=token_data)
    if response:
        return {"status": "success", "message": "Token sold successfully.", "data": response}
    return {"status": "error", "message": "Failed to sell token."}


def create_buy_order(order_data):
    """Create a buy order."""
    response = make_authenticated_request("/trade/create-buy-order", method="POST", data=order_data)
    if response:
        return {"status": "success", "message": "Buy order created successfully.", "data": response}
    return {"status": "error", "message": "Failed to create buy order."}


def create_sell_order(order_data):
    """Create a sell order."""
    response = make_authenticated_request("/trade/create-sell-order", method="POST", data=order_data)
    if response:
        return {"status": "success", "message": "Sell order created successfully.", "data": response}
    return {"status": "error", "message": "Failed to create sell order."}


def cancel_order(order_id):
    """Cancel a trade order."""
    response = make_authenticated_request("/trade/cancel-order", method="POST", data={"orderKey": order_id})
    if response:
        return {"status": "success", "message": "Order canceled successfully.", "data": response}
    return {"status": "error", "message": "Failed to cancel order."}


def get_live_orders():
    """Get live orders."""
    response = make_authenticated_request("/trade/live-orders", method="GET")
    if response:
        return {"status": "success", "message": "Live orders retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch live orders."}


def get_past_orders():
    """Get past orders."""
    response = make_authenticated_request("/trade/past-orders", method="GET")
    if response:
        return {"status": "success", "message": "Past orders retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch past orders."}


def get_tracked_tokens(reasons):
    """Get all tracked tokens with specified reasons."""
    data = {"reasons": reasons}
    response = make_authenticated_request("/trade/get-tracked-tokens", method="POST", data=data)
    if response:
        return {"status": "success", "message": "Tracked tokens retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch tracked tokens."}


def get_tracked_token(token_id):
    """Get details of a tracked token."""
    response = make_authenticated_request(f"/trade/get-tracked-token?mint={token_id}", method="GET")
    if response:
        return {"status": "success", "message": "Tracked token retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch tracked token."}


def get_spl_token(mint):
    """Get details of a SPL token."""
    response = make_authenticated_request(f"/trade/spl-token?mint={mint}", method="GET")
    if response:
        return {"status": "success", "message": "SPL token details retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch SPL token details."}


def trade_voice_interaction(command, data=None):
    """
    Handle trade-related commands.
    :param command: The command string provided by the user.
    :param data: Optional dictionary containing additional data for commands.
    """
    if 'buy' in command and 'create' not in command:
        return buy_token(data) if data else {"status": "error", "message": "Token data required to buy."}
    elif 'sell' in command and 'create' not in command:
        return sell_token(data) if data else {"status": "error", "message": "Token data required to sell."}
    elif 'buy' in command and 'create' in command:
        return create_buy_order(data) if data else {"status": "error", "message": "Order data required to create buy order."}
    elif 'sell' in command and 'create' in command:
        return create_sell_order(data) if data else {"status": "error", "message": "Order data required to create sell order."}
    elif 'cancel' in command:
        return cancel_order(data.get("orderKey")) if data and "orderKey" in data else {"status": "error", "message": "Order ID required to cancel order."}
    elif 'live' in command:
        return get_live_orders()
    elif 'past' in command:
        return get_past_orders()
    elif 'spl' in command:
        return get_spl_token(data.get("mint")) if data and "mint" in data else {"status": "error", "message": "Mint ID required to fetch SPL token details."}
    elif 'tokens' in command:
        return get_tracked_tokens(data)
    elif 'token' in command:
        return get_tracked_token(data.get("mint")) if data and "mint" in data else {"status": "error", "message": "Token ID required to fetch tracked token details."}
    else:
        return {"status": "error", "message": "Unknown trade command."}
