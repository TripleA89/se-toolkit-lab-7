"""Handler for /health command."""

import httpx
from services.api_client import LMSClient


def handle_health() -> str:
    """Handle the /health command.
    
    Returns:
        Backend health status.
    """
    client = LMSClient()
    try:
        result = client.check_health()
        return f"Backend is healthy. {result['item_count']} items available."
    except httpx.ConnectError as e:
        return f"Backend error: connection refused ({client.base_url}). Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down."
    except httpx.RequestError as e:
        return f"Backend error: {str(e)}. Check that the services are running."
