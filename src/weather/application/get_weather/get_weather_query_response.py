from dataclasses import dataclass


@dataclass(frozen=True)
class GetWeatherQueryResponse:
    location: str
    temperature: float
    condition: str
    last_updated: str
