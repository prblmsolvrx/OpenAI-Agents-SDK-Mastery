# Production-Ready Comprehensive Travel Agent System

A comprehensive, production-ready AI agent system demonstrating all aspects of **OpenAI Agents SDK Mastery**, covering materials 1-4 from the learning course.

## 🚀 Features

This project demonstrates a complete travel planning AI agent system that showcases:

### 📚 Material 1: Getting Started with OpenAI Agents
- ✅ Agent instructions and configuration
- ✅ Model selection and tuning
- ✅ Structured outputs with Pydantic models
- ✅ Debugging and result inspection
- ✅ Async execution and streaming
- ✅ Usage metrics tracking

### 🔗 Material 2: Coordinating Agent Workflows
- ✅ Multi-turn conversations with history management
- ✅ Agent chaining for sequential workflows
- ✅ Handoffs and task delegation
- ✅ Passing context between agents
- ✅ Complex multi-agent workflows

### 🛠️ Material 3: Integrating Tools
- ✅ OpenAI hosted tools (WebSearchTool)
- ✅ Custom function tools with structured inputs
- ✅ Agents as callable tools
- ✅ Tool registration and inspection
- ✅ TypedDict for structured tool inputs

### 🔒 Material 4: Controlling and Securing
- ✅ Secure context injection with RunContextWrapper
- ✅ RunHooks for workflow monitoring
- ✅ AgentHooks for agent-specific monitoring
- ✅ Input guardrails (keyword + LLM-based)
- ✅ Output guardrails (leakage prevention)
- ✅ Layered security defenses

## 📁 Project Structure

```
production_travel_agent/
├── __init__.py           # Package initialization
├── main.py               # Main application and CLI interface
├── travel_agents.py      # Agent definitions and factory functions
├── models.py             # Pydantic models for structured I/O
├── tools.py              # Custom function tools
├── hooks.py              # RunHooks and AgentHooks implementations
├── guardrails.py         # Input/output guardrails
├── example_usage.py      # Usage examples
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🏗️ Architecture

### Agent System

The system includes multiple specialized agents:

1. **Travel Recommender** - Provides destination recommendations with structured output
2. **Travel Researcher** - Researches current travel information using web search
3. **Itinerary Generator** - Creates detailed day-by-day itineraries
4. **Packing List Generator** - Generates comprehensive packing lists
5. **Travel Safety Expert** - Provides safety advice and health precautions
6. **Booking Specialist** - Handles bookings with secure context
7. **Travel Genie** - Main coordinator with handoff capabilities
8. **Travel Triage** - Routes requests to appropriate specialists

### Key Patterns Demonstrated

- **Structured Outputs**: All agents use Pydantic models for consistent, typed responses
- **Agent Chaining**: Sequential workflows where agents build on each other's outputs
- **Handoffs**: Intelligent delegation to specialized agents
- **Agents as Tools**: Agents can be used as callable tools by other agents
- **Secure Context**: Sensitive data is passed through RunContextWrapper
- **Comprehensive Monitoring**: Hooks track all aspects of agent execution
- **Multi-Layer Security**: Input and output guardrails protect the system

## 🚦 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone or navigate to the project directory:
```bash
git clone <your-repo-url>
cd production_travel_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

### Usage

#### Interactive Mode

Run the system in interactive mode for conversational interaction:

```bash
python main.py --mode interactive
```

#### Demo Mode

Run a specific demonstration:

```bash
python main.py --mode demo
```

#### All Demos

Run all demonstration scenarios:

```bash
python main.py --mode all-demos
```

#### Command-Line Options

```bash
python main.py [OPTIONS]

Options:
  --mode {interactive,demo,all-demos}  Run mode (default: interactive)
  --no-hooks                           Disable hooks
  --no-guardrails                      Disable guardrails
  --quiet                              Quiet mode (less verbose output)
```

## 📖 Usage Examples

### Example 1: Structured Output

```python
from travel_agents import create_agent_system
from agents import Runner

agents = create_agent_system()
result = await Runner.run(
    starting_agent=agents["recommender"],
    input="Recommend a destination for a food lover."
)

# Access structured output
recommendation = result.final_output
print(f"Destination: {recommendation.destination}")
```

### Example 2: Agent Chaining

```python
# Step 1: Get recommendation
recommender = agents["recommender"]
rec_result = await Runner.run(
    starting_agent=recommender,
    input="Suggest a honeymoon destination."
)

# Step 2: Create itinerary using recommendation context
itinerary_input = rec_result.to_input_list() + [
    {"role": "user", "content": "Create a 5-day itinerary."}
]
itinerary_result = await Runner.run(
    starting_agent=agents["itinerary_agent"],
    input=itinerary_input
)
```

See `example_usage.py` for more comprehensive examples.

## 🛡️ Security Features

### Input Guardrails

- **Keyword Filter**: Fast first-line defense against inappropriate content
- **LLM-Based Analysis**: Intelligent detection of subtle violations
- **Policy Compliance**: Ensures requests align with company policies

### Output Guardrails

- **Information Leakage Prevention**: Detects and redacts sensitive information
- **Format Validation**: Ensures response quality and completeness
- **Profanity Filter**: Filters inappropriate language

### Secure Context

- Sensitive user data is passed through `RunContextWrapper`
- LLM never sees sensitive information directly
- Context is securely injected at runtime

## 📊 Monitoring and Hooks

### Global Hooks

Monitor the entire workflow:
- Workflow start/end
- Agent executions
- Handoffs between agents
- Error tracking

### Agent-Specific Hooks

Monitor individual agents:
- Agent start/end
- Tool invocations
- Dynamic context injection
- Performance metrics

## 🧪 Testing Different Features

The system includes comprehensive demos:

1. **Structured Output Demo**: Shows Pydantic model outputs
2. **Agent Chaining Demo**: Demonstrates sequential workflows
3. **Handoffs Demo**: Shows intelligent delegation
4. **Secure Context Demo**: Demonstrates secure data handling
5. **Streaming Demo**: Shows real-time event streaming
6. **Result Inspection Demo**: Shows accessing result properties
7. **Agents as Tools Demo**: Shows agents used as callable tools

## 📝 Key Learnings Demonstrated

1. **Agent Design Patterns**: Standalone, chaining, handoffs, tools
2. **Structured I/O**: Pydantic models for type-safe inputs/outputs
3. **Tool Integration**: Custom tools, hosted tools, agents as tools
4. **Security**: Context wrappers, guardrails, secure data handling
5. **Monitoring**: Hooks for comprehensive observability
6. **Conversation Management**: History tracking, multi-turn conversations
7. **Async & Streaming**: Non-blocking execution and real-time events

## 🔧 Customization

### Adding New Agents

```python
from agents import Agent
from models import YourModel

def create_your_agent():
    return Agent(
        name="Your Agent",
        instructions="Your instructions",
        model="gpt-4o",
        output_type=YourModel
    )
```

### Adding New Tools

```python
from agents import function_tool

@function_tool
def your_tool(param: str) -> str:
    """Your tool description."""
    return "Result"
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and paths are correct
2. **API Key Issues**: Verify OPENAI_API_KEY is set correctly (check .env file)
3. **Model Availability**: Ensure you have access to the models being used (gpt-4o, etc.)
4. **Quota Issues**: Check your OpenAI account billing and quota limits

### Debug Mode

Enable verbose output:
```bash
python main.py --mode interactive
```

Or in code:
```python
config = Config()
config.VERBOSE_OUTPUT = True
system = TravelAgentSystem(config)
```

## 📚 Additional Resources

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/assistants/overview)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- OpenAI Agents SDK Mastery Course Materials

## 🎯 Production Readiness

This project includes:
- ✅ Comprehensive error handling
- ✅ Type safety with Pydantic
- ✅ Security best practices
- ✅ Monitoring and observability
- ✅ Modular architecture
- ✅ Extensive documentation
- ✅ Example usage patterns

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to use it as a reference for your own implementations.

---

**Built with OpenAI Agents SDK** | **Comprehensive demonstration of all SDK features**

