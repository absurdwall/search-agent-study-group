"""Deterministic weather tool used by the Orders-agent workshop."""


FAKE_WEATHER = {
    "seattle": {
        "city": "Seattle",
        "condition": "rain",
        "temperature_f": 58,
        "precipitation_chance_percent": 80,
    }
}


def get_weather(city: str) -> dict:
    """Return simulated current weather for a supported city."""
    normalized = " ".join(city.split()).casefold()
    return FAKE_WEATHER.get(normalized, {"error": f"No simulated weather for {city}."})
