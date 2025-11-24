import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from backend.ingest_utils import extract_text, save_preview

router = APIRouter(prefix="/api/content", tags=["content"])

# Calculate project root relative to this file: backend/routers/content.py
# backend/routers/ -> backend/ -> project_root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOADS_DIR = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Form(...), user_role: str = Form("teacher")):
    """
    Save uploaded file to the uploads/ folder and return metadata.
    Supports: PDF, DOCX, PPTX, TXT, MD, CSV, and images (PNG, JPG, JPEG, BMP, TIFF, GIF)
    Both teachers and students can upload.
    """
    filename = file.filename
    
    # Validate file type
    allowed_extensions = {
        '.pdf', '.docx', '.pptx', '.txt', '.md', '.csv',
        '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'
    }
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file_ext}. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Create user-specific subdirectory
    user_dir = os.path.join(UPLOADS_DIR, user_role, user_id)
    os.makedirs(user_dir, exist_ok=True)
    
    # Add timestamp to prevent overwrites
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(filename)[0]
    new_filename = f"{base_name}_{timestamp}{file_ext}"
    save_path = os.path.join(user_dir, new_filename)

    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    resp = {
        "file_id": new_filename,  # Frontend expects file_id
        "original_filename": filename,
        "saved_filename": new_filename,
        "saved_path": save_path,
        "user_id": user_id,
        "user_role": user_role,
        "file_type": file_ext,
        "size_bytes": len(contents),
    }

    # --- RAG Ingestion ---
    try:
        # Extract text
        text = extract_text(save_path)
        
        if not text or len(text.strip()) < 10:
            resp["ingestion_status"] = "warning"
            resp["ingestion_message"] = "File uploaded but no text extracted (empty or unsupported content)"
            return JSONResponse(resp)
        
        # Ingest into Vector Store
        from backend.rag import ingest_document
        num_chunks = ingest_document(save_path, text)
        resp["ingestion_status"] = "success"
        resp["chunks_added"] = num_chunks
        resp["text_length"] = len(text)
    except Exception as e:
        print(f"Ingestion failed: {e}")
        resp["ingestion_status"] = "failed"
        resp["ingestion_error"] = str(e)
    # ---------------------

    return JSONResponse(resp)


@router.post("/process_sync")
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
