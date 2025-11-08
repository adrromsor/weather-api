from dataclasses import dataclass


@dataclass(frozen=True)
class GetWeatherQuery:
    location: str
