from fastapi import FastAPI
from api.endpoints import health
from core.logg import setup_logging
from core.config import config

app = FastAPI(docs_url="/docs")

setup_logging()

app.include_router(health.route)


if config.ENVIRONMENT == "dev" and __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=config.API_PORT)
