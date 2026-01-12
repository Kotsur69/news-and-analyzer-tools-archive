# -*- coding: utf-8 -*-

import json
from datetime import datetime
from analyzer.local_lm import LocalLM

lm = LocalLM(model_name="eepseek-r1-distill-qwen-1.5b")


def build_evaluation_prompt(prediction, new_article):
    return f"""
Jesteś Polskim analitykiem rynku stali.

WCZEŚNIEJSZA PREDYKCJA:
{json.dumps(prediction, ensure_ascii=False, indent=2)}

NOWY ARTYKUŁ (nowsze dane rynkowe):
{new_article}

ZADANIE:
1. Oceń trafność predykcji:
   - trafiona
   - częściowo trafiona
   - błędna
2. Porównaj prognozowaną cenę z aktualną sytuacją.
3. Jeśli nietrafiona:
   - wyjaśnij przyczyny
   - wskaż anomalie (polityczne, logistyczne, regulacyjne)
4. Zaproponuj skorygowany model myślenia.

FORMAT JSON:
{{
  "evaluation_result": "",
  "price_deviation": "",
  "anomalies": [],
  "explanation": "",
  "corrected_reasoning": "",
  "updated_confidence_score": 0
}}
"""


def evaluate_prediction(prediction, new_article_text):
    prompt = build_evaluation_prompt(prediction, new_article_text)
    response = lm.generate(prompt)

    try:
        evaluation = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("LM zwrócił niepoprawny JSON")

    evaluation["evaluated_at"] = datetime.utcnow().isoformat()
    evaluation["prediction_id"] = prediction.get("created_at")

    return evaluation
