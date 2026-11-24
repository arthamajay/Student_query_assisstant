import logging
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

from chatbot import create_chain

logging.basicConfig(level=logging.INFO)

chain = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chain
    chain = create_chain()
    yield


app = FastAPI(title="CVR College Chatbot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if chain is None:
        raise HTTPException(status_code=503, detail="Chatbot not ready yet")
    try:
        response = chain.invoke({"question": request.message})
        return ChatResponse(answer=response["answer"])
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok", "chain_ready": chain is not None}
