- # NOD Backend

## Installation

1. **Clone the repository:**

    ```sh
    git clone  git@github.com:eliataylor/nod-backend.git nod_backend
    cd nod_backend
    python3.9 -m venv .venv
    source .venv/bin/activate  # On Windows use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate --run-syncdb
    python manage.py migrate --run-syncdb
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```
