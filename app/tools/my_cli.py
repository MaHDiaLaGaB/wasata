import secrets

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def generate_secret_key(admin_password: str) -> str:
    admin_password_bytes = admin_password.encode("utf-8")

    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(admin_password_bytes)).decode("utf-8")

    admin_secret_fernet_instance = Fernet(key).generate_key().hex()
    return admin_secret_fernet_instance


if __name__ == "__main__":
    print("=========== Create Admin Key ===========")
    admin_pass = input("Please enter your password to create Admin Key: ")
    the_key = generate_secret_key(admin_password=admin_pass)
    print("============ Your Admin Key ============")
    print(f"Your admin key ----> {the_key} <----")
    print("==== Keep your admin key safe please ===")
