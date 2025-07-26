## ClaimForge: Gemini-Powered Prior Art Discovery for Patents
[![ClaimForge CI](https://github.com/RamlaSuhra/team-claimforge/actions/workflows/ci.yml/badge.svg)](https://github.com/RamlaSuhra/team-claimforge/actions/workflows/ci.yml)

<p align="center">
  <img src="images/claimforge.gif" alt="Demo animation" height="650"/>
</p>

---

## Overview
ClaimForge is an AI-powered web application that enables users to analyze patent claims, search for prior art using Google Patents (via SerpAPI), and generate a comprehensive report with recommendations. The system leverages Google Gemini for reasoning and report generation, and provides a user-friendly web interface for input and results. Users can register, log in, and manage their analysis sessions through the UI.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Google Gemini API key (obtain from [Google AI Studio](https://aistudio.google.com/))
- SerpAPI key (obtain from [SerpAPI](https://serpapi.com/))
- Dependencies listed in `environment.yml` or `requirements.txt`

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/RamlaSuhra/team-claimforge.git
   cd team-claimforge
   ```

2. **Set Up Environment**:
   - Use the provided `environment.yml` to create a Conda environment:
     ```bash
     conda env create -f environment.yml
     conda activate claimforge
     ```
   - Or use pip:
     ```bash
     pip install -r requirements.txt
     ```
   - Alternatively, use the `Dockerfile` for a containerized setup:
     ```bash
     docker build -t claimforge .
     docker run -it claimforge
     ```

3. **Configure API Keys**:
   - Copy `.env.example` to `.env` and add your keys:
     ```plaintext
     GOOGLE_API_KEY=your_gemini_key
     SERP_API_KEY=your_serpapi_key
     ```
   - Ensure the `.env` file is listed in `.gitignore` to avoid committing the key.

4. **Run the Web Application**:
   ```bash
   python src/ui/app.py
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

## 📂 Folder Structure
- `src/`: Contains the core application code.
  - `agent/`: Core agent logic (GeminiPatentAgent, memory, tools, prompts)
  - `ui/`: Flask web app (app.py, HTML templates, static assets)
  - `data/`: (Optional) Database and data access
  - `main.py`: CLI entry point for agent (optional)
- `ARCHITECTURE.md`: Details the system design and workflow.
- `EXPLANATION.md`: Explains the agent’s reasoning, memory usage, and limitations.
- `DEMO.md`: Links to a video demo with timestamps.

## 🛠️ How It Works
ClaimForge uses a web-based workflow powered by the Google Gemini API:
1. **User Interface:** Users register or log in, then paste or type their patent claim into the web UI and submit it for analysis.
2. **Agent (Planner & Executor):** The agent receives the claim, generates search queries using Gemini, and calls the `search` tool (integrated with SerpAPI) to find relevant prior art.
3. **Memory:** The agent logs all user inputs, LLM thoughts, tool calls, and results for full traceability and context.
4. **Report Generation:** After gathering prior art, the agent uses Gemini to generate a comprehensive report and recommendation, which is displayed in the UI.
5. **Observability:** All steps, errors, and results are logged to the console and tracked in memory for debugging and transparency.

## 📋 Dependencies
- Python libraries: `Flask`, `flask-cors`, `python-dotenv`, `requests`, `google-generativeai`, `tenacity`, `serpapi`, and more.
- See `requirements.txt` or `environment.yml` for the full list.

## 🏅 Judging Criteria Alignment
- **Technical Excellence:** Robust code with error handling, efficient Gemini and SerpAPI integration, and a modern web UI.
- **Solution Architecture & Documentation:** Clear folder structure, comprehensive `ARCHITECTURE.md`, and detailed `EXPLANATION.md`.
- **Innovative Gemini Integration:** Creative use of Gemini API for query generation, reasoning, and report writing.
- **Societal Impact & Novelty:** Automates prior art discovery, reducing human effort and ensuring fair patent validation.

## 📹 Demo
See `DEMO.md` for a link to our 3–5 minute video showcasing the agent workflow, Gemini integration, and edge case handling.

## 📝 Documentation
- `ARCHITECTURE.md`: System design with a diagram of agent interactions.
- `EXPLANATION.md`: Details on planning, memory, tool use, and limitations.
- `DEMO.md`: Video link with timestamps for setup, planning, tool calls, and output.

## 📌 Notes
- Ensure your Gemini and SerpAPI keys are securely stored and not committed to the repository.
- The repository is public for hackathon judging.
- For issues or questions, contact the team captain via the submission form.

## About
This project is a submission for the Agentic AI App Hackathon, hosted at [github.com/RamlaSuhra/team-claimforge](https://github.com/RamlaSuhra/team-claimforge). It aims to revolutionize prior art discovery using Gemini-powered agents.
