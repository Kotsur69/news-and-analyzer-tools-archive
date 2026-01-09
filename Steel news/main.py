from scraper.scraper import scrape_article
from analyzer.lm_analyzer import analyze_article
from utils.storage import save_to_json, save_to_csv
from utils.data_loader import load_all_documents

urls = [
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

results = []

results = []

# 🔹 Ładujemy PDF + Excel RAZ
extra_docs_chunks = load_all_documents(chunk_size=3000)

for url in urls:
    article = scrape_article(url)

    # Łączymy artykuł + wszystkie chunk-i PDF/Excel
    combined_text_chunks = [article.get("content", "")] + extra_docs_chunks

    # Analiza po chunkach
    analysis_parts = []
    for chunk in combined_text_chunks:
        analysis_chunk = analyze_article(chunk)
        analysis_parts.append(analysis_chunk)

    # Łączymy fragmenty w jedną analizę
    full_analysis = "\n\n".join(analysis_parts)

    results.append({
        "url": url,
        "title": article.get("title", ""),
        "date": article.get("date", ""),
        "analysis": full_analysis
    })

# 🔹 Zapis wyników
save_to_json(results)
save_to_csv(results)

print("Gotowe! Wyniki zapisane w folderze data/")