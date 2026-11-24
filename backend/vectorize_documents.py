"""
Build the ChromaDB vector store from the knowledge-base files.

Sources (both are loaded):
  - backend/rag_data/   curated .txt files  (primary)
  - backend/data/       raw PDFs            (supplementary)

Run once after cloning, or whenever the source files change:
    cd backend
    python vectorize_documents.py
"""

import shutil
from pathlib import Path

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

BASE_DIR     = Path(__file__).parent
RAG_DATA_DIR = BASE_DIR / "rag_data"
PDF_DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vector_db_dir"


# ── loaders ──────────────────────────────────────────────────────────────────

def load_txt_documents(directory: Path) -> list[Document]:
    docs = []
    for path in sorted(directory.glob("*.txt")):
        try:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                docs.append(Document(page_content=text, metadata={"source": path.name}))
                print(f"  ✓ {path.name}")
        except Exception as exc:
            print(f"  ✗ {path.name}: {exc}")
    return docs


def load_pdf_documents(directory: Path) -> list[Document]:
    docs = []
    for path in sorted(directory.glob("*.pdf")):
        try:
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
            if text:
                docs.append(Document(page_content=text, metadata={"source": path.name}))
                print(f"  ✓ {path.name}")
        except Exception as exc:
            print(f"  ✗ {path.name}: {exc}")
    return docs


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    all_docs: list[Document] = []

    # Load .txt knowledge base
    if RAG_DATA_DIR.exists():
        print(f"\nLoading text files from {RAG_DATA_DIR.name}/...")
        txt_docs = load_txt_documents(RAG_DATA_DIR)
        print(f"  → {len(txt_docs)} text file(s) loaded.")
        all_docs.extend(txt_docs)
    else:
        print(f"⚠  {RAG_DATA_DIR} not found, skipping.")

    # Load PDFs
    if PDF_DATA_DIR.exists():
        print(f"\nLoading PDFs from {PDF_DATA_DIR.name}/...")
        pdf_docs = load_pdf_documents(PDF_DATA_DIR)
        print(f"  → {len(pdf_docs)} PDF(s) loaded.")
        all_docs.extend(pdf_docs)
    else:
        print(f"⚠  {PDF_DATA_DIR} not found, skipping.")

    if not all_docs:
        print("\n✗ No documents found. Add files and re-run.")
        return

    print(f"\nTotal documents loaded: {len(all_docs)}")

    # Split into chunks
    print("\nSplitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(all_docs)
    print(f"  → {len(chunks)} chunks created.")

    # Wipe existing vector DB and rebuild clean
    if VECTOR_DB_DIR.exists():
        print(f"\nClearing existing vector store at {VECTOR_DB_DIR.name}/...")
        shutil.rmtree(VECTOR_DB_DIR)
    VECTOR_DB_DIR.mkdir(parents=True)

    print("\nLoading embedding model (this takes a moment)...")
    embeddings = HuggingFaceEmbeddings()

    print("Building vector store...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
    )

    print(f"\n✓ Vector store ready — {len(chunks)} chunks stored in {VECTOR_DB_DIR.name}/")


if __name__ == "__main__":
    main()
