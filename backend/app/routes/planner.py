from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime, date
from app.database import get_db
from app.models.plan import PlanRequest
from app.services.marks_service import analyze_marks
from app.services.planner_service import rule_based_plan, reschedule_missed_tasks
from app.services.ai_service import generate_ai_plan
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/planner", tags=["planner"])

@router.post("/generate-plan")
async def generate_plan(body: PlanRequest, user=Depends(get_current_user)):
    db = get_db()
    uid = ObjectId(user["id"])

    # Fetch subjects and marks
    subjects = []
    async for s in db.subjects.find({"user_id": uid}):
        s["id"] = str(s.pop("_id"))
        subjects.append(s)

    marks_list = []
    async for m in db.marks.find({"user_id": uid}):
        m["id"] = str(m.pop("_id"))
        marks_list.append(m)

    if not subjects:
        raise HTTPException(status_code=400, detail="Add subjects before generating a plan")

    marks_analysis = analyze_marks(marks_list)
    start_date = body.start_date or date.today().isoformat()

    # Try AI first, fall back to rule-based
    weekly_plan = await generate_ai_plan(subjects, marks_analysis, body.study_hours_per_day, start_date)
    generated_by = "ai"

    if not weekly_plan:
        weekly_plan = rule_based_plan(subjects, marks_analysis, body.study_hours_per_day, start_date)
        generated_by = "rule_based"

    summary = (
        f"Generated {len(weekly_plan)}-day plan. "
        f"Weak subjects: {marks_analysis['summary'].get('weak', 0)}, "
        f"Risk subjects: {marks_analysis['summary'].get('risk_count', 0)}."
    )

    plan_doc = {
        "user_id": uid,
        "weekly_plan": weekly_plan,
        "summary": summary,
        "generated_by": generated_by,
        "study_hours_per_day": body.study_hours_per_day,
        "created_at": datetime.utcnow(),
    }

    # Replace existing active plan
    await db.study_plans.replace_one({"user_id": uid}, plan_doc, upsert=True)
    saved = await db.study_plans.find_one({"user_id": uid})
    saved["id"] = str(saved.pop("_id"))
    saved["user_id"] = str(saved["user_id"])
    saved["created_at"] = saved["created_at"].isoformat()
    return saved

@router.get("/current-plan")
async def get_current_plan(user=Depends(get_current_user)):
    db = get_db()
    plan = await db.study_plans.find_one({"user_id": ObjectId(user["id"])})
    if not plan:
        raise HTTPException(status_code=404, detail="No plan found. Generate one first.")
    plan["id"] = str(plan.pop("_id"))
    plan["user_id"] = str(plan["user_id"])
    plan["created_at"] = plan["created_at"].isoformat()
    return plan

@router.post("/reschedule")
async def reschedule(missed_date: str, user=Depends(get_current_user)):
    db = get_db()
    uid = ObjectId(user["id"])
    plan = await db.study_plans.find_one({"user_id": uid})
    if not plan:
        raise HTTPException(status_code=404, detail="No plan found")

    updated = reschedule_missed_tasks(plan, missed_date)
    await db.study_plans.replace_one({"user_id": uid}, updated)
    return {"message": "Rescheduled successfully"}
