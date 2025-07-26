from flask import Flask, request, render_template, jsonify, send_from_directory
from dotenv import load_dotenv
import os
from pathlib import Path
import google.generativeai as genai
from src.agent.GeminiPatentAgent import GeminiPatentAgent

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Retrieve required API keys
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    SERP_API_KEY = os.environ["SERP_API_KEY"]
except KeyError as e:
    raise EnvironmentError(f"Missing required environment variable: {e}")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")
agent = GeminiPatentAgent(model=model, serpapi_api_key=SERP_API_KEY)

# Initialize Flask app, use docs/ as template dir
app = Flask(__name__, template_folder="docs")

@app.route("/")
def index():
    return render_template("index.html")

# Serve static assets directly from /docs/
@app.route("/<path:filename>")
def serve_static_from_docs(filename):
    return send_from_directory("docs", filename)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    claim = data.get("claim", "").strip()

    if not claim:
        return jsonify({"error": "Missing claim text"}), 400

    try:
        result = agent.run(user_input=claim)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
