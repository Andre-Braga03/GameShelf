from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import Base, engine
from app.models import User  # noqa: F401
from app.routers import auth


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        pass
    yield


app = FastAPI(title="GameShelf", lifespan=lifespan)
app.include_router(auth.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db", response_model=None)
def health_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except OperationalError:
        return JSONResponse(
            {"status": "error", "database": "disconnected"},
            status_code=503,
        )
    return {"status": "ok", "database": "connected"}
