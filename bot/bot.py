"""Telegram bot entry point with --test mode support."""

import argparse
import sys
from handlers.start import handle_start
from handlers.help import handle_help
from handlers.health import handle_health
from handlers.labs import handle_labs
from handlers.scores import handle_scores


def get_handler(command: str):
    """Get handler function for a command.
    
    Args:
        command: Command name without slash (e.g., 'start' for '/start').
        
    Returns:
        Handler function or None if command not found.
    """
    handlers = {
        'start': handle_start,
        'help': handle_help,
        'health': handle_health,
        'labs': handle_labs,
        'scores': handle_scores,
    }
    return handlers.get(command)


def run_test_mode(command: str) -> None:
    """Run a command in test mode and print result to stdout.
    
    Args:
        command: Full command string (e.g., '/start' or '/scores lab-04').
    """
    # Split command and arguments
    parts = command.strip().split()
    cmd_name = parts[0].lstrip('/')
    args = parts[1:] if len(parts) > 1 else []
    
    handler = get_handler(cmd_name)
    if handler is None:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)
    
    # Call handler with arguments if it accepts them
    if args and cmd_name == 'scores':
        result = handler(args[0])
    else:
        result = handler()
    
    print(result)
    sys.exit(0)


def run_telegram_mode() -> None:
    """Run the bot in Telegram mode (requires BOT_TOKEN)."""
    print("Telegram mode not implemented yet — use --test mode for now.")
    sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description='LMS Telegram Bot')
    parser.add_argument(
        '--test',
        type=str,
        metavar='COMMAND',
        help='Run in test mode with the given command (e.g., "/start")'
    )
    
    args = parser.parse_args()
    
    if args.test:
        run_test_mode(args.test)
    else:
        run_telegram_mode()


if __name__ == '__main__':
    main()
