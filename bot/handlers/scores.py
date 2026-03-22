"""Handler for /scores command."""

import httpx
from services.api_client import LMSClient


def handle_scores(lab_id: str | None = None) -> str:
    """Handle the /scores command.
    
    Args:
        lab_id: Optional lab identifier to filter scores.
        
    Returns:
        Pass rates for the specified lab.
    """
    if not lab_id:
        return "Usage: /scores <lab-id>. Example: /scores lab-04"
    
    client = LMSClient()
    try:
        pass_rates = client.get_pass_rates(lab_id)
        
        if not pass_rates:
            return f"No pass rate data found for {lab_id}."
        
        result = f"Pass rates for {lab_id}:"
        for rate in pass_rates:
            task_name = rate.get("task_title", rate.get("task", "Unknown"))
            pass_rate = rate.get("pass_rate", 0) * 100  # Convert to percentage
            attempts = rate.get("attempts", 0)
            result += f"\n- {task_name}: {pass_rate:.1f}% ({attempts} attempts)"
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Lab '{lab_id}' not found. Use /labs to see available labs."
        return f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}."
    except httpx.ConnectError as e:
        return f"Backend error: connection refused ({client.base_url}). Check that the services are running."
    except httpx.RequestError as e:
        return f"Backend error: {str(e)}. Check that the services are running."
