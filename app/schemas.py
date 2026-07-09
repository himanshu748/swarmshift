from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
    capabilities: list[str] = Field(min_length=1, max_length=32)
    cost_per_hour: float = Field(default=0.0, ge=0, le=100_000)
    max_parallel: int = Field(default=1, ge=1, le=8)

    @field_validator("capabilities")
    @classmethod
    def normalize_capabilities(cls, values: list[str]) -> list[str]:
        normalized = sorted({value.strip().lower() for value in values if value.strip()})
        if not normalized:
            raise ValueError("at least one non-empty capability is required")
        return normalized


class TaskSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
    duration_minutes: int = Field(gt=0, le=10_080)
    requires: list[str] = Field(default_factory=list, max_length=16)
    depends_on: list[str] = Field(default_factory=list, max_length=32)
    priority: int = Field(default=3, ge=1, le=5)

    @field_validator("requires")
    @classmethod
    def normalize_requirements(cls, values: list[str]) -> list[str]:
        return sorted({value.strip().lower() for value in values if value.strip()})

    @field_validator("depends_on")
    @classmethod
    def normalize_dependencies(cls, values: list[str]) -> list[str]:
        return list(dict.fromkeys(value.strip() for value in values if value.strip()))


class PlanObjective(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: Literal["fastest", "cheapest", "balanced"] = "balanced"
    cost_weight: float = Field(default=0.35, ge=0, le=1)
    deadline_minutes: int | None = Field(default=None, gt=0, le=43_200)


class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tasks: list[TaskSpec] = Field(min_length=1, max_length=100)
    agents: list[AgentSpec] = Field(min_length=1, max_length=50)
    objective: PlanObjective = Field(default_factory=PlanObjective)


class Assignment(BaseModel):
    task_id: str
    agent_id: str
    start_minute: int
    end_minute: int
    duration_minutes: int
    cost: float
    critical: bool
    reasons: list[str]


class PlanWave(BaseModel):
    start_minute: int
    task_ids: list[str]


class PlanMetrics(BaseModel):
    makespan_minutes: int
    critical_path_minutes: int
    total_cost: float
    deadline_met: bool | None
    parallelism_peak: int


class PlanResponse(BaseModel):
    plan_hash: str
    assignments: list[Assignment]
    waves: list[PlanWave]
    critical_path: list[str]
    metrics: PlanMetrics
    explanation: list[str]
    warnings: list[str]


class CompletedTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    agent_id: str | None = None
    ended_at_minute: int = Field(ge=0)


class ReplanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mission: PlanRequest
    current_minute: int = Field(ge=0)
    completed: list[CompletedTask] = Field(default_factory=list, max_length=100)
    failed_agent_ids: list[str] = Field(default_factory=list, max_length=50)


class ReplanResponse(BaseModel):
    replanned_from_minute: int
    completed_task_ids: list[str]
    removed_agent_ids: list[str]
    plan: PlanResponse
    changes: list[str]


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, object] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail
