from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import AviaMetricsDB
from app.schemas.aviaModel import AviaMetricsCreate

MODEL_FIELDS = (
    "model",
    "airline",
    "altitude",
    "speed",
    "latitude",
    "longitude",
    "roll",
    "timestamp",
)


def get_metrics(db: Session) -> list[AviaMetricsDB]:
    statement = select(AviaMetricsDB).order_by(AviaMetricsDB.id)
    return list(db.scalars(statement).all())


def get_metric(db: Session, record_id: int) -> Optional[AviaMetricsDB]:
    return db.get(AviaMetricsDB, record_id)


def create_metric(db: Session, metric_data: AviaMetricsCreate) -> AviaMetricsDB:
    payload = metric_data.model_dump()
    record = AviaMetricsDB(
        **{field: payload[field] for field in MODEL_FIELDS},
        liner_status=payload["linerStatus"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_metric(
    db: Session, record_id: int, metric_data: AviaMetricsCreate
) -> Optional[AviaMetricsDB]:
    record = db.get(AviaMetricsDB, record_id)
    if record is None:
        return None

    payload = metric_data.model_dump()
    for field in MODEL_FIELDS:
        setattr(record, field, payload[field])
    record.liner_status = payload["linerStatus"]

    db.commit()
    db.refresh(record)
    return record


def delete_metric(db: Session, record_id: int) -> bool:
    record = db.get(AviaMetricsDB, record_id)
    if record is None:
        return False

    db.delete(record)
    db.commit()
    return True
