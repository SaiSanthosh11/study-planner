from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime
from app.database import get_db
from app.models.subject import SubjectCreate, SubjectOut
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/subjects", tags=["subjects"])

def serialize(doc) -> dict:
    doc["id"] = str(doc.pop("_id"))
    doc["user_id"] = str(doc["user_id"])
    return doc

@router.post("", status_code=201)
async def add_subject(body: SubjectCreate, user=Depends(get_current_user)):
    db = get_db()
    doc = {
        **body.model_dump(),
        "user_id": ObjectId(user["id"]),
        "created_at": datetime.utcnow(),
    }
    result = await db.subjects.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize(doc)

@router.get("")
async def get_subjects(user=Depends(get_current_user)):
    db = get_db()
    cursor = db.subjects.find({"user_id": ObjectId(user["id"])})
    subjects = []
    async for doc in cursor:
        subjects.append(serialize(doc))
    return subjects

@router.delete("/{subject_id}", status_code=204)
async def delete_subject(subject_id: str, user=Depends(get_current_user)):
    db = get_db()
    result = await db.subjects.delete_one({"_id": ObjectId(subject_id), "user_id": ObjectId(user["id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subject not found")
