import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="📄 Document Intelligence Assistant", layout="wide")
st.title("📄 Document Intelligence Assistant")
st.caption("Upload a document and ask questions using RAG + Groq LLM")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Info")
    st.markdown(f"- **Backend:** FastAPI")
    st.markdown(f"- **Vector DB:** FAISS")
    st.markdown(f"- **LLM:** `{os.getenv('GROQ_MODEL')}`")
    st.markdown("---")
    st.markdown("Developed by Aayush 🚀")

# --- Upload Document ---
st.subheader("📤 Upload Document")

uploaded_file = st.file_uploader("Choose a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    if st.button("📤 Upload to Backend"):
        with st.spinner("Uploading and processing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)

                if response.status_code == 200:
                    st.success(f"✅ {uploaded_file.name} uploaded and embedded.")
                    st.json(response.json())
                else:
                    st.error("❌ Upload failed. Check backend logs.")
                    st.text(response.text)

            except Exception as e:
                st.error(f"❌ Connection error during upload:\n\n{e}")

# --- Ask a Question ---
st.subheader("💬 Ask a Question")

query = st.text_input("Enter your question:")

if st.button("Ask") and query:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={"query": query})

            if response.status_code == 200:
                data = response.json()
                st.markdown("### 🤖 Answer")
                st.success(data["answer"])

                with st.expander("📚 Retrieved Chunks"):
                    for i, chunk in enumerate(data["context_chunks"]):
                        st.markdown(f"**Chunk {i+1}:**\n```{chunk}```")
            else:
                st.error("❌ Chat failed. Check backend logs.")
                st.text(response.text)

        except Exception as e:
            st.error(f"❌ Connection error during chat:\n\n{e}")
