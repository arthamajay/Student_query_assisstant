import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import create_chain

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CVR College Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chain once at startup
chain = None

@app.on_event("startup")
async def startup_event():
    global chain
    chain = create_chain()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    global chain
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
