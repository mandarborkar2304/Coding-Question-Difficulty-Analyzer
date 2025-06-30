import re
from flask import Flask, request, jsonify, render_template
from groq_interface import GroqLLMAnalyzer

app = Flask(__name__, template_folder='templates')


def extract_sections(details):
    def get_section(label, text):
        match = re.search(rf"{label}[\s\S]*?(?=\n[A-Z][a-zA-Z ]*:|\Z)", text, re.IGNORECASE)
        return match.group(0).replace(label, "").strip() if match else ""

    return {
        "note": get_section("Note", details),
        "function_description": get_section("Function Description", details),
        "constraints": get_section("Constraints", details).splitlines(),
        "sample_input": get_section("Sample Input", details),
        "sample_output": get_section("Sample Output", details),
    }


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    topic = data.get("topic", "").strip()
    title_and_question = data.get("title", "").strip()
    details = data.get("details", "")

    question_text = title_and_question.split("\n", 1)[1] if "\n" in title_and_question else title_and_question
    problem_title = title_and_question.split("\n", 1)[0] if "\n" in title_and_question else "Untitled Problem"

    sections = extract_sections(details)

    problem = {
        "title": f"{topic} - {problem_title}",
        "question": question_text,
        "note": sections["note"],
        "function_description": sections["function_description"],
        "constraints": sections["constraints"],
        "sample_input": sections["sample_input"],
        "sample_output": sections["sample_output"],
        "topic": topic
    }

    try:
        llm = GroqLLMAnalyzer()
        raw_result = llm.analyze_question(problem)

        # Match both malformed and standard difficulty tags
        difficulty_match = re.search(
            r"<b[^>]*>\s*Difficulty\s*[:\-]?\s*</b>\s*<?\s*(Easy|Medium|Hard)\s*>?",
            raw_result,
            re.IGNORECASE
        )

        if difficulty_match:
            llm_difficulty = difficulty_match.group(1).capitalize()
            cleaned_reasoning = re.sub(
                r"<b[^>]*>\s*Difficulty\s*[:\-]?\s*</b>\s*<?\s*(Easy|Medium|Hard)\s*>?<br><br>",
                "",
                raw_result,
                flags=re.IGNORECASE
            )
        else:
            # Fallback: search plain text
            text_only = re.sub(r"<[^>]+>", "", raw_result)
            fallback = re.search(r"\b(Easy|Medium|Hard)\b", text_only, re.IGNORECASE)
            llm_difficulty = fallback.group(1).capitalize() if fallback else "Unknown"
            cleaned_reasoning = raw_result

        result = {
            "llm_difficulty": llm_difficulty,
            "llm_reasoning": cleaned_reasoning.strip()
        }

    except Exception as e:
        result = {
            "llm_difficulty": "LLM Error",
            "llm_reasoning": f"<p>{str(e)}</p>"
        }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
