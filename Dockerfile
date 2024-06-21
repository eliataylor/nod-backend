# syntax=docker/dockerfile:1

# Use the official Python image from the Docker Hub
FROM python:3.9.18-slim

# Define build-time arguments
# ARG DJANGO_ENV
# ARG DJANGO_SECRET_KEY
# ARG GCP_REGION
# ARG GCP_SA_KEY
# ARG GCP_PROJECT_ID
# ARG GCP_BUCKET_NAME

# Set environment variables
# ENV DJANGO_ENV=production
# ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
# ENV GCP_REGION=$GCP_REGION
# ENV GCP_SA_KEY=test
# ENV GCP_PROJECT_ID=$GCP_PROJECT_ID
# ENV GCP_BUCKET_NAME=test

# Set environment variable
ENV DJANGO_ENV=production

# Set environment variables for superuser creation
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the application code to the working directory
COPY . .

# Run database migrations and collect static files
# RUN python manage.py migrate \
#     && python manage.py collectstatic --noinput
# RUN python manage.py makemigrations \
#     python manage.py migrate && \
#     python manage.py migrate --run-syncdb

# Expose the port the app runs on
ENV PORT=8080
EXPOSE 8000

# Command to run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "8", "nod_backend.wsgi:application"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]