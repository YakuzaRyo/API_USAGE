from pathlib import Path
from cryptography.fernet import Fernet

from config import settings

_key: Fernet | None = None
KEY_FILE = Path("data/.fernet_key")


def _get_fernet() -> Fernet:
    global _key
    if _key is not None:
        return _key

    secret = settings.SECRET_KEY
    if secret:
        _key = Fernet(secret.encode())
        return _key

    if KEY_FILE.exists():
        _key = Fernet(KEY_FILE.read_bytes())
        return _key

    key_bytes = Fernet.generate_key()
    _key = Fernet(key_bytes)
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_bytes(key_bytes)
    return _key


def encrypt(value: str) -> str:
    return _get_fernet().encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    return _get_fernet().decrypt(value.encode()).decode()


def mask_key(value: str) -> str:
    if len(value) <= 4:
        return "****"
    return f"...{value[-4:]}"
