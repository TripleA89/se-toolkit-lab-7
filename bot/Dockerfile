FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy all files from bot directory (context is ./bot)
COPY . .

# Install dependencies
RUN uv sync --frozen

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["uv", "run", "python", "bot.py"]
