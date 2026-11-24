# CVR College RAG Chatbot

A full-stack **Retrieval-Augmented Generation (RAG) chatbot** for CVR College of Engineering. It answers student queries about courses, faculty, placements, infrastructure, and more — using college-specific documents as its knowledge base.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Embeddings | HuggingFace `all-mpnet-base-v2` |
| Vector DB | ChromaDB |
| Backend | FastAPI + Uvicorn |
| Frontend | React (Vite) + react-markdown |
| Orchestration | LangChain |

## Project Structure

```
edureach-platform/
├── backend/
│   ├── api.py                  # FastAPI app (REST endpoints)
│   ├── chatbot.py              # LangChain RAG chain
│   ├── vectorize_documents.py  # Builds vector DB from PDFs
│   ├── requirements.txt
│   └── rag_data/               # Text knowledge-base files
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ChatMessage.jsx
│   │       └── ChatInput.jsx
│   ├── package.json
│   └── vite.config.js
├── .env.example                # Copy to .env and add your keys
└── README.md
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Groq API key](https://console.groq.com)

### 1. Clone the repo

```bash
git clone <repo-url>
cd edureach-platform
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Open .env and set GROQ_API_KEY
```

### 3. Set up the Python environment

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Build the vector database

Place your college PDF documents in `backend/data/`, then run:

```bash
python vectorize_documents.py
```

This creates the `backend/vector_db_dir/` ChromaDB store. Only needs to run once (or when PDFs change).

### 5. Install frontend dependencies

```bash
cd ../frontend
npm install
```

## Running

### Backend (Terminal 1)

```bash
cd backend
uvicorn api:app --reload --port 8000
```

### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Returns backend and chain status |
| `POST` | `/chat` | Send a question, get an answer |

**POST /chat**
```json
// Request
{ "message": "What courses does CVR offer?" }

// Response
{ "answer": "CVR College offers B.Tech programs in..." }
```

## Notes

- `vector_db_dir/` and `data/` are excluded from git — each collaborator runs `vectorize_documents.py` after cloning.
- Never commit `.env` or `config.json`.
