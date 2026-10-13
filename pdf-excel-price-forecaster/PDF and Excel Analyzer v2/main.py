import os
import json
from utils.data_loader import load_pdfs, load_excels, merge_data
from analyzer import SteelMarketAnalyzer
import matplotlib.pyplot as plt

DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdf")
EXCEL_DIR = os.path.join(DATA_DIR, "excel")


def main():
    print("=== START ANALIZY RYNKU STALI ===\n")

    # 1. Wczytanie danych
    print("📂 Ładowanie plików PDF...")
    pdf_data = load_pdfs(PDF_DIR)

    print("📊 Ładowanie plików Excel...")
    excel_data = load_excels(EXCEL_DIR)

    # 2. Połączenie danych (liczbowe + tekstowe)
    print("🔗 Scalanie danych...")
    merged_data = merge_data(
        pdf_data=pdf_data,
        excel_data=excel_data
    )

    # 3. Inicjalizacja analizatora
    analyzer = SteelMarketAnalyzer(timeline_data=merged_data)

    # 4. Analiza + predykcje w jednym kroku
    print("📈 Analiza miesięcy i generowanie predykcji...")
    predictions_2026 = analyzer.run(limit_months=2, max_files_per_month=2)

    # 5. Zapis analizy i predykcji do JSON
    output_json_path = os.path.join(DATA_DIR, "analysis_results.json")
    full_results = {
        "monthly_analysis": analyzer.monthly_outputs,
        "predictions_2026": predictions_2026
    }
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(full_results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Analiza i predykcje zapisane w: {output_json_path}")

    # 6. Wykres predykcji (bez pola 'price', LLM string jako placeholder)
    print("📊 Tworzenie wykresu predykcji...")
    plt.figure(figsize=(12, 6))

    # Jeżeli predictions_2026["2026"] zawiera tylko LLM_result jako string
    for steel_type, content in predictions_2026.items():
        if isinstance(content, dict):
            months_sorted = sorted(content.keys())
            # używamy indeksu jako placeholder ceny
            prices = list(range(1, len(months_sorted) + 1))
            plt.plot(months_sorted, prices, marker='o', label=steel_type)
        else:
            # jeśli LLM zwrócił string
            months_sorted = ["2026.01", "2026.02"]  # placeholder dla dwóch miesięcy
            prices = [1, 2]
            plt.plot(months_sorted, prices, marker='o', label="LLM_result")

    plt.title("Predykcje cen stali na 2026 (placeholdery)")
    plt.xlabel("Miesiąc")
    plt.ylabel("Cena (placeholder)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
