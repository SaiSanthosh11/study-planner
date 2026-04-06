from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.database import get_db
from app.models.user import UserRegister, UserLogin
from app.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(body: UserRegister):
    db = get_db()
    existing = await db.users.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name": body.name,
        "email": body.email,
        "password": hash_password(body.password),
        "branch": body.branch,
        "semester": body.semester,
        "streak": 0,
        "created_at": datetime.utcnow(),
    }
    result = await db.users.insert_one(user_doc)
    token = create_access_token({"sub": str(result.inserted_id)})
    return {"token": token, "user": {"id": str(result.inserted_id), "name": body.name, "email": body.email}}

@router.post("/login")
async def login(body: UserLogin):
    db = get_db()
    user = await db.users.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "branch": user.get("branch", "CSE"),
            "semester": user.get("semester", 1),
            "streak": user.get("streak", 0),
        },
    }
