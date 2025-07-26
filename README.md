# ClaimForge: Gemini-Powered Prior Art Discovery for Patents

<p align="center">
  <img src="images/claimforge.gif" alt="Demo animation" height="600"/>
</p>

---

## Overview
ClaimForge is an Agentic AI application designed for the Agentic AI App Hackathon. It leverages Google Gemini API to automate the discovery of prior art for patent claims, reducing the human effort required to identify documents that prove an invention was previously discovered. By analyzing patent documents, generating search queries, and validating results, ClaimForge streamlines the process of invalidating non-original patent claims.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key (obtain from [Google AI Studio](https://aistudio.google.com/))
- Dependencies listed in `environment.yml`

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
   - Alternatively, use the `Dockerfile` for a containerized setup:
     ```bash
     docker build -t claimforge .
     docker run -it claimforge
     ```

3. **Configure API Key**:
   - Create a `.env` file in the root directory.
   - Add your Gemini API key:
     ```plaintext
     GEMINI_API_KEY=your_api_key_here
     ```
   - Ensure the `.env` file is listed in `.gitignore` to avoid committing the key.

4. **Run the Application**:
   - Execute the main script:
     ```bash
     python src/main.py
     ```

## 📂 Folder Structure
- `src/`: Contains the core application code.
  - `planner.py`: Parses patent documents and generates search queries based on keywords, dates, and terms.
  - `executor.py`: Executes search queries using Gemini API and external search tools (e.g., Google).
  - `memory.py`: Logs search results and maintains context for iterative processing.
  - `main.py`: Orchestrates the agent workflow.
- `ARCHITECTURE.md`: Details the system design and workflow.
- `EXPLANATION.md`: Explains the agents' reasoning, memory usage, and limitations.
- `DEMO.md`: Links to a video demo with timestamps.

## 🛠️ How It Works
ClaimForge uses a multi-agent system powered by the Google Gemini API:
1. **Agent 1 (Planner)**: Receives a patent document, extracts key terms, dates, and concepts, and creates a search query.
2. **Agent 2 (Executor)**: Uses the query to search external sources (e.g., Google) via Gemini API and retrieves potential prior art documents.
3. **Agent 3 (Quality Control)**: Compares search results against the original patent, evaluates relevance, and determines if prior art is found.
4. **Iteration**: Agents refine queries and results iteratively to improve accuracy.

## 📋 Dependencies
- Python libraries: `python-dotenv`, `requests`, `google-generativeai`
- Full list in `environment.yml`

## 🏅 Judging Criteria Alignment
- **Technical Excellence**: Robust code with error handling and efficient Gemini API calls.
- **Solution Architecture & Documentation**: Clear folder structure, comprehensive `ARCHITECTURE.md`, and detailed `EXPLANATION.md`.
- **Innovative Gemini Integration**: Creative use of Gemini API for query generation and result validation.
- **Societal Impact & Novelty**: Automates prior art discovery, reducing human effort and ensuring fair patent validation.

## 📹 Demo
See `DEMO.md` for a link to our 3–5 minute video showcasing the agent workflow, Gemini integration, and edge case handling.

## 📝 Documentation
- `ARCHITECTURE.md`: System design with a diagram of agent interactions.
- `EXPLANATION.md`: Details on planning, memory, tool use, and limitations.
- `DEMO.md`: Video link with timestamps for setup, planning, tool calls, and output.

## 📌 Notes
- Ensure your Gemini API key is securely stored and not committed to the repository.
- The repository is public for hackathon judging.
- For issues or questions, contact the team captain via the submission form.

## About
This project is a submission for the Agentic AI App Hackathon, hosted at [github.com/RamlaSuhra/team-claimforge](https://github.com/RamlaSuhra/team-claimforge). It aims to revolutionize prior art discovery using Gemini-powered agents.
