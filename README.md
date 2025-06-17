# 📄 Document Intelligence Assistant

A full-stack GenAI-powered assistant that ingests documents (PDF, TXT, DOCX), generates vector embeddings, performs semantic search with RAG (Retrieval Augmented Generation), and answers user questions using Groq LLM.

---

## 🚀 Features

### ✅ Document Processing Pipeline

* Upload support: PDF, TXT, DOCX
* Text extraction via PyPDF2, python-docx, plain `.txt`
* Text chunking: `RecursiveCharacterTextSplitter`
* Embedding model: `all-MiniLM-L6-v2` via HuggingFace
* Vector DB: FAISS (switched from Chroma due to Windows stability)

### 💬 RAG Pipeline

* Similarity search via FAISS
* Question-answering via Groq LLM (`llama3-8b-8192`)
* Context-aware prompt construction

### 🧠 LLM Integration

* Primary: Groq
* Fallback ready: Easily extendable to OpenRouter or Gemini

### 🌐 Frontend

* Built with Streamlit
* Document uploader
* Question box
* Answer + retrieved context display

---

## 🛠️ Tech Stack

* **Backend**: FastAPI
* **Frontend**: Streamlit
* **Embeddings**: HuggingFace
* **LLM**: Groq API (`llama3-8b-8192`)
* **Vector DB**: FAISS

---

## 📁 Folder Structure

```
├── app
│   ├── routes         # FastAPI route handlers (upload, chat)
│   ├── services       # Core logic (embedding, file_handler, semantic_search)
│   └── main.py        # FastAPI entrypoint
├── streamlit_app.py   # Frontend
├── vectordb_faiss     # Saved FAISS index
├── uploaded_docs      # Stored user-uploaded files
├── .env               # API keys and model config
```

---

## 🧪 Setup Instructions

### 1. Clone Repo

```bash
git clone <repo-url>
cd document-intelligence-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env`

```env
GROQ_API_KEY=your_groq_api_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama3-8b-8192
```

### 5. Run Backend

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 6. Run Frontend

```bash
streamlit run streamlit_app.py
```

---

## 🧠 Prompt Engineering

```text
Use the following context to answer the user question:
[...top chunks...]
Question: <user input>
Answer:
```

System prompt ensures helpful, grounded responses.

---

## 🔍 Future Enhancements

* Add support for images via OCR
* Enable multi-LLM fallback (e.g. OpenRouter)
* Add document summarization & query rewriting
* Integrate logging, streaming, and chunk metadata

---

## 📬 Author

Developed by Aayush 🚀
