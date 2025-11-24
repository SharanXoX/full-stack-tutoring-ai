# 🎓 FULL STACK TUTORING WITH AI

An intelligent, adaptive learning platform powered by AI that provides personalized education through document analysis, interactive quizzing, and adaptive teaching.


## ✨ Features

### Core Capabilities
- **📚 Document Upload & Analysis**: Upload PDFs, DOCX, PPTX, TXT, and image files
- **🤖 AI-Powered Summarization**: Automatic content summarization with adaptive length (50-600 words)
- **❓ Intelligent Quiz Generation**: Creates MCQ and True/False questions based on uploaded content
- **📊 Adaptive Learning**: Performance-based recommendations (Struggling/Average/Advanced)
- **💬 AI Chat**: RAG-powered conversations about your study materials
- **📝 Homework Help**: Step-by-step solutions with progressive hints
- **🌓 Light/Dark Theme**: Beautiful UI with smooth theme transitions

### Technology Stack

#### Backend
- **Framework**: Python 3.12, FastAPI
- **AI/LLM**: Groq API (llama-3.1-8b-instant)
- **Vector Database**: ChromaDB for RAG
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Database**: SQLite
- **Document Processing**: PyMuPDF, python-docx, python-pptx, Tesseract OCR

#### Frontend
- **Framework**: React 18, Vite 5
- **Routing**: React Router v6
- **Styling**: Vanilla CSS with CSS Variables
- **State Management**: React Context API

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Tesseract OCR (for image processing)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-tutor.git
cd ai-tutor
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp backend/.env.example backend/.env
# Add your GROQ_API_KEY to backend/.env
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
```

### Running the Application

#### Start Backend
```bash
# From project root, with venv activated
uvicorn backend.main:app --reload
```
Backend runs on: `http://127.0.0.1:8000`

#### Start Frontend
```bash
# In a new terminal
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:5173`

## 📖 Usage

1. **Upload Documents**: Navigate to the Upload page and select your study materials
2. **View Summary**: AI automatically generates a detailed summary with key points
3. **Take Quiz**: Click "Take Quiz" to test your knowledge
4. **Get Recommendations**: Receive personalized learning paths based on quiz performance
5. **Ask Questions**: Use the Chat feature to ask questions about your materials
6. **Get Homework Help**: Receive step-by-step guidance with progressive hints

## 🎨 Theme Customization

The app supports light and dark themes. Click the 🌙/☀️ button in the top-right corner to toggle.

CSS variables are defined in `frontend/src/index.css` and can be customized.

## 📁 Project Structure

```
ai-tutor/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── rag.py               # RAG & summarization logic
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── content.py
│   │   ├── exam.py
│   │   ├── homework.py
│   │   └── adaptive_learning.py
│   └── .env                 # Environment variables (not in repo)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── context/         # React contexts (App, Theme)
│   │   └── index.css        # Global styles & theme
│   └── package.json
├── chroma_db/               # Vector database (not in repo)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔑 Environment Variables

Create `backend/.env` with:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Groq for providing fast LLM inference
- HuggingFace for embedding models
- ChromaDB for vector search capabilities

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ - FULL STACK TUTORING WITH AI
