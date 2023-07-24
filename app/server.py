import secrets
from typing import AsyncGenerator, Dict, Any

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from app.api.endpoints import health, users, admin, routes, submit_form
from app.core.logg import setup_logging
from app.core.config import config
from app.db.database_engine import UserDB, get_user_db
from app.exceptions.exception import WasataException
from app.exceptions.handler import handle_exception
from app.exceptions import Unauthorized, Forbidden


async def start_user_db_session(
    db: UserDB = Depends(get_user_db),
) -> AsyncGenerator[None, None]:
    with db.create_session():
        yield


app = FastAPI(
    title="FastApi",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    dependencies=[Depends(start_user_db_session)],
)
security = HTTPBasic()

setup_logging()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(
        credentials.username, config.ADMIN_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, config.ADMIN_PASSWORD
    )
    if not (correct_username and correct_password):
        raise Unauthorized()
    return credentials.username


# Define CORS settings
origins = [
    "http://localhost",
    "http://localhost:3030",
]

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(WasataException)
def exception_handler_middleware(
    _request: Request, exception: WasataException
) -> JSONResponse:
    return handle_exception(config, exception)


app.include_router(health.route)
app.include_router(users.route)
app.include_router(admin.route)
app.include_router(submit_form.route)


@app.get(routes.DOCS, include_in_schema=False)
async def get_swagger_documentation(
    username: str = Depends(get_current_username),
) -> HTMLResponse:
    if not username:
        raise Forbidden()
    return get_swagger_ui_html(openapi_url=routes.OPENAPI, title="docs")


@app.get(routes.REDOC, include_in_schema=False)
async def get_redoc_documentation(
    username: str = Depends(get_current_username),
) -> HTMLResponse:
    if not username:
        raise Forbidden()
    return get_redoc_html(openapi_url=routes.OPENAPI, title="docs")


@app.get(routes.OPENAPI, include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)) -> Dict[str, Any]:
    if not username:
        raise Forbidden()
    return get_openapi(title=config.NAME, version=config.VERSION, routes=app.routes)


if config.ENV == "dev" and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=config.WASATA_PORT)
