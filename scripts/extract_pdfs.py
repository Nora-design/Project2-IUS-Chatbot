import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs_from_ius_page(url, download_dir="data/pdfs"):
    os.makedirs(download_dir, exist_ok=True)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".pdf"):
            file_url = urljoin(url, href)
            file_name = os.path.basename(href.split("?")[0])  # remove query strings
            file_path = os.path.join(download_dir, file_name)

            pdf = requests.get(file_url)
            with open(file_path, "wb") as f:
                f.write(pdf.content)
            
            print(f"✅ Downloaded: {file_name}")
