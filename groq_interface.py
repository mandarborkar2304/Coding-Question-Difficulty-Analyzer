import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

class GroqLLMAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def build_prompt(self, data):
        topic = data.get('topic', 'General').strip()
        sample_input = data.get('sample_input', 'N/A')
        sample_output = data.get('sample_output', 'N/A')

        return f"""
You are an expert programming problem analyst.

Analyze the following coding problem and classify its difficulty as Easy, Medium, or Hard based on:

- Algorithmic Concepts (e.g., bit manipulation, recursion, dynamic programming, greedy, graph traversal)
- Problem Structure Complexity
- Implementation Difficulty
- Optimization Needs
- Input Size Constraints

---

<b>Topic:</b> {topic}

This topic indicates that the problem may involve concepts or techniques typically found in "{topic}" problems. Use this as a guide in your reasoning, especially for complexity and difficulty judgment.

---

<b>Problem Title:</b>
{data['title']}

<b>Question:</b>
{data['question']}

<b>Note:</b>
{data['note']}

<b>Function Description:</b>
{data['function_description']}

<b>Sample Input:</b>
{sample_input}

<b>Constraints:</b>
{"; ".join(data['constraints'])}

<b>Sample Output:</b>
{sample_output}

---

Please respond in HTML format using the following structure.
Keep each section short (2–3 concise sentences at most). 
Avoid any form of code, pseudocode, or overly detailed walkthroughs.
Focus on key insights and avoid repetition across sections.

Be strict in difficulty evaluation:

- Rate as <b>Hard</b> if the problem requires dynamic programming, greedy optimization over substrings, memoization, or making multi-level decisions.
- Rate as <b>Medium</b> only if logic is non-trivial but manageable without multi-step optimization.
- Rate as <b>Easy</b> only if the solution is direct, with simple loops, counting, or pattern validation.

<b>Difficulty:</b> <Easy / Medium / Hard><br><br>

<b>Reasoning:</b><br>
<Brief paragraph summarizing the key challenges and complexity><br><br>
<br></br>
<b>Algorithmic Concepts:</b><br>
<Discuss algorithms needed: e.g., DP, greedy, string matching><br><br>
<br></br>
<b>Problem Structure Complexity:</b><br>
<Describe logical branching, combinations, recursion depth, etc.><br><br>
<br></br>
<b>Implementation Difficulty:</b><br>
<Explain if the solution is code-heavy, prone to bugs, or edge-case sensitive><br><br>
<br></br>
<b>Optimization Needs:</b><br>
<Describe time/space limits, need to prune brute-force, etc.><br><br>
<br></br>
<b>Input Size Constraints:</b><br>
<Explain how input size drives complexity, e.g., loops vs. DP>
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
# This code defines a class for interacting with the Groq LLM API to analyze programming problems.
# It includes methods to build a prompt based on the problem data and to send a request to