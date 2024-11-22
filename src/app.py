import os
from flask import Flask, request, jsonify
from bot_logic.auth import validate_token
from bot_logic.voice_interaction import handle_user_command

app = Flask(__name__)

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

    command = data["command"]
    additional_data = data.get("data")  # Optional data for specific commands

    try:
        print(f"Received command: {command}")
        response = handle_user_command(command, additional_data)
        if "Failed" in response:
            return jsonify({"error": "Invalid command"}), 400
        else:
            return jsonify({"message": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(Debug=True)
