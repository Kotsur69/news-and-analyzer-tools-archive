from multi_domain_crawler import DomainCrawler
from analyzer import analyze_with_local_llm

URLS = [
    "https://www.wnp.pl/tematy/hutnictwo,7178.html",
    "https://mepsinternational.com/gb/en/news",
    "https://puds.pl",
    "https://gmk.center/en/",
    "https://www.kallanish.com/en/news/steel/free-content/",
    "https://www.euronews.com/tag/steel-industry",
    "https://mepsinternational.com/gb/en/landing-page/stainless-steel/europe",
    "https://www.hiph.org/GLOWNA/aktual.php",
    "https://www.piks.com.pl/",
    "https://www.steelonthenet.com/news/regions/europe.php",
    "https://worldsteel.org/",
    "https://www.steelorbis.com/"
]

def main():
    all_articles = []

    for url in URLS:
        crawler = DomainCrawler(url)
        articles = crawler.crawl()
        all_articles.extend(articles)

    if not all_articles:
        print("Brak artykułów")
        return

    analysis = analyze_with_local_llm(all_articles)
    print("\n📊 ANALIZA RYNKU STALI:\n")
    print(analysis)

if __name__ == "__main__":
    main()
