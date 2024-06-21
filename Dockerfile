# syntax=docker/dockerfile:1

# Use the official Python image from the Docker Hub
FROM python:3.9.18-slim

# Define build-time arguments
ARG DJANGO_ENV
ARG DJANGO_SECRET_KEY
ARG GCP_SERVICE_NAME
ARG GCP_REGION
ARG GCP_SA_KEY
ARG GCP_PROJECT_ID
ARG SERVICE_NAME
ARG MYSQL_INSTANCE
ARG MYSQL_DATABASE
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG GCP_BUCKET_NAME

# Set environment variables
ENV DJANGO_ENV=$DJANGO_ENV
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV GCP_SERVICE_NAME=$GCP_SERVICE_NAME
ENV GCP_REGION=$GCP_REGION
ENV GCP_SA_KEY=$GCP_SA_KEY
ENV GCP_PROJECT_ID=$GCP_PROJECT_ID
ENV SERVICE_NAME=$SERVICE_NAME
ENV MYSQL_INSTANCE=$MYSQL_INSTANCE
ENV MYSQL_DATABASE=$MYSQL_DATABASE
ENV MYSQL_USER=$MYSQL_USER
ENV MYSQL_PASSWORD=$MYSQL_PASSWORD
ENV GCP_BUCKET_NAME=$GCP_BUCKET_NAME

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