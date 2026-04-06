from pydantic import BaseModel, Field
from typing import Optional, List

class SubjectCreate(BaseModel):
    name: str
    code: Optional[str] = ""
    exam_date: Optional[str] = None
    difficulty: int = Field(default=3, ge=1, le=5)
    syllabus: List[str] = Field(default=[], description="List of topics in the syllabus")

class SubjectOut(SubjectCreate):
    id: str
    user_id: str
    priority: Optional[int] = None
    performance: Optional[str] = None
