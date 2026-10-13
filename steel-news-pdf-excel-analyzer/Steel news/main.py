import time
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

# 🔹 Ładujemy PDF + Excel RAZ
extra_docs_chunks = load_all_documents(chunk_size=3000) or []

for url in urls:
    article = scrape_article(url)

    # Łączymy artykuł + wszystkie chunk-i PDF/Excel
    combined_chunks = [article.get("content", "")] + extra_docs_chunks

    start_time = time.time()
    analysis_parts = []

    # Analiza po chunkach
    for i, chunk in enumerate(combined_chunks, 1):
        analysis_chunk = analyze_article(chunk)
        analysis_parts.append(analysis_chunk)

        # partial save po każdym chunku
        partial_result = {
            "url": article.get("url", url),
            "title": article.get("title", ""),
            "date": article.get("date", ""),
            "chunk_index": i,
            "analysis_so_far": "\n\n".join(analysis_parts)
        }
        save_to_json(results + [partial_result], filename="data/steel_news_partial.json")

        # progress w konsoli
        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining = avg_time * (len(combined_chunks) - i)
        print(f"[{article.get('title','Brak tytułu')}] Chunk {i}/{len(combined_chunks)} - "
              f"Avg: {avg_time:.2f}s, Estimated remaining: {remaining:.2f}s")

    # Łączymy fragmenty w pełną analizę
    full_analysis = "\n\n".join(analysis_parts)

    results.append({
        "url": article.get("url", url),
        "title": article.get("title", ""),
        "date": article.get("date", ""),
        "analysis": full_analysis
    })

# 🔹 Zapis wyników końcowych
save_to_json(results, filename="data/steel_news_analysis.json")
save_to_csv(results, filename="data/steel_news_analysis.csv")

print("Gotowe! Wyniki zapisane w folderze data/")
