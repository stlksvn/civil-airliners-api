from fastapi import FastAPI
from controller.avia_controller import router as avia_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Avia Metrics API")

# 1. Экспорт метрик Prometheus через инструмент (будет доступен /metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(avia_router, prefix="/api/v1")


# 3. Эндпоинты проверки состояния (Health Info)
@app.get("/health", tags=["System Status"])
def health_check():
    """Аналог /actuator/health"""
    return {
        "status": "up",
        "components": {
            "db": {
                "status": "up",
                "details": {
                    "database": "json for now, will be postgres later :)",
                    "free_space": "unlimited",
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
        "developer": {
            "name": "Nedoviziy_Pisarenko_Smirnov",
            "variant": 6,
            "group": "2387",
        },
    }
