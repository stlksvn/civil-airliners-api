from itertools import count
from typing import List, Optional
from schemas.aviaModel import AviaMetrics, AviaMetricsCreate


class AviaMetricsService:
    def __init__(self):
        self._db: dict[int, dict] = {
            1: {
                "id": 1,
                "model": "Airbus A320",
                "airline": "Aeroflot",
                "altitude": 10500.0,
                "speed": 840.5,
                "latitude": 55.7558,
                "longitude": 37.6173,
                "lainerStatus": "В полете",
                "roll": 0.0,
                "timestamp": "2026-10-26T15:00:00+00:00",
            }
        }
        self._id_counter = count(1)
        next(self._id_counter)

    def get_all(self) -> List[dict]:
        return list(self._db.values())

    def get_by_id(self, record_id: int) -> Optional[dict]:
        return self._db.get(record_id)

    def create(self, metric_data: AviaMetricsCreate) -> dict:
        new_id = next(self._id_counter)
        new_record = metric_data.model_dump()
        new_record["id"] = new_id

        self._db[new_id] = new_record
        return new_record

    def update(self, record_id: int, metric_data: AviaMetricsCreate) -> Optional[dict]:
        if record_id not in self._db:
            return None
        updated_record = metric_data.model_dump()
        updated_record["id"] = record_id
        self._db[record_id] = updated_record
        return self._db[record_id]

    def delete(self, record_id: int) -> bool:
        if record_id not in self._db:
            return False
        del self._db[record_id]
        return True
