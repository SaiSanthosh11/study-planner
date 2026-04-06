from pydantic import BaseModel
from typing import Optional, Dict

class ProgressUpdate(BaseModel):
    plan_id: str
    date: str
    subject: str
    topic: str
    completed: bool
    time_spent_minutes: Optional[int] = 0

class ProgressOut(BaseModel):
    user_id: str
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    streak: int
    exam_readiness: Dict[str, float]
    weak_alerts: list
