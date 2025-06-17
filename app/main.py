from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes import upload, chat

app = FastAPI(
    title="Document Intelligence Assistant",
    description="Upload documents and ask questions using RAG + Groq LLM",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routers
app.include_router(upload.router)
app.include_router(chat.router)
