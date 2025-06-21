from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF

app = FastAPI()

def extract_text_from_pdf(file_bytes):
    """Extracts text from PDF using PyMuPDF (fitz)."""
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)

        if not text.strip():
            return JSONResponse(status_code=400, content={"error": "No text found in the uploaded PDF."})

        return {"filename": file.filename, "text": text}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
