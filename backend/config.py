"""Application settings and domain constants."""

import os
from dataclasses import dataclass


def _allowed_origins() -> tuple[str, ...]:
    configured = os.getenv("CORS_ORIGINS", "")
    if configured:
        return tuple(origin.strip().rstrip("/") for origin in configured.split(",") if origin.strip())
    return (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://nebu1ax.netlify.app",
    )


@dataclass(frozen=True)
class Settings:
    app_name: str = "LTA Track Access Planner API"
    api_prefix: str = "/api/v1"
    max_file_size_bytes: int = 25 * 1024 * 1024
    allowed_origins: tuple[str, ...] = _allowed_origins()


settings = Settings()

REQUIRED_TABLES = (
    "01_LINES",
    "02_STATIONS",
    "03_SECTORS",
    "04_LOCATION_SUPPLY",
    "05_BUFFER_LOCATION",
    "06_PARAMETERS",
    "07_PROJECT_DETAILS",
    "08_ACTIVITY_DETAILS",
)

SCENARIOS = {
    "A": {
        "name": "Fixed Capacity",
        "description": "Protect nominal network capacity and allow schedule extension.",
        "rules": ["Nominal capacity enforced", "ECLO disabled", "Schedule extension permitted"],
    },
    "B": {
        "name": "Fixed Completion Dates",
        "description": "Prioritise committed completion dates with controlled capacity relief.",
        "rules": ["Deadlines enforced", "Excess capacity permitted", "ECLO permitted"],
    },
    "C": {
        "name": "Balanced Operations",
        "description": "Balance delivery, capacity pressure, and continuity constraints.",
        "rules": ["Capacity flexibility controlled", "Delivery and capacity balanced", "ECLO controlled"],
    },
}
