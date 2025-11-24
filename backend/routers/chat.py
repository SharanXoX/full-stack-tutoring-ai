from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from backend.db import get_db
from backend.models import Message, User
from backend.rag import query_knowledge_base

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: str # For now, we use the string ID from frontend (e.g. "student_demo")
    course_id: Optional[str] = None
    message: str

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True  # Changed from orm_mode for Pydantic v2

# Helper to resolve user_id string to DB ID
def resolve_user(db: Session, user_identifier: str) -> User:
    # Try to find user by email (since our demo uses email-like IDs or just strings)
    # For the demo "student_demo", we might need to create a dummy user or just pick the first student.
    # To keep it simple for this MVP: if user_identifier is "student_demo", we pick the first student user.
    if user_identifier == "student_demo":
        user = db.execute(select(User).where(User.role == "student")).scalars().first()
        if user: return user
    
    # Fallback: try to find by email
    user = db.execute(select(User).where(User.email == user_identifier)).scalars().first()
    if user: return user

    # Fallback: create a temporary user if not exists (for demo purposes)
    # In a real app, you would use `current_user` from auth dependency.
    return None

@router.get("/chat/history", response_model=List[MessageOut])
def get_chat_history(user_id: str, db: Session = Depends(get_db)):
    user = resolve_user(db, user_id)
    if not user:
        return []
    
    messages = db.execute(
        select(Message).where(Message.user_id == user.id).order_by(Message.timestamp)
    ).scalars().all()
    return messages

@router.post("/chat")
async def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    """
    RAG-enabled chat endpoint with persistence and proper LLM integration.
    """
    try:
        if not req.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # 0. Resolve User
        user = resolve_user(db, req.user_id)
        if not user:
            # Create a dummy student for the demo if missing
            from backend.core.security import hash_password
            user = User(email="student_demo@example.com", hashed_password=hash_password("demo"), role="student")
            db.add(user)
            db.commit()
            db.refresh(user)

        # 1. Save User Message
        user_msg = Message(user_id=user.id, role="user", content=req.message)
        db.add(user_msg)
        db.commit()
        
        # 2. Retrieve relevant context
        results = query_knowledge_base(req.message, k=3)
        
        # Format context
        context_text = "\n\n".join([doc.page_content for doc in results])
        
        # 3. Generate Answer with OpenAI
        answer_text = ""
        
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        import os
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            answer_text = "⚠️ Groq API key not configured. Please set GROQ_API_KEY in the .env file. Get one free at https://console.groq.com"
        else:
            llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7, api_key=api_key)
            
            # If we have context from documents, use it
            if context_text and len(context_text.strip()) > 0:
                prompt = ChatPromptTemplate.from_template("""
You are a helpful, friendly AI Tutor. Your goal is to help the student understand the material, not just give them the answer.

Context from uploaded course materials:
{context}

Student's Question:
{question}

Instructions:
1. Use the provided context to answer the question.
2. If the context is relevant, explain the concept clearly using examples from the text.
3. If the context is NOT relevant, use your general knowledge but explicitly state: "I couldn't find this in your uploaded notes, but here is a general explanation..."
4. Be encouraging and concise.
5. Do not make up facts if they are not in the context or your general knowledge.

Your helpful answer:
""")
                chain = prompt | llm | StrOutputParser()
                answer_text = chain.invoke({"context": context_text, "question": req.message})
            else:
                # No documents uploaded yet, use general knowledge
                prompt = ChatPromptTemplate.from_template("""
You are a helpful, friendly AI Tutor. The student has asked a question, but no course materials have been uploaded yet.

Provide a helpful, educational answer using your general knowledge. Be clear, conversational, and break down complex topics.

At the end, mention: "💡 Tip: For answers specific to your course, ask your teacher to upload course materials!"

Student's Question:
{question}

Your helpful answer:
""")
                chain = prompt | llm | StrOutputParser()
                answer_text = chain.invoke({"question": req.message})

        # 4. Save AI Message
        ai_msg = Message(user_id=user.id, role="ai", content=answer_text)
        db.add(ai_msg)
        db.commit()
        
        return {"answer": answer_text}

    except Exception as e:
        import traceback
        with open("backend_error.log", "w", encoding="utf-8") as f:
            f.write(f"Error in chat_endpoint: {e}\n")
            f.write(traceback.format_exc())
        print(f"Error in chat_endpoint: {e}")
        
        # Check if it's an OpenAI quota error
        error_str = str(e)
        if "insufficient_quota" in error_str or "rate_limit" in error_str.lower():
            raise HTTPException(
                status_code=503,
                detail="⚠️ OpenAI API quota exceeded. Please add credits to your OpenAI account at https://platform.openai.com/account/billing"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
