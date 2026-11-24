# Student Query Assistant

A full-stack **Retrieval-Augmented Generation (RAG) chatbot** for CVR College of Engineering. It answers student queries about courses, faculty, placements, infrastructure, and more — using college-specific documents as its knowledge base.

## Tech Stack

| Layer | Technology |
|-------|------------|
| LLM | Groq — `openai/gpt-oss-120b` |
| Embeddings | HuggingFace `all-mpnet-base-v2` |
| Vector DB | ChromaDB |
| Backend | FastAPI + Uvicorn |
| Frontend | React (Vite) + react-markdown |
| Orchestration | LangChain |

## Project Structure

```
Student_query_assisstant/
├── backend/
│   ├── api.py                   # FastAPI app — REST endpoints
│   ├── chatbot.py               # LangChain RAG chain setup
│   ├── vectorize_documents.py   # Builds the ChromaDB vector store
│   ├── requirements.txt
│   └── rag_data/                # Curated knowledge-base text files
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ChatMessage.jsx
│   │       └── ChatInput.jsx
│   ├── package.json
│   └── vite.config.js
├── .env.example                 # Copy to .env and fill in your keys
└── README.md
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Groq API key](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/arthamajay/Student_query_assisstant.git
cd Student_query_assisstant
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Open .env and set your GROQ_API_KEY
```

### 3. Set up the Python environment

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Build the vector database

The script loads from `backend/rag_data/` (curated text files) and optionally `backend/data/` (PDFs).

```bash
python vectorize_documents.py
```

This creates `backend/vector_db_dir/`. Run once after cloning, or whenever the source files change.

### 5. Install frontend dependencies

```bash
cd ../frontend
npm install
```

## Running

### Backend — Terminal 1

```bash
cd backend
uvicorn api:app --reload --port 8000
```

### Frontend — Terminal 2

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser (Vite may use 5174/5175 if 5173 is taken).

## API Reference

| Method | Endpoint  | Description                        |
|--------|-----------|------------------------------------|
| `GET`  | `/health` | Returns backend and chain status   |
| `POST` | `/chat`   | Send a question, receive an answer |

**POST /chat**
```json
// Request
{ "message": "What courses does CVR offer?" }

// Response
{ "answer": "CVR College offers B.Tech programs in..." }
```

## Notes

- `vector_db_dir/` and `data/` are excluded from git. Every collaborator must run `vectorize_documents.py` after cloning.
- Never commit `.env` or `config.json` — use `.env.example` as the template.
