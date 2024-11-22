from flask import Flask, request, jsonify
from bot_logic.auth import login, logout
from bot_logic.voice_interaction import handle_user_command

app = Flask(__name__)

# To store user login state
user_logged_in = False

@app.route("/login", methods=["POST"])
def login_user():
    """Login the user."""
    global user_logged_in
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    try:
        token = login(username, password)
        user_logged_in = True
        return jsonify({"message": "Login successful", "token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/command", methods=["POST"])
def execute_command():
    """Execute user commands."""
    global user_logged_in

    if not user_logged_in:
        return jsonify({"error": "User not logged in. Please log in first."}), 401

    data = request.get_json()

    if not data or "command" not in data:
        return jsonify({"error": "Command is required"}), 400

    command = data["command"]
    additional_data = data.get("data")  # Optional data for specific commands

    try:
        response = handle_user_command(command, additional_data)
        return jsonify({"message": "Command executed successfully", "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/logout", methods=["POST"])
def logout_user():
    """Logout the user."""
    global user_logged_in
    if not user_logged_in:
        return jsonify({"error": "No user is logged in"}), 400

    try:
        logout()
        user_logged_in = False
        return jsonify({"message": "Logout successful"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
