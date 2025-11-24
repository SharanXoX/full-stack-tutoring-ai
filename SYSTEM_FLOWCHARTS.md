# ANTIGRAVITY SYSTEM - DETAILED FLOWCHARTS

## 1. OVERALL SYSTEM FLOWCHART

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ANTIGRAVITY SYSTEM                           │
│                    Complete Learning Pipeline Flow                   │
└─────────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ▼
                    ┌───────────────────────┐
                    │   User Login/Access   │
                    │   (Student Portal)    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Upload Document      │
                    │  (PDF/DOCX/PPTX/TXT)  │
                    └───────────┬───────────┘
                                │
                                ▼
        ═══════════════════════════════════════════════════
                        STAGE 1: SUMMARIZATION
        ═══════════════════════════════════════════════════
                                │
                    ┌───────────▼───────────┐
                    │  Document Validation  │
                    │  - Format check       │
                    │  - Size validation    │
                    └───────────┬───────────┘
                                │
                        ┌───────┴───────┐
                        │   Valid?      │
                        └───┬───────┬───┘
                    NO      │       │      YES
                    ────────┘       └─────────
                    │                         │
            ┌───────▼────────┐               │
            │ Error Message  │               │
            │ Return to      │               │
            │ Upload         │               │
            └────────────────┘               │
                                             ▼
                                ┌────────────────────────┐
                                │  Text Extraction       │
                                │  - PyPDF2 (PDF)        │
                                │  - python-docx (DOCX)  │
                                │  - python-pptx (PPTX)  │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Text Chunking         │
                                │  Chunk Size: 1000 chars│
                                │  Overlap: 200 chars    │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Embedding Generation  │
                                │  Model: MiniLM-L6-v2   │
                                │  Dimension: 384        │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Vector Storage        │
                                │  ChromaDB with         │
                                │  Metadata (file_id)    │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Similarity Search     │
                                │  Top-k=20 chunks       │
                                │  Filter by file_id     │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  LLM Summarization     │
                                │  Groq llama-3.1-8b     │
                                │  Temp: 0.3             │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  JSON Parsing          │
                                │  Extract: topic,       │
                                │  summary, key_points   │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Display Summary       │
                                │  Professional Card UI  │
                                │  3-5 Key Concepts      │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                    "Take Quiz" Button
                                             │
        ═══════════════════════════════════════════════════
                    STAGE 2: QUIZ GENERATION
        ═══════════════════════════════════════════════════
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  User Clicks           │
                                │  "Take Quiz"           │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Navigate to           │
                                │  Exam Prep Page        │
                                │  Topic auto-filled     │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  User Clicks           │
                                │  "Generate Quiz"       │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Filtered Retrieval    │
                                │  k=15, filter=file_id  │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Context Aggregation   │
                                │  Max 8000 chars        │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  LLM Quiz Generation   │
                                │  Groq llama-3.1-8b     │
                                │  Temp: 0.5             │
                                │  Output: 5 questions   │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  JSON Cleaning         │
                                │  Remove markdown ```   │
                                └────────────┬───────────┘
                                             │
                                             ▼
                                ┌────────────────────────┐
                                │  Schema Validation     │
                                │  Verify: quiz_title,   │
                                │  questions[], id, type │
                                └────────────┬───────────┘
                                             │
                        ┌────────────────────┴────────┐
                        │   Valid Schema?             │
                        └────┬──────────────────┬─────┘
                    NO       │                  │      YES
                    ─────────┘                  └──────────
                    │                                      │
            ┌───────▼────────┐                            │
            │ Parse Error    │                            │
            │ Display Error  │                            │
            │ to User        │                            │
            └────────────────┘                            │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Store Quiz in DB       │
                                            │  - quiz_attempts table  │
                                            │  - quiz_questions table │
                                            └─────────────┬───────────┘
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Display Interactive    │
                                            │  Quiz Interface         │
                                            │  - Radio buttons        │
                                            │  - 5 questions          │
                                            └─────────────┬───────────┘
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Student Selects        │
                                            │  Answers                │
                                            └─────────────┬───────────┘
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  User Clicks            │
                                            │  "Submit Quiz"          │
                                            └─────────────┬───────────┘
                                                          │
        ═══════════════════════════════════════════════════
                STAGE 3: ADAPTIVE LEARNING
        ═══════════════════════════════════════════════════
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Retrieve Stored        │
                                            │  Questions from DB      │
                                            └─────────────┬───────────┘
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Compare Answers        │
                                            │  User vs Correct        │
                                            │  (Case-insensitive)     │
                                            └─────────────┬───────────┘
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Calculate Score        │
                                            │  (correct/total) × 100  │
                                            └─────────────┬───────────┘
                                                          │
                                        ┌─────────────────┼────────────────┐
                                        │                 │                │
                                        ▼                 ▼                ▼
                            ┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
                            │  Score ≥ 80%    │ │ 60% ≤ S <80% │ │  Score < 60% │
                            │  ADVANCED       │ │  AVERAGE     │ │  STRUGGLING  │
                            └────────┬────────┘ └──────┬───────┘ └──────┬───────┘
                                     │                 │                │
                                     ▼                 ▼                ▼
                    ┌────────────────────────┐ ┌─────────────────┐ ┌──────────────────┐
                    │ Recommendations:       │ │ Recommendations:│ │ Recommendations: │
                    │ - Advanced topics      │ │ - Reinforce     │ │ - Foundational   │
                    │ - Deep connections     │ │ - Core concepts │ │ - Step-by-step   │
                    │ - Complex problems     │ │ - Practice more │ │ - Basic review   │
                    └────────────┬───────────┘ └────────┬────────┘ └────────┬─────────┘
                                 │                      │                   │
                                 └──────────────────────┼───────────────────┘
                                                        │
                                                        ▼
                                            ┌─────────────────────────┐
                                            │  Update User Profile    │
                                            │  - Performance level    │
                                            │  - Average score        │
                                            └─────────────┬───────────┘
                                                          │
                                                          ▼
                                            ┌─────────────────────────┐
                                            │  Display Results        │
                                            │  - Score card           │
                                            │  - Badge                │
                                            │  - Recommendations      │
                                            └─────────────┬───────────┘
                                                          │
                                        ┌─────────────────┴─────────────────┐
                                        │                                   │
                                        ▼                                   ▼
                            ┌───────────────────────┐        ┌──────────────────────┐
                            │  "Take Another Quiz"  │        │ "View Adaptive       │
                            │  Button               │        │  Lessons" Button     │
                            └───────────┬───────────┘        └──────────┬───────────┘
                                        │                               │
                                        ▼                               ▼
                            ┌───────────────────────┐        ┌──────────────────────┐
                            │  Return to            │        │  Navigate to         │
                            │  Quiz Generation      │        │  Adaptive Learning   │
                            └───────────────────────┘        │  Page                │
                                                             └──────────────────────┘
                                                                       │
                                                                       ▼
                                                                      END
```

---

## 2. DOCUMENT PROCESSING FLOWCHART (DETAILED)

```
                          DOCUMENT UPLOAD
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Receive File Upload  │
                    │  FormData from Client │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────────────┐
                    │  Validate File                │
                    │  - Check extension            │
                    │  - Check file size (< 50MB)   │
                    └───────────┬───────────────────┘
                                │
                        ┌───────┴───────┐
                   Valid│               │Invalid
                        ▼               ▼
            ┌──────────────────┐   ┌──────────────┐
            │ Generate File ID │   │ Return Error │
            │ timestamp_uuid   │   │ 400 Response │
            └────────┬─────────┘   └──────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Save to File System        │
        │ Path: uploads/{user_id}/   │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Determine File Type        │
        └────┬────┬────┬────┬────────┘
             │    │    │    │
     ┌───────┘    │    │    └───────┐
     │            │    │            │
     ▼            ▼    ▼            ▼
┌─────────┐  ┌──────┐ ┌──────┐  ┌─────┐
│  .pdf   │  │.docx │ │.pptx │  │.txt │
└────┬────┘  └──┬───┘ └──┬───┘  └──┬──┘
     │          │        │         │
     ▼          ▼        ▼         ▼
┌─────────┐  ┌──────┐ ┌──────┐  ┌─────┐
│ PyPDF2  │  │docx  │ │pptx  │  │ open│
│.extract │  │.text │ │.text │  │.read│
└────┬────┘  └──┬───┘ └──┬───┘  └──┬──┘
     │          │        │         │
     └──────────┴────────┴─────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  Combined Text Content     │
    └────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  Text Chunking             │
    │  RecursiveCharacterSplitter│
    │  - chunk_size: 1000        │
    │  - chunk_overlap: 200      │
    └────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  For Each Chunk:           │
    │  1. Generate Embedding     │
    │     (HuggingFace MiniLM)   │
    │  2. Create Metadata        │
    │     {source: file_id,      │
    │      page: n, chunk: i}    │
    └────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  Store in ChromaDB         │
    │  - Vector: 384-dim         │
    │  - Metadata: dict          │
    │  - Text: chunk             │
    └────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  Return Response           │
    │  {file_id, title, size}    │
    └────────────────────────────┘
```

---

## 3. QUIZ GENERATION FLOWCHART (DETAILED)

```
                    QUIZ GENERATION REQUEST
                    {topic, file_id, num_q}
                            │
                            ▼
                ┌───────────────────────┐
                │  Validate Inputs      │
                │  - Check topic        │
                │  - Verify file_id     │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Retrieve Document Chunks │
                │  query_knowledge_base()   │
                │  - Query: topic           │
                │  - k: 15                  │
                │  - Filter: {source: f_id} │
                └───────────┬───────────────┘
                            │
                    ┌───────┴────────┐
               Found│                │Not Found
                    ▼                ▼
        ┌───────────────────┐  ┌──────────────┐
        │ Aggregate Context │  │ Retry        │
        │ Top 15 chunks     │  │ Without      │
        │ Max 8000 chars    │  │ Filter       │
        └────────┬──────────┘  └──────┬───────┘
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Construct LLM Prompt     │
                │  - System: "Antigravity"  │
                │  - Task: Generate Quiz    │
                │  - Context: aggregated    │
                │  - Schema: JSON strict    │
                │  - Num questions: 5       │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Call Groq LLM            │
                │  Model: llama-3.1-8b      │
                │  Temperature: 0.5         │
                │  Max tokens: 2000         │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Receive LLM Response     │
                │  (Raw text)               │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Clean Response           │
                │  1. Strip whitespace      │
                │  2. Remove ```json        │
                │  3. Remove ```            │
                │  4. Trim                  │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Parse JSON               │
                └───────────┬───────────────┘
                            │
                    ┌───────┴────────┐
              Valid │                │ Invalid
                    ▼                ▼
        ┌───────────────────┐  ┌──────────────────┐
        │ Extract Questions │  │ JSON Fallback    │
        │ Array             │  │ Extract between  │
        └────────┬──────────┘  │ first { and last}│
                 │              └──────┬───────────┘
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Create Quiz Attempt      │
                │  DB: quiz_attempts table  │
                │  - user_id                │
                │  - score: 0.0             │
                │  - total_q: len(questions)│
                │  - timestamp              │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  For Each Question:       │
                │  Store in DB              │
                │  quiz_questions table     │
                │  - quiz_attempt_id        │
                │  - question text          │
                │  - correct_answer         │
                │  - user_answer: NULL      │
                │  - is_correct: FALSE      │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Prepare Response         │
                │  {quiz_id, quiz_title,    │
                │   questions[], total_q}   │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │  Return to Frontend       │
                │  Display Interactive Quiz │
                └───────────────────────────┘
```

---

## 4. ADAPTIVE LEARNING FLOWCHART (DETAILED)

```
                    QUIZ SUBMISSION
              {quiz_id, user_id, answers[]}
                        │
                        ▼
            ┌───────────────────────────┐
            │  Retrieve Quiz Attempt    │
            │  FROM quiz_attempts       │
            │  WHERE id = quiz_id       │
            └───────────┬───────────────┘
                        │
                ┌───────┴────────┐
           Found│                │Not Found
                ▼                ▼
    ┌──────────────────┐   ┌──────────────┐
    │Get All Questions │   │Return Error  │
    │FROM quiz_questions│   │404 Not Found │
    │WHERE quiz_id     │   └──────────────┘
    └────────┬─────────┘
             │
             ▼
    ┌────────────────────────────┐
    │  Initialize Counters       │
    │  correct_count = 0         │
    │  total_questions = len(q)  │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │  For Each Answer:          │
    │  1. Get question index     │
    │  2. Get user answer        │
    │  3. Get correct answer     │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │  Normalize Both Answers    │
    │  - Strip whitespace        │
    │  - Convert to lowercase    │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │  Compare Answers           │
    └────┬──────────────┬────────┘
         │Match         │No Match
         ▼              ▼
    ┌─────────┐    ┌─────────┐
    │correct_ │    │ Skip    │
    │count++  │    │         │
    │is_correct│    │         │
    │= TRUE   │    │         │
    └────┬────┘    └─────────┘
         │
         └──────┬───────────────┘
                │
                ▼
    ┌────────────────────────────┐
    │  Calculate Score           │
    │  score = (correct_count /  │
    │          total_q) × 100    │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │  Classify Performance      │
    └────┬───────┬────────┬──────┘
         │       │        │
    ≥80% │  60-79%│  <60% │
         ▼       ▼        ▼
    ┌────────┐┌──────┐┌──────────┐
    │Advanced││Average││Struggling│
    └────┬───┘└───┬──┘└─────┬────┘
         │        │         │
         ▼        ▼         ▼
┌───────────────────────────────────┐
│  Generate Recommendations         │
│                                   │
│  Advanced:                        │
│  • Deeper theoretical connections │
│  • Advanced topics from doc       │
│  • Complex applications           │
│                                   │
│  Average:                         │
│  • Reinforce core concepts        │
│  • Review weak areas              │
│  • Practice similar problems      │
│                                   │
│  Struggling:                      │
│  • Foundational review            │
│  • Step-by-step explanations      │
│  • Basic concept clarification    │
└───────────┬───────────────────────┘
            │
            ▼
┌────────────────────────────┐
│  Update User Profile       │
│  UPDATE users SET:         │
│  - performance_level       │
│  - avg_quiz_score          │
│    (running average)       │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Update Quiz Attempt       │
│  UPDATE quiz_attempts SET: │
│  - score = calculated      │
│  - completed_at = now()    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Prepare Response          │
│  {                         │
│    quiz_id,                │
│    score,                  │
│    percentage,             │
│    correct_answers,        │
│    total_questions,        │
│    performance_level,      │
│    recommendations[]       │
│  }                         │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Return to Frontend        │
│  Display Results Dashboard │
└────────────────────────────┘
```

---

## 5. ERROR HANDLING FLOWCHART

```
                    ANY SYSTEM OPERATION
                            │
                            ▼
                    ┌───────────────┐
                    │  Try Block    │
                    │  Execute      │
                    └───────┬───────┘
                            │
                    ┌───────┴────────┐
              Success│                │Error/Exception
                    ▼                ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Return Success   │  │  Exception Caught    │
        │ Response         │  │  Analyze Type        │
        └──────────────────┘  └──────────┬───────────┘
                                         │
                    ┌────────────────────┼─────────────────┐
                    │                    │                 │
                    ▼                    ▼                 ▼
        ┌──────────────────┐  ┌─────────────────┐  ┌────────────┐
        │ JSON Parse Error │  │ Database Error  │  │ LLM Error  │
        └────────┬─────────┘  └────────┬────────┘  └─────┬──────┘
                 │                     │                  │
                 ▼                     ▼                  ▼
        ┌──────────────────┐  ┌─────────────────┐  ┌────────────┐
        │ - Log error      │  │ - Rollback      │  │ - Retry 3x │
        │ - Try JSON       │  │ - Log details   │  │ - Fallback │
        │   extraction     │  │ - Return 500    │  │ - Return   │
        │ - Return 500     │  └─────────────────┘  │   error    │
        └──────────────────┘                       └────────────┘
                 │                     │                  │
                 └─────────────────────┼──────────────────┘
                                       │
                                       ▼
                            ┌──────────────────────┐
                            │  Frontend Error      │
                            │  Display              │
                            │  - User-friendly msg │
                            │  - Retry option      │
                            └──────────────────────┘
```

---

## 6. DATA FLOW DIAGRAM

```
┌──────────────┐
│   Student    │
└──────┬───────┘
       │ Upload Document
       ▼
┌──────────────────────────┐
│   Frontend (React)       │
│   - FormData creation    │
│   - File validation      │
└──────┬───────────────────┘
       │ POST /api/content/upload
       ▼
┌──────────────────────────┐
│   Backend (FastAPI)      │
│   - Receive file         │
│   - Save to filesystem   │
│   - Extract text         │
└──────┬───────────────────┘
       │ Text content
       ▼
┌──────────────────────────┐
│   RAG Pipeline           │
│   - Chunk text           │
│   - Generate embeddings  │
└──────┬───────────────────┘
       │ Vectors + metadata
       ▼
┌──────────────────────────┐
│   ChromaDB               │
│   - Store vectors        │
│   - Index for search     │
└──────┬───────────────────┘
       │ Storage confirmation
       ▼
┌──────────────────────────┐
│   Backend                │
│   - Trigger summarize    │
└──────┬───────────────────┘
       │ Retrieve top-k chunks
       ▼
┌──────────────────────────┐
│   ChromaDB               │
│   - Similarity search    │
│   - Return chunks        │
└──────┬───────────────────┘
       │ Relevant chunks
       ▼
┌──────────────────────────┐
│   Groq LLM               │
│   - Receive context      │
│   - Generate summary     │
└──────┬───────────────────┘
       │ {topic, summary, key_points}
       ▼
┌──────────────────────────┐
│   Backend                │
│   - Parse JSON           │
│   - Return to frontend   │
└──────┬───────────────────┘
       │ Summary data
       ▼
┌──────────────────────────┐
│   Frontend               │
│   - Display summary      │
│   - Show "Take Quiz" btn │
└──────┬───────────────────┘
       │ User clicks button
       ▼
┌──────────────────────────┐
│   (Quiz Generation Flow) │
│   Similar data flow...   │
└──────────────────────────┘
```

---

**Note**: These flowcharts use ASCII art for clarity. For IEEE paper submission, convert to proper flowchart diagrams using tools like:
- Microsoft Visio
- Draw.io (diagrams.net)  
- Lucidchart
- LaTeX TikZ

All logical flows have been documented in detail for technical accuracy.
