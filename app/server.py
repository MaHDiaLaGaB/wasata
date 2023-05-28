from fastapi import FastAPI, Depends
from app.api.endpoints import health, users, admin
from .core.logg import setup_logging
from .core.config import config
from app.db.database_engine import UserDB, get_user_db
from typing import AsyncGenerator


async def start_user_db_session(
    db: UserDB = Depends(get_user_db),
) -> AsyncGenerator[None, None]:
    with db.create_session():
        yield


app = FastAPI(docs_url="/docs", dependencies=[Depends(start_user_db_session)])

setup_logging()

app.include_router(health.route)
app.include_router(users.route)
app.include_router(admin.route)


if config.ENVIRONMENT == "dev" and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=config.API_PORT)
