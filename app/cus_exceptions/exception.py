from http import HTTPStatus
from typing import Any, Dict, Optional

from .const import ExceptionCategory


class WasataException(Exception):
    category_code: int = ExceptionCategory.GENERIC
    exception_code: int = 1
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    description: Optional[str] = "Internal Server Error"
    payload: Optional[Dict[str, Any]] = None

    def __init__(
        self, description: Optional[str] = None, payload: Dict[str, Any] | None = None
    ) -> None:
        super().__init__()
        self.description = description or self.description
        self.payload = payload

    @classmethod
    def error_code(cls) -> str:
        return f"E{cls.category_code:03}{cls.exception_code:03}"
