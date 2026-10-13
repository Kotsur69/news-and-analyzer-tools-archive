# -*- coding: utf-8 -*-

import json
from datetime import datetime
from analyzer.local_lm import LocalLM





def load_history(path="memory/historical_data.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def build_prediction_prompt(article_text, history):
    return f"""
Jesteś polskim analitykiem rynku stali.

DANE HISTORYCZNE (wcześniejsze prognozy):
{json.dumps(history[-5:], ensure_ascii=False, indent=2)}

NOWY ARTYKUŁ:
{article_text}

ZADANIE:
1. Wygeneruj prognozę cen stali (rodzaj, grubość, zakres cenowy).
2. Określ confidence score (0–100).
3. Określ risk score (0–100).
4. Wypisz założenia predykcji.
5. Wypisz potencjalne czynniki ryzyka.

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


def generate_prediction(article_text):
    history = load_history()
    prompt = build_prediction_prompt(article_text, history)

    response = lm.generate(prompt)

    try:
        prediction = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("LM zwrócił niepoprawny JSON")

    prediction["created_at"] = datetime.utcnow().isoformat()
    prediction["status"] = "active"

    return prediction
