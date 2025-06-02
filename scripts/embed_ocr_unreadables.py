import os
import shutil
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from chromadb import HttpClient
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
client = HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection("ius_documents")

def is_pdf_readable(path):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return len(text.strip()) > 100
    except:
        return False

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang="eng")
    return text.strip()

def embed_ocr_pdfs(data_dir="./data"):
    scanned_dir = os.path.join(data_dir, "scanned")
    os.makedirs(scanned_dir, exist_ok=True)

    for file in os.listdir(data_dir):
        if not file.endswith(".pdf"):
            continue

        path = os.path.join(data_dir, file)

        if is_pdf_readable(path):
            continue  # Skip readable files

        print(f"🟡 Unreadable: {file} → Processing with OCR")

        # Move to scanned/
        dest = os.path.join(scanned_dir, file)
        shutil.move(path, dest)

        text = extract_text_with_ocr(dest)

        if len(text.strip()) == 0:
            print(f"❌ OCR failed: {file}")
            continue

        # Optional: Save extracted text to txt for review
        with open(dest.replace(".pdf", ".txt"), "w", encoding="utf-8") as f:
            f.write(text)

        # Add to Chroma
        doc_id = file.replace(".pdf", "").lower().replace(" ", "_")
        collection.add(
            documents=[text],
            metadatas=[{
                "filename": file,
                "source": "OCR",
                "extracted_via": "ocr"
            }],
            ids=[doc_id]
        )

        print(f"✅ Embedded {file} via OCR")

