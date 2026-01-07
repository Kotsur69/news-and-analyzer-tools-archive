import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import json

# =========================
# KONFIGURACJA
# =========================
INPUT_XLSX = "data/steel_monthly_summary.xlsx"

OUTPUT_DIR = "output"
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

YEARS = ["2024", "2025"]
FORECAST_YEAR = "2026"

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_MODEL = "mistralai/ministral-3-14b-reasoning"

SEASONS = {
    "ZIMA": [12, 1, 2],
    "WIOSNA": [3, 4, 5],
    "LATO": [6, 7, 8],
    "JESIEŃ": [9, 10, 11]
}

# =========================
# FUNKCJE
# =========================
def month_to_season(month):
    for season, months in SEASONS.items():
        if month in months:
            return season
    return "N/A"

def ask_llm(prompt):
    response = requests.post(
        LM_STUDIO_URL,
        json={
            "model": LM_MODEL,
            "messages": [
                {"role": "system", "content": "Jesteś analitykiem biznesowym rynku stali."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        },
        timeout=120
    )
    return response.json()["choices"][0]["message"]["content"]

# =========================
# WCZYTANIE EXCELA
# =========================
df = pd.read_excel(INPUT_XLSX)




steel_types = df.columns[1:-2]  # kolumny ze stalą

for steel in steel_types:


    df["Year"] = df["Month"].astype(str).str[:4]
    df["MonthNum"] = df["Month"].astype(str).str[5:7].astype(int)

steel_types = df.columns[1:-2]

# =========================
# WYKRESY
# =========================
for year in YEARS:
    for steel in steel_types:
        data = df[df["Year"] == year].sort_values("MonthNum")

        plt.figure()
        plt.plot(data["MonthNum"], data[steel], marker="o")
        plt.title(f"{steel} – zakupy w {year}")
        plt.xlabel("Miesiąc")
        plt.ylabel("Ilość (tony)")
        plt.xticks(range(1, 13))
        plt.grid(True)

        plt.savefig(f"{CHART_DIR}/{year}_{steel}.png")
        plt.close()

# =========================
# PROGNOZA
# =========================
forecast = []

for steel in steel_types:
    for month in range(1, 13):
        values = df[df["MonthNum"] == month][steel].values
        forecast_value = round(np.mean(values)) if len(values) else 0

        forecast.append({
            "Month": f"{FORECAST_YEAR}-{month:02d}",
            "Steel": steel,
            "Forecast_tons": forecast_value
        })

forecast_df = pd.DataFrame(forecast)
forecast_df.to_csv(f"{OUTPUT_DIR}/forecast_2026.csv", index=False)

# =========================
# PROMPT DLA AI
# =========================
summary = df.groupby(["Year"])[steel_types].sum().to_dict()

prompt = f"""
Dane przedstawiają miesięczne zakupy stali z lat 2024–2025.

Podsumowanie roczne (tony):
{json.dumps(summary, indent=2)}

Prognoza na 2026 znajduje się w danych.

Napisz raport biznesowy w języku polskim:
- wskaż trendy sezonowe
- porównaj lata 2024 i 2025
- wskaż najczęściej kupowane typy stali
- opisz zachowanie rynku wiosną i jesienią
- dodaj rekomendacje zakupowe na 2026
"""

report = ask_llm(prompt)

with open(f"{OUTPUT_DIR}/business_report_ai.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("✅ Analiza, wykresy, prognoza i raport AI gotowe")
