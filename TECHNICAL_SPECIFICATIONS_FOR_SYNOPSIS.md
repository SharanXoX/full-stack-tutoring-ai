# TECHNICAL SPECIFICATIONS FOR SYNOPSIS
## Add these details to your "Methodology" or "System Design" section

---

### 1. SYSTEM ARCHITECTURE & ALGORITHMS

**A. AI & NLP Pipeline**
*   **Large Language Model (LLM)**: Groq API powering `llama-3.1-8b-instant` for sub-second text generation and reasoning.
*   **Retrieval Augmented Generation (RAG)**: Custom pipeline using `LangChain` to retrieve context from `ChromaDB` before generating answers, ensuring factual accuracy.
*   **Vector Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) for converting text into dense vector representations for semantic search.
*   **Similarity Search**: Cosine Similarity algorithm used to rank and retrieve the top-k most relevant document chunks.

**B. Document Processing Engine**
*   **Text Extraction**: 
    *   `PyMuPDF` (FitZ) for high-fidelity PDF text extraction.
    *   `python-docx` and `python-pptx` for Office documents.
    *   `Tesseract OCR` (v5.0) via `pytesseract` for extracting text from scanned images and diagrams.
*   **Chunking Strategy**: `RecursiveCharacterTextSplitter` with a chunk size of 1000 tokens and 200-token overlap to preserve context across boundaries.

**C. Adaptive Learning Engine**
*   **Performance Classification**: Rule-based algorithm classifying students into *Struggling (<50%)*, *Average (50-75%)*, and *Advanced (>75%)* tiers.
*   **Dynamic Content**: Conditional logic that adjusts quiz difficulty and hint granularity (Chain-of-Thought prompting) based on the user's tier.

---

### 2. SOFTWARE TECHNOLOGY STACK

| Component | Technology / Tool | Version | Purpose |
|-----------|------------------|---------|---------|
| **Frontend** | React.js | 18.2.0 | Component-based UI architecture |
| | Vite | 5.0+ | Next-generation frontend tooling & bundler |
| | React Router | 6.20 | Client-side routing for SPA |
| | Axios | 1.6.0 | Promise-based HTTP client for API requests |
| **Backend** | Python | 3.12 | Core programming language |
| | FastAPI | 0.104 | High-performance async web framework |
| | Uvicorn | 0.24 | ASGI web server implementation |
| | SQLAlchemy | 2.0 | ORM for relational database interactions |
| **AI / ML** | LangChain | 0.1.0 | Framework for LLM application development |
| | ChromaDB | 0.4.18 | Open-source embedding database (Vector Store) |
| | Groq SDK | 0.4.0 | Interface for LPU-based LLM inference |
| **Database** | SQLite / PostgreSQL | Latest | Relational data storage (Users, Logs) |
| **DevOps** | Git & GitHub | Latest | Version control and collaboration |

---

### 3. HARDWARE REQUIREMENTS (DEVELOPMENT & DEPLOYMENT)

*   **Processor**: Minimum Intel i5 (10th Gen) or AMD Ryzen 5 (3000 series) to handle local embedding generation and vector search.
*   **RAM**: 16 GB DDR4 recommended (Minimum 8 GB) to run the React dev server, FastAPI backend, and ChromaDB in memory simultaneously.
*   **Storage**: SSD with at least 10 GB free space for vector indices and document cache.
*   **Network**: Stable broadband connection (min 10 Mbps) required for communicating with the cloud-based Groq API.
