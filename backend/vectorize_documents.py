"""
Build the ChromaDB vector store from PDF files in backend/data/.

Run once after cloning (or whenever the PDFs change):
    cd backend
    python vectorize_documents.py
"""

import os
from pathlib import Path

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vector_db_dir"


def load_pdf_documents(directory: Path) -> list[Document]:
    documents = []
    for pdf_path in sorted(directory.glob("*.pdf")):
        try:
            print(f"  Processing {pdf_path.name}...")
            reader = PdfReader(str(pdf_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            documents.append(Document(page_content=text, metadata={"source": pdf_path.name}))
            print(f"  ✓ {pdf_path.name}")
        except Exception as exc:
            print(f"  ✗ {pdf_path.name}: {exc}")
    return documents


def main():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
        print(f"Created {DATA_DIR} — add your PDF files there, then re-run.")
        return

    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings()

    print(f"Loading PDFs from {DATA_DIR}...")
    documents = load_pdf_documents(DATA_DIR)

    if not documents:
        print("No PDFs found. Add files to backend/data/ and re-run.")
        return

    print(f"Loaded {len(documents)} document(s). Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Building vector store...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
    )
    print(f"✓ Vector store saved to {VECTOR_DB_DIR}")


if __name__ == "__main__":
    main()
