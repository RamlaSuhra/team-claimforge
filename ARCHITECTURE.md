## 2. `ARCHITECTURE.md`

```markdown
# Architecture Overview

This document outlines the architecture of the GeminiPatentAgent - an AI-powered patent prior art search and analysis system.

## High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  GeminiPatentAgent │───▶│  Final Report   │
│ (Invention File)│    │   (Core Agent)    │    │ (Analysis)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Tools Layer    │
                       │  - patent_search │
                       │  - final_report  │
                       └──────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  External APIs   │
                       │ - Google Gemini  │
                       │ - SerpAPI        │
                       └──────────────────┘
```

## Components

### 1. **User Interface**  
- **CLI Interface**: `main.py` - Command-line entry point
- **File Input**: Reads invention disclosure from `invention_disclosure.txt`
- **Output**: Console-based final patentability analysis

### 2. **Agent Core** (`GeminiPatentAgent.py`)

#### **Planner**: 
- Uses ReAct (Reasoning + Acting) pattern
- Structured prompts from `prompts.py` guide the reasoning process
- Step-by-step thought process before each action

#### **Executor**: 
- **LLM Integration**: Google Gemini 2.5 Pro via `_call_gemini()`
- **Tool Calling Logic**: XML-style `<use_tool>` parsing via `_parse_action()`
- **Retry Logic**: Tenacity decorators for API resilience
- **Rate Limiting**: Exponential backoff for Google API limits

#### **Memory**: 
- **AgentMemory Class**: Simple in-memory conversation history
- **Context Preservation**: Maintains full conversation chain
- **History Format**: Sequential entries with timestamps

### 3. **Tools / APIs** (`tools.py`)

#### **patent_search**:
- **API**: SerpAPI Google Patents integration
- **Functionality**: Searches existing patents using AI-generated queries
- **Query Cleaning**: Sanitizes AI queries for optimal API performance
- **Resilience**: Tenacity retry logic for network failures
- **Output**: Structured patent data (title, number, date, abstract, URL)

#### **final_report**:
- **Functionality**: Generates comprehensive patentability analysis
- **Input**: Original invention + search results
- **Output**: Structured analysis with novelty assessment and recommendations

### 4. **Observability** (`memory.py`, logging)

#### **Logging**:
- **Console Output**: Step-by-step execution visibility
- **Error Handling**: Graceful degradation for API failures
- **Debug Information**: Tool execution status and results

#### **Memory Tracking**:
- **Conversation History**: Full agent reasoning chain
- **Tool Results**: Structured observation storage
- **Context Preservation**: Maintains state across iterations

## Data Flow

1. **Input Processing**: Invention disclosure read from file
2. **Agent Initialization**: Gemini model + SerpAPI key setup
3. **ReAct Loop**: 
   - Thought process generation
   - Tool selection and execution
   - Result observation and memory update
4. **Final Analysis**: Comprehensive patentability report generation

## Key Features

- **Resilient API Calls**: Exponential backoff for rate limits
- **Structured Tool Calling**: XML-style parsing for reliability
- **Context-Aware Memory**: Full conversation history preservation
- **Flexible Query Generation**: AI-powered search query optimization
- **Comprehensive Analysis**: Multi-step patentability assessment

## Dependencies

- **Google Generative AI**: Core LLM functionality
- **SerpAPI**: Patent search capabilities
- **Tenacity**: Retry logic for resilience
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment variable management

