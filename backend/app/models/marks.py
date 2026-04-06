from pydantic import BaseModel, Field
from typing import Optional

class MarksCreate(BaseModel):
    subject_id: str
    subject_name: str
    marks_obtained: float = Field(ge=0, le=100)
    total_marks: float = Field(default=100, ge=1)
    exam_type: Optional[str] = "mid"  # mid / final / quiz

class MarksOut(MarksCreate):
    id: str
    user_id: str
    percentage: float
    performance: str  # weak / moderate / strong
    is_risk: bool
