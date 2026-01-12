import json

# œcie¿ka do pliku
file_path = "data/steel_news_analysis.json"

# wczytanie danych
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# sprawdzenie ile rekordów
print(f"Liczba artyku³ów: {len(data)}")

# podgl¹d pierwszego elementu
print(json.dumps(data[0], indent=4, ensure_ascii=False))
