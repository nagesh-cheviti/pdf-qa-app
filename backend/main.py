from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.pdf_utils import extract_text_from_pdf, get_answer
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    for existing_file in os.listdir(UPLOAD_DIR):
        file_path_to_delete = os.path.join(UPLOAD_DIR, existing_file)
        if os.path.isfile(file_path_to_delete):
            os.remove(file_path_to_delete)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename}

@app.post("/ask")
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    file_path = f"{UPLOAD_DIR}/{filename}"
    content = extract_text_from_pdf(file_path)
    answer = get_answer(content, question)
    return JSONResponse(content={"answer": answer})

