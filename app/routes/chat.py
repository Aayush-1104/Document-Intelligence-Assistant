from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.semantic_search import get_similar_chunks, ask_groq

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
def chat_with_documents(request: ChatRequest):
    try:
        chunks = get_similar_chunks(request.query)
        context = "\n\n".join([chunk["chunk"] for chunk in chunks])
        answer = ask_groq(request.query, context)

        return {
            "query": request.query,
            "answer": answer,
            "context_chunks": chunks
        }

    except Exception as e:
        print("❌ Chat error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groq-test")
def test_groq():
    from app.services.semantic_search import ask_groq
    dummy_context = "This document is about using AI to answer questions from files."
    query = "What is the main topic?"

    try:
        answer = ask_groq(query, dummy_context)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
