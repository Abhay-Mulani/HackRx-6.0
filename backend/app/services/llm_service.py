import os
import requests
import json

def query_llm(question: str, context: str = "") -> str:
    api_key = os.getenv("GROK_API_KEY")
    if api_key:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are an insurance document assistant."},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0.2,
            "max_tokens": 256
        }
        
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Grok API error: {e}"
    return f"Grok response to: {question} (context: {context})" 