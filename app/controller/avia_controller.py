from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.aviaModel import AviaMetricsCreate, AviaMetrics
from app.service.avia_service import AviaMetricsService
from app.locales import get_locale

avia_service = AviaMetricsService()
router = APIRouter(prefix="/metrics", tags=["Avia Metrics"])


def generate_hateoas_links(request: Request, record_id: int, locale: dict) -> dict:
    """Вспомогательная функция генерации и локализации ссылок HATEOAS"""
    return {
        locale["link_self"]: str(request.url_for("get_metric", record_id=record_id)),
        locale["link_create"]: str(request.url_for("create_metric")),
        locale["link_update"]: str(
            request.url_for("update_metric", record_id=record_id)
        ),
        locale["link_delete"]: str(
            request.url_for("delete_metric", record_id=record_id)
        ),
    }


@router.get(
    "",
    response_model=List[AviaMetrics],
    summary="Получить все данные лайнера",
    name="get_all_metrics",
)
def get_all_metrics(
    request: Request,
    db: Session = Depends(get_db),
    locale: dict = Depends(get_locale),
):
    records = avia_service.get_all(db)
    for item in records:
        item["links"] = generate_hateoas_links(request, item["id"], locale)
    return records


@router.get(
    "/{record_id}",
    response_model=AviaMetrics,
    summary="Получить данные лайнера по ID",
    name="get_metric",
)
def get_metric(
    record_id: int,
    request: Request,
    db: Session = Depends(get_db),
    locale: dict = Depends(get_locale),
):
    result = avia_service.get_by_id(db, record_id)
    if not result:
        raise HTTPException(status_code=404, detail=locale["not_found"])
    result["links"] = generate_hateoas_links(request, record_id, locale)
    return result


@router.post(
    "",
    response_model=AviaMetrics,
    status_code=201,
    summary="Создать запись о лайнере",
    name="create_metric",
)
def create_metric(
    metric: AviaMetricsCreate,
    request: Request,
    db: Session = Depends(get_db),
    locale: dict = Depends(get_locale),
):
    result = avia_service.create(db, metric)
    result["links"] = generate_hateoas_links(request, result["id"], locale)
    return result


@router.put(
    "/{record_id}",
    response_model=AviaMetrics,
    summary="Обновить данные лайнера",
    name="update_metric",
)
def update_metric(
    record_id: int,
    updated_metric: AviaMetricsCreate,
    request: Request,
    db: Session = Depends(get_db),
    locale: dict = Depends(get_locale),
):
    result = avia_service.update(db, record_id, updated_metric)
    if not result:
        raise HTTPException(status_code=404, detail=locale["not_found"])
    result["links"] = generate_hateoas_links(request, record_id, locale)
    return result


@router.delete("/{record_id}", summary="Удалить запись о лайнере", name="delete_metric")
def delete_metric(
    record_id: int,
    db: Session = Depends(get_db),
    locale: dict = Depends(get_locale),
):
    success = avia_service.delete(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail=locale["not_found"])
    return {"message": locale["deleted"].format(record_id=record_id)}
