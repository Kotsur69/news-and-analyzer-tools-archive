# analyzer.py
import requests
import json
from prompts import STEEL_ANALYSIS_PROMPT

LMSTUDIO_URL = "http://localhost:1234/v1/responses"
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b"
HISTORY_FILE = "history.json"  # plik do przechowywania kontekstu

class LMAnalyzer:
    _instance = None

    @staticmethod
    def get_instance():
        """Zwraca singleton LMAnalyzer"""
        if LMAnalyzer._instance is None:
            LMAnalyzer._instance = LMAnalyzer()
        return LMAnalyzer._instance

    def __init__(self):
        if LMAnalyzer._instance is not None:
            raise Exception("To jest singleton – użyj get_instance()")
        # Ładowanie historii
        self.history = self.load_history()
        print("LMAnalyzer załadowany – gotowy do analizy.")

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"prompt": STEEL_ANALYSIS_PROMPT, "articles": [], "analysis": ""}

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def analyze(self, new_articles: list[str]) -> str:
        """Analizuje nowe artykuły i zwraca wynik analizy"""
        # Filtrowanie tylko nowych artykułów
        new_articles_filtered = [a for a in new_articles if a not in self.history["articles"]]
        if not new_articles_filtered:
            return "Brak nowych artykułów do analizy."

        combined_text = "\n\n".join(new_articles_filtered)
        self.history["articles"].extend(new_articles_filtered)

        # Tworzymy prompt dla LM Studio
        history_prompt = self.history["prompt"] + "\n\nNOWE ARTYKUŁY:\n" + combined_text
        if self.history["analysis"]:
            history_prompt += "\n\nPOPPRZEDNIA ANALIZA:\n" + self.history["analysis"]

        payload = {
            "model": MODEL_NAME,
            "input": history_prompt,
            "max_output_tokens": 15000,
            "temperature": 0.2
        }

        try:
            response = requests.post(LMSTUDIO_URL, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Błąd połączenia z LM Studio: {e}")

        data = response.json()
        analysis = data.get("output_text", str(data))  # fallback dla debugowania

        # Aktualizacja historii
        self.history["analysis"] += "\n\n" + analysis
        self.save_history()

        return analysis
