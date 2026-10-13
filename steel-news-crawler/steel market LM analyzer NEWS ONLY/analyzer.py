import requests
import json
from prompts import STEEL_ANALYSIS_PROMPT

LMSTUDIO_URL = "http://localhost:1234/v1/responses"
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b"
HISTORY_FILE = "history.json"  # plik do przechowywania kontekstu

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"prompt": STEEL_ANALYSIS_PROMPT, "articles": [], "analysis": ""}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def analyze_with_local_llm(new_articles: list[str]) -> str:
    history = load_history()

    # Filtrowanie tylko nowych artykułów (unikalne)
    new_articles_filtered = [a for a in new_articles if a not in history["articles"]]
    if not new_articles_filtered:
        return "Brak nowych artykułów do analizy."

    # Dodaj nowe artykuły do historii
    combined_text = "\n\n".join(new_articles_filtered)
    history["articles"].extend(new_articles_filtered)

    # Tworzymy prompt dla LM Studio
    history_prompt = history["prompt"] + "\n\nNOWE ARTYKUŁY:\n" + combined_text
    if history["analysis"]:
        history_prompt += "\n\nPOPPRZEDNIA ANALIZA:\n" + history["analysis"]

    payload = {
        "model": MODEL_NAME,
        "input": history_prompt,
        "max_output_tokens": 15000,
        "temperature": 0.2
    }

    response = requests.post(LMSTUDIO_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    if "output_text" in data:
        analysis = data["output_text"]
    else:
        analysis = str(data)  # fallback dla debugowania

    # Aktualizujemy historię
    history["analysis"] += "\n\n" + analysis
    save_history(history)

    return analysis
