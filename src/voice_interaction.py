from auth import logout
from configuration import config_voice_interaction
from trade import trade_voice_interaction
from user import user_voice_interaction
from wallet import wallet_voice_interaction


# commands
wallet_commands = ['generate', 'add', 'remove', 'balance', 'default', 'all', 'list']
trade_commands = ['buy', 'sell', 'order', 'create', 'cancel', 'live', 'past', 'token', 'tokens']
config_commands = ['set', 'get', 'update']
user_commands = ['data', 'username', 'change']


def handle_user_command(command):
    """Handle the user's command and take appropriate action."""
    if 'wallet' in command.lower() and any(cmd in command.lower() for cmd in wallet_commands):
        wallet_voice_interaction(command)
    elif 'trade' in command.lower() and any(cmd in command.lower() for cmd in trade_commands):
        trade_voice_interaction(command)
    elif 'configuration' in command.lower() and any(cmd in command.lower() for cmd in config_commands):
        config_voice_interaction(command)
    elif 'user' in command.lower() and any(cmd in command.lower() for cmd in user_commands):
        user_voice_interaction(command)
    elif 'logout' in command.lower() or 'exit' in command.lower():
        logout()
    else:
        print("Sorry, I didn't understand the command. Can you repeat it?")


def start():
    """Start the bot and handle voice interaction."""
    print("Welcome to Skye! How can I assist you today?")

    while True:
        command = input("Command : ")
        if command:
            if 'exit' in command.lower():
                print("Goodbye!")
                break
            handle_user_command(command)
        else:
            print("Sorry, I didn't catch that. Can you say it again?")
