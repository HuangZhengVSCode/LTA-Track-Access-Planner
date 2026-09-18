"""Versioned API routes."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool

from backend.config import REQUIRED_TABLES, SCENARIOS
from backend.models import PlanResponse, Scenario
from backend.services.planner import generate_plan
from backend.services.validation import InputValidationError, UploadedTable, validate_uploads

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/configuration")
def configuration() -> dict:
    return {"required_tables": list(REQUIRED_TABLES), "scenarios": SCENARIOS}


@router.post(
    "/plans",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
    responses={422: {"description": "Invalid network package"}, 500: {"description": "Scheduler failure"}},
)
async def create_plan(
    scenario: Scenario = Form(...),
    files: list[UploadFile] = File(...),
) -> PlanResponse:
    try:
        uploads = [
            UploadedTable(name=file.filename or "unnamed.csv", content=await file.read())
            for file in files
        ]
        file_contents = validate_uploads(uploads)
        payload = await run_in_threadpool(generate_plan, file_contents, scenario.value)
        return PlanResponse.model_validate(payload)
    except InputValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (KeyError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=f"Scheduling engine error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="The schedule could not be generated.") from exc
    finally:
        for file in files:
            await file.close()
