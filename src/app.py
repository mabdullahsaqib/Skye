import os
from flask import Flask, request, jsonify
from bot_logic.auth import validate_token
from bot_logic.voice_interaction import handle_user_command
import google.generativeai as genai
import json
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {"origins": ["http://localhost:3000", "https://jarvis-ai-bot.vercel.app"]}
})

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
Extract the required information from the following command and return a dictionary. The dictionary keys should match the expected fields for the Skye Bot API commands, and the values should be extracted or inferred from the command. If a value is missing in the command, leave it.

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
(  // if reason is burned, value is 0
  // if reason is new_pool, value is 0
  // if reason is renounced, value is 0
  // if reason is pumpfun_migrated, value is 100
  // if reason is moonshot_migrated, value is 100
  // if reason is pumpfun_migrating, value is percentage migrated (eg. 10%, 20%, 50%)
  // if reason is moonshot_migrating, value is percentage migrated (eg. 10%, 20%, 50%)
  // if reason is mc_x, value is in x (e.g. 2x, 5x, 10x)
    
    For burned, it means tokens whos supply was burnt
    New pools are new tokens
    and so on

    The value is  only useful in migrating where it specifies the percentage migrated
    And in mc_x, where it specifies how much has the token value increased )

- orderKey: The key or ID of an order (if applicable).
- new_username: A new username for the user (if applicable).
- name: The name of the token or coin (if applicable).
- label: The label of the wallet (if applicable).
#Below are the keys required for the configuration operations
- amountInSOLO: The amount in SOLO tokens (if applicable).
- autoSniping: A boolean value for enabling auto-sniping (if applicable).
- burnLP: A boolean value for burning LP tokens (if applicable).
- dexPaid: A boolean value for paying DEX fees (if applicable).
- jitoTip: A boolean value for tipping Jito (if applicable).
- launchTime: A timestamp for the launch time (if applicable).
- maxMarketCap: A maximum market cap value (if applicable).
- mevProtection: A boolean value for MEV protection (if applicable).
- minMarketCap: A minimum market cap value (if applicable).
- renounced: A boolean value for renouncing ownership (if applicable).
- slippage: A percentage value for slippage(if applicable).
- top10HP: A value for the top 10 holders percentage (if applicable).

Example Inputs and Outputs:

1. Input: "buy token with mint XYZ123 and wallet address ABC456"
   Output: {{"command": "buy token", "mint": "XYZ123", "address": "ABC456"}}

2. Input: "sell token with mint XYZ123 at 50% to wallet DEF789"
   Output: {{"command": "sell token", "mint": "XYZ123", "address": "DEF789","percentage": "50"}}

3. Input: "generate wallet S bank"
   Output: {{"command": "generate wallet", "label": "S bank"}}
   
4. Input: "get wallet by label S bank"
    Output: {{"command": "get wallet by label", "label": "S bank"}}
    
5. Input: "Raise my jitotip to 0.001 and set slippage to 15"
    Output: {{"command": "update config", "jitoTip": "0.001", "slippage": "15%"}}
    
6. Input: "how many wallets do i have?"
    Output: {{"command": "get all wallets"}}
    
7. Input: "can you generate a new wallet for me?"
    Output: {{"command": "generate wallet"}}
    
8. Input: "how much sol is in my default account?"
    Output: {{"command": "get wallet balance", "label": "default"}}
    
9. Input: "which tokens do i own?"
    Output: {{"command": "get wallet balance"}}
    
10. Input: "do i have the mango token?"
    Output: {{"command": "get wallet balance"}}
    
11. Input: "whats the name of this token : XYZ123"
    Output: {{"command": "get spl token", "mint": "XYZ123"}}
    
12. Input: "can you buy this token XYZ123 with a 0.0001 sol?"
    Output: {{"command": "buy token", "mint": "XYZ123", "amount": "0.0001"}}
    
13. Input: "what is my current slippage?"
    Output: {{"command": "get config"}}
    
14. Input: "what tokens have done moonshot migration recently?"
    Output: {{"command": "get tracked tokens", "reasons": ["moonshot_migrating"]}}
    
15. Input: "what new tokens are created recently?"
    Output: {{"command": "get tracked tokens",   "reasons": ["new_pool"]}}
    
16. Input: "fetch my wallet balance"
    Output: {{"command": "get wallet balance"}}
    
17. Input: "add a new wallet called elpis and use private key ABC123"
    Output: {{"command": "add wallet", "label": "elpis", "privateKey": "ABC123"}}
    
18. Input: "what is my username?"
    Output: {{"command": "get user data"}}
    
19. Input: "change my username to mitta"
    Output: {{"command": "change username", "username": "mitta"}}
    
20. Input: "start my autosniper"
    Output: {{"command": "update config", "autoSniping": true}}
    
21. Input: "set min market cap to one billion"
    Output: {{"command": "update config", "minMarketCap": "one billion"}}
    
22. Input: "what is the symbol of the mango token"
    Output: {{"command": "get spl token", "name": "mango"}}
    
23. Input: "how many orders have i made"
    Output: {{"command": "get past orders"}}
    
24. Input: "cancel order with key XYZ123"
    Output: {{"command": "cancel order", "orderKey": "XYZ123"}}
    
25. Input: "create a buy order for token XYZ123 at 0.0001 sol"
    Output: {{"command": "create buy order", "mint": "XYZ123", "price": "0.0001"}}
    
26. Input: "create a sell order for token XYZ123 at 0.0001 sol"
    Output: {{"command": "create sell order", "mint": "XYZ123", "price": "0.0001"}}
    
27. Input: "What new tokens have been released?"
    Output: {{"command": "get tracked tokens", "reasons": ["new_pool"]}}
    
28. Input: "What are the recent pumpfun tokens?"
    Output: {{"command": "get tracked tokens", "reasons":   "reasons": ["pumpfun_migrated"]}}
    
29. Input: "Which tokens are migrating to moonshot?"
    Output: {{"command": "get tracked tokens", "reasons": ["moonshot_migrating"]}}
    
30. Input: "Fetch my default wallet"
    Output: {{"command": "get default wallet"}}
    

Only provide the dictionary in the response. nothing more, nothing less. Don't even write anything or before the brackets.

Now process the following command: "{raw_command}"
"""
)

    try:
        # Generate the content from Gemini
        print(f"Raw response from Gemini: {parsed_command_response.text}")

        # Clean and parse the JSON
        parsed_command_text = parsed_command_response.text.strip("```").strip("json").strip("\n").strip("```").strip()

        try:
            parsed_command = json.loads(parsed_command_text)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Failed to parse the command: {parsed_command_text}"}), 400

        print(f"Parsed command: {parsed_command}")
        api_response = handle_user_command(parsed_command["command"], parsed_command)
        print(f"API response: {api_response}\n")
        if "Failed" in api_response:
            return jsonify({"error": "Invalid command"}), 400
        else:
            natural_response = model.generate_content(f"""
            You are provided with a user's command and data retrieved from an API response. Use these inputs to generate an accurate and user-friendly answer to the command. Interpret the raw command based on the API response structure and provide the best response.

            ### Instructions:
            1. Analyze the **Raw Command** to determine the user's intent.
            2. Use the **API Response** to extract the relevant information to answer the user's command.
            3. If the response requires computations (e.g., counting items, checking for conditions), perform the required operations.
            4. If the API response does not contain enough information, indicate what is missing and suggest potential next steps.

            ### Example Inputs and Outputs:

            #### Example 1
            **Raw Command**: "how much SOL is in my default account?"
            **API Response**:
            {{
              "message": "success",
              "data": {{
                "solBalance": 0.019002153,
                "splBalances": [
                  {{
                    "mint": "2kzd9ys6zx4xvpvkp4PnHKwPJgqk5tRZhRGoPPP8NrtzaTQZQRSB",
                    "balance": 1088.933627,
                    "name": "BOOK OF TIKTOK",
                    "symbol": "BOTT",
                    "image": "https://ipfs.io/ipfs/QmezVNtxQWibk4BBAojgqk5tRZhRGoPPP8NrtzaTQZQRSB",
                    "description": "A book of tiktok's most viral moments"
                  }}
                ]
              }}
            }}
            **Output**: "Your default account has a SOL balance of 0.019002153."

            ---

            #### Example 2
            **Raw Command**: "do I have the mango token?"
            **API Response**:
            {{
              "message": "success",
              "data": {{
                "solBalance": 0.019002153,
                "splBalances": [
                  {{
                    "mint": "2kzd9ys6zx4xvpvkp4PnHKwPJgqk5tRZhRGoPPP8NrtzaTQZQRSB",
                    "balance": 1088.933627,
                    "name": "BOOK OF TIKTOK",
                    "symbol": "BOTT",
                    "image": "https://ipfs.io/ipfs/QmezVNtxQWibk4BBAojgqk5tRZhRGoPPP8NrtzaTQZQRSB",
                    "description": "A book of tiktok's most viral moments"
                  }}
                ]
              }}
            }}
            **Output**: "No, you do not own the Mango token."

            ---

            #### Example 3
            **Raw Command**: "how many wallets do I have?"
            **API Response**:
            {{
              "message": "success",
              "data": [
                {{
                  "_id": "673f393f13fa3ce0779d2566",
                  "owner": "673f2fb687ead8b8d85ff8ed",
                  "label": "S Bank",
                  "address": "4mExDzmP9f6ioiifc41M33UyUmcGy8cjaqePaG3LFtxu",
                  "createdAt": "2024-11-21T13:44:31.757Z",
                  "updatedAt": "2024-11-21T13:53:04.279Z",
                  "__v": 0,
                  "isDefault": true
                }}
              ]
            }}
            **Output**: "You have 1 wallet."

            ---

            #### Example 4
            **Raw Command**: "What new tokens have been released?"
            **API Response**:
            {{
              "message": "success",
              "data": [
                {{
                  "_id": "673f39e662364c1aff52faf4",
                  "mint": "GqbsSrHKgtzrJMpRMtK2uRXuiXsGcQhN47oAexwaQgCq",
                  "reason": "new_pool",
                  "value": 0,
                  "createdAt": "2024-11-21T13:47:18.974Z",
                  "updatedAt": "2024-11-21T13:47:18.974Z",
                  "__v": 0
                }}
              ]
            }}
            **Output**: "The new token released is associated with the mint address GqbsSrHKgtzrJMpRMtK2uRXuiXsGcQhN47oAexwaQgCq."
            
            ---            

            ### Inputs:
            **Raw Command**: "{raw_command}"
            **API Response**: {api_response}

            ### Answer:
            """)
            return jsonify({"response": natural_response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(Debug=True)
