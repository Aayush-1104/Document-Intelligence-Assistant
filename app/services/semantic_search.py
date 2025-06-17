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
    return [doc.page_content for doc in results]

def ask_groq(query, context):
    print("🧠 Preparing Groq request...")

    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Use the following context to answer the user's question.
    Context:
    {context}

    Question: {query}
    Answer:
    """

    payload = {
        "model": groq_model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    print("📡 Sending request to Groq...")
    response = requests.post(f"{groq_url}/chat/completions", headers=headers, json=payload)
    print("📥 Response received.")

    try:
        data = response.json()
        print("🔍 Raw Groq response:", data)  # Debug output

        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to parse Groq response:", str(e))
        return f"Error from Groq API: {response.text}"
