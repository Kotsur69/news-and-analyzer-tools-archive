import json
import csv
from pathlib import Path

DATA_DIR = Path("data")

def save_to_json(data, filename="steel_news_analysis.json"):
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_csv(data, filename="steel_news_analysis.csv"):
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename

    if not data:
        print("Brak danych do zapisu CSV")
        return

    # 🔹 zbierz WSZYSTKIE
