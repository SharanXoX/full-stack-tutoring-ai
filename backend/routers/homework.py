from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from backend.db import get_db
from backend.models import HomeworkSession, User
from backend.rag import query_knowledge_base

router = APIRouter(prefix="/api/homework", tags=["homework"])

class HomeworkRequest(BaseModel):
    user_id: str
    problem: str

class HintRequest(BaseModel):
    session_id: int

class HomeworkResponse(BaseModel):
    session_id: int
    hints: List[str]
    solution: Optional[str] = None
    hint_count: int

# Helper to resolve user_id
def resolve_user(db: Session, user_identifier: str) -> User:
    if user_identifier == "student_demo":
        user = db.execute(select(User).where(User.role == "student")).scalars().first()
        if user: return user
    
    user = db.execute(select(User).where(User.email == user_identifier)).scalars().first()
    if user: return user
    
    return None

@router.post("/solve", response_model=HomeworkResponse)
async def solve_homework(req: HomeworkRequest, db: Session = Depends(get_db)):
    """
    Solve a homework problem with step-by-step solution and hints.
    """
    if not req.problem:
        raise HTTPException(status_code=400, detail="Problem cannot be empty")
    
    # Resolve user
    user = resolve_user(db, req.user_id)
    if not user:
        from backend.core.security import hash_password
        user = User(email="student_demo@example.com", hashed_password=hash_password("demo"), role="student")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Retrieve context from uploaded materials
    results = query_knowledge_base(req.problem, k=3)
    context_text = "\n\n".join([f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}" for doc in results])
    
    if not context_text:
        context_text = "No relevant documents found. I'll provide general guidance."
    
    # Generate step-by-step solution with hints using OpenAI
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        import os
        import json
        
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(status_code=500, detail="Groq API key not configured. Get one free at https://console.groq.com")
        
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
        
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful AI Tutor. A student needs help with the following problem:
        
        Problem: {problem}
        
        Context from course materials:
        {context}
        
        Provide a response in JSON format with the following structure:
        {{
            "hints": ["hint1", "hint2", "hint3"],
            "solution": "full step-by-step solution"
        }}
        
        Instructions:
        1. "hints": Provide 3 progressive hints. 
           - Hint 1: A small nudge or question to get them started.
           - Hint 2: A more specific clue about the method or concept.
           - Hint 3: A strong clue that almost reveals the next step.
           - Do NOT reveal the final answer in the hints.
        
        2. "solution": Provide a complete, clear, step-by-step explanation of the solution.
           - Explain the 'why', not just the 'how'.
           - Use the provided context if relevant.
        """)
        
        chain = prompt | llm | StrOutputParser()
        response_text = chain.invoke({"problem": req.problem, "context": context_text})
        
        # Parse JSON response
        try:
            response_data = json.loads(response_text)
            hints = response_data.get("hints", [])
            solution = response_data.get("solution", "")
        except:
            # Fallback if JSON parsing fails
            hints = ["Try breaking down the problem into smaller steps.", "Review the relevant course materials.", "Consider similar examples you've seen before."]
            solution = response_text
        
        # Save session to database
        session = HomeworkSession(
            user_id=user.id,
            problem=req.problem,
            solution=solution,
            hint_count=0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return HomeworkResponse(
            session_id=session.id,
            hints=hints,
            solution=None,  # Don't reveal solution immediately
            hint_count=0
        )
        
    except Exception as e:
        print(f"Homework solve error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating solution: {str(e)}")

@router.post("/hint")
async def get_hint(req: HintRequest, db: Session = Depends(get_db)):
    """
    Get the next hint for a homework session.
    """
    session = db.execute(
        select(HomeworkSession).where(HomeworkSession.id == req.session_id)
    ).scalars().first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Increment hint count
    session.hint_count += 1
    db.commit()
    
    # Return hint based on count
    # In a real implementation, hints would be stored in the session
    # For now, we'll return a generic message
    return {
        "hint_number": session.hint_count,
        "message": f"Hint {session.hint_count} requested. Review the problem carefully."
    }

@router.get("/history")
async def get_homework_history(user_id: str, db: Session = Depends(get_db)):
    """
    Get homework history for a user.
    """
    user = resolve_user(db, user_id)
    if not user:
        return []
    
    sessions = db.execute(
        select(HomeworkSession).where(HomeworkSession.user_id == user.id).order_by(HomeworkSession.timestamp.desc())
    ).scalars().all()
    
    return [
        {
            "id": s.id,
            "problem": s.problem,
            "hint_count": s.hint_count,
            "timestamp": s.timestamp
        }
        for s in sessions
    ]
