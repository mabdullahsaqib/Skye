from .auth import logout
from .user import user_voice_interaction
from .wallet import wallet_voice_interaction
from .trade import trade_voice_interaction
from .configuration import config_voice_interaction

# commands
wallet_commands = ['generate', 'add', 'remove', 'balance', 'default', 'all', 'list']
trade_commands = ['buy', 'sell', 'order', 'create', 'cancel', 'live', 'past', 'token', 'tokens']
config_commands = ['set', 'get', 'update']
user_commands = ['data', 'username', 'change']

def handle_user_command(command, data= None):
    """Handle the user's command and return the appropriate response."""
    if 'wallet' in command.lower() or any(cmd in command.lower() for cmd in wallet_commands):
        return wallet_voice_interaction(command, data)
    elif 'trade' in command.lower() or any(cmd in command.lower() for cmd in trade_commands):
        return trade_voice_interaction(command,data)
    elif 'configuration' in command.lower() or any(cmd in command.lower() for cmd in config_commands):
        return config_voice_interaction(command,data)
    elif 'user' in command.lower() or any(cmd in command.lower() for cmd in user_commands):
        return user_voice_interaction(command, data)
    elif 'logout' in command.lower() or 'exit' in command.lower():
        logout()
        return "User logged out."
    else:
        return "Failed"