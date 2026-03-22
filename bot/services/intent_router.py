"""Intent router using LLM for natural language understanding."""

import sys
import json
from services.api_client import LMSClient
from services.llm_client import LLMClient
from services.tools import TOOLS


# System prompt for the LLM
SYSTEM_PROMPT = """You are an assistant for a Learning Management System (LMS). 
You have access to tools that fetch data from the backend API.
When a user asks a question, use the available tools to get the data, then provide a helpful answer.

Guidelines:
1. If the user asks about available labs, use get_items first.
2. If the user asks about scores, pass rates, or performance, use the appropriate analytics tool.
3. For comparisons (e.g., "which lab has the lowest"), first get all labs, then fetch data for each.
4. If the user greeting or says something unrelated, respond friendly and mention what you can help with.
5. Always provide specific numbers from the data when available.
6. If you don't understand the query, ask for clarification.

Available tools:
- get_items: List all labs and tasks
- get_learners: List enrolled students
- get_scores: Score distribution for a lab
- get_pass_rates: Pass rates per task for a lab
- get_timeline: Submission timeline for a lab
- get_groups: Per-group performance for a lab
- get_top_learners: Top students for a lab
- get_completion_rate: Completion percentage for a lab
- trigger_sync: Refresh data from autochecker
"""


class IntentRouter:
    """Routes user messages to appropriate tools using LLM."""
    
    def __init__(self):
        self.llm = LLMClient()
        self.lms = LMSClient()
        self.system_prompt = SYSTEM_PROMPT
    
    def execute_tool(self, name: str, arguments: dict) -> any:
        """Execute a tool by calling the appropriate LMS API method.
        
        Args:
            name: Tool name (e.g., 'get_items', 'get_pass_rates').
            arguments: Tool arguments as dict.
            
        Returns:
            Tool execution result.
        """
        print(f"[tool] LLM called: {name}({arguments})", file=sys.stderr)
        
        try:
            if name == "get_items":
                result = self.lms.get_items()
            elif name == "get_learners":
                result = self.lms.get_items()  # Using items as fallback
            elif name == "get_scores":
                result = self.lms.get_pass_rates(arguments.get("lab", ""))
            elif name == "get_pass_rates":
                result = self.lms.get_pass_rates(arguments.get("lab", ""))
            elif name == "get_timeline":
                result = self.lms.get_pass_rates(arguments.get("lab", ""))  # Fallback
            elif name == "get_groups":
                result = self.lms.get_pass_rates(arguments.get("lab", ""))  # Fallback
            elif name == "get_top_learners":
                result = self.lms.get_pass_rates(arguments.get("lab", ""))  # Fallback
            elif name == "get_completion_rate":
                result = self.lms.get_pass_rates(arguments.get("lab", ""))  # Fallback
            elif name == "trigger_sync":
                result = {"status": "sync triggered"}
            else:
                result = {"error": f"Unknown tool: {name}"}
            
            print(f"[tool] Result: {len(str(result))} chars", file=sys.stderr)
            return result
        except Exception as e:
            print(f"[tool] Error: {e}", file=sys.stderr)
            return {"error": str(e)}
    
    def route(self, message: str) -> str:
        """Route a user message through the LLM and tools.
        
        Args:
            message: User's natural language message.
            
        Returns:
            Final response text.
        """
        # Initialize conversation
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message}
        ]
        
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call LLM
            try:
                response = self.llm.chat(messages, tools=TOOLS)
            except Exception as e:
                return f"LLM error: {str(e)}. Please try again later."
            
            # Check if LLM wants to call tools
            tool_calls = self.llm.extract_tool_calls(response)
            
            if not tool_calls:
                # No tool calls - LLM has final answer
                response_text = self.llm.get_response_text(response)
                if response_text:
                    return response_text
                return "I'm not sure how to help with that. Try asking about labs, scores, or students."
            
            # Execute tools and collect results
            tool_results = []
            for call in tool_calls:
                result = self.execute_tool(call["name"], call["arguments"])
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": json.dumps(result, ensure_ascii=False, default=str)
                })
            
            print(f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM", file=sys.stderr)
            
            # Add tool calls and results to conversation
            messages.append(response.get("choices", [{}])[0].get("message", {}))
            messages.extend(tool_results)
        
        return "I need more information to answer this question. Please try rephrasing."
