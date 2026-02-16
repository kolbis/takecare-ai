"""Get schedule for user and date."""
from dataclasses import dataclass
from datetime import date
from typing import List

from app.domain.entities import Medication
from app.repositories.schedule_repository import ScheduleRepository


@dataclass
class GetScheduleForUserResult:
    medications: List[Medication]


class GetScheduleForUser:
    def __init__(self, schedule_repository: ScheduleRepository):
        self._repo = schedule_repository

    def execute(self, user_id: str, for_date: date) -> GetScheduleForUserResult:
        medications = self._repo.get_schedule(user_id, for_date)
        return GetScheduleForUserResult(medications=medications)
