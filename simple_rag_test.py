import requests

# Test 1: Upload document
print("=" * 60)
print("TEST 1: Uploading Document")
print("=" * 60)

url = "http://127.0.0.1:8000/api/content/upload"
file_path = "test_photosynthesis.txt"

with open(file_path, "rb") as f:
    files = {"file": f}
    data = {"user_id": "student_demo", "user_role": "student"}
    response = requests.post(url, files=files, data=data)
    
print(f"✓ Upload Status: {response.status_code}")
print(f"✓ Response: {response.json()}\n")

# Test 2: Ask question about uploaded content
print("=" * 60)
print("TEST 2: Testing RAG Retrieval")
print("=" * 60)

chat_url = "http://127.0.0.1:8000/api/chat"
question = "What are the two main stages of photosynthesis according to my notes?"

payload = {"user_id": "student_demo", "message": question}
response = requests.post(chat_url, json=payload)

print(f"Question: {question}")
print(f"Status: {response.status_code}")
print(f"\nAI Answer:\n{response.json()['answer']}\n")

print("=" * 60)
print("✓ RAG Test Complete!")
print("=" * 60)
