"""LLM client for intent routing."""

import json
import httpx
from config import get_llm_api_key, get_llm_api_base_url, get_llm_model


class LLMClient:
    """Client for interacting with the LLM API."""
    
    def __init__(self):
        self.api_key = get_llm_api_key()
        self.base_url = get_llm_api_base_url()
        self.model = get_llm_model()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """Send a chat request to the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'.
            tools: Optional list of tool definitions.
            
        Returns:
            LLM response dict with 'choices' containing the message.
            
        Raises:
            httpx.RequestError: If the LLM is unavailable.
            httpx.HTTPStatusError: If the LLM returns an error.
        """
        payload = {
            "model": self.model,
            "messages": messages,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    
    def extract_tool_calls(self, response: dict) -> list[dict]:
        """Extract tool calls from LLM response.
        
        Args:
            response: LLM response dict.
            
        Returns:
            List of tool calls with 'name' and 'arguments'.
        """
        message = response.get("choices", [{}])[0].get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        result = []
        for call in tool_calls:
            func = call.get("function", {})
            try:
                arguments = json.loads(func.get("arguments", "{}"))
            except json.JSONDecodeError:
                arguments = {}
            
            result.append({
                "id": call.get("id"),
                "name": func.get("name"),
                "arguments": arguments
            })
        
        return result
    
    def get_response_text(self, response: dict) -> str:
        """Extract response text from LLM response.
        
        Args:
            response: LLM response dict.
            
        Returns:
            Response text content.
        """
        message = response.get("choices", [{}])[0].get("message", {})
        return message.get("content", "")
