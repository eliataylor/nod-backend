from datetime import datetime, timedelta

from cryptography.fernet import Fernet

from nod_backend import settings


def encrypt(item):
    f = Fernet(settings.FERNET_KEY)
    return f.encrypt(item.encode())


def decrypt(encrypted_id):
    f = Fernet(settings.FERNET_KEY)
    return f.decrypt(encrypted_id).decode()
