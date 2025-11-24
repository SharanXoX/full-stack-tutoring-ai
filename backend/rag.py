import os
import chromadb
from chromadb.config import Settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

# --- Configuration ---
# Persist ChromaDB in the project root/chroma_db
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DB_DIR = os.path.join(PROJECT_ROOT, "chroma_db")

# Initialize Embeddings (using local CPU-friendly model)
# This downloads the model once and caches it.
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Vector Store
# We use a simple persistent client
vector_store = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embedding_function,
    collection_name="ai_tutor_knowledge"
)

def ingest_document(file_path: str, text_content: str):
    """
    Splits text into chunks and adds them to the vector store.
    """
    if not text_content:
        return 0

    # 1. Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(text_content)

    # 2. Create Document objects with metadata
    filename = os.path.basename(file_path)
    docs = [
        Document(page_content=t, metadata={"source": filename})
        for t in texts
    ]

    # 3. Add to ChromaDB
    if docs:
        vector_store.add_documents(docs)
        # vector_store.persist() # In newer Chroma versions, persist is automatic or not needed like this, but good to know.
    
    return len(docs)

def query_knowledge_base(query: str, k: int = 3, filter: dict = None):
    """
    Retrieves the top-k most relevant chunks for the query.
    """
    results = vector_store.similarity_search(query, k=k, filter=filter)
    return results

def summarize_text(text: str, max_length: int = 500):
    """
    Summarizes raw text using Groq LLM following Antigravity AI Tutor Stage 1 specifications.
    Returns a dict with {"summary": str, "key_points": List[str], "topic": str}
    Adapts summary length based on content size.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, api_key=api_key)
    
    # Adaptive summary length based on text size
    text_word_count = len(text.split())
    
    if text_word_count < 100:
        target_words = "50-100"
        target_points = "2-3"
    elif text_word_count < 500:
        target_words = "100-200"
        target_points = "3-4"
    elif text_word_count < 2000:
        target_words = "200-350"
        target_points = "4-5"
    else:
        target_words = "400-600"
        target_points = "5-7"
    
    prompt = ChatPromptTemplate.from_template("""
You are Antigravity, an Expert AI Tutor and Adaptive Learning System running on Groq LLM infrastructure.

CRITICAL RULE: All generated content MUST be based EXCLUSIVELY on the provided document text. DO NOT introduce outside information.

TASK: Stage 1 - Summarization and Flow Initiation

Analyze the following document content and generate a professional instructional summary.

DOCUMENT TEXT:
{text}

REQUIREMENTS:

1. **Summary Quality**: Generate a professionally written summary.
   - **Length**: The summary should be approximately **{target_words} words** (adapt to content length).
   - **Depth**: Explain the main concepts clearly and comprehensively.
   - **Structure**: Use paragraphs to organize information logically.

2. **Importance Criteria for Key Points**:
   - Frequency of mention in the document
   - Centrality to the document's overall purpose
   - Explicit definitions or principles stated

3. **Key Points**: Extract {target_points} most important, foundational concepts based on the criteria above.

4. **Topic Identification**: Determine the single primary topic/subject of the document.

OUTPUT FORMAT (valid JSON only):
{{
    "topic": "Single Primary Topic Name",
    "summary": "A professional summary ({target_words} words approximately). Well-structured with clear explanations.",
    "key_points": [
        "First key concept...",
        "Second key concept..."
    ]
}}

CRITICAL: Respond with ONLY valid JSON. No markdown, no code blocks, no extra text. Just the JSON object.
""")
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({"text": text[:25000], "target_words": target_words, "target_points": target_points})
        
        # Clean up response - remove markdown code blocks if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        # Parse JSON
        try:
            result = json.loads(response)
            return {
                "summary": result.get("summary", ""),
                "key_points": result.get("key_points", []),
                "topic": result.get("topic", "Document Summary")
            }
        except json.JSONDecodeError as json_err:
            print(f"JSON parse error: {json_err}")
            # Fallback: try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    result = json.loads(response[start:end])
                    return {
                        "summary": result.get("summary", ""),
                        "key_points": result.get("key_points", []),
                        "topic": result.get("topic", "Document Summary")
                    }
                except:
                    pass
            
            # Ultimate fallback: return the text as-is with basic formatting
            print(f"Creating fallback summary from raw response")
            return {
                "summary": text[:500] + "..." if len(text) > 500 else text,
                "key_points": ["Main content extracted from document"],
                "topic": "Document Summary"
            }
    except Exception as e:
        print(f"Summarize text error: {e}")
        # Log the raw response if available for debugging
        if 'response' in locals():
             print(f"Raw response was: {response[:200]}")
        
        # Graceful fallback: return a basic summary from the text itself
        return {
            "summary": text[:500] + "..." if len(text) > 500 else text,
            "key_points": ["Content from uploaded document"],
            "topic": "Document Analysis"
        }

def summarize_document(file_id: str, max_length: int = 500):
    """
    Summarizes a document by retrieving its chunks from ChromaDB.
    """
    # Retrieve more chunks for comprehensive summary
    results = query_knowledge_base("What is the main content of this document?", k=40, filter={"source": file_id})
    
    if not results:
        return {"summary": "No content found for this file.", "key_points": []}
    
    combined_text = "\n\n".join([doc.page_content for doc in results])
    return summarize_text(combined_text, max_length)
