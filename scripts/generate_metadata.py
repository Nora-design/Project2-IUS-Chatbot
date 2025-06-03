import os
import json
import re

PDF_DIR = "data/pdfs"
META_DIR = "data/metadata"
os.makedirs(META_DIR, exist_ok=True)

def detect_language_from_filename(name):
    if "eng" in name.lower() or "en" in name.lower():
        return "EN"
    elif "ba" in name.lower():
        return "BA"
    return "Unknown"

def infer_category_from_filename(name):
    name = re.sub(r"[\d\-_]+", " ", name)  # remove numbers/dashes/underscores
    name = name.replace(".pdf", "").strip().lower()
    words = name.split()
    # pick top 3-6 meaningful words as rough category
    keywords = [w for w in words if len(w) > 3]
    return " ".join(keywords[:6]) if keywords else "General"

def generate_metadata(pdf_name):
    language = detect_language_from_filename(pdf_name)
    category = infer_category_from_filename(pdf_name)
    metadata = {
        "filename": pdf_name,
        "source_url": "", 
        "category": category,
        "language": language
    }
    json_name = pdf_name.replace(".pdf", ".json")
    with open(os.path.join(META_DIR, json_name), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"✅ Metadata saved for: {pdf_name}")

def run_for_all_pdfs():
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            generate_metadata(file)

if __name__ == "__main__":
    run_for_all_pdfs()
