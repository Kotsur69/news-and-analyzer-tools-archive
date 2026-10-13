# prosty wrapper do Local LM Studio
import requests

class LocalLM:
    def __init__(self, base_url="http://localhost:1234/v1", api_key="lm-studio", model_name="deepseek-r1-distill-qwen-1.5b"):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name

    def chat(self, prompt):
        data = {
            "model": "deepseek-r1-distill-qwen-1.5b",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 1000
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=data
        )
        return response.json()["choices"][0]["message"]["content"]
