# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_article(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else "Brak tytulu"
    content = " ".join([p.text for p in soup.find_all("p")])
    date = datetime.now().strftime("%Y-%m-%d")
    
    return {"url": url, "title": title, "content": content, "date": date}
