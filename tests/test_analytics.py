import pandas as pd

from backend.services.analytics import build_assurance, build_capacity, build_summary


def test_summary_matches_original_dashboard_metrics():
    access = pd.DataFrame(
        [
            {"activity_id": "A1", "access_seq": 1, "week": 2, "eclo": 0},
            {"activity_id": "A1", "access_seq": 1, "week": 3, "eclo": 1},
            {"activity_id": "A2", "access_seq": 1, "week": 7, "eclo": 0},
        ]
    )
    results = pd.DataFrame([{"overrun_days": 0}, {"overrun_days": 4}])

    summary = build_summary(access, results)

    assert summary == {
        "activities": 2,
        "access_allocations": 3,
        "contracts_late": 1,
        "total_overrun_days": 4,
        "eclo_accesses": 1,
        "final_week": 7,
        "duplicate_access_ids": 1,
    }


def test_fixed_capacity_flags_eclo_usage():
    checks = build_assurance(
        {"activities": 2, "duplicate_access_ids": 0, "eclo_accesses": 1}, "A"
    )
    assert next(check for check in checks if check["key"] == "eclo")["status"] == "fail"


def test_capacity_rollup_counts_unique_possessions():
    occupancy = pd.DataFrame(
        [
            {"location_id": "S1", "week": 1, "activity_id": "A1", "co_share_group": "P1"},
            {"location_id": "S1", "week": 1, "activity_id": "A2", "co_share_group": "P1"},
            {"location_id": "S1", "week": 2, "activity_id": "A2", "co_share_group": "P2"},
        ]
    )
    capacity = build_capacity(occupancy)
    assert capacity["summary"][0]["total_possessions"] == 2
    assert capacity["summary"][0]["peak_weekly_possessions"] == 1
