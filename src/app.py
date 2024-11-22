import os
from flask import Flask, request, jsonify
from bot_logic.auth import login, logout, validate_token
from bot_logic.voice_interaction import handle_user_command

app = Flask(__name__)

# To store user login state and token
user_logged_in = False
current_token = None  # Store the Bearer token


@app.route("/login", methods=["POST"])
def login_user():
    """Login the user."""
    global user_logged_in, current_token
    if user_logged_in:
        return jsonify({"message": "User already logged in"}), 200

    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    try:
        token = login(username, password)
        if token:
            user_logged_in = True
            current_token = token
            return jsonify({"message": "Login successful", "token": token}), 200
        else:
            return jsonify({"error": "Login failed. Please check your credentials."}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


@app.route("/logout", methods=["POST"])
def logout_user():
    """Logout the user."""
    global user_logged_in, current_token
    if not user_logged_in:
        return jsonify({"error": "No user is logged in"}), 400

    try:
        flag = logout()
        if flag:
            user_logged_in = False
            current_token = None  # Clear the token
            return jsonify({"message": "Logout successful"}), 200
        else:
            return jsonify({"error": "Logout failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(Debug=True)
