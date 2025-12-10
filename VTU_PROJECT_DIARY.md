# VTU Project Diary - Antigravity AI Tutor

## Entry 1 – Literature Survey & Problem Definition
**Date:** 25/08/2025
**What I worked on?**
- Conducted a comprehensive literature survey on existing AI-based tutoring systems and their limitations.
- Researched Retrieval Augmented Generation (RAG) architectures to solve LLM hallucination issues.
- Defined the core problem statement: "Static learning materials lack interactivity and personalization."
- Identified key features: Document Summarization, Quiz Generation, and Adaptive Learning.

**Hours Worked:** 8-10
**Learning / Outcomes**
- Gained deep understanding of Vector Database technologies (ChromaDB, Pinecone).
- Finalized the decision to use a Microservices-based architecture for scalability.
- Outcome: Project Abstract and Requirement Specification Document.

**Blocker / Risks**
- Difficulty in finding open-source datasets for educational benchmarking.
- Risk of high API costs for LLM inference (mitigated by choosing Groq).

**Skills Used**
- Technical Research
- System Analysis
- Requirement Engineering

---

## Entry 2 – Environment Setup & Git Initialization
**Date:** 26/08/2025
**What I worked on?**
- Set up the development environment for Backend (Python 3.12) and Frontend (Node.js 18+).
- Initialized the Git repository with a structured branching strategy (main, develop, feature branches).
- Installed core dependencies: `fastapi`, `uvicorn`, `langchain`, and `react-vite`.
- Configured virtual environments and `.gitignore` files to prevent secret leakage.

**Hours Worked:** 6-8
**Learning / Outcomes**
- Learned best practices for project structure in full-stack AI applications.
- Successfully established a working "Hello World" connection between FastAPI and React.
- Outcome: Development Environment ready and version control established.

**Blocker / Risks**
- Dependency conflicts between different Python libraries (resolved using virtualenv).
- Ensuring cross-platform compatibility (Windows/Linux) for team members.

**Skills Used**
- Python & Node.js
- Git/GitHub
- DevOps (Environment Config)

---

## Entry 3 – System Architecture & Database Design
**Date:** 08/09/2025
**What I worked on?**
- Designed the high-level system architecture including API Gateway and Service layers.
- Created the database schema for User Management and Quiz Results using SQLAlchemy models.
- Designed the RESTful API endpoints specification (OpenAPI/Swagger).
- Selected ChromaDB as the vector store for semantic search operations.

**Hours Worked:** 7-9
**Learning / Outcomes**
- Gained deeper insight into Relational vs. Vector database use cases.
- Understood how to structure database models for efficient querying in an educational context.
- Outcome: Database Schema Diagram and API Specification.

**Blocker / Risks**
- Complexity in designing relationships for adaptive learning paths.
- ensuring data consistency between SQL and Vector databases.

**Skills Used**
- Database Design (SQL)
- System Architecture
- REST API Design

---

## Entry 4 – Vector Database & LLM Integration
**Date:** 09/09/2025
**What I worked on?**
- Implemented the initial database migration scripts using Alembic.
- Configured ChromaDB locally and tested basic vector insertion and retrieval.
- Integrated HuggingFace Embeddings (`all-MiniLM-L6-v2`) for converting text to vectors.
- Set up the Groq API client for high-speed LLM inference (`llama-3.1-8b-instant`).

**Hours Worked:** 6-8
**Learning / Outcomes**
- Learned how to generate and store high-dimensional vector embeddings.
- Achieved successful connection to external LLM APIs (Groq) with <1s latency.
- Outcome: Functional Database and Vector Store integration.

**Blocker / Risks**
- Rate limits on the free tier of LLM providers.
- Handling dimension mismatch errors in embeddings.

**Skills Used**
- ChromaDB / Vector Databases
- HuggingFace Transformers
- LLM API Integration

---

## Entry 5 – Document Ingestion Service
**Date:** 22/09/2025
**What I worked on?**
- Developed the Document Ingestion Service to handle file uploads.
- Implemented multi-format parsers using `PyMuPDF` for PDFs and `python-docx` for Word documents.
- Created validation logic to ensure only supported file types are uploaded.
- Built the file storage logic to save uploaded documents securely.

**Hours Worked:** 5-7
**Learning / Outcomes**
- Mastered Python libraries for extracting raw text from complex document formats.
- Learned to handle binary file streams in FastAPI.
- Outcome: Robust file upload and text extraction module.

**Blocker / Risks**
- Handling corrupted or password-protected PDF files.
- Memory usage spikes when processing large files.

**Skills Used**
- Python File I/O
- PyMuPDF (Fitz)
- FastAPI UploadFile

---

## Entry 6 – OCR & Text Chunking Pipeline
**Date:** 23/09/2025
**What I worked on?**
- Integrated `Tesseract OCR` to extract text from scanned images within PDFs.
- Implemented the Text Chunking pipeline using LangChain's `RecursiveCharacterTextSplitter`.
- Optimized chunk sizes (1000 characters) and overlap (200 characters) for better context retention.
- Handled edge cases for noisy or corrupted text data.

**Hours Worked:** 7-9
**Learning / Outcomes**
- Understood the importance of "Chunking Strategies" in RAG performance.
- Learned how to preprocess and clean text data for AI consumption.
- Outcome: Clean, chunked data ready for embedding.

**Blocker / Risks**
- OCR accuracy on low-quality scanned images.
- Determining the optimal chunk size for different types of content.

**Skills Used**
- OCR (Tesseract)
- LangChain Text Splitters
- Data Preprocessing

---

## Entry 7 – Embedding & Retrieval Engine
**Date:** 06/10/2025
**What I worked on?**
- Built the Embedding Pipeline to process text chunks in batches.
- Stored generated embeddings into ChromaDB with appropriate metadata (source, page number).
- Implemented a similarity search function to retrieve relevant context based on user queries.
- Tested retrieval accuracy using sample educational documents.

**Hours Worked:** 8-10
**Learning / Outcomes**
- Learned about "Cosine Similarity" and how it ranks relevance.
- Optimized the retrieval process to ensure fast response times (<100ms).
- Outcome: Working Semantic Search engine.

**Blocker / Risks**
- "Lost in the Middle" phenomenon where relevant context is missed.
- Performance degradation as the vector store grows.

**Skills Used**
- Vector Embeddings
- Cosine Similarity Algorithms
- Python Async/Await

---

## Entry 8 – Summarization Engine
**Date:** 07/10/2025
**What I worked on?**
- Developed the Summarization Engine using Map-Reduce algorithms.
- Created specific prompts to generate concise summaries and "Key Points" from documents.
- Integrated the summarization logic into the upload flow (auto-summarize on upload).
- Handled token limit constraints for large documents.

**Hours Worked:** 6-8
**Learning / Outcomes**
- Mastered Prompt Engineering techniques for summarization tasks.
- Learned how to handle large context windows effectively.
- Outcome: Automatic document summarization feature.

**Blocker / Risks**
- LLM hallucinating details not present in the text.
- Processing time for very large documents (>100 pages).

**Skills Used**
- Prompt Engineering
- Map-Reduce Algorithms
- LangChain Chains

---

## Entry 9 – RAG Pipeline Implementation
**Date:** 13/10/2025
**What I worked on?**
- Implemented the core Retrieval Augmented Generation (RAG) pipeline.
- Connected the Retrieval step (ChromaDB) with the Generation step (Groq LLM).
- Designed the "Context Injection" logic to feed relevant document parts into the LLM prompt.
- Built the backend endpoint for the Chat/Q&A feature.

**Hours Worked:** 8-10
**Learning / Outcomes**
- Deepened understanding of the full RAG lifecycle (Retrieve -> Augment -> Generate).
- Solved issues related to context relevance and hallucination.
- Outcome: Functional Context-Aware Q&A backend.

**Blocker / Risks**
- Balancing the trade-off between context length and latency.
- Ensuring the model cites sources correctly.

**Skills Used**
- RAG Architecture
- LLM Context Management
- FastAPI

---

## Entry 10 – Chat Logic & Chain-of-Thought
**Date:** 14/10/2025
**What I worked on?**
- Refined the LLM prompts for educational tone and accuracy.
- Implemented "Chain-of-Thought" (CoT) prompting for complex homework questions.
- Added history management to support multi-turn conversations.
- Tested the chat system with various subject materials (Science, History, Math).

**Hours Worked:** 7-9
**Learning / Outcomes**
- Learned how to maintain conversation state (Memory) in stateless APIs.
- Improved the quality of AI responses through iterative prompt testing.
- Outcome: Intelligent Chatbot capable of explaining concepts.

**Blocker / Risks**
- Managing token limits with long conversation histories.
- Preventing the model from giving direct answers without explanation.

**Skills Used**
- Chain-of-Thought Prompting
- Conversation Memory Management
- Python

---

## Entry 11 – Quiz Generation Engine
**Date:** 03/11/2025
**What I worked on?**
- Developed the Quiz Generation Engine.
- Created prompts to output questions in structured JSON format (MCQs, True/False).
- Implemented logic to parse the raw LLM output into usable frontend data objects.
- Added difficulty level parameters (Easy, Medium, Hard) to the generation request.

**Hours Worked:** 6-8
**Learning / Outcomes**
- Learned techniques to force LLMs to output structured data (JSON Mode).
- Outcome: Automated Quiz Generator that creates questions from uploaded content.

**Blocker / Risks**
- LLM occasionally outputting invalid JSON.
- Generating questions that are too ambiguous or incorrect.

**Skills Used**
- JSON Parsing
- Prompt Engineering (Structured Output)
- Algorithm Design

---

## Entry 12 – Adaptive Learning Algorithm
**Date:** 04/11/2025
**What I worked on?**
- Built the Adaptive Learning Algorithm.
- Implemented logic to analyze quiz scores and classify user proficiency.
- Designed the recommendation engine to suggest specific topics based on weak areas.
- Created the backend endpoints to fetch personalized study plans.

**Hours Worked:** 8-10
**Learning / Outcomes**
- Understood how to translate quantitative data (scores) into qualitative actions (learning paths).
- Outcome: Adaptive system that responds to user performance.

**Blocker / Risks**
- Defining accurate thresholds for proficiency classification.
- Cold start problem for new users with no quiz data.

**Skills Used**
- Data Analysis Logic
- Adaptive Algorithms
- Backend Logic

---

## Entry 13 – Frontend Development: UI Skeleton
**Date:** 10/11/2025
**What I worked on?**
- Started intensive Frontend development using React and Vite.
- Built the core layout components: Sidebar, Header, and Main Content Area.
- Implemented the "Upload & Summarize" UI with progress bars and loading states.
- Styled the application using modern CSS and responsive design principles.

**Hours Worked:** 7-9
**Learning / Outcomes**
- Improved skills in building responsive, user-friendly interfaces.
- Learned to manage asynchronous file uploads in React.
- Outcome: Core UI skeleton and Upload interface.

**Blocker / Risks**
- CSS conflicts when using multiple styling libraries.
- Ensuring consistent design across different screen sizes.

**Skills Used**
- React.js
- CSS3 / Tailwind
- UI/UX Design

---

## Entry 14 – Frontend Integration: Chat & Quiz
**Date:** 11/11/2025
**What I worked on?**
- Integrated the Chat and Quiz backend APIs with the Frontend.
- Built the interactive Chat Interface with message bubbles and auto-scroll.
- Developed the Quiz Taking Interface with timer and score calculation.
- Implemented global state management using React Context API.

**Hours Worked:** 8-10
**Learning / Outcomes**
- Mastered API integration using Axios and handling async data states.
- Learned to build complex interactive components (Quiz UI).
- Outcome: Fully interactive Chat and Quiz modules on the frontend.

**Blocker / Risks**
- Handling race conditions in API calls.
- State management complexity with real-time updates.

**Skills Used**
- React Hooks (useState, useEffect)
- Context API
- Axios

---

## Entry 15 – Authentication & Security
**Date:** 24/11/2025
**What I worked on?**
- Implemented User Authentication (Login/Signup) logic.
- Secured API endpoints using JWT (JSON Web Tokens).
- Added session persistence to keep users logged in.
- Built the Dashboard to visualize user progress and recent activities.

**Hours Worked:** 6-8
**Learning / Outcomes**
- Understood the security principles of stateless authentication (JWT).
- Learned to protect frontend routes (Private Routes).
- Outcome: Secure application with user profiles.

**Blocker / Risks**
- Storing tokens securely (HttpOnly cookies vs LocalStorage).
- Handling token expiration and refresh flows seamlessly.

**Skills Used**
- JWT Authentication
- Web Security
- React Routing

---

## Entry 16 – Theming & UI Polish
**Date:** 25/11/2025
**What I worked on?**
- Implemented the Light/Dark Theme toggle using CSS variables.
- Polished the UI with micro-interactions and smooth transitions.
- Refined the "Adaptive Learning" display to show dynamic study paths.
- Fixed UI bugs and consistency issues across different pages.

**Hours Worked:** 5-7
**Learning / Outcomes**
- Learned how to implement global theming systems.
- Enhanced the overall User Experience (UX) through visual polish.
- Outcome: Aesthetically pleasing and responsive application.

**Blocker / Risks**
- Flash of unstyled content (FOUC) during theme switch.
- Maintaining contrast ratios for accessibility in both themes.

**Skills Used**
- Advanced CSS
- Theming
- Frontend Optimization

---

## Entry 17 – Testing (Unit & Integration)
**Date:** 08/12/2025
**What I worked on?**
- Conducted comprehensive Unit Testing for backend services using PyTest.
- Performed Integration Testing to ensure frontend-backend data flow is correct.
- Executed Load Testing on the RAG endpoints to check performance under stress.
- Identified and fixed minor bugs in the quiz scoring logic.

**Hours Worked:** 7-9
**Learning / Outcomes**
- Gained proficiency in writing test cases and debugging.
- Ensured the system is robust and handles errors gracefully.
- Outcome: Stable and bug-free application.

**Blocker / Risks**
- Mocking external API calls (Groq/ChromaDB) for unit tests.
- Time constraints for achieving 100% test coverage.

**Skills Used**
- PyTest
- Debugging
- Quality Assurance

---

## Entry 18 – Documentation & Deployment
**Date:** 09/12/2025
**What I worked on?**
- Finalized the project documentation (README, API Docs, User Manual).
- Prepared the project for deployment (Dockerizing services).
- Conducted a final code review and cleanup.
- Prepared the final project presentation and demo video.

**Hours Worked:** 6-8
**Learning / Outcomes**
- Learned the importance of good documentation for software maintenance.
- Completed the full software development lifecycle (SDLC).
- Outcome: Project ready for submission and evaluation.

**Blocker / Risks**
- Last-minute environment issues during deployment.
- Ensuring documentation matches the final implemented features.

**Skills Used**
- Documentation
- Docker
- Presentation Skills
