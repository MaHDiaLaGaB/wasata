# pylint: disable=W0602
from typing import Dict, Type

from .const import ExceptionCategory
from .exception import WasataException

KNOWN_EXCEPTIONS: Dict[str, Type[WasataException]] = {}


def register_exception(
    exception_type: Type[WasataException],
) -> Type[WasataException]:
    key = exception_type.error_code()
    global KNOWN_EXCEPTIONS
    if key in KNOWN_EXCEPTIONS:
        raise Exception(
            f"Duplicate Exception with code {key} registered. {KNOWN_EXCEPTIONS[key]} and {exception_type}"
        )
    if exception_type.category_code not in [item.value for item in ExceptionCategory]:
        raise Exception(f"Unknown Category {exception_type.category_code}")
    KNOWN_EXCEPTIONS[key] = exception_type
    return exception_type
