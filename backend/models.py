"""Typed request and response models used at the API boundary."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Scenario(str, Enum):
    fixed_capacity = "A"
    fixed_completion = "B"
    balanced = "C"


class Dataset(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]


class PlanSummary(BaseModel):
    activities: int = 0
    access_allocations: int = 0
    contracts_late: int = 0
    total_overrun_days: int = 0
    eclo_accesses: int = 0
    final_week: int = 0
    duplicate_access_ids: int = 0


class AssuranceCheck(BaseModel):
    key: str
    label: str
    status: str
    message: str


class PlanResponse(BaseModel):
    scenario: str
    scenario_name: str
    summary: PlanSummary
    assurance: list[AssuranceCheck]
    datasets: dict[str, Dataset]
    analytics: dict[str, Any] = Field(default_factory=dict)


class ApiError(BaseModel):
    detail: str
