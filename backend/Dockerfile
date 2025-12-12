# Use an official lightweight Python image.
# 3.10-slim is a common standard (small, secure, stable).
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files (useless in containers)
ENV PYTHONDONTWRITEBYTECODE=1
# Force stdout/stderr to be unbuffered (logs show up immediately)
# If this is not set, Python might buffer logs and we won't see crash errors in Docker.
ENV PYTHONUNBUFFERED=1
# Install system dependencies (needed for some python packages like psycopg2)
# We clean up the apt cache afterwards to keep the image small.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first!
# Docker caches layers. If requirements don't change, it skips pip install.
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command to run the API
# host 0.0.0.0 is required for Docker containers to be accessible from outside
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
