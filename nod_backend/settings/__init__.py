import os

# Determine environment
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

# Load appropriate settings
if DJANGO_ENV == 'production':
    print(f"DJANGO_ENV: production is SET")
    from .production import *
elif DJANGO_ENV == 'development':
    print(f"DJANGO_ENV: development is SET")
    from .development import *
else:
    raise ImportError("Invalid DJANGO_ENV setting")