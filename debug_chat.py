
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.getcwd())

# Load env
load_dotenv()

try:
    from backend.rag import query_knowledge_base, vector_store
    print("[OK] Imported backend.rag")
except Exception as e:
    import traceback
    with open("error_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Failed to import backend.rag: {e}\n")
        f.write(traceback.format_exc())
    print("[FAIL] See error_log.txt")

try:
    from backend.routers.chat import chat_endpoint, ChatRequest
    print("[OK] Imported backend.routers.chat")
except Exception as e:
    print(f"[FAIL] Failed to import backend.routers.chat: {e}")

from backend.db import get_db
from backend.models import User

# Mock DB session for simplicity or just use a real one if possible
# For this test, we just want to check RAG first.

def test_rag():
    print("--- Testing RAG Retrieval ---")
    if 'query_knowledge_base' not in globals():
        print("[FAIL] query_knowledge_base not imported. Skipping RAG test.")
        return

    try:
        query = "photosynthesis" # Generic query
        results = query_knowledge_base(query, k=3)
        
        if not results:
            print("[WARN] No results found in Vector Store.")
            if 'vector_store' in globals():
                print(f"Collection count: {vector_store._collection.count()}")
        else:
            print(f"[OK] Found {len(results)} documents.")
            for doc in results:
                print(f" - Source: {doc.metadata.get('source')}")
                print(f" - Content Preview: {doc.page_content[:100]}...")
    except Exception as e:
        print(f"[FAIL] RAG Error: {e}")

def test_openai_key():
    print("\n--- Testing OpenAI Key ---")
    key = os.getenv("OPENAI_API_KEY")
    if key:
        print(f"[OK] API Key found: {key[:5]}...{key[-4:]}")
    else:
        print("[FAIL] OPENAI_API_KEY not found in environment.")

if __name__ == "__main__":
    test_openai_key()
    test_rag()
