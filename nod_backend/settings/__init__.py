# settings/__init__.py
import os
from .base import *

ENVIRONMENT = os.getenv('DJANGO_ENV', 'production')

if ENVIRONMENT == 'development':
    from .dev import *
else:
    from .production import *

print("DJANGO_ENV:", os.getenv('DJANGO_ENV', 'Not Set'))
print("ENVIRONMENT:", ENVIRONMENT)