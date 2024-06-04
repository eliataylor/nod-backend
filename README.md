- # NOD Backend

This project is a simple Django 5 application that exposes all CRUD (Create, Read, Update, Delete) endpoints for its default admin and an API via Django Rest Framework (DRF). The aim is to provide a basic setup that can be extended for more complex applications.

## Features

- Full CRUD operations for Django admin
- RESTful API endpoints for all models using Django Rest Framework
- Simple and extendable codebase

## Requirements

- Python 3.8+
- Django 5.0
- Django Rest Framework

## Installation

1. **Clone the repository:**

    ```sh
    git clone  git@github.com:eliataylor/nod-backend.git nod_backend
    cd nod_backend
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## API Endpoints

The API provides CRUD endpoints for each model. Below are the general patterns for the endpoints:

- List and Create: `/api/<model-name>/`
- Retrieve, Update, and Delete: `/api/<model-name>/<id>/`

### Example

Assuming you have a model called `Book`, the endpoints would be:

- List and Create: `/api/books/`
- Retrieve, Update, and Delete: `/api/books/<id>/`

### URL Patterns

```text
GET    /api/<model-name>/          - List all items
POST   /api/<model-name>/          - Create a new item
GET    /api/<model-name>/<id>/     - Retrieve a specific item
PUT    /api/<model-name>/<id>/     - Update a specific item
PATCH  /api/<model-name>/<id>/     - Partially update a specific item
DELETE /api/<model-name>/<id>/     - Delete a specific item
