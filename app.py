from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS  # Add this import
from dotenv import load_dotenv
import os
from pathlib import Path
import google.generativeai as genai
from src.agent.GeminiPatentAgent import GeminiPatentAgent

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Initialize Flask app with CORS
app = Flask(__name__, template_folder="docs")
CORS(app)  # Enable CORS for all routes

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<path:filename>")
def serve_static_from_docs(filename):
    return send_from_directory("docs", filename)

@app.route("/analyze", methods=["POST", "OPTIONS"])  # Add OPTIONS method
def analyze():
    if request.method == "OPTIONS":
        # Handle CORS preflight
        response = jsonify({"status": "preflight"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
        
    claim = data.get("claim", "").strip()
    if not claim:
        return jsonify({"error": "Missing claim text"}), 400

    try:
        result = agent.run(user_input=claim)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)