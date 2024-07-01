# syntax=docker/dockerfile:1

# Stage 2: Build dependencies
FROM python:3.9.18 AS builder

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime stage
FROM python:3.9.18-slim AS runner

# Prepare build dependencies
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmariadb3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_EMAIL=admin@example.com \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Create and set the working directory
WORKDIR /app

# Copy the entrypoint script and application code to the working directory
COPY entrypoint.sh /entrypoint.sh
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]