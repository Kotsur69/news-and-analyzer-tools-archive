import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10
MAX_LINKS_PER_PAGE = 1
MAX_PAGES_PER_DOMAIN = 1
DELAY = 1


def normalize(url):
    return url.split("#")[0].rstrip("/")


class DomainCrawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.queue = deque([start_url])
        self.visited = set()
        self.articles = []

    def same_domain(self, url):
        return urlparse(url).netloc == self.domain

    def extract_links(self, soup, base_url):
        links = []

        for a in soup.find_all("a", href=True):
            href = normalize(urljoin(base_url, a["href"]))

            if self.same_domain(href) and href not in self.visited:
                links.append(href)

            if len(links) >= MAX_LINKS_PER_PAGE:
                break

        return links

    def scrape_article(self, soup):
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)

        if len(text) > 500:
            return text

        return None

    def crawl(self):
        while self.queue and len(self.visited) < MAX_PAGES_PER_DOMAIN:
            url = self.queue.popleft()

            if url in self.visited:
                continue

            print(f"🕷️ [{self.domain}] {url}")
            self.visited.add(url)

            try:
                r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")

                article = self.scrape_article(soup)
                if article:
                    self.articles.append(article)

                links = self.extract_links(soup, url)
                for link in links:
                    self.queue.append(link)

                time.sleep(DELAY)

            except Exception as e:
                print(f"❌ {url}: {e}")

        return self.articles
