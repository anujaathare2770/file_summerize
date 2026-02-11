from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from summarizer import summarize



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/summarize-file")
async def summarize_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        print("Received:", file.filename)
        print("File size:", len(contents))

        if not contents:
            return {"summary": "File is empty"}

        filename = file.filename.lower()

        if filename.endswith(".txt"):
            text = contents.decode("utf-8", errors="ignore")

        elif filename.endswith(".pdf"):
            from io import BytesIO
            reader = PdfReader(BytesIO(contents))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

        else:
            return {"summary": "Only TXT and PDF allowed"}

        if not text.strip():
            return {"summary": "No readable text found in file"}

        summary = summarize(text)

        return {"summary": summary}

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return {"summary": f"Server error: {str(e)}"}
