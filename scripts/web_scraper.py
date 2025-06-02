import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

DATA_DIR = "data"
RAW_HTML_DIR = os.path.join(DATA_DIR, "raw_html")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
META_DIR = os.path.join(DATA_DIR, "metadata")

for d in [RAW_HTML_DIR, PDF_DIR, META_DIR]:
    os.makedirs(d, exist_ok=True)

# Setup headless browser
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def detect_lang(text):
    try:
        return detect(text)
    except:
        return "unknown"

def process_page(url, category="General"):
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Extract and save page text
    body = soup.get_text(separator="\n")
    filename_base = url.strip("/").split("/")[-1] or "index"
    lang = detect_lang(body)
    text_path = os.path.join(RAW_HTML_DIR, f"{filename_base}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(body)

    # Save page metadata
    metadata = {
        "source_url": url,
        "filename": f"{filename_base}.txt",
        "category": category,
        "language": lang
    }
    meta_path = os.path.join(META_DIR, f"{filename_base}.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"📝 Text saved for {url}")

    # Look for PDFs
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.lower().endswith(".pdf"):
            pdf_url = urljoin(url, href)
            pdf_name = os.path.basename(href.split("?")[0])
            pdf_path = os.path.join(PDF_DIR, pdf_name)

            r = requests.get(pdf_url)
            with open(pdf_path, "wb") as f:
                f.write(r.content)
            print(f"📄 PDF downloaded: {pdf_name}")

            # Save metadata for PDF
            pdf_meta = {
                "source_url": url,
                "filename": pdf_name,
                "category": category,
                "language": detect_lang(pdf_name)
            }
            with open(os.path.join(META_DIR, pdf_name.replace(".pdf", ".json")), "w", encoding="utf-8") as f:
                json.dump(pdf_meta, f, ensure_ascii=False, indent=2)

def load_links(file="C:\Users\Emre Sevinç\Downloads\Cleaned_IUS_URLs.csv"):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.startswith("http")]

def run_all():
    urls = load_links()
    for url in urls:
        print(f"🔗 Processing: {url}")
        process_page(url)

if __name__ == "__main__":
    run_all()
