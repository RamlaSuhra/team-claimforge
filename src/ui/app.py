import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from data.db_client import (
    SessionLocal,
    create_user,
    get_user_by_username,
    get_all_users,
    update_user_email,
    delete_user,
)

import google.generativeai as genai
from agent.GeminiPatentAgent import GeminiPatentAgent

# Initialize Flask app
app = Flask(__name__, template_folder="docs")
CORS(app)

# Retrieve required API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

if not GOOGLE_API_KEY or not SERP_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY or SERP_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")
agent = GeminiPatentAgent(model=model, serpapi_api_key=SERP_API_KEY)

app.secret_key = 'your_super_secret_key_here'  # 🔐 Change this in production

# --- Flask Routes ---

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    message_type = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']   
        email = f"{username}"     

        db = SessionLocal()
        try:
            if get_user_by_username(db, username):
                message = "Username already exists."
                message_type = "error"
            else:
                create_user(db, username, email)
                message = "Registration successful! Please log in."
                message_type = "success"
        except Exception as e:
            db.rollback()
            message = f"Error during registration: {str(e)}"
            message_type = "error"
        finally:
            db.close()

    return render_template('register.html', message=message, message_type=message_type)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    message_type = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Not validated in this demo

        db = SessionLocal()
        try:
            user = get_user_by_username(db, username)
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                message = "Invalid username."
                message_type = "error"
        finally:
            db.close()

    return render_template('login.html', message=message, message_type=message_type)


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# --- Main Execution ---

if __name__ == '__main__':
    app.run(debug=True)
