# backend/app.py
import os
import traceback
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# import ingest helpers (local file)
from backend.ingest_utils import extract_text, save_preview

# load .env if present
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# --- AUTH / DB imports (used later in this file) ---
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from backend.models import get_engine, create_tables, User as UserModel
from backend.auth_utils import get_password_hash as hash_password, verify_password, create_access_token, decode_access_token
# get_current_user is defined locally below, not imported from dependencies
from backend.schemas import SignupRequest, LoginRequest, TokenResponse, UserOut
from backend.teachers import router as teacher_router



# ----------------------------------------------------

app = FastAPI(title="AI Tutor Backend")

# Include routers
app.include_router(teacher_router)

# Allow requests from Vite dev server and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uploads directory (project_root/uploads)
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))  # one level up from backend/
UPLOADS_DIR = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# ---------------------------
# Database setup (SQLAlchemy)
# ---------------------------
# Engine and tables (ai_tutor.db in project root by default)
ENGINE = get_engine()
create_tables(ENGINE)

# simple session factory
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# ---------------------------

@app.get("/")
def root():
    return {
        "message": "AI Tutor Backend API",
        "docs": "/docs",
        "health": "/health",
        "version": "0.1.0"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/content/upload")
async def upload_file(file: UploadFile = File(...), teacher_id: str = Form(...)):
    """
    Save uploaded file to the uploads/ folder and return metadata.
    teacher_id is passed as a simple form field for now.
    """
    filename = file.filename
    # Prevent accidental overwrite — you can extend with timestamp if you wish
    save_path = os.path.join(UPLOADS_DIR, filename)

    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    resp = {
        "original_filename": filename,
        "saved_path": save_path,
        "teacher_id": teacher_id,
        "size_bytes": len(contents),
    }
    return JSONResponse(resp)


@app.post("/api/content/process_sync")
async def process_sync(filename: str = Form(...)):
    """
    Synchronous processing (simple): given a filename in uploads/, extract text and save preview JSON.
    Use this to test ingestion quickly.
    """
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse({"error": "file not found", "path": file_path}, status_code=404)
    try:
        text = extract_text(file_path)
        preview_path = save_preview(text, file_path)
        return JSONResponse({"status": "processed", "preview_path": preview_path, "length": len(text)})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# --- AUTH ROUTES AND DEPENDENCY (paste near the end of app.py) ---

# helper dependency: get current user from Authorization header
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth header")
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub") or payload.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = db.execute(select(UserModel).where(UserModel.id == int(user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# --- Signup endpoint with error handling ---
@app.post("/auth/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    """
    DEBUG version: catches exceptions and returns the exception message + traceback
    so you can see the underlying error directly via HTTP response.
    Remove/restore original implementation after debugging.
    """
    try:
        # original signup code (kept identical)
        if req.role not in ("teacher", "student"):
            raise HTTPException(status_code=400, detail="role must be 'teacher' or 'student'")
        existing = db.execute(select(UserModel).where(UserModel.email == req.email)).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        user = UserModel(email=req.email, hashed_password=hash_password(req.password), role=req.role, teacher_id=req.teacher_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        # re-raise known HTTPExceptions (preserve status codes)
        raise
    except Exception as e:
        tb = traceback.format_exc()
        # return the exception type, message and traceback in JSON for debugging
        return JSONResponse(status_code=500, content={
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": tb
        })


@app.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(UserModel).where(UserModel.email == req.email)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/teachers/{teacher_id}/students", response_model=list[UserOut])
def get_teacher_students(teacher_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # only allow teacher access to their own students
    if current_user.role != "teacher" or current_user.id != teacher_id:
        raise HTTPException(status_code=403, detail="Only the teacher can view their students")
    students = db.execute(select(UserModel).where(UserModel.teacher_id == teacher_id)).scalars().all()
    return students
    

# --- end auth routes ---
