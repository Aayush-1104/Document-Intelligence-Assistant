# For implementing Frontend
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="📄 Document Intelligence Assistant", layout="wide")

# --- Main Title ---
st.markdown("""
    <h1 style='text-align: center;'>📄 Document Intelligence Assistant</h1>
    <p style='text-align: center; color: gray;'>Upload a document and ask questions using RAG + Groq LLM</p>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.header("⚙️ System Info")
    st.success("**Backend:** FastAPI")
    st.info("**Vector DB:** FAISS")
    st.warning(f"**LLM:** `{os.getenv('GROQ_MODEL')}`")
    st.markdown("---")
    st.markdown("<small>Developed by Aayush 🚀</small>", unsafe_allow_html=True)

# --- Upload Section ---
st.subheader("📤 Upload Document")
st.markdown("Select a document below. Accepted formats: PDF, DOCX, TXT")

uploaded_file = st.file_uploader("", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    if st.button("📤 Upload to Backend"):
        with st.spinner("📄 Uploading and processing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)

                if response.status_code == 200:
                    st.success(f"✅ `{uploaded_file.name}` uploaded and embedded successfully.")
                    st.json(response.json())
                else:
                    st.error("❌ Upload failed. See logs below.")
                    st.text(response.text)

            except Exception as e:
                st.error(f"❌ Connection error during upload:\n\n{e}")

# --- QA Section ---
st.subheader("💬 Ask a Question")
st.markdown("Enter a question related to the uploaded document:")

query = st.text_input("Type your question here:")

if st.button("💡 Ask") and query:
    with st.spinner("🤔 Thinking..."):
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={"query": query})

            if response.status_code == 200:
                data = response.json()
                st.markdown("### 🤖 Answer")
                st.success(data["answer"])

                with st.expander("📚 Retrieved Chunks with Confidence"):
                    for i, item in enumerate(data["context_chunks"]):
                        st.markdown(f"**Chunk {i+1}** (confidence: `{item['score']}`)\n\n```{item['chunk']}```")
            else:
                st.error("❌ Chat failed. See logs below.")
                st.text(response.text)

        except Exception as e:
            st.error(f"❌ Connection error during chat:\n\n{e}")
