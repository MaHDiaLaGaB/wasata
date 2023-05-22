from enum import IntEnum


class ExceptionCategory(IntEnum):
    # generic
    GENERIC = 1

    # blockchain related exceptions

    # Exceptions related to entities and business logic
    ENTITY = 200
    USER = 201

    # clients
    CLIENT = 300
