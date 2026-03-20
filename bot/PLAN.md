# Bot Development Plan

## Overview

This document outlines the development plan for the Telegram bot that interacts with the Learning Management System (LMS) backend. The bot provides students with access to their lab assignments, scores, and answers to questions about the course.

## Architecture

The bot follows a layered architecture with clear separation of concerns:

1. **Entry Point** (`bot.py`) — Handles Telegram bot initialization and `--test` mode for offline testing
2. **Handlers** (`handlers/`) — Command logic as pure functions that take input and return text, independent of Telegram
3. **Services** (`services/`) — External API clients (LMS backend, LLM) that handle HTTP communication
4. **Configuration** (`config.py`) — Environment variable loading from `.env.bot.secret`

## Task 1: Project Scaffold

Create the project structure with testable handlers. The key deliverable is the `--test` mode that allows testing handlers without Telegram connection. Handlers return placeholder text initially.

## Task 2: Backend Integration

Implement real API calls to the LMS backend. Create an API client service that uses Bearer token authentication. Commands like `/health`, `/labs`, `/scores` will query the backend and return real data.

## Task 3: LLM Intent Routing

Add natural language understanding using an LLM. Instead of regex-based command parsing, the LLM analyzes user messages and decides which tool (handler) to call. Tool descriptions must be clear and descriptive.

## Task 4: Docker Deployment

Containerize the bot and deploy using Docker Compose. Configure proper networking so the bot container can reach the backend using service names (not `localhost`). Set up health checks and logging.

## Testing Strategy

- **Unit tests**: Test handlers in isolation with mocked services
- **Test mode**: `--test` flag for manual testing without Telegram
- **Integration tests**: Verify API client with real backend responses

## File Structure

```
bot/
├── bot.py              # Entry point with --test mode
├── config.py           # Environment configuration
├── pyproject.toml      # Dependencies
├── handlers/
│   ├── __init__.py
│   ├── start.py        # /start command
│   ├── help.py         # /help command
│   ├── health.py       # /health command
│   ├── labs.py         # /labs command
│   └── scores.py       # /scores command
└── services/
    ├── __init__.py
    ├── api_client.py   # LMS API client
    └── llm_client.py   # LLM client for Task 3
```
