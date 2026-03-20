"""Configuration loader from environment variables."""

import os
from dotenv import load_dotenv

# Load environment variables from .env.bot.secret
load_dotenv(".env.bot.secret")


def get_bot_token() -> str | None:
    """Get Telegram bot token."""
    return os.getenv("BOT_TOKEN")


def get_lms_api_url() -> str:
    """Get LMS API URL."""
    return os.getenv("LMS_API_URL", "http://localhost:42002")


def get_lms_api_key() -> str:
    """Get LMS API key."""
    return os.getenv("LMS_API_KEY", "")


def get_llm_api_key() -> str:
    """Get LLM API key."""
    return os.getenv("LLM_API_KEY", "")


def get_llm_api_base_url() -> str:
    """Get LLM API base URL."""
    return os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")


def get_llm_model() -> str:
    """Get LLM model name."""
    return os.getenv("LLM_API_MODEL", "coder-model")
