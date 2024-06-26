import secrets
import base64
import click
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def generate_secret_key(admin_password: str) -> str:
    """Generate an admin key based on the provided password."""

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


@click.command()
@click.option(
    "--admin-password",
    prompt="Please enter your password to create Admin Key",
    help="Password to generate the admin key.",
)
def main(admin_password: str):
    """Command-line interface for generating an admin key."""
    admin_key = generate_secret_key(admin_password)
    click.echo("=========== Create Admin Key ===========")
    click.echo("============ Your Admin Key ============")
    click.secho(f"Your admin key ----> {admin_key} <----", fg="red", bold=True)
    click.echo("==== Keep your admin key safe please ===")


if __name__ == "__main__":
    main()
