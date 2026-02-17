from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.domain.entities import UserEntity
from app.domain.value_objects import (
    CaregiverId,
    DateOfBirth,
    FirstName,
    Language,
    LastName,
    Phone,
    Timezone,
    UserId,
)
from .mock import MOCK_USER_ID, MOCK_CAREGIVER_ID


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[UserEntity]: ...

    @abstractmethod
    def get_by_phone(self, phone: str) -> Optional[UserEntity]: ...


class MockUserRepository(UserRepository):
    """Mock: returns a fixed user for any phone."""

    def __init__(self):
        self._user = UserEntity(
            id=UserId.from_str(MOCK_USER_ID),
            phone=Phone("+1234567890"),
            language=Language("en"),
            timezone=Timezone("UTC"),
            first_name=FirstName("Test"),
            last_name=LastName("User"),
            date_of_birth=DateOfBirth(date(1950, 1, 1)),
            caregiver_ids=[CaregiverId.from_str(MOCK_CAREGIVER_ID)],
            medications=[],
        )

    def get_by_id(self, user_id: str) -> Optional[UserEntity]:
        if str(self._user.id) == user_id:
            return self._user
        return self._user  # mock: same user for any id

    def get_by_phone(self, phone: str) -> Optional[UserEntity]:
        if str(self._user.phone) == phone:
            return self._user
        return self._user  # mock: same user for any phone
