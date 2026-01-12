import time
from analyzer.predictor import generate_prediction
from utils.data_loader import load_all_documents
from utils.storage import save_to_json, save_to_csv
from tqdm import tqdm


# 🔹 Wczytanie wszystkich dokumentów (PDF + Excel) jako chunk-i
chunks = load_all_documents(chunk_size=4000) or []

results = []

total_chunks = len(chunks)
print(f"Znaleziono {total_chunks} chunków do analizy.\n")

start_time_total = time.time()

for i, chunk in enumerate(chunks, 1):
    start_time = time.time()
    
    # 🔹 Generowanie predykcji
    analysis = generate_prediction(chunk)
    
    results.append({
        "chunk_index": i,
        "analysis": analysis
    })
    
    # 🔹 Partial save
    save_to_json(results, filename="data/documents_partial.json")
    
    # 🔹 Progress bar / procent
    percent_done = (i / total_chunks) * 100
    elapsed = time.time() - start_time_total
    avg_time = elapsed / i
    remaining = avg_time * (total_chunks - i)
    
    print(f"Chunk {i}/{total_chunks} ({percent_done:.1f}%) - "
          f"Avg: {avg_time:.2f}s, Estimated remaining: {remaining/60:.2f} min")

# 🔹 Zapis końcowy
save_to_json(results, filename="data/documents_analysis.json")
save_to_csv(results, filename="data/documents_analysis.csv")

print("\nGotowe! Wyniki zapisane w folderze data/")
