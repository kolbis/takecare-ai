from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Age:
    value: int

    MIN_AGE = 0
    MAX_AGE = 130  # realistic human upper bound

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("Age must be an integer.")

        if not (self.MIN_AGE <= self.value <= self.MAX_AGE):
            raise ValueError(f"Age must be between {self.MIN_AGE} and {self.MAX_AGE}.")

    def is_adult(self) -> bool:
        return self.value >= 18

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)
