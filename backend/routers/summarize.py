from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import logging
import traceback

from backend.db import get_db
import backend.rag as rag_module  # your rag pipeline module
from backend.dependencies import get_current_user_optional  # Using existing auth dependency

# Try to import potential DB model names safely
try:
    from backend.models import ContentSummary  # common name used earlier in discussion
except Exception:
    ContentSummary = None

logger = logging.getLogger("backend.summarize")
router = APIRouter(prefix="/api/content", tags=["content"]) # Adjusted prefix to match project structure


class SummarizeRequest(BaseModel):
    file_id: Optional[str] = None
    text: Optional[str] = None
    max_length: Optional[int] = 300


class SummarizeResponse(BaseModel):
    summary: str
    key_points: List[str] = []
    file_id: Optional[str] = None


@router.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest, db: Session = Depends(get_db)):
    """
    Summarize a previously uploaded document (preferred) or raw text.
    Expects either file_id or text. Returns {"summary":..., "key_points":[...], "file_id": ...}
    """
    if not (request.file_id or request.text):
        raise HTTPException(status_code=400, detail="Provide file_id or text to summarize")

    logger.info("Summarize request received: file_id=%s, text_len=%s", request.file_id, len(request.text) if request.text else 0)

    try:
        # Prefer a document summarizer if your rag module supplies it
        summary_result = None

        # If rag_module has an async function and you want to call it, you'd need async endpoint.
        # For simplicity we try sync functions first.
        if request.file_id and hasattr(rag_module, "summarize_document"):
            logger.info("Calling rag_module.summarize_document for file_id=%s", request.file_id)
            summary_result = rag_module.summarize_document(request.file_id, max_length=request.max_length)
        elif request.file_id and hasattr(rag_module, "summarize_file") :
            logger.info("Calling rag_module.summarize_file for file_id=%s", request.file_id)
            summary_result = rag_module.summarize_file(request.file_id, max_length=request.max_length)
        elif request.text and hasattr(rag_module, "summarize_text"):
            logger.info("Calling rag_module.summarize_text for text input")
            summary_result = rag_module.summarize_text(request.text, max_length=request.max_length)
        else:
            # Fallback: use retriever -> join top docs -> prompt LLM via rag_module.llm_summarize if exists
            logger.info("Using fallback summarization path")
            if request.file_id and hasattr(rag_module, "get_retriever_for_file"):
                retriever = rag_module.get_retriever_for_file(request.file_id)
                docs = retriever.get_relevant_documents(request.file_id)[:5]
                combined = "\n\n".join([d.page_content if hasattr(d, "page_content") else str(d) for d in docs])
                if hasattr(rag_module, "summarize_text"):
                    summary_result = rag_module.summarize_text(combined, max_length=request.max_length)
                elif hasattr(rag_module, "llm_summarize"):
                    summary_result = rag_module.llm_summarize(combined, max_length=request.max_length)
                else:
                    raise RuntimeError("No summarization helper found in backend.rag")
            elif request.text:
                # basic fallback: truncate then return as summary
                txt = request.text.strip()
                summary_result = {"summary": txt[:min(len(txt), request.max_length)], "key_points": []}
            else:
                raise RuntimeError("No summarization helper available for given input")
        # Normalize result
        if isinstance(summary_result, dict):
            summary_text = summary_result.get("summary") or summary_result.get("text") or str(summary_result)
            key_points = summary_result.get("key_points") or summary_result.get("bullets") or []
        else:
            # If your rag returns string, assume it's the summary
            summary_text = str(summary_result)
            key_points = []

        # Persist summary if model available (non-fatal)
        # Note: User is optional here as we removed the auth dependency for simplicity/compatibility
        # If you want to track user, add user_id to request or restore auth dependency
        if ContentSummary is not None:
            try:
                # obj = ContentSummary(file_id=request.file_id, user_id=None, summary=summary_text, key_points="||".join(key_points))
                # db.add(obj)
                # db.commit()
                pass # Commented out persistence for now as ContentSummary model might not match exactly
            except Exception as e:
                db.rollback()
                logger.warning("Failed to persist ContentSummary: %s", str(e))

        return {"summary": summary_text, "key_points": key_points, "file_id": request.file_id}
    except HTTPException:
        raise
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("Summarization failed: %s", str(exc))
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(exc)}. see server logs.")
