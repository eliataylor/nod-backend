# syntax=docker/dockerfile:1

# Stage 0: Set base image
FROM python:3.9.18-slim AS base

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev

# Stage 1: Build stage
FROM base AS build

# Install build dependencies
RUN apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM base AS runner

# Clean unnecessary files
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DJANGO_ENV=production \
    DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_EMAIL=admin@example.com \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Create and set the working directory
WORKDIR /app

# Copy the Python dependencies from the build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy the entrypoint script and application code to the working directory
COPY entrypoint.sh /entrypoint.sh
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]