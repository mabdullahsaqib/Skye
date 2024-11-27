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
    response = make_authenticated_request("/trade/get-tracked-tokens", method="POST", data={"reasons": reasons})
    if response:
        return {"status": "success", "message": "Tracked tokens retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch tracked tokens."}

def make_reasons_list(data):
    """Create a list of reasons from the data. e.g, "mc_x" | "burned" | "renounced" | "moonshot_migrated" | "moonshot_migrating" | "pumpfun_migrated" | "pumpfun_migrating" | "new_pool" """

    reasons = []
    if "mc_x" in data["reasons"]:
        reasons.append("mc_x")
    if "burned" in data["reasons"]:
        reasons.append("burned")
    if "renounced" in data["reasons"]:
        reasons.append("renounced")
    if "moonshot_migrated" in data["reasons"]:
        reasons.append("moonshot_migrated")
    if "moonshot_migrating" in data["reasons"]:
        reasons.append("moonshot_migrating")
    if "pumpfun_migrated" in data["reasons"]:
        reasons.append("pumpfun_migrated")
    if "pumpfun_migrating" in data["reasons"]:
        reasons.append("pumpfun_migrating")
    if "new_pool" in data["reasons"]:
        reasons.append("new_pool")
    return reasons


def get_tracked_token(token_id):
    """Get details of a tracked token."""
    response = make_authenticated_request(f"/trade/get-tracked-token?mint={token_id}", method="GET")
    if response:
        return {"status": "success", "message": "Tracked token retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch tracked token."}


def get_spl_token(mint=None, name=None):
    """Get details of a SPL token."""
    if mint and name:
        response = make_authenticated_request(f"/trade/spl-token?mint={mint}&name={name}", method="GET")
    elif mint:
        response = make_authenticated_request(f"/trade/spl-token?mint={mint}", method="GET")
    elif name:
        response = make_authenticated_request(f"/trade/spl-token?name={name}", method="GET")
    else:
        return {"status": "error", "message": "Mint or label required to fetch SPL token."}
    if response:
        return {"status": "success", "message": "SPL token retrieved.", "data": response}
    return {"status": "error", "message": "Failed to fetch SPL token."}


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
        if data and ("mint" in data and "name" in data):
            return get_spl_token(data["mint"], data["name"])
        elif data and "mint" in data:
            return get_spl_token(data["mint"])
        elif data and "name" in data:
            return get_spl_token(name=data["name"])
        return {"status": "error", "message": "Mint or name required to fetch SPL token."}
    elif 'tokens' in command:
        reasons = make_reasons_list(data)
        return get_tracked_tokens(reasons)
    elif 'token' in command:
        return get_tracked_token(data.get("mint")) if data and "mint" in data else {"status": "error", "message": "Token ID required to fetch tracked token details."}
    else:
        return {"status": "error", "message": "Unknown trade command."}
