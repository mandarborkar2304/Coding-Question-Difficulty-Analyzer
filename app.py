from flask import Flask, request, jsonify, render_template
from groq_interface import GroqLLMAnalyzer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    problem = {
        "title": data.get("topic"),
        "description": data.get("details"),
        "constraints": [],
        "examples": []
    }

    try:
        llm = GroqLLMAnalyzer()
        result = llm.analyze_question(problem)  # already returns JSON dict
    except Exception as e:
        result = {
            "llm_difficulty": "LLM error",
            "llm_reasoning": str(e)
        }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
