"""LMS API client for backend communication."""

import httpx
from config import get_lms_api_url, get_lms_api_key


class LMSClient:
    """Client for interacting with the LMS backend API."""
    
    def __init__(self):
        self.base_url = get_lms_api_url()
        self.api_key = get_lms_api_key()
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    def get_items(self) -> list[dict]:
        """Get all items (labs and tasks) from the backend.
        
        Returns:
            List of items (labs/tasks).
            
        Raises:
            httpx.RequestError: If the backend is unavailable.
            httpx.HTTPStatusError: If the backend returns an error.
        """
        with httpx.Client() as client:
            response = client.get(f"{self.base_url}/items/", headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    def get_pass_rates(self, lab_id: str) -> list[dict]:
        """Get pass rates for a specific lab.
        
        Args:
            lab_id: Lab identifier (e.g., 'lab-04').
            
        Returns:
            List of pass rate data per task.
            
        Raises:
            httpx.RequestError: If the backend is unavailable.
            httpx.HTTPStatusError: If the backend returns an error.
        """
        with httpx.Client() as client:
            response = client.get(
                f"{self.base_url}/analytics/pass-rates",
                headers=self.headers,
                params={"lab": lab_id}
            )
            response.raise_for_status()
            return response.json()
    
    def check_health(self) -> dict:
        """Check backend health by fetching items count.
        
        Returns:
            Dict with 'healthy' status and 'item_count'.
            
        Raises:
            httpx.RequestError: If the backend is unavailable.
            httpx.HTTPStatusError: If the backend returns an error.
        """
        items = self.get_items()
        return {"healthy": True, "item_count": len(items)}
