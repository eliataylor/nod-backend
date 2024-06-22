import os
from .base import *

# Set the environment variable
ENVIRONMENT = os.getenv('DJANGO_ENV', 'production')

# Load the appropriate settings based on the environment
if ENVIRONMENT == 'production':
    from .production import *
else:
    from .dev import *

# Debugging logs for verifying the environment setting
print(f"DJANGO_ENV: {os.getenv('DJANGO_ENV', 'Not Set')}")
print(f"ENVIRONMENT: {ENVIRONMENT}")