class WeatherLocationNotFoundError(Exception):
    def __init__(self, location: str) -> None:
        super().__init__(f"Location {location} was not found.")
