from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document  

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    print("🔪 Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def embed_and_store(chunks, persist_path="vectordb_faiss"):
    print("🧠 [embed_and_store] Starting FAISS embedding...")

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("📦 HuggingFace embeddings loaded")

        vectordb = FAISS.from_texts(texts=chunks, embedding=embeddings)
        vectordb.save_local(persist_path)

        print(f"✅ FAISS index saved to: {persist_path}")
        return vectordb

    except Exception as e:
        print("❌ FAISS embedding crash:", str(e))
        raise
