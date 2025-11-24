from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from backend.db import get_db
from backend.models import User
from backend.schemas import SignupRequest, TokenResponse, LoginRequest, UserOut
from backend.core import security as security_core  # your existing security utils
from backend.core.auth_helpers import get_current_user

router = APIRouter(prefix="/auth_v2", tags=["Auth_v2"])


@router.post("/signup", response_model=UserOut)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash the plain password and store in hashed_password column
    hashed = security_core.hash_password(payload.password)

    user_kwargs = {
        "email": payload.email,
        "hashed_password": hashed,
        "role": payload.role
    }
    if payload.teacher_id is not None:
        user_kwargs["teacher_id"] = payload.teacher_id

    user = User(**user_kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2-style form login (Content-Type: application/x-www-form-urlencoded).
    Frontend can use this, or use /login_json below which accepts JSON.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security_core.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    access_token = security_core.create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=access_token)


# JSON login convenience endpoint (uses your LoginRequest schema)
@router.post("/login_json", response_model=TokenResponse)
def login_json(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not security_core.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    access_token = security_core.create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
