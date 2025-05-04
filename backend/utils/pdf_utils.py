import fitz
import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core import Document

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("❌ TOGETHER_API_KEY is missing. Please check your .env file.")

Settings.embed_model = TogetherEmbedding(
    model_name="BAAI/bge-base-en-v1.5",
    api_key=TOGETHER_API_KEY
)

Settings.llm = TogetherLLM(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    api_key=TOGETHER_API_KEY
)

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def get_answer(pdf_text, question):
    try:
        # Truncate pdf_text to fit token limits (approx 400 tokens)
        truncated_text = pdf_text[:1700]  # Rough estimation

        with open("temp.txt", "w") as f:
            f.write(truncated_text)

        reader = SimpleDirectoryReader(input_files=["temp.txt"])
        docs = reader.load_data()

        index = VectorStoreIndex.from_documents(docs)
        query_engine = index.as_query_engine()
        return query_engine.query(question).response

    except Exception as e:
        error_message = str(e)
        if "tokens + `max_new_tokens` must be <=" in error_message:
            return "❌ The input text is too long for the AI model. Please try uploading a shorter PDF or reduce the content."
    
        return "❌ Something went wrong while processing your request. Please try again later."