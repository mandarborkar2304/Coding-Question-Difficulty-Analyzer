import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

class GroqLLMAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def build_prompt(self, data):
        sample_input = data.get('sample_input', 'N/A')
        sample_output = data.get('sample_output', 'N/A')

        return f"""
You are an expert programming problem analyst.

Analyze the following coding problem and classify its difficulty as Easy, Medium, or Hard based on:

- Algorithmic Concepts (e.g., bit manipulation, validation)
- Problem Structure Complexity
- Implementation Difficulty
- Optimization Needs
- Input Size Constraints

---

Problem Title:
{data['title']}

Question:
{data['question']}

Note:
{data['note']}

Function Description:
{data['function_description']}

Sample Input:
{sample_input}

Constraints:
{"; ".join(data['constraints'])}

Sample Output:
{sample_output}

---

Please respond EXACTLY in this format:

Difficulty: <Easy / Medium / Hard>
Reasoning: <A brief 2-3 sentence explanation for the difficulty rating>
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