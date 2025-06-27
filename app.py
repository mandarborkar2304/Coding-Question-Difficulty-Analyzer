import re
from flask import Flask, request, jsonify, render_template
from groq_interface import GroqLLMAnalyzer

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    problem = {
    "title": data.get("topic"),
    "question": data.get("question", ""),
    "note": data.get("note", ""),
    "function_description": data.get("function_description", ""),
    "constraints": data.get("constraints", []),
    "sample_input": data.get("sample_input", ""),
    "sample_output": data.get("sample_output", "")
    }

    try:
        llm = GroqLLMAnalyzer()
        raw_result = llm.analyze_question(problem)

        # Parse Difficulty and Reasoning from LLM raw output
        difficulty_match = re.search(r"Difficulty:\s*(Easy|Medium|Hard)", raw_result, re.IGNORECASE)
        reasoning_match = re.search(r"Reasoning:\s*(.*)", raw_result, re.DOTALL)

        llm_difficulty = difficulty_match.group(1) if difficulty_match else "Unknown"
        llm_reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided."

        result = {
            "llm_difficulty": llm_difficulty,
            "llm_reasoning": llm_reasoning
        }

    except Exception as e:
        result = {
            "llm_difficulty": "LLM error",
            "llm_reasoning": str(e)
        }

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)
# app.py - Flask application to analyze coding problems using Groq LLM
# This application provides a web interface to submit coding problems and receive difficulty analysis.