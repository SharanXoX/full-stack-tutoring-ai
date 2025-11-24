from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import User
from backend.core import security  # import your existing security module

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_v2/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Safe helper that uses decode_access_token from your existing security.py
    Does not modify security.py — only imports and uses it.
    """
    payload = security.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # convert user_id to int if possible
    try:
        user_id_int = int(user_id)
    except:
        user_id_int = user_id

    # get user from DB
    user = db.query(User).filter(User.id == user_id_int).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
