# syntax=docker/dockerfile:1

# Use the official Python image from the Docker Hub
FROM python:3.9.18-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /app/

# Run database migrations and collect static files
RUN python manage.py migrate \
    && python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["gunicorn", "nod_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]