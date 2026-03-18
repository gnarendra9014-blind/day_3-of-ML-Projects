import re

SENSITIVE_PATTERNS = [
    (r"\b(password|secret|token|api.?key)\b", "credentials", 40),
    (r"\b(ssn|social.?security|passport)\b", "identity", 50),
    (r"\b(diagnosis|medical|prescription|symptom)\b", "medical", 35),
    (r"\b(salary|bank|credit.?card|income)\b", "financial", 30),
    (r"\b(my name is|i am called|address is)\b", "personal", 20),
]

def analyze_privacy(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    detected = []
    penalty = 0

    for pattern, label, score in SENSITIVE_PATTERNS:
        if re.search(pattern, prompt_lower):
            detected.append(label)
            penalty += score

    cloud_score = max(0, 100 - penalty)

    return {
        "local_privacy_score": 100,
        "cloud_privacy_score": cloud_score,
        "detected_sensitive": detected,
        "recommendation": "Use local" if penalty > 20 else "Cloud is fine",
    }

def word_count(text: str) -> int:
    return len(text.split())

def compare_quality(local_text: str, cloud_text: str) -> dict:
    return {
        "local_words": word_count(local_text),
        "cloud_words": word_count(cloud_text),
        "longer_response": "Local" if word_count(local_text) > word_count(cloud_text) else "Cloud",
    }