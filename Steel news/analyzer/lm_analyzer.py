from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # cokolwiek, LM Studio tego nie sprawdza
)

def analyze_article(article_text):
    prompt = f"""
Analizuj artykuł o rynku stali i wypisz:
1. Prognozę cen stali (rodzaj, grubość, przewidywana cena)
2. Informacje o transporcie, imporcie i logistyce
3. W skróconej formie (bullet points)

Artykuł:
{article_text}
"""

    response = client.chat.completions.create(
        model="mistralai/ministral-3-3b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content
