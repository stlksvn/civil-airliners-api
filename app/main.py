from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from prometheus_fastapi_instrumentator import Instrumentator

from app import db_models
from app.config import ENVIRONMENT, settings
from app.controller.avia_controller import router as avia_router
from app.database import Base, engine


def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Avia Metrics API", lifespan=lifespan)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(avia_router, prefix="/api/v1")


@app.get("/health", tags=["System Status"])
def health_check():
    """Аналог /actuator/health"""
    db_status = "up"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        db_status = "down"

    return {
        "status": "up" if db_status == "up" else "degraded",
        "components": {
            "db": {
                "status": db_status,
                "details": {
                    "database": "postgresql",
                    "host": settings.db_host,
                    "name": settings.db_name,
                },
            }
        },
    }


@app.get("/info", tags=["System Status"])
def info_check():
    """Аналог /actuator/info"""
    return {
        "app": {
            "name": "Avia Metrics API Service",
            "version": "0.1.0",
            "description": "CRUD Service for avialiners' telemetry",
        },
        "config": {
            "environment": ENVIRONMENT,
            "app_env": settings.app_env,
            "feature_flag": settings.feature_flag,
            "database": {
                "host": settings.db_host,
                "port": settings.db_port,
                "name": settings.db_name,
            },
        },
        "developer": {
            "name": "Nedoviziy_Pisarenko_Smirnov",
            "variant": 6,
            "group": "2387",
        },
    }
