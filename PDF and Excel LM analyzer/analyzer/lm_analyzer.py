from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def analyze_article(article_text):
    prompt = f"""
Jesteś analitykiem rynku stali w Polsce i Europie.

ZADANIE:
1. Określ, czy artykuł dotyczy:
   - przeszłości
   - teraźniejszości
   - przyszłości

2. Wypisz FAKTY rynkowe:
   - ceny (jeśli podane)
   - rodzaj stali
   - grubość
   - region
   - czynniki wpływu

3. Wypisz HIPOTEZY / OPINIE autora.

4. Określ, czy artykuł nadaje się do:
   - generowania predykcji
   - ewaluacji wcześniejszych prognoz

5. Oceń wpływ wydarzeń opisanych w artykule na polski rynek:
   - Import, eksport, transport, logistyka
   - Potencjalne anomalie cenowe lub ryzyka

FORMAT JSON:
{{
  "time_scope": "",
  "polish_market_impact": "...",
  "market_facts": [],
  "opinions": [],
  "steel_products": [],
  "regions": [],
  "usable_for_prediction": true,
  "usable_for_evaluation": false
  "anomalies": ["..."]
}}

ARTYKUŁ:
{article_text}
"""

    response = client.chat.completions.create(
        model="mdeepseek-r1-distill-qwen-1.5b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=400
    )

    return response.choices[0].message.content
