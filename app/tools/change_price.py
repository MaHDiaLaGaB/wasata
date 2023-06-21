import os
import click
from typing import Tuple, Any
from app.core.config import config
from dotenv import load_dotenv, find_dotenv


@click.command()
@click.option(
    "--admin-key",
    prompt="Please Enter your Admin Secret Key",
    hide_input=True,
    help="Admin secret key to authorize the update.",
)
@click.option(
    "--usdt-value",
    prompt="Please enter the new USDT value",
    help="New USDT value to be set.",
)
def create_update_env_variable(
    admin_key: str, usdt_value: str
) -> Tuple[Any, Any] | None:
    """Update the USDT value in the .env file."""

    # Load the .env file
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    # Check if secret key matches
    if admin_key != os.getenv("SECRET_KEY"):
        raise ValueError("Invalid admin secret key")

    # Update the environment variable
    os.environ["PRICE"] = usdt_value

    # Write the variable to the .env file
    # with open(dotenv_path, "a") as f:
    #     f.write(f"PRICE={usdt_value}\n")

    return "PRICE", usdt_value


if __name__ == "__main__":
    key, value = create_update_env_variable()
    click.echo("==== the price has been changed successfully ====")
    click.echo(f"=========> {key}: {value} <=========")
