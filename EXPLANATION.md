# Technical Explanation

## 1. Agent Workflow

The GeminiPatentAgent follows a ReAct (Reasoning + Acting) pattern for patent prior art analysis:

1. **Receive User Input**: Invention disclosure read from `invention_disclosure.txt`
2. **Initialize Agent**: Set up Gemini model and SerpAPI credentials
3. **ReAct Loop** (max 5 iterations):
   - **Thought**: LLM generates reasoning about the patent search strategy
   - **Action**: LLM selects and calls appropriate tool using XML format
   - **Observation**: Tool results are captured and added to memory
   - **Memory Update**: Full conversation chain preserved for context
4. **Tool Execution**:
   - `patent_search`: Query SerpAPI for existing patents
   - `final_report`: Generate comprehensive patentability analysis
5. **Return Final Output**: Structured patentability assessment with novelty analysis

## 2. Key Modules

- **GeminiPatentAgent** (`GeminiPatentAgent.py`): Core agent implementing ReAct pattern with tool calling logic
- **Tools** (`tools.py`): External API integrations for patent search and report generation
- **Memory** (`memory.py`): Simple in-memory conversation history tracking
- **Prompts** (`prompts.py`): Structured prompts for guiding LLM reasoning and tool selection
- **Main** (`main.py`): CLI entry point and orchestration

## 3. Tool Integration

### **patent_search** (`tools.py`):
- **API**: SerpAPI Google Patents integration
- **Function**: `patent_search(query, max_results=3, api_key)`
- **Process**: 
  - Sanitizes AI-generated queries for optimal API performance
  - Executes search with retry logic for resilience
  - Returns structured patent data (title, number, date, abstract, URL)
- **Error Handling**: Graceful degradation for API failures with tenacity retry logic

### **final_report** (`tools.py`):
- **Function**: `final_report(model, invention_text, search_results)`
- **Process**: 
  - Takes original invention and search results
  - Calls Gemini with structured prompt for analysis
  - Generates comprehensive patentability assessment
- **Output**: Structured report with novelty analysis and recommendations

### **LLM Integration**:
- **API**: Google Gemini 2.5 Pro via `_call_gemini()`
- **Tool Calling**: XML-style `<use_tool>` parsing via `_parse_action()`
- **Resilience**: Tenacity decorators for rate limiting and API failures

## 4. Observability & Testing

### **Logging**:
- **Console Output**: Step-by-step execution visibility with clear iteration markers
- **Memory Tracking**: Full conversation history preserved in `AgentMemory` class
- **Tool Status**: Real-time feedback on tool execution and results
- **Error Handling**: Detailed error messages for API failures and rate limits

### **Debug Information**:
- **Thought Process**: LLM reasoning visible before each action
- **Tool Results**: Structured JSON output for patent search results
- **Memory Chain**: Complete conversation history for context preservation
- **Iteration Tracking**: Clear markers for each ReAct loop iteration

### **Testing**:
- **Main Execution**: `main.py` provides end-to-end testing
- **Error Scenarios**: Handles API failures, rate limits, and invalid inputs
- **Memory Validation**: Conversation history maintained across iterations

## 5. Known Limitations

### **API Dependencies**:
- **SerpAPI Rate Limits**: Patent search limited by SerpAPI quotas
- **Google Gemini Rate Limits**: Exponential backoff for API rate limiting
- **Network Resilience**: Dependent on external API availability

### **Input Constraints**:
- **File-Based Input**: Currently requires invention disclosure in text file format
- **Query Complexity**: AI-generated queries may need manual refinement for optimal results
- **Patent Database Coverage**: Limited to patents available through SerpAPI

### **Performance Considerations**:
- **Iteration Limits**: Maximum 5 ReAct iterations to prevent infinite loops
- **Memory Growth**: Conversation history grows with each iteration
- **API Latency**: External API calls can introduce significant delays

### **Edge Cases**:
- **No Search Results**: Agent must handle cases where no relevant patents are found
- **Ambiguous Inventions**: Complex inventions may require multiple search iterations
- **Tool Selection**: LLM may fail to select appropriate tools in some scenarios

