import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

class GroqLLMAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def build_prompt(self, data):
        return f"""
Analyze the following coding problem and classify its difficulty as Easy, Medium, or Hard.

### Criteria:
- Algorithmic Concepts (e.g., DP, graphs, etc.)
- Problem Structure Complexity
- Implementation Difficulty
- Optimization Requirements
- Input Size Constraints

### Problem
Title: {data['title']}
Description: {data['description']}
Constraints: {"; ".join(data['constraints'])}
Examples: {data.get('examples', [])}

### Output Format:
- Difficulty: Easy / Medium / Hard
- Reasoning: Short justification (2-3 sentences)
"""

    def analyze_question(self, data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful AI code reviewer."},
                {"role": "user", "content": self.build_prompt(data)}
            ],
            "temperature": 0.2
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"GROQ API error: {response.status_code} {response.text}")
