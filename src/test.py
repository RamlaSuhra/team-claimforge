import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("❌ GEMINI_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Prompt (can replace or make dynamic)
prompt = "Gemini can you provide high-level information about patents, patent law, and a robust source of API's for patent data?"
response = model.generate_content(prompt)
output = response.text

# Print to console
print(output)

# Save to logs/
logs_dir = Path(__file__).resolve().parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = logs_dir / f"gemini_output_{timestamp}.txt"

with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"Prompt: {prompt}\n\nResponse:\n{output}")

print(f"[LOGGED] Response saved to {log_file}")

