# settings/__init__.py
from .base import *

ENVIRONMENT = os.environ.get('DJANGO_ENV', 'dev')

if ENVIRONMENT == 'development':
    from .dev import *
else:
    from .production import *