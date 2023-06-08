from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from app.api.endpoints import health, users, admin
from app.core.logg import setup_logging
from app.core.config import config
from app.db.database_engine import UserDB, get_user_db
from typing import AsyncGenerator
from app.exceptions.exception import WasataException
from app.exceptions.handler import handle_exception


async def start_user_db_session(
        db: UserDB = Depends(get_user_db),
) -> AsyncGenerator[None, None]:
    with db.create_session():
        yield


app = FastAPI(docs_url="/docs", dependencies=[Depends(start_user_db_session)])

setup_logging()


@app.exception_handler(WasataException)
def exception_handler_middleware(
        _request: Request, exception: WasataException
) -> JSONResponse:
    return handle_exception(config, exception)


@app.get("/", response_class=RedirectResponse)
async def redirect_fastapi() -> str:
    return "/docs"


app.include_router(health.route)
app.include_router(users.route)
app.include_router(admin.route)

if config.ENVIRONMENT == "dev" and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=config.API_PORT)
