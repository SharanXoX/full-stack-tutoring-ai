from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import logging

from backend.db import get_db
from backend.models import User
from backend.schemas import SignupRequest, LoginRequest, TokenResponse
from backend.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger("uvicorn.error")

@router.post("/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    try:
        if req.role not in ("teacher", "student"):
            raise HTTPException(status_code=400, detail="role must be 'teacher' or 'student'")

        existing = db.execute(
            select(User).where(User.email == req.email)
        ).scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            email=req.email,
            hashed_password=hash_password(req.password),
            role=req.role,
            teacher_id=req.teacher_id
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token({"sub": str(user.id), "role": user.role})
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception:
        logger.exception("Signup error")
        raise HTTPException(status_code=500, detail="Internal server error")
