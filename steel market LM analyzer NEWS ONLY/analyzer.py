import requests
from prompts import STEEL_ANALYSIS_PROMPT

LMSTUDIO_URL = "http://localhost:1234/v1/responses"
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b"

def analyze_with_local_llm(articles: list[str]) -> str:
    combined_text = "\n\n".join(articles)
    prompt = STEEL_ANALYSIS_PROMPT + "\n\nARTYKUŁY:\n" + combined_text

    payload = {
        "model": MODEL_NAME,
        "input": prompt,             # <- tutaj LM Studio oczekuje 'input'
        "max_output_tokens": 15000,   # <- zamiast max_tokens
        "temperature": 0.2
    }

    response = requests.post(LMSTUDIO_URL, json=payload, timeout=600)
    response.raise_for_status()

    data = response.json()
    # LM Studio /v1/responses używa "output_text" lub choices
    if "output_text" in data:
        return data["output_text"]
    elif "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["text"]
    else:
        return str(data)
