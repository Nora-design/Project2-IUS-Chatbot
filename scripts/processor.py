import os
import json
import fitz  # PyMuPDF
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

PDF_DIR = "data/pdfs"
META_DIR = "data/metadata"

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection("ius_documents")

embedder = SentenceTransformer("all-MiniLM-L6-v2")
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def extract_text(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def process_pdf(pdf_name):
    print(f"📄 Processing: {pdf_name}")
    pdf_path = os.path.join(PDF_DIR, pdf_name)
    meta_path = os.path.join(META_DIR, pdf_name.replace(".pdf", ".json"))

    if not os.path.exists(meta_path):
        print(f"⚠️ Metadata not found for {pdf_name}")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    text = extract_text(pdf_path)
    chunks = splitter.split_text(text)
    embeddings = embedder.encode(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        chunk_id = f"{pdf_name}_{i}"
        collection.add(
            documents=[chunk],
            metadatas=[metadata],
            embeddings=[emb.tolist()],
            ids=[chunk_id]
        )

    print(f"✅ Stored {len(chunks)} chunks for {pdf_name}")

def run_all():
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            process_pdf(file)

if __name__ == "__main__":
    run_all()
