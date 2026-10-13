# -*- coding: utf-8 -*-

import json
from datetime import datetime
from analyzer.local_lm import LocalLM  # Twój wrapper LM Studio

# 🔹 Inicjalizacja LM globalnie
lm = LocalLM()  # jeśli Twój wrapper wymaga konfiguracji, dodaj np. model_name

# 🔹 Wczytywanie historii predykcji
def load_history(path="memory/historical_data.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 🔹 Tworzenie promptu dla LM
def build_prediction_prompt(article_text, history):
    return f"""
Jesteś polskim analitykiem rynku stali.

DANE HISTORYCZNE (ostatnie 5 prognoz):
{json.dumps(history[-5:], ensure_ascii=False, indent=2)}

NOWY ARTYKUŁ:
{article_text}

ZADANIE:
1. Wygeneruj prognozę cen stali (rodzaj, grubość, zakres cenowy).
2. Określ confidence score (0–100).
3. Określ risk score (0–100).
4. Wypisz założenia predykcji.
5. Wypisz potencjalne czynniki ryzyka.
6. Wypisz wpływ na polski rynek (pole: "polish_market_impact").

FORMAT JSON:
{{
  "steel_type": "",
  "thickness": "",
  "predicted_price_range": "",
  "prediction_horizon": "",
  "confidence_score": 0,
  "risk_score": 0,
  "polish_market_impact": "...",
  "assumptions": [],
  "risk_factors": []
}}
"""

# 🔹 Funkcja generująca predykcję
def generate_prediction(article_text):
    history = load_history()
    prompt = build_prediction_prompt(article_text, history)

    # 🔹 Wywołanie LM (tutaj używamy chat(), zmień jeśli Twój wrapper ma inną nazwę)
    response_text = lm.chat(prompt)

    # 🔹 Parsowanie JSON
    try:
        prediction = json.loads(response_text)
    except json.JSONDecodeError:
        # Jeśli LM zwróci niepoprawny JSON, zwracamy pustą strukturę
        prediction = {
            "steel_type": "",
            "thickness": "",
            "predicted_price_range": "",
            "prediction_horizon": "",
            "confidence_score": 0,
            "risk_score": 0,
            "polish_market_impact": "",
            "assumptions": [],
            "risk_factors": []
        }

    # 🔹 Dodanie metadanych
    prediction["created_at"] = datetime.utcnow().isoformat()
    prediction["status"] = "active"

    return prediction
