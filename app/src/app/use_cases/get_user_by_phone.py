"""Get user by phone number."""
from dataclasses import dataclass
from typing import Optional

from app.domain.entities import UserEntity
from app.repositories.user_repository import UserRepository


@dataclass
class GetUserByPhoneResult:
    user: Optional[UserEntity]


class GetUserByPhone:
    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    def execute(self, phone: str) -> GetUserByPhoneResult:
        user = self._repo.get_by_phone(phone)
        return GetUserByPhoneResult(user=user)
