from typing import List, Dict

def classify_performance(percentage: float) -> str:
    if percentage < 50:
        return "weak"
    elif percentage <= 70:
        return "moderate"
    return "strong"

def is_risk_subject(percentage: float) -> bool:
    return percentage < 40

def analyze_marks(marks_list: List[Dict]) -> Dict:
    """
    Returns ranked subjects, risk subjects, and performance summary.
    """
    if not marks_list:
        return {"ranked": [], "risk_subjects": [], "summary": {}}

    enriched = []
    for m in marks_list:
        pct = (m["marks_obtained"] / m["total_marks"]) * 100
        enriched.append({
            **m,
            "percentage": round(pct, 2),
            "performance": classify_performance(pct),
            "is_risk": is_risk_subject(pct),
        })

    # Sort by percentage ascending → highest priority first
    ranked = sorted(enriched, key=lambda x: x["percentage"])

    risk_subjects = [s for s in ranked if s["is_risk"]]

    summary = {
        "total_subjects": len(ranked),
        "weak": len([s for s in ranked if s["performance"] == "weak"]),
        "moderate": len([s for s in ranked if s["performance"] == "moderate"]),
        "strong": len([s for s in ranked if s["performance"] == "strong"]),
        "risk_count": len(risk_subjects),
        "average_percentage": round(sum(s["percentage"] for s in ranked) / len(ranked), 2),
    }

    return {"ranked": ranked, "risk_subjects": risk_subjects, "summary": summary}
