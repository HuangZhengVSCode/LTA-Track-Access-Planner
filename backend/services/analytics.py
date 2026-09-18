"""Read-only operational analytics derived from scheduler outputs."""

from typing import Any

import pandas as pd


def _integer_sum(frame: pd.DataFrame, column: str) -> int:
    if frame.empty or column not in frame:
        return 0
    return int(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


def build_summary(access: pd.DataFrame, results: pd.DataFrame) -> dict[str, int]:
    duplicates = 0
    if not access.empty and {"activity_id", "access_seq"}.issubset(access.columns):
        duplicates = int(access.duplicated(subset=["activity_id", "access_seq"]).sum())

    overruns = (
        pd.to_numeric(results.get("overrun_days", pd.Series(dtype=float)), errors="coerce")
        .fillna(0)
    )
    weeks = pd.to_numeric(access.get("week", pd.Series(dtype=float)), errors="coerce")

    return {
        "activities": int(access["activity_id"].nunique()) if "activity_id" in access else 0,
        "access_allocations": int(len(access)),
        "contracts_late": int((overruns > 0).sum()),
        "total_overrun_days": int(overruns.sum()),
        "eclo_accesses": _integer_sum(access, "eclo"),
        "final_week": int(weeks.max()) if not weeks.empty else 0,
        "duplicate_access_ids": duplicates,
    }


def build_assurance(summary: dict[str, int], scenario: str) -> list[dict[str, str]]:
    generated = summary["activities"] > 0
    duplicates = summary["duplicate_access_ids"]
    invalid_eclo = scenario == "A" and summary["eclo_accesses"] > 0
    return [
        {
            "key": "schedule",
            "label": "Schedule",
            "status": "pass" if generated else "fail",
            "message": "Schedule generated successfully." if generated else "The generated schedule is empty.",
        },
        {
            "key": "duplicates",
            "label": "Access identifiers",
            "status": "pass" if duplicates == 0 else "fail",
            "message": "No duplicate access identifiers detected."
            if duplicates == 0
            else f"{duplicates} duplicate access identifier(s) detected.",
        },
        {
            "key": "eclo",
            "label": "ECLO policy",
            "status": "fail" if invalid_eclo else "pass",
            "message": "ECLO access detected under Fixed Capacity mode."
            if invalid_eclo
            else "Early Closure / Late Opening status is normal.",
        },
    ]


def build_capacity(occupancy: pd.DataFrame) -> dict[str, Any]:
    required = {"location_id", "week", "activity_id", "co_share_group"}
    if occupancy.empty or not required.issubset(occupancy.columns):
        return {"summary": [], "locations": []}

    weekly = (
        occupancy.groupby(["location_id", "week"], dropna=False)
        .agg(activities=("activity_id", "nunique"), possessions=("co_share_group", "nunique"))
        .reset_index()
    )
    totals = (
        weekly.groupby("location_id", dropna=False)
        .agg(
            total_possessions=("possessions", "sum"),
            total_activities=("activities", "sum"),
            active_weeks=("week", "nunique"),
            peak_weekly_possessions=("possessions", "max"),
        )
        .reset_index()
        .sort_values("total_possessions", ascending=False)
    )

    location_series = []
    for location, group in weekly.groupby("location_id", dropna=False):
        location_series.append(
            {
                "location_id": str(location),
                "weeks": [
                    {
                        "week": int(row.week),
                        "activities": int(row.activities),
                        "possessions": int(row.possessions),
                    }
                    for row in group.sort_values("week").itertuples()
                ],
            }
        )

    return {
        "summary": [
            {
                "location_id": str(row.location_id),
                "total_possessions": int(row.total_possessions),
                "total_activities": int(row.total_activities),
                "active_weeks": int(row.active_weeks),
                "peak_weekly_possessions": int(row.peak_weekly_possessions),
            }
            for row in totals.itertuples()
        ],
        "locations": location_series,
    }


def build_analytics(access: pd.DataFrame, occupancy: pd.DataFrame) -> dict[str, Any]:
    activity_options = (
        sorted(access["activity_id"].astype(str).unique().tolist())
        if "activity_id" in access
        else []
    )
    return {"activity_options": activity_options, "capacity": build_capacity(occupancy)}
