# CVR College RAG Chatbot

A full-stack **Retrieval-Augmented Generation (RAG) chatbot** for CVR College of Engineering. It answers student queries about courses, faculty, placements, infrastructure, and more — using college-specific documents as its knowledge base.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq (llama-3.3-70b-versatile) |
| Embeddings | HuggingFace Transformers |
| Vector DB | ChromaDB |
| Backend | FastAPI + Uvicorn |
| Frontend | React (Vite) + react-markdown |
| Orchestration | LangChain |

---

## Project Structure

```
edureach-platform/
├── api.py                  # FastAPI backend
├── chatbot.py              # LangChain RAG chain setup
├── vectorize_documents.py  # Script to build vector DB from PDFs
├── main.py                 # Legacy Streamlit interface
├── rag_data/               # Text knowledge base files
├── requirements.txt        # Python dependencies
└── frontend/               # React web UI
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── ChatMessage.jsx
        │   └── ChatInput.jsx
        └── App.css
```

---

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

### 2. Create Python virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API key

Create a `config.json` in the project root:

```json
{
  "GROQ_API_KEY": "your_groq_api_key_here",
  "COLLEGE_NAME": "CVR College of Engineering"
}
```

> `config.json` is in `.gitignore` — never commit it.

### 5. Build the vector database

Place your college PDF documents in the `data/` folder, then run:

```bash
python vectorize_documents.py
```

This creates the `vector_db_dir/` ChromaDB store.

### 6. Install frontend dependencies

```bash
cd frontend
npm install
```

---

## Running

### Backend (Terminal 1)

```bash
uvicorn api:app --reload --port 8000
```

### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check if backend and chain are ready |
| `POST` | `/chat` | Send a message, get an answer |

**POST /chat request:**
```json
{ "message": "What courses does CVR offer?" }
```

**Response:**
```json
{ "answer": "CVR College offers B.Tech programs in..." }
```

---

## Notes

- The vector database is built locally and excluded from git (`vector_db_dir/` is in `.gitignore`). Each collaborator needs to run `vectorize_documents.py` after cloning.
- `config.json` and `.env` are excluded from git to protect API keys.
