"""Handler for /start command."""

from config import get_bot_token


def handle_start() -> str:
    """Handle the /start command.
    
    Returns:
        Welcome message for new users.
    """
    bot_token = get_bot_token()
    bot_name = "LMS Bot"
    
    # Extract bot name from token if available (format: <id>:<token>)
    if bot_token and ":" in bot_token:
        bot_id = bot_token.split(":")[0]
        bot_name = f"Bot #{bot_id}"
    
    return f"Welcome to {bot_name}! Use /help to see available commands."
