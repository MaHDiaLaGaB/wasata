import os
from typing import Tuple, Any
from app.core.config import config

from dotenv import load_dotenv, find_dotenv


def create_update_env_variable(k: str, v: str, secret_key: str) -> Tuple[Any, Any] | None:
    # Load the .env file
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    # Check if secret key matches
    if secret_key != os.getenv("SECRET_KEY"):
        raise ValueError()

    # Update the environment variable
    os.environ[k] = v

    # Write the variable to the .env file
    with open(dotenv_path, "a") as f:
        f.write(f"{k}={v}\n")

    return k, v


if __name__ == "__main__":
    admin_key = input("Please Enter your Admin Secret Key:")
    print("================================================")
    print("you are going to change the price of the -> USDT <-")
    usdt_value = input("Please enter the new USDT value: ")
    if create_update_env_variable(config.COIN, usdt_value, admin_key) is not None:
        key, value = create_update_env_variable(config.COIN, usdt_value, admin_key)
        print("==== the price has been changed successfully ====")
        print(f"=========> {key}: {value} <=========")
    else:
        print("+++++++++++++ Error ++++++++++++")
