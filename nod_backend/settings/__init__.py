import os

# Determine environment
DJANGO_ENV = os.getenv('DJANGO_ENV', 'dev')

from .production import *

# Load appropriate settings
# if DJANGO_ENV == 'dev':
#     print(f"DJANGO_ENV: {os.getenv('DJANGO_ENV')} is SET")
#     from .dev import *
# elif DJANGO_ENV == 'production':
#     print(f"DJANGO_ENV: {os.getenv('DJANGO_ENV')} is SET")
#     from .production import *
# else:
#     raise ImportError("Invalid DJANGO_ENV setting")