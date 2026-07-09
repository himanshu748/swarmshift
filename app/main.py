from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

from app.schemas import (
    ErrorDetail,
    ErrorResponse,
    PlanRequest,
    PlanResponse,
    ReplanRequest,
    ReplanResponse,
)
from app.services.scheduler import PlannerError, create_plan, replan
from app.skill_template import render_skill
from app.web import PAGE

app = FastAPI(
    title="SwarmShift",
    version="0.1.0",
    summary="Deterministic multi-agent task scheduling and failure replanning.",
    description=(
        "Assign dependent tasks across capable AI agents to minimize time and cost. "
        "Identical inputs always produce the same plan and SHA-256 plan hash."
    ),
    contact={"name": "SwarmShift", "url": "https://github.com/himanshu748/swarmshift"},
    license_info={"name": "Apache-2.0", "identifier": "Apache-2.0"},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))[:128]
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-Ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.exception_handler(PlannerError)
async def planner_error_handler(_: Request, exc: PlannerError) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
    )
    return JSONResponse(status_code=422, content=payload.model_dump(mode="json"))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    payload = {
        "error": {
            "code": "invalid_request",
            "message": "The JSON payload does not match the API contract.",
            "details": {"issues": exc.errors()},
        }
    }
    return JSONResponse(status_code=422, content=payload)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home() -> HTMLResponse:
    return HTMLResponse(PAGE)


@app.get("/health", tags=["service"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "swarmshift", "version": "0.1.0"}


@app.get("/skill.md", response_class=PlainTextResponse, include_in_schema=False)
async def skill(request: Request) -> PlainTextResponse:
    forwarded_proto = request.headers.get("x-forwarded-proto")
    base = str(request.base_url)
    if forwarded_proto == "https" and base.startswith("http://"):
        base = "https://" + base.removeprefix("http://")
    return PlainTextResponse(render_skill(base), media_type="text/markdown; charset=utf-8")


@app.post(
    "/v1/plan",
    response_model=PlanResponse,
    responses={422: {"model": ErrorResponse}},
    tags=["planning"],
    summary="Create a deterministic multi-agent execution plan",
)
async def plan(mission: PlanRequest) -> PlanResponse:
    return create_plan(mission)


@app.post(
    "/v1/replan",
    response_model=ReplanResponse,
    responses={422: {"model": ErrorResponse}},
    tags=["planning"],
    summary="Replan after an agent fails without redoing completed work",
)
async def replan_route(payload: ReplanRequest) -> ReplanResponse:
    return replan(payload)
