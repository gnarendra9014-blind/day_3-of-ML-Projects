import requests
import json
import time

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def get_local_response(prompt: str) -> dict:
    start = time.perf_counter()
    
    try:
        # Reduced timeout to 15 seconds for snappier feedback
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        end = time.perf_counter()

        return {
            "text": data.get("response", ""),
            "latency_ms": round((end - start) * 1000),
            "source": "local",
            "data_sent_outside": False,
            "model": "LLaMA 3.2 (local)",
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {
            "text": "Ollama is not responding. Please run 'ollama run llama3.2' in a separate terminal.",
            "latency_ms": 0,
            "source": "local",
            "error": str(e)
        }