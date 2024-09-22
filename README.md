# NOD Backend

## Installation

1. **Clone the repository:**

    ```sh
    git clone  git@github.com:eliataylor/nod_backend.git
    cd nod_backend
    python3.12 -m venv .venv
    source .venv/bin/activate  # On Windows use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    python manage.py migrate --run-syncdb
    python manage.py makemigrations
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver 8000
    ```


------

# To Connect to remote SQL:
- `./cloud-sql-proxy trackauthoritymusic:us-west1:sql-v8/nod_django_01 --credentials-file ./keys/nod-django-app.json`
