"""Handler for /labs command."""

import httpx
from services.api_client import LMSClient


def handle_labs() -> str:
    """Handle the /labs command.
    
    Returns:
        List of available labs.
    """
    client = LMSClient()
    try:
        items = client.get_items()
        # Filter only labs (type == 'lab')
        labs = [item for item in items if item.get("type") == "lab"]
        
        if not labs:
            return "No labs available."
        
        result = "Available labs:"
        for lab in labs:
            result += f"\n- {lab.get('title', 'Unknown')} (ID: {lab.get('id', 'unknown')})"
        return result
    except httpx.ConnectError as e:
        return f"Backend error: connection refused ({client.base_url}). Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down."
    except httpx.RequestError as e:
        return f"Backend error: {str(e)}. Check that the services are running."
