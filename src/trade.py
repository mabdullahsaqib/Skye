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
    response = make_authenticated_request("/trade/cancel-order", method="POST", data={"orderKey": order_id})
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


def get_tracked_tokens(reasons):
    """Get all tracked tokens with specified reasons."""
    data = {"reasons": reasons}
    response = make_authenticated_request("/trade/get-tracked-tokens", method="POST", data=data)
    if response:
        print("Tracked Tokens:", response)
        return response
    return None



def get_tracked_token(token_id):
    """Get details of a tracked token."""
    response = make_authenticated_request(f"/trade/get-tracked-token?mint={token_id}", method="GET")
    if response:
        print("Tracked Token:", response)
        return response
    return None

def get_spl_token(mint):
    """Get details of a tracked token."""
    response = make_authenticated_request(f"/trade/spl-token?mint={mint}", method="GET")
    if response:
        print("Tracked Token:", response)
        return response
    return None


def get_reasons_from_input(input_text):
    """Converts user input into a list of reasons."""
    reason_map = {
        "new pool": "new_pool",
        "high volume": "high_volume",
        "low cap": "low_cap",
        "price drop": "price_drop",
        # Add more mappings here as needed
    }

    # Process the user input
    input_text = input_text.lower()
    reasons = []

    # Look for keywords in the input text
    for reason, code in reason_map.items():
        if reason in input_text:
            reasons.append(code)

    # Return the reasons found
    if reasons:
        return reasons
    else:
        print("No valid reasons found in the input.")
        return None

def trade_voice_interaction(command):
    """Handle trade commands."""
    if 'buy' in command and 'create' not in command:
        print("What token would you like to buy?")
        token_data = input()
        if token_data:
            response = buy_token(token_data)
            print(response)
    elif 'sell' in command and 'create' not in command:
        print("What token would you like to sell?")
        token_data = input()
        if token_data:
            response = sell_token(token_data)
            print(response)
    elif 'buy' in command and 'create' in command:
        print("What order would you like to create?")
        order_data = input()
        if order_data:
            response = create_buy_order(order_data)
            print(response)
    elif 'sell' in command and 'create' in command:
        print("What order would you like to create?")
        order_data = input()
        if order_data:
            response = create_sell_order(order_data)
            print(response)
    elif 'cancel' in command:
        print("What is the order ID?")
        order_id = input()
        if order_id:
            response = cancel_order(order_id)
            print(response)
    elif 'live' in command:
        response = get_live_orders()
        print(response)
    elif 'past' in command:
        response = get_past_orders()
        print(response)
    elif 'tokens' in command:
        reasons = input("What are the reasons for tracking the tokens?")
        reasons = get_reasons_from_input(reasons)
        if reasons:
            response = get_tracked_tokens(reasons)
            print(response)
    elif 'token' in command:
        print("What is the token ID?")
        token_id = input()
        if token_id:
            response = get_tracked_token(token_id)
            print(response)
    else:
        print("I'm not sure how to handle that trade command.")
