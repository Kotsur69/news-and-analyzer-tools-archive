import requests

LMSTUDIO_URL = "http://localhost:1234/v1/completions"
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b"

payload = {
    "model": MODEL_NAME,
    "prompt": "Hello LM Studio! Napisz krótko, co wiesz o stali.",
    "max_tokens": 150,
    "temperature": 0.2
}

try:
    response = requests.post(LMSTUDIO_URL, json=payload, timeout=60)
    response.raise_for_status()
    print("✅ Model odpowiedział:")
    print(response.json())  # <--- wypisz cały JSON, zobaczymy strukturę
except Exception as e:
    print("❌ Błąd połączenia lub model nie odpowiada:")
    print(e)
