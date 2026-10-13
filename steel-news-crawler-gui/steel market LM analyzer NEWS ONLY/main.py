from multi_domain_crawler import DomainCrawler
from analyzer import LMAnalyzer  # nowy singleton

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
    "https://www.steelorbis.com/",
    "https://www.onet.pl/premium/diewelt?utm_source=google&utm_medium=cpc&utm_campaign=dsapremium_google_acq_paid&utm_content=display&tpcc=dsapremium_google_acq_paid&gad_source=1&gad_campaignid=22983951836&gclid=CjwKCAiAmp3LBhAkEiwAJM2JUHIzE7x-K_6UH33k_vlcH0Ph7tecOKwwHyqZ6pmzoZKKpzGQrsnKThoCq8AQAvD_BwE"
]

def main():
    all_articles = []

    # Crawlowanie artykułów
    for url in URLS:
        crawler = DomainCrawler(url)
        articles = crawler.crawl()
        all_articles.extend(articles)

    if not all_articles:
        print("Brak artykułów do analizy.")
        return

    # Tworzymy singleton analizatora
    analyzer = LMAnalyzer.get_instance()

    # Analiza artykułów
    analysis = analyzer.analyze(all_articles)

    print("\n📊 AKTUALIZOWANA ANALIZA RYNKU STALI:\n")
    print(analysis)

    # Zapis do pliku tekstowego
    with open("last_analysis.txt", "w", encoding="utf-8") as f:
        f.write(analysis)

if __name__ == "__main__":
    main()
