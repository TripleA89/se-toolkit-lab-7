"""Inline keyboard definitions for the bot."""


def get_quick_actions_keyboard():
    """Get inline keyboard with quick action buttons.
    
    Returns:
        List of lists containing button dicts.
    """
    return [
        [
            {"text": "📚 List Labs", "callback_data": "action_labs"},
            {"text": "📊 My Scores", "callback_data": "action_scores"},
        ],
        [
            {"text": "💚 Health Check", "callback_data": "action_health"},
            {"text": "❓ Help", "callback_data": "action_help"},
        ],
        [
            {"text": "🏆 Top Students Lab 04", "callback_data": "action_top_lab04"},
            {"text": "📈 Lab 04 Pass Rates", "callback_data": "action_rates_lab04"},
        ],
    ]


def format_keyboard_message(text: str, keyboard: list) -> str:
    """Format a message with keyboard hint.
    
    Args:
        text: Message text.
        keyboard: Keyboard layout.
        
    Returns:
        Formatted message with keyboard hint.
    """
    return f"{text}\n\n👇 Quick actions:"
