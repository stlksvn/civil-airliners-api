from typing import List, Optional

from sqlalchemy.orm import Session

from app import crud
from app.db_models import AviaMetricsDB
from app.schemas.aviaModel import AviaMetricsCreate


class AviaMetricsService:
    @staticmethod
    def _to_dict(record: AviaMetricsDB) -> dict:
        return {
            "id": record.id,
            "model": record.model,
            "airline": record.airline,
            "altitude": record.altitude,
            "speed": record.speed,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "linerStatus": record.liner_status,
            "roll": record.roll,
            "timestamp": record.timestamp,
        }

    def get_all(self, db: Session) -> List[dict]:
        return [self._to_dict(record) for record in crud.get_metrics(db)]

    def get_by_id(self, db: Session, record_id: int) -> Optional[dict]:
        record = crud.get_metric(db, record_id)
        return self._to_dict(record) if record else None

    def create(self, db: Session, metric_data: AviaMetricsCreate) -> dict:
        return self._to_dict(crud.create_metric(db, metric_data))

    def update(
        self, db: Session, record_id: int, metric_data: AviaMetricsCreate
    ) -> Optional[dict]:
        record = crud.update_metric(db, record_id, metric_data)
        return self._to_dict(record) if record else None

    def delete(self, db: Session, record_id: int) -> bool:
        return crud.delete_metric(db, record_id)
