from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import os
import time
import sys

from app.services.file_handler import extract_text_from_file
from app.services.embedding import chunk_text, embed_and_store

router = APIRouter()
UPLOAD_DIR = "uploaded_docs"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print("📥 Received file:", file.filename)
    try:
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["pdf", "docx", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        save_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)

        print("📥 File saved:", save_path)

        # Step 1
        extracted_text = extract_text_from_file(save_path)
        print("📝 Text extracted.")

        # Step 2
        chunks = chunk_text(extracted_text)
        print("🧩 Chunks created:", len(chunks))

        # Step 3
        embed_and_store(chunks)
        print("📦 Embedded and stored.")

        # Flush + slight delay to avoid Streamlit's connection reset
        sys.stdout.flush()
        time.sleep(0.1)

        return JSONResponse(content={
            "filename": file.filename,
            "status": "✅ Uploaded successfully(embedding skipped)",
            "chunks": len(chunks)
        })

    except Exception as e:
        print("❌ Backend upload failed:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
