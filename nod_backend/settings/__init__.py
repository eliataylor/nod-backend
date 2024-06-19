# settings/__init__.py
import os
from .base import *

ENVIRONMENT = os.environ.get('DJANGO_ENV', 'dev')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .dev import *