# Instructions to use Groq (FREE alternative)

## 1. Get Groq API Key
- Go to: https://console.groq.com
- Sign up (free)
- Get your API key from the dashboard

## 2. Update your .env file
Replace:
OPENAI_API_KEY=your_key_here

With:
GROQ_API_KEY=your_groq_key_here

## 3. Update chat.py, homework.py, adaptive_learning.py, exam.py
Replace this line:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)

With:
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7, api_key=api_key)

## 4. Install Groq package
Run: pip install langchain-groq
