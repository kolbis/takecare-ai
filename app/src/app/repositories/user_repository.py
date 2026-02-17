"""User repository interface and mock."""
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_phone(self, phone: str) -> Optional[User]:
        ...


class MockUserRepository(UserRepository):
    """Mock: returns a fixed user for any phone."""

    def __init__(self):
        self._user = User(
            id="u1",
            phone="+1234567890",
            language="en",
            timezone="UTC",
            caregiver_ids=["c1"],
            first_name="Test",
            last_name="User",
            age=None,
            name="Test User",
        )

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._user if user_id == self._user.id else self._user

    def get_by_phone(self, phone: str) -> Optional[User]:
        return self._user
