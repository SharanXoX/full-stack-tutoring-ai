from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime

from backend.db import get_db
from backend.models import User, QuizAttempt
from backend.rag import query_knowledge_base

router = APIRouter(prefix="/api/learning", tags=["adaptive_learning"])

class LearningRecommendation(BaseModel):
    performance_level: str
    avg_score: float
    recommendations: List[str]
    next_topics: List[str]

class LessonRequest(BaseModel):
    user_id: str
    topic: Optional[str] = None

# Helper to resolve user_id
def resolve_user(db: Session, user_identifier: str) -> User:
    if user_identifier == "student_demo":
        user = db.execute(select(User).where(User.role == "student")).scalars().first()
        if user: return user
    
    user = db.execute(select(User).where(User.email == user_identifier)).scalars().first()
    if user: return user
    
    return None

def calculate_performance_level(avg_score: float) -> str:
    """Determine performance level based on average quiz score."""
    if avg_score < 60:
        return "struggling"
    elif avg_score <= 80:
        return "average"
    else:
        return "advanced"

def update_user_performance(db: Session, user: User):
    """Calculate and update user's performance level based on quiz history."""
    # Get all quiz attempts for this user
    attempts = db.execute(
        select(QuizAttempt).where(QuizAttempt.user_id == user.id)
    ).scalars().all()
    
    if not attempts:
        user.performance_level = "average"
        user.avg_quiz_score = 0.0
        return
    
    # Calculate average score
    avg_score = sum(a.score for a in attempts) / len(attempts)
    user.avg_quiz_score = avg_score
    user.performance_level = calculate_performance_level(avg_score)
    
    db.commit()

@router.get("/recommendations/{user_id}", response_model=LearningRecommendation)
async def get_recommendations(user_id: str, db: Session = Depends(get_db)):
    """
    Get personalized learning recommendations based on quiz performance.
    """
    user = resolve_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update performance level
    update_user_performance(db, user)
    
    # Generate recommendations based on performance level
    level = user.performance_level
    avg_score = user.avg_quiz_score
    
    if level == "struggling":
        recommendations = [
            "Review fundamental concepts with simplified explanations",
            "Practice with easier problems to build confidence",
            "Request step-by-step guidance in Homework Help",
            "Take shorter quizzes to focus on specific topics"
        ]
        next_topics = [
            "Basic concepts review",
            "Foundational principles",
            "Simple practice problems"
        ]
    elif level == "average":
        recommendations = [
            "Continue with current pace and difficulty",
            "Try mixed difficulty practice problems",
            "Review topics where you scored below 70%",
            "Challenge yourself with occasional harder questions"
        ]
        next_topics = [
            "Standard course progression",
            "Balanced practice",
            "Topic reinforcement"
        ]
    else:  # advanced
        recommendations = [
            "Explore advanced topics and applications",
            "Try challenging problems and edge cases",
            "Study theoretical foundations in depth",
            "Connect concepts across different topics"
        ]
        next_topics = [
            "Advanced applications",
            "Complex problem solving",
            "Theoretical deep dives"
        ]
    
    return LearningRecommendation(
        performance_level=level,
        avg_score=avg_score,
        recommendations=recommendations,
        next_topics=next_topics
    )

@router.post("/lesson")
async def generate_adaptive_lesson(req: LessonRequest, db: Session = Depends(get_db)):
    """
    Generate an adaptive lesson based on student's performance level.
    Content is derived from uploaded PDFs.
    """
    user = resolve_user(db, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update performance level
    update_user_performance(db, user)
    
    # Get relevant content from uploaded materials
    topic = req.topic if req.topic else "general course content"
    results = query_knowledge_base(topic, k=5)
    
    if not results:
        raise HTTPException(status_code=400, detail="No course materials found. Please upload PDFs first.")
    
    context_text = "\n\n".join([doc.page_content for doc in results])
    
    # Generate adaptive lesson using OpenAI
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        import os
        
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(status_code=500, detail="Groq API key not configured. Get one free at https://console.groq.com")
        
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
        
        # Customize prompt based on performance level
        level = user.performance_level
        
        if level == "struggling":
            teaching_style = """
            Use SIMPLE, CLEAR language. Break down concepts into small, digestible steps.
            Provide MANY examples and analogies. Avoid jargon. Be encouraging and patient.
            Focus on building foundational understanding before moving to complex ideas.
            """
        elif level == "average":
            teaching_style = """
            Use standard academic language. Provide balanced explanations with examples.
            Progress at a moderate pace. Include some challenging elements to encourage growth.
            """
        else:  # advanced
            teaching_style = """
            Use advanced terminology and concepts. Dive deep into theoretical foundations.
            Present challenging problems and edge cases. Make connections to related advanced topics.
            Encourage critical thinking and independent exploration.
            """
        
        prompt = ChatPromptTemplate.from_template("""
        You are an AI Tutor teaching a {performance_level} student about: {topic}
        
        Teaching Style Instructions:
        {teaching_style}
        
        Course Material:
        {context}
        
        Create a comprehensive lesson that:
        1. Introduces the topic appropriately for this student's level.
        2. Explains key concepts using the course material.
        3. Provides examples relevant to their understanding.
        4. Includes practice questions at the right difficulty.
        5. Summarizes main takeaways.
        
        Format the lesson in a clear, structured way using Markdown (headers, bullet points, bold text).
        Make it engaging and interactive.
        """)
        
        chain = prompt | llm | StrOutputParser()
        lesson = chain.invoke({
            "performance_level": level,
            "topic": topic,
            "teaching_style": teaching_style,
            "context": context_text
        })
        
        return {
            "performance_level": level,
            "topic": topic,
            "lesson": lesson,
            "avg_score": user.avg_quiz_score
        }
        
    except Exception as e:
        print(f"Adaptive lesson error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating lesson: {str(e)}")
