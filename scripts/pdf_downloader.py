from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urljoin
import json
from langdetect import detect

def detect_language_from_filename(name):
    try:
        lang = detect(name)
        return "EN" if lang == "en" else "BA"
    except:
        return "unknown"

def generate_metadata(file_name, source_url, category):
    return {
        "filename": file_name,
        "source_url": source_url,
        "category": category,
        "language": detect_language_from_filename(file_name)
    }

def download_pdfs_with_selenium(page_url, category, download_dir="data/pdfs"):
    os.makedirs(download_dir, exist_ok=True)

    # Set up headless browser
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(page_url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Inside your selenium script, after soup is created:
        for tag in soup.find_all():
            if ".pdf" in str(tag).lower():
                print("🧠 Found possible PDF tag:")
                print(tag)


        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.lower().endswith(".pdf"):
                file_url = urljoin(page_url, href)
                file_name = os.path.basename(href.split("?")[0])
                file_path = os.path.join(download_dir, file_name)

                response = requests.get(file_url)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Downloaded: {file_name}")

                metadata = generate_metadata(file_name, page_url, category)
                with open(file_path.replace(".pdf", ".json"), "w", encoding="utf-8") as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                print(f"📄 Metadata saved for: {file_name}")

    finally:
        driver.quit()
