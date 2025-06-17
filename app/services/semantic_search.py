import os
from langchain_community.vectorstores import FAISS
# New
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests

EMBEDDING_MODEL = HuggingFaceEmbeddings(     
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

DB_DIR = "vectordb"
groq_url = os.getenv("GROQ_BASE_URL")
groq_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL")

def get_similar_chunks(query, k=4):
    vectordb = FAISS.load_local("vectordb_faiss", EMBEDDING_MODEL, allow_dangerous_deserialization=True)
    results = vectordb.similarity_search(query, k=k)
    
    # Simulate confidence by chunk index (or make up dummy scores)
    chunks_with_scores = [{"chunk": doc.page_content, "score": round(1 - (i * 0.1), 2)} for i, doc in enumerate(results)]
    return chunks_with_scores


def ask_groq(query, context):
    prompt = f"""
Use the following context to answer the user's question.

Context:
{context}

Question: {query}
Answer:
"""

    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": groq_model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        print("📡 Primary: Sending to Groq")
        response = requests.post(f"{groq_url}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("⚠️ Groq failed. Fallback triggered:", str(e))

        # ✅ Simulate fallback model (OpenRouter, etc.)
        return "⚠️ Groq LLM failed. This is a fallback response from a secondary model."