from datetime import date
from dataclasses import dataclass
from .age import Age

@dataclass(frozen=True, slots=True)
class DateOfBirth:
    value: date

    def age(self, today: date | None = None) -> Age:
        today = today or date.today()
        years = today.year - self.value.year
        if (today.month, today.day) < (self.value.month, self.value.day):
            years -= 1
        return Age(years)
