from dataclasses import dataclass
from typing import Self


@dataclass
class Weather:
    location: str
    temperature: float
    condition: str
    last_updated: str

    @classmethod
    def from_primitives(
        cls, location: str, temperature: float, condition: str, last_updated: str
    ) -> Self:
        return cls(
            location=location,
            temperature=temperature,
            condition=condition,
            last_updated=last_updated,
        )
