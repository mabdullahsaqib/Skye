from api_requests import make_authenticated_request

def buy_token(token_data):
    """Buy a token."""
    response = make_authenticated_request("/trade/buy-token", method="POST", data=token_data)
    if response:
        print("Token Bought:", response)
        return response
    return None

def sell_token(token_data):
    """Sell a token."""
    response = make_authenticated_request("/trade/sell-token", method="POST", data=token_data)
    if response:
        print("Token Sold:", response)
        return response
    return None

def create_buy_order(order_data):
    """Create a buy order."""
    response = make_authenticated_request("/trade/create-buy-order", method="POST", data=order_data)
    if response:
        print("Buy Order Created:", response)
        return response
    return None

def create_sell_order(order_data):
    """Create a sell order."""
    response = make_authenticated_request("/trade/create-sell-order", method="POST", data=order_data)
    if response:
        print("Sell Order Created:", response)
        return response
    return None

def cancel_order(order_id):
    """Cancel a trade order."""
    response = make_authenticated_request("/trade/cancel-order", method="POST", data={"order_id": order_id})
    if response:
        print("Order Canceled:", response)
        return response
    return None

def get_live_orders():
    """Get live orders."""
    response = make_authenticated_request("/trade/live-orders", method="GET")
    if response:
        print("Live Orders:", response)
        return response
    return None

def get_past_orders():
    """Get past orders."""
    response = make_authenticated_request("/trade/past-orders", method="GET")
    if response:
        print("Past Orders:", response)
        return response
    return None

def get_tracked_tokens():
    """Get all tracked tokens."""
    response = make_authenticated_request("/trade/get-tracked-tokens", method="POST")
    if response:
        print("Tracked Tokens:", response)
        return response
    return None

def get_tracked_token(token_id):
    """Get details of a tracked token."""
    response = make_authenticated_request(f"/trade/get-tracked-token?token_id={token_id}", method="GET")
    if response:
        print("Tracked Token:", response)
        return response
    return None
