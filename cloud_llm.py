import os, time
from groq import Groq
from dotenv import load_dotenv

# Path-aware load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("GROQ_API_KEY")

def get_cloud_response(prompt: str) -> dict:
    if not api_key:
        return {
            "text": "GROQ_API_KEY not found in .env file.",
            "latency_ms": 0,
            "source": "cloud",
            "error": "Missing API Key"
        }
        
    start = time.perf_counter()
    try:
        client = Groq(api_key=api_key)
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )

        end = time.perf_counter()

        return {
            "text": res.choices[0].message.content,
            "latency_ms": round((end - start) * 1000),
            "source": "cloud",
            "data_sent_outside": True,
            "model": "LLaMA 3 (Groq cloud)",
            "error": None
        }
    except Exception as e:
        return {
            "text": f"Error calling Groq: {str(e)}",
            "latency_ms": 0,
            "source": "cloud",
            "error": str(e)
        }