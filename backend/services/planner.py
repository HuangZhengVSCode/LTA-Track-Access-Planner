"""Application service that isolates the API from the scheduling engine."""

from io import BytesIO
from typing import Any

from backend.config import SCENARIOS
from backend.services.analytics import build_analytics, build_assurance, build_summary
from backend.services.serialization import dataframe_to_dataset
from scheduler import run_track_access_scheduler


def generate_plan(file_contents: dict[str, bytes], scenario: str) -> dict[str, Any]:
    file_objects = {name: BytesIO(content) for name, content in file_contents.items()}
    access, occupancy, results = run_track_access_scheduler(file_objects, scenario=scenario)
    summary = build_summary(access, results)

    return {
        "scenario": scenario,
        "scenario_name": SCENARIOS[scenario]["name"],
        "summary": summary,
        "assurance": build_assurance(summary, scenario),
        "datasets": {
            "access": dataframe_to_dataset(access),
            "occupancy": dataframe_to_dataset(occupancy),
            "results": dataframe_to_dataset(results),
        },
        "analytics": build_analytics(access, occupancy),
    }
