from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from backend.db import get_db
from backend.models import QuizAttempt, QuizQuestion, User
from backend.rag import query_knowledge_base

router = APIRouter(prefix="/api/exam", tags=["exam"])

class QuizGenerateRequest(BaseModel):
    user_id: Optional[str] = "student_demo"
    topic: Optional[str] = None
    file_id: Optional[str] = None
    num_questions: Optional[int] = 5

class QuizSubmitRequest(BaseModel):
    user_id: str
    quiz_id: int
    answers: List[dict]  # [{"question_id": 1, "answer": "..."}]

class QuestionOut(BaseModel):
    id: int
    type: Optional[str] = "MCQ"  # MCQ or True/False
    question: str
    options: Optional[List[str]] = None  # For multiple choice
    explanation: Optional[str] = None  # For showing after submission

class QuizOut(BaseModel):
    quiz_id: int
    quiz_title: Optional[str] = "Quiz"
    questions: List[QuestionOut]
    total_questions: int

# Helper to resolve user_id
def resolve_user(db: Session, user_identifier: str) -> User:
    if user_identifier == "student_demo":
        user = db.execute(select(User).where(User.role == "student")).scalars().first()
        if user: return user
    
    user = db.execute(select(User).where(User.email == user_identifier)).scalars().first()
    if user: return user
    
    return None

@router.post("/generate", response_model=QuizOut)
async def generate_quiz(req: QuizGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate an adaptive quiz from uploaded materials.
    Tries to generate 20 questions, falls back to 15 or 10 if content insufficient.
    """
    # Resolve user
    user = resolve_user(db, req.user_id)
    if not user:
        from backend.core.security import hash_password
        user = User(email="student_demo@example.com", hashed_password=hash_password("demo"), role="student")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Retrieve content - filter by file_id if provided
    topic_query = req.topic if req.topic else "quiz questions"
    
    # If file_id is provided, filter results by source metadata
    if req.file_id:
        results = query_knowledge_base(topic_query, k=15, filter={"source": req.file_id})
        if not results:
            # Fallback: try without filter if no results
            results = query_knowledge_base(topic_query, k=15)
    else:
        results = query_knowledge_base(topic_query, k=15)
    
    context_text = "\n\n".join([doc.page_content for doc in results])
    
    if not context_text:
        raise HTTPException(status_code=400, detail="No content available to generate quiz. Please upload course materials first.")
    
    # Use requested number of questions or calculate based on content length
    if req.num_questions:
        target_questions = req.num_questions
    else:
        content_length = len(context_text)
        if content_length > 5000:
            target_questions = 20
        elif content_length > 2500:
            target_questions = 15
        else:
            target_questions = 10
    
    # Generate quiz using OpenAI
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        import os
        import json
        
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(status_code=500, detail="Groq API key not configured. Get one free at https://console.groq.com")
        
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5)
        
        prompt = ChatPromptTemplate.from_template("""
You are Antigravity, an Expert AI Tutor and Adaptive Learning System running on Groq LLM infrastructure.

CRITICAL RULE: All quiz content MUST be based EXCLUSIVELY on the provided document text. DO NOT introduce outside information.

CRITICAL RULE 2 (JSON Fix): Your output MUST be a single, valid JSON object. DO NOT include any surrounding markdown markers like ```json or ```. Output ONLY the JSON object itself.

TASK: Stage 2 - Quiz Generation

Generate exactly {num_questions} quiz questions based on the following document content:

DOCUMENT CONTENT:
{context}

REQUIREMENTS:

1. **Question Count**: Generate EXACTLY {num_questions} questions.

2. **Question Types**: Use a mix of Multiple Choice (MCQ) and True/False questions.

3. **Source Verification**: ALL questions and options must be verifiable within the provided document text.

4. **Schema Compliance**: Follow this EXACT structure:

{{
  "quiz_title": "Assessment on [Primary Topic from Document]",
  "questions": [
    {{
      "id": 1,
      "type": "MCQ",
      "question": "Question text based on document content",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer_key": "Option A",
      "explanation": "Brief explanation referencing the document text"
    }},
    {{
      "id": 2,
      "type": "True/False",
      "question": "Statement to evaluate as true or false",
      "options": ["True", "False"],
      "answer_key": "True",
      "explanation": "Brief explanation referencing the document text"
    }}
  ]
}}

CRITICAL OUTPUT INSTRUCTION:
- Output ONLY the JSON object
- NO markdown code blocks (no ```json or ```)
- NO additional text before or after the JSON
- Start directly with {{ and end directly with }}
""")
        
        chain = prompt | llm | StrOutputParser()
        response_text = chain.invoke({"num_questions": target_questions, "context": context_text[:8000]})
        
        # CRITICAL: Clean up response - remove markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON response
        try:
            response_data = json.loads(response_text)
            questions_data = response_data.get("questions", [])
        except json.JSONDecodeError as e:
            # Try to extract JSON if there's extra text
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    response_data = json.loads(response_text[start:end])
                    questions_data = response_data.get("questions", [])
                except:
                    raise HTTPException(status_code=500, detail=f"Failed to parse quiz questions: {str(e)}")
            else:
                raise HTTPException(status_code=500, detail=f"Failed to parse quiz questions: {str(e)}")
        
        # Create quiz attempt
        quiz_attempt = QuizAttempt(
            user_id=user.id,
            score=0.0,  # Will be updated when submitted
            total_questions=len(questions_data)
        )
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)
        
        # Create quiz questions and store in database
        question_objects = []
        for idx, q_data in enumerate(questions_data):
            # Use answer_key from new schema, fallback to correct_answer for backwards compatibility
            correct_ans = q_data.get("answer_key") or q_data.get("correct_answer", "")
            
            question = QuizQuestion(
                quiz_attempt_id=quiz_attempt.id,
                question=q_data.get("question", ""),
                correct_answer=correct_ans,  # Store in DB
                user_answer=None,
                is_correct=False
            )
            db.add(question)
            
            # Prepare response for frontend
            question_objects.append({
                "id": q_data.get("id", idx + 1),  # Use id from response or fallback to index
                "type": q_data.get("type", "MCQ"),
                "question": q_data.get("question", ""),
                "options": q_data.get("options", []),
                "explanation": q_data.get("explanation", "")  # Include for later display
            })
        
        db.commit()
        
        # Get quiz title from response, fallback to topic
        quiz_title = response_data.get("quiz_title", f"Assessment on {topic_query}")
        
        return QuizOut(
            quiz_id=quiz_attempt.id,
            quiz_title=quiz_title,
            questions=[QuestionOut(**q) for q in question_objects],
            total_questions=len(questions_data)
        )
        
    except Exception as e:
        print(f"Quiz generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.post("/submit")
async def submit_quiz(req: QuizSubmitRequest, db: Session = Depends(get_db)):
    """
    Submit quiz answers and calculate score.
    """
    # Get quiz attempt
    quiz_attempt = db.execute(
        select(QuizAttempt).where(QuizAttempt.id == req.quiz_id)
    ).scalars().first()
    
    if not quiz_attempt:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get all questions for this quiz
    questions = db.execute(
        select(QuizQuestion).where(QuizQuestion.quiz_attempt_id == req.quiz_id)
    ).scalars().all()
    
    # Update answers and check correctness
    correct_count = 0
    for answer_data in req.answers:
        question_idx = answer_data.get("question_id", 0) - 1  # Convert to 0-indexed
        if question_idx < len(questions):
            question = questions[question_idx]
            user_answer = answer_data.get("answer", "")
            question.user_answer = user_answer
            
            # Check if answer is correct (case-insensitive)
            if user_answer.strip().lower() == question.correct_answer.strip().lower():
                question.is_correct = True
                correct_count += 1
    
    # Calculate score
    score = (correct_count / len(questions)) * 100 if questions else 0
    quiz_attempt.score = score
    
    db.commit()
    
    # Automatically update user's performance level
    user = db.execute(select(User).where(User.id == quiz_attempt.user_id)).scalars().first()
    if user:
        # Calculate new average score
        all_attempts = db.execute(
            select(QuizAttempt).where(QuizAttempt.user_id == user.id)
        ).scalars().all()
        
        avg_score = sum(a.score for a in all_attempts) / len(all_attempts)
        user.avg_quiz_score = avg_score
        
        # Update performance level
        if avg_score < 60:
            user.performance_level = "struggling"
        elif avg_score <= 80:
            user.performance_level = "average"
        else:
            user.performance_level = "advanced"
        
        db.commit()
        
        # Generate adaptive recommendations
        if user.performance_level == "struggling":
            recommendations = [
                "Don't worry! Let's review the basics together.",
                "I'll provide simpler explanations and more examples.",
                "Try the Homework Help for step-by-step guidance."
            ]
        elif user.performance_level == "average":
            recommendations = [
                "Good progress! Keep practicing at this pace.",
                "Review topics where you scored below 70%.",
                "Try mixing in some challenging problems."
            ]
        else:
            recommendations = [
                "Excellent work! You're ready for advanced topics.",
                "Explore deeper concepts and applications.",
                "Challenge yourself with complex problems."
            ]
        
        return {
            "quiz_id": quiz_attempt.id,
            "score": score,
            "correct_answers": correct_count,
            "total_questions": len(questions),
            "percentage": f"{score:.1f}%",
            "performance_level": user.performance_level,
            "avg_score": user.avg_quiz_score,
            "recommendations": recommendations
        }
    
    return {
        "quiz_id": quiz_attempt.id,
        "score": score,
        "correct_answers": correct_count,
        "total_questions": len(questions),
        "percentage": f"{score:.1f}%"
    }

@router.get("/history")
async def get_quiz_history(user_id: str, db: Session = Depends(get_db)):
    """
    Get quiz history for a user.
    """
    user = resolve_user(db, user_id)
    if not user:
        return []
    
    attempts = db.execute(
        select(QuizAttempt).where(QuizAttempt.user_id == user.id).order_by(QuizAttempt.timestamp.desc())
    ).scalars().all()
    
    return [
        {
            "id": a.id,
            "score": a.score,
            "total_questions": a.total_questions,
            "percentage": f"{a.score:.1f}%",
            "timestamp": a.timestamp
        }
        for a in attempts
    ]
