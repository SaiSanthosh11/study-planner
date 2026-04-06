import json
from typing import List, Dict, Optional
from app.config import settings

AI_PROMPT_TEMPLATE = """
You are an expert B.Tech academic study planner. Your job is to create a precise 7-day study schedule.

Student Profile:
- Study hours available per day: {study_hours}
- Plan start date: {start_date}

Here are the subjects with their COMPLETE SYLLABUS and performance data:
{subjects_json}

STRICT RULES — follow every one:
1. EVERY task topic MUST be taken EXACTLY from the subject's "syllabus" list above. Do NOT invent or paraphrase topic names.
2. Distribute syllabus topics across the 7 days — each topic should appear on a DIFFERENT day for first-time study.
3. Weak subjects (performance=weak, percentage<50) get 3x more daily time allocation.
4. Moderate subjects (50-70%) get 2x more time. Strong subjects get 1x.
5. Risk subjects (percentage<40) MUST have at least one task EVERY day.
6. Day 3 and Day 6 are REVISION days — only use task_type "revision" and prefix topic with "Revision: ".
7. On revision days, revisit topics already covered in previous days.
8. On study days, use task_type "study" for new topics, "practice" for the last session of weak subjects.
9. Each session is 50-60 minutes. Include 10-min breaks (don't count breaks in total_hours).
10. total_hours must NOT exceed {study_hours}.
11. Be specific — use the exact topic name from the syllabus list.

Return a JSON array of exactly 7 objects. Each object:
{{
  "date": "YYYY-MM-DD",
  "day_label": "Monday",
  "tasks": [
    {{
      "subject": "<exact subject name>",
      "topic": "<exact topic from syllabus>",
      "duration_minutes": 60,
      "task_type": "study",
      "completed": false
    }}
  ],
  "total_hours": 4.0,
  "is_revision_day": false
}}

Return ONLY the raw JSON array. No markdown fences, no explanation, no extra text.
"""


def _build_subject_payload(subjects: List[Dict], marks_analysis: Dict) -> List[Dict]:
    ranked = marks_analysis.get("ranked", [])
    subject_map = {s["name"]: s for s in subjects}
    enriched = []

    for r in ranked:
        name = r.get("subject_name", "")
        subj = subject_map.get(name, {})
        syllabus = subj.get("syllabus", [])
        enriched.append({
            "subject_name": name,
            "percentage": r.get("percentage", 60),
            "performance": r.get("performance", "moderate"),
            "is_risk": r.get("is_risk", False),
            "exam_date": subj.get("exam_date", ""),
            "difficulty": subj.get("difficulty", 3),
            "syllabus": syllabus if syllabus else [f"{name} Topic {i+1}" for i in range(8)],
        })

    # Fallback: no marks data
    if not enriched:
        for s in subjects:
            syllabus = s.get("syllabus", [])
            enriched.append({
                "subject_name": s["name"],
                "percentage": 60,
                "performance": "moderate",
                "is_risk": False,
                "exam_date": s.get("exam_date", ""),
                "difficulty": s.get("difficulty", 3),
                "syllabus": syllabus if syllabus else [f"{s['name']} Topic {i+1}" for i in range(8)],
            })

    return enriched


async def generate_ai_plan(
    subjects: List[Dict],
    marks_analysis: Dict,
    study_hours: float,
    start_date: str,
) -> Optional[List[Dict]]:
    if not settings.gemini_api_key:
        return None

    try:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)

        enriched = _build_subject_payload(subjects, marks_analysis)
        subjects_json = json.dumps(enriched, indent=2, default=str)

        prompt = AI_PROMPT_TEMPLATE.format(
            study_hours=study_hours,
            start_date=start_date,
            subjects_json=subjects_json,
        )

        last_error = None
        response = None
        for model in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                print(f"✅ Gemini model used: {model}")
                break
            except Exception as e:
                print(f"⚠️  Model {model} failed: {e}")
                last_error = e

        if response is None:
            raise last_error

        content = response.text.strip()
        # Strip markdown fences if present
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        plan = json.loads(content)
        print(f"✅ AI plan: {len(plan)} days generated")
        return plan

    except Exception as e:
        print(f"⚠️  Gemini failed → rule-based fallback. Reason: {e}")
        return None
