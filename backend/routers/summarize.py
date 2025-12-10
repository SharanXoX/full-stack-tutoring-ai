from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Union, Any
from sqlalchemy.orm import Session
import logging
import traceback

from backend.db import get_db
import backend.rag as rag_module 
from backend.dependencies import get_current_user_optional

# Try to import potential DB model names safely
try:
    from backend.models import ContentSummary 
except Exception:
    ContentSummary = None

logger = logging.getLogger("backend.summarize")
router = APIRouter(prefix="/api/content", tags=["content"]) 


class SummarizeRequest(BaseModel):
    file_id: Optional[str] = None
    text: Optional[str] = None
    max_length: Optional[int] = 300


class SummarizeResponse(BaseModel):
    summary: Optional[str] = None
    summary_paragraphs: Optional[List[str]] = None
    key_points: List[Any] = []
    topic: Optional[str] = "Document Summary"
    file_id: Optional[str] = None


@router.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest, db: Session = Depends(get_db)):
    """
    Summarize a previously uploaded document (preferred) or raw text.
    Expects either file_id or text. Returns structured summary data.
    """
    if not (request.file_id or request.text):
        raise HTTPException(status_code=400, detail="Provide file_id or text to summarize")

    logger.info("Summarize request received: file_id=%s, text_len=%s", request.file_id, len(request.text) if request.text else 0)

    try:
        # Prefer a document summarizer if your rag module supplies it
        summary_result = None

        if request.file_id:
            # Check for summarize_document
            if hasattr(rag_module, "summarize_document"):
                logger.info("Calling rag_module.summarize_document for file_id=%s", request.file_id)
                summary_result = rag_module.summarize_document(request.file_id, max_length=request.max_length)
            elif hasattr(rag_module, "summarize_file"):
                summary_result = rag_module.summarize_file(request.file_id, max_length=request.max_length)
        elif request.text and hasattr(rag_module, "summarize_text"):
            logger.info("Calling rag_module.summarize_text for text input")
            summary_result = rag_module.summarize_text(request.text, max_length=request.max_length)
        
        # Fallback Logic if nothing computed yet
        if summary_result is None:
             logger.info("Using fallback summarization path")
             # Simple fallback to just strip text if available
             if request.text:
                summary_result = {"summary": request.text[:500], "key_points": []}
             else:
                raise RuntimeError("No suitable summarization function found for input")

        # Normalize result structure
        response_data = {
            "summary": None,
            "summary_paragraphs": [],
            "key_points": [],
            "topic": "Document Summary",
            "file_id": request.file_id
        }

        if isinstance(summary_result, dict):
            response_data["summary"] = summary_result.get("summary")
            response_data["summary_paragraphs"] = summary_result.get("summary_paragraphs")
            response_data["topic"] = summary_result.get("topic") or "Document Summary"
            response_data["key_points"] = summary_result.get("key_points") or []
        else:
            response_data["summary"] = str(summary_result)

        return response_data

    except HTTPException:
        raise
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("Summarization failed: %s", str(exc))
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(exc)}")
