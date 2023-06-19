from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .models import users_mapper_registry
from app.core.config import config

TDecorated = TypeVar("TDecorated", bound=Callable[..., Any])  # pylint: disable=C0103


class DB:
    def __init__(self, mapper_registry: Any, connection_string: str) -> None:
        self.engine = (
            create_engine(
                connection_string,
                connect_args={
                    "connect_timeout": config.DB_CONNECTION_TIMEOUT,
                    "options": "-c statement_timeout=10000",
                },
                future=True,
            )
            if config.ENVIRONMENT == "demo"
            else create_engine(connection_string)
        )
        self.mapper_registry = mapper_registry
        self._sessionmaker = sessionmaker(
            self.engine, autocommit=False, autoflush=False
        )
        self._current_session: Session = ContextVar("_current_session", default=None)  # type: ignore
        self.commit_on_flush: bool = False

    def create_tables(self) -> None:
        self.mapper_registry.metadata.create_all(bind=self.engine, checkfirst=True)

    def drop_tables(self) -> None:
        self.mapper_registry.metadata.drop_all(bind=self.engine, checkfirst=True)

    def reset(self) -> None:
        self.drop_tables()
        self.create_tables()

    @property
    def session(self) -> Session:
        assert (
            self._current_session.get()  # type: ignore
        ), f"Please run within database session context, for example use the @requires_db decorator {self}"
        return self._current_session.get()

    @contextmanager
    def create_session(self, commit_on_flush: bool = False) -> Any:
        """
        Create a session in a context manager block, can be configured to run with or without
        """
        assert (
            not self._current_session.get()  # type: ignore
        ), "Nested database sessions are not possible"
        try:
            self.commit_on_flush = commit_on_flush
            with self._sessionmaker() as session:
                self._current_session.set(session)  # type: ignore
                yield
                session.commit()
        except Exception as exc:
            raise exc
        finally:
            self._current_session.set(None)  # type: ignore
            self.commit_on_flush = False

    # decorate a whole endpoint if the session scope is this full endpoint
    def requires_db(self, commit_on_flush: bool = False) -> Any:
        """
        Decorator for API endpoints to start a database session
        """

        def decorator(func: TDecorated) -> TDecorated:
            @wraps(func)
            def decorated(*args: Any, **kwargs: Any) -> Any:
                with self.create_session(commit_on_flush=commit_on_flush):
                    return func(*args, **kwargs)

            return cast(TDecorated, decorated)

        return decorator

    def flush(self) -> None:
        """
        Flush changes to the database, if requested will commit instead of flushing (good for testing)
        """
        if self.commit_on_flush:
            self.commit()
        else:
            self.session.flush()

    def commit(self) -> None:
        self.session.commit()


class UserDB(DB):
    def __init__(self) -> None:
        super().__init__(
            mapper_registry=users_mapper_registry,
            connection_string=config.DATABASE_URI
            if config.ENVIRONMENT == "demo"
            else config.DATABASE_URI_DEV,
        )


# for now, we have a global user db for using inside our app bc dependencies don't work properly
user_db = UserDB()


def get_user_db() -> UserDB:
    return user_db
