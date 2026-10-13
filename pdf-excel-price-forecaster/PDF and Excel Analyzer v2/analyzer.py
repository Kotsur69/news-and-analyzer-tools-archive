# -*- coding: utf-8 -*-

import os
import json
from openai import OpenAI
from tqdm import tqdm


class SteelMarketAnalyzer:
    def __init__(self, timeline_data, results_dir="results"):
        """
        timeline_data:
        {
          "2025.01": {
              "files": [
                  {
                      "filename": "...",
                      "role": "core/context/supplement",
                      "chunks": [...]
                  }
              ]
          }
        }
        """
        self.timeline = timeline_data

        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"
        )

        self.monthly_outputs = {}
        self.predictions = {}

        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)

    # --------------------------------------------------
    # 💾 ZAPIS PROGRESU
    # --------------------------------------------------
    def _save_progress(self):
        progress_file = os.path.join(self.results_dir, "progress.json")
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "monthly_outputs": self.monthly_outputs,
                    "predictions": self.predictions
                },
                f,
                ensure_ascii=False,
                indent=2
            )

    # --------------------------------------------------
    # 🔹 GŁÓWNY ENTRY POINT
    # --------------------------------------------------
    def run(self, limit_months=None, max_files_per_month=None):
        self._analyze_timeline(
            limit_months=limit_months,
            max_files_per_month=max_files_per_month
        )

        self._build_predictions(year="2026")

        output_file = os.path.join(self.results_dir, "full_analysis.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "monthly_outputs": self.monthly_outputs,
                    "predictions": self.predictions
                },
                f,
                ensure_ascii=False,
                indent=2
            )

        return self.predictions

    # --------------------------------------------------
    # 🔹 ANALIZA MIESIĘCZNA
    # --------------------------------------------------
    def _analyze_timeline(self, limit_months=None, max_files_per_month=None):
        months = sorted(self.timeline.keys())
        if limit_months:
            months = months[:limit_months]

        for month in tqdm(months, desc="Analiza miesięcy", unit="miesiąc", ncols=100):
            self.monthly_outputs[month] = self._analyze_month(
                month,
                max_files_per_month=max_files_per_month
            )

            # zapis po KAŻDYM miesiącu
            self._save_progress()

    def _analyze_month(self, month, max_files_per_month=None):
        files = self.timeline[month]["files"]
        if max_files_per_month:
            files = files[:max_files_per_month]

        core_text = []
        context_text = []

        for f in files:
            if f["role"] == "core":
                core_text.extend(f["chunks"])
            else:
                context_text.extend(f["chunks"])

        return {
            "core": self._analyze_with_prompt(month, "core", "\n".join(core_text)),
            "context": self._analyze_with_prompt(month, "context", "\n".join(context_text)),
        }

    # --------------------------------------------------
    # 🔹 ANALIZA Z CHUNKOWANIEM
    # --------------------------------------------------
    def _analyze_with_prompt(self, month, role, text, chunk_size=3000):
        if not text.strip():
            return "Brak danych."

        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        results = []

        for i, chunk in enumerate(chunks, 1):
            prompt = f"""
KONTEKST TECHNICZNY:
- Miesiąc danych: {month}
- Typ danych: {role}
- Chunk {i}/{len(chunks)}

ZASADY:
- Jeśli typ = core → analizuj price action i ceny
- Jeśli typ ≠ core:
  → NIE zmieniaj cen tego miesiąca
  → wpływ rozważaj dla kolejnych 1–3 miesięcy

{self._base_prompt()}

ARTYKUŁ / DANE:
{chunk}
"""
            try:
                result = self._call_llm(prompt)
            except Exception as e:
                print(f"❌ Błąd LLM w miesiącu {month}, chunk {i}: {e}")
                result = "Błąd w analizie."

            results.append(result)

        return "\n---\n".join(results)

    # --------------------------------------------------
    # 🔹 TWÓJ PROMPT (NIERUSZONY)
    # --------------------------------------------------
    def _base_prompt(self):
        return """
Jesteś zaawansowanym analitykiem rynku surowców,
specjalizującym się w price action, analizie trendów cenowych
oraz interpretacji danych makroekonomicznych i geopolitycznych.
Twoim celem jest analiza dokumentów PDF i Excel zawierających dane
o cenach stali, identyfikacja typów stali, analiza ich historycznych zmian cen
oraz predykcja przyszłych cen na podstawie danych liczbowych i tekstowych.
"""

    # --------------------------------------------------
    # 🔮 PREDYKCJE (BEZ PRZEPEŁNIENIA, STRUKTURA DLA WYKRESU)
    # --------------------------------------------------
    def _build_predictions(self, year, chunk_months=3):
        months = sorted(self.monthly_outputs.keys())
        predictions_chunks = []

        # finalna struktura: { "typ_stali": { "2026.01": { "price": ..., "change": ... }, ... } }
        predictions_dict = {}

        for i in range(0, len(months), chunk_months):
            sub_months = months[i:i + chunk_months]

            data_slice = {
                m: {
                    "core": self.monthly_outputs[m]["core"],
                    "context": self.monthly_outputs[m]["context"],
                }
                for m in sub_months
            }

            prompt = f"""
Masz analizy miesięczne 2024–2025.
Na ich podstawie:

- przewidź ceny miesięczne dla {year}
- osobno dla każdego typu stali
- podaj ceny, zmiany %, uzasadnienie
- wskaż ryzyka i alternatywne scenariusze

DANE HISTORYCZNE:
{data_slice}
"""
            try:
                result = self._call_llm(prompt)
            except Exception as e:
                print(f"❌ Błąd predykcji dla {sub_months}: {e}")
                result = "Błąd w predykcji."

            predictions_chunks.append(result)

            # 🟢 STRUKTURA DLA WYKRESU:
            # Na razie traktujemy wynik LLM jako string, można potem parsować do konkretnych cen.
            for month in sub_months:
                predictions_dict[month] = {"LLM_result": result}

        self.predictions[year] = predictions_dict
        self._save_progress()

    # --------------------------------------------------
    # 🤖 LLM CALL
    # --------------------------------------------------
    def _call_llm(self, prompt):
        response = self.client.chat.completions.create(
            model="mdeepseek-r1-distill-qwen-1.5b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400
        )
        return response.choices[0].message.content
