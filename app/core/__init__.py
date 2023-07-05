import os
from typing import Type, List
from .base_configuration import BaseConfig


other_optional_envs = ["SENTRY_DSN"]


def generate_config(
    Config: Type[BaseConfig],
    optional_envs: List[str] = None,  # type: ignore
) -> Type[BaseConfig]:
    if optional_envs is None:
        optional_envs = []

    all_optional_envs = optional_envs + other_optional_envs

    for attr in [a for a in dir(Config) if not a.startswith("__")]:
        # set attr from environment
        if os.environ.get(attr):
            setattr(Config, attr, os.environ[attr])

        # assert all required attributes are set
        if attr not in all_optional_envs:
            value = getattr(Config, attr)
            assert (
                value is not None and value != ""
            ), f"Config Error: Attribute {attr} not set"
    return Config
