## 2. `ARCHITECTURE.md`

```markdown
# Architecture Overview

![System Architecture](architecture.png)

## System Diagram (ASCII)

```
┌────────────────────────────┐
│        User Input          │
│ (invention_disclosure.txt) │
└─────────────┬──────────────┘
              │
              ▼
┌──────────────────────────────────────────────┐
│           GeminiPatentAgent (Core)           │
│ ┌──────────────┬──────────────┬────────────┐ │
│ │   Planner    │   Executor   │   Memory   │ │
│ │ (ReAct loop) │ (Tool calls) │ (History)  │ │
│ └──────────────┴──────────────┴────────────┘ │
│        │                │                   │
│        ▼                ▼                   │
│   ┌────────────┐   ┌────────────┐           │
│   │  Prompts   │   │  Tools     │           │
│   │ (planning  │   │ (patent_   │           │
│   │  & report) │   │  search,   │           │
│   └────────────┘   │  final_    │           │
│                    │  report)   │           │
│                    └────┬───────┘           │
│                         ▼                   │
│         ┌────────────────────────────┐      │
│         │   External Integrations    │      │
│         │ - Google Gemini LLM        │      │
│         │ - SerpAPI (Google Patents) │      │
│         └────────────────────────────┘      │
│                                            │
│   ┌─────────────────────────────────────┐   │
│   │ Logging & Observability             │   │
│   │ - Console logs (steps, errors)      │   │
│   │ - Memory chain (AgentMemory)        │   │
│   └─────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────┐
│   Final Report Output      │
└────────────────────────────┘
```

---

## Components

### 1. **Planner**
- **Location:** `GeminiPatentAgent.py` (ReAct loop)
- **Role:** Generates reasoning and plans next action using LLM and structured prompts.

### 2. **Executor**
- **Location:** `GeminiPatentAgent.py`
- **Role:** Parses LLM output, calls tools (`patent_search`, `final_report`), manages tool results.

### 3. **Memory**
- **Location:** `memory.py` (`AgentMemory` class)
- **Role:** Stores full conversation history (user input, LLM thoughts, tool results) for context in each iteration.

### 4. **Tool Integrations**
- **Gemini LLM:** For reasoning, planning, and report generation.
- **SerpAPI (Google Patents):** For patent search via `tools.py`.
- **Tool logic:** Encapsulated in `tools.py` and called by the executor.

### 5. **Prompts**
- **Location:** `prompts.py`
- **Role:** Provides structured instructions for LLM (planning, tool call format, final report).

### 6. **Logging & Observability**
- **Console Output:** Step-by-step logs, errors, and tool results.
- **Memory Chain:** Full trace of agent’s reasoning and actions via `AgentMemory`.
- **Error Handling:** Graceful handling of API failures and rate limits.

---

## Data Flow

1. **User Input:** Read from file.
2. **Agent Initialization:** LLM and API keys set up.
3. **ReAct Loop:** Planner generates thought, executor parses and calls tools, memory updated.
4. **Tool Execution:** Results from SerpAPI and LLM.
5. **Final Report:** Generated and output to user.

---

## Suggestions for Improvement

- If you add a database, show it as a separate “Storage” block.
- If you add a web UI, show it as a separate “UI” block feeding into the agent.
- If you add more tools, expand the “Tools” section in the diagram.
- For advanced observability, consider logging to files or external monitoring.

