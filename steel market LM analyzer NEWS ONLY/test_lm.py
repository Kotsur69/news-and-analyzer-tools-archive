import requests

LMSTUDIO_URL = "http://localhost:1234/v1/models"  # zmień port jeśli inny

try:
    response = requests.get(LMSTUDIO_URL, timeout=5)
    response.raise_for_status()
    print("✅ LM Studio działa, odpowiedź serwera:")
    print(response.json())
except Exception as e:
    print("❌ Nie udało się połączyć z LM Studio:")
    print(e)
    response = requests.post(LMSTUDIO_URL, json=payload, timeout=600)
response.raise_for_status()
print(response.json())  # <--- dodaj to tymczasowo
