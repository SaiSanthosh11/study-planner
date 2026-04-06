from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class PlanRequest(BaseModel):
    study_hours_per_day: float = 6.0
    start_date: Optional[str] = None  # ISO date, defaults to today

class TaskItem(BaseModel):
    subject: str
    topic: str
    duration_minutes: int
    task_type: str  # study / revision / practice
    completed: bool = False

class DayPlan(BaseModel):
    date: str
    day_label: str
    tasks: List[TaskItem]
    total_hours: float
    is_revision_day: bool = False

class StudyPlanOut(BaseModel):
    id: str
    user_id: str
    weekly_plan: List[DayPlan]
    summary: str
    generated_by: str  # ai / rule_based
    created_at: str
