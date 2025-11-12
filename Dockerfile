FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by some Python packages (psycopg2)
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
         build-essential \
         gcc \
         libpq-dev \
         netcat-openbsd \
         bash \
     && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Ensure scripts are executable
RUN chmod +x /app/scripts/*.sh

EXPOSE 8000

# Run the start script which will run migrations and start gunicorn
ENTRYPOINT ["/bin/sh", "/app/scripts/start.sh"]
