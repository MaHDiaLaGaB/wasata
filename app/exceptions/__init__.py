from http import HTTPStatus
from typing import Union, Optional
from uuid import UUID
from .const import ExceptionCategory
from .exception import WasataException
from .registry import register_exception

register_exception(WasataException)


#
# Define a bunch of basic exceptions we always need
#
@register_exception
class GenericHTTPException(WasataException):
    category_code: int = ExceptionCategory.ENTITY
    exception_code: int = 100
    status_code: int = HTTPStatus.NOT_FOUND
    description: Optional[str] = "Http Exception"

    def __init__(self, status_code: int = HTTPStatus.NOT_FOUND) -> None:
        super().__init__()
        self.status_code = status_code


@register_exception
class NotFound(WasataException):
    category_code: int = ExceptionCategory.GENERIC
    exception_code: int = 2
    status_code: int = HTTPStatus.NOT_FOUND
    description: Optional[str] = "Requested object not found"

    def __init__(self, object_id: str = None) -> None:
        super().__init__()
        if object_id:
            self.description: Optional[str] = f"Object with id {object_id} not found"


@register_exception
class ObjectNotFound(WasataException):
    category_code: int = ExceptionCategory.ENTITY
    exception_code: int = 1
    status_code: int = HTTPStatus.NOT_FOUND
    description: Optional[str] = "Requested object not found"

    def __init__(self, object_id: Union[str, UUID] = None) -> None:
        super().__init__()
        if object_id:
            self.description: Optional[
                str
            ] = f"Requested object with id '{object_id}' not found"


@register_exception
class Forbidden(WasataException):
    exception_code: int = 3
    status_code: int = HTTPStatus.FORBIDDEN
    description: Optional[str] = "Access Forbidden"


@register_exception
class Unauthorized(WasataException):
    exception_code: int = 4
    status_code: int = HTTPStatus.UNAUTHORIZED
    description: Optional[str] = "Unauthorized"


@register_exception
class Conflict(WasataException):
    exception_code: int = 5
    status_code: int = HTTPStatus.CONFLICT
    description: Optional[str] = "Conflict"


@register_exception
class ServiceUnavailable(WasataException):
    exception_code: int = 6
    status_code: int = HTTPStatus.SERVICE_UNAVAILABLE
    description: Optional[str] = "Service Unavailable"


@register_exception
class BadRequest(WasataException):
    exception_code: int = 7
    status_code: int = HTTPStatus.BAD_REQUEST
    description: Optional[str] = "Bad Request"


@register_exception
class CouldNotParseFile(WasataException):
    exception_code: int = 8
    status_code: int = HTTPStatus.BAD_REQUEST
    description: Optional[str] = "Could not parse file"


@register_exception
class CouldNotParseEntry(WasataException):
    exception_code: int = 9
    status_code: int = HTTPStatus.BAD_REQUEST
    description: Optional[str] = "Could not parse Entry"
