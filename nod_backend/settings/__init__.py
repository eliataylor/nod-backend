import os
from dotenv import load_dotenv


# Determine environment
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Load appropriate settings
if DJANGO_ENV == 'production' or DJANGO_ENV == 'deploy':
    print(f"DJANGO_ENV: production is SET")

    if os.path.exists(ROOT_DIR + '/.env.prod'):
        load_dotenv(dotenv_path=ROOT_DIR + '/.env.prod', override=True)
        print(f"loading prod variables")
    if os.path.exists(ROOT_DIR + '/.env.gcp'):
        load_dotenv(dotenv_path=ROOT_DIR + '/.env.gcp', override=True)
        print(f"loading gcp variables")

    from .production import *
else:
    if os.path.exists(ROOT_DIR + '/.env.dev'):
        load_dotenv(dotenv_path=ROOT_DIR + '/.env.dev', override=True)
    print(f"DJANGO_ENV: development default is SET")
    from .development import *