import os
from flask import Flask, request, jsonify
from bot_logic.auth import validate_token
from bot_logic.voice_interaction import handle_user_command
import google.generativeai as genai
import json

app = Flask(__name__)

# Configure the generative model
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Set up model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# To store user login state and token
user_logged_in = False
current_token = None  # Store the Bearer token


@app.route("/command", methods=["POST"])
def execute_command():
    """Execute user commands."""
    global user_logged_in, current_token

    # Check if a token is provided in the Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        provided_token = auth_header.split(" ")[1]
        if validate_token(provided_token):  # Validate the provided token
            current_token = provided_token  # Update the token in the environment
            user_logged_in = True
            os.environ["AUTH_TOKEN"] = provided_token  # Store token for subsequent requests
        else:
            return jsonify({"error": "Invalid token"}), 401

    # If still not logged in after checking for token
    if not user_logged_in:
        return jsonify({"error": "User not logged in. Please log in first."}), 401

    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Command is required"}), 400

    raw_command = data["command"]

    print(f"Raw command: {raw_command}\n\n")

    parsed_command_response = model.generate_content(f"""
Extract the required information from the following command and return a dictionary. The dictionary keys should match the expected fields for the Skye Bot API commands, and the values should be extracted or inferred from the command. If a value is missing in the command, leave it as `null`.

Expected Keys:
- command: The main action requested (e.g., "buy token", "sell token").
- mint: The mint address of a token (if applicable).
- address: A wallet address (if applicable).
- privateKey: A private key for wallets (if applicable).
- percentage: A percentage value for operations like selling tokens (if applicable).
- amount: An amount value for orders or transactions (if applicable).
- price: A price value for creating orders (if applicable).
- hours: A duration in hours for timed operations (if applicable).
- reasons: A list of reasons for token tracking (if applicable).
- config_data: A dictionary of configuration fields like "amountInSOL" or "slippage" (if applicable).
- orderKey: The key or ID of an order (if applicable).
- new_username: A new username for the user (if applicable).
- token_name: The name of the token or coin (if applicable).
- wallet_label: The label of the wallet (if applicable).

Example Inputs and Outputs:

1. Input: "buy token with mint XYZ123 and wallet address ABC456"
   Output: {{"command": "buy token", "mint": "XYZ123", "address": "ABC456", "privateKey": null, "percentage": null, "amount": null, "price": null, "hours": null, "reasons": null, "config_data": null, "orderKey": null}}

2. Input: "sell token with mint XYZ123 at 50% to wallet DEF789"
   Output: {{"command": "sell token", "mint": "XYZ123", "address": "DEF789", "privateKey": null, "percentage": "50", "amount": null, "price": null, "hours": null, "reasons": null, "config_data": null, "orderKey": null}}

3. Input: "generate wallet"
   Output: {{"command": "generate wallet", "mint": null, "address": null, "privateKey": null, "percentage": null, "amount": null, "price": null, "hours": null, "reasons": null, "config_data": null, "orderKey": null}}


Only provide the dictionary in the response. nothing more, nothing less. Don't even write anything or before the brackets.

Now process the following command: "{raw_command}"
"""
)

    try:
        # Generate the content from Gemini
        print(f"Raw response from Gemini: {parsed_command_response.text}")

        # Clean and parse the JSON
        parsed_command_text = parsed_command_response.text.strip("```").strip("json").strip()
        parsed_command = json.loads(parsed_command_text)

        print(f"Parsed command: {parsed_command}")
        response = handle_user_command(parsed_command["command"], parsed_command)
        if "Failed" in response:
            return jsonify({"error": "Invalid command"}), 400
        else:
            return jsonify({"message": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(Debug=True)
