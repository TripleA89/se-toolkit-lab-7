"""Handler for natural language messages using LLM."""

from services.intent_router import IntentRouter


def handle_message(text: str) -> str:
    """Handle a natural language message using LLM routing.
    
    Args:
        text: User's message text.
        
    Returns:
        Response from the intent router.
    """
    router = IntentRouter()
    return router.route(text)
