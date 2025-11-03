# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Your API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run the System

#### Interactive Mode (Recommended)
```bash
python main.py --mode interactive
```

#### Run All Demos
```bash
python main.py --mode all-demos
```

#### Run Specific Demo
```bash
python main.py --mode demo
```

### 4. Try Example Usage

```bash
python example_usage.py
```

## 📋 Basic Usage Example

```python
import asyncio
from agents import Runner
from agents import create_agent_system

async def main():
    # Create agent system
    agents = create_agent_system()
    
    # Use an agent
    result = await Runner.run(
        starting_agent=agents["recommender"],
        input="Recommend a destination for a food lover."
    )
    
    print(result.final_output)

asyncio.run(main())
```

## 🎯 What's Included

- ✅ 8 specialized agents
- ✅ Custom tools with structured inputs
- ✅ Security guardrails
- ✅ Comprehensive monitoring hooks
- ✅ Multi-turn conversations
- ✅ Agent chaining and handoffs
- ✅ Streaming support
- ✅ Structured outputs

## 🔧 Common Commands

```bash
# Interactive mode
python main.py

# Quiet mode
python main.py --quiet

# Disable hooks
python main.py --no-hooks

# Disable guardrails
python main.py --no-guardrails
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore [example_usage.py](example_usage.py) for code examples
3. Customize agents in `agents.py`
4. Add your own tools in `tools.py`
5. Configure guardrails in `guardrails.py`

## 🆘 Troubleshooting

**Issue**: Import errors
- **Solution**: Ensure you're in the `production_travel_agent` directory

**Issue**: API key not found
- **Solution**: Set `OPENAI_API_KEY` environment variable

**Issue**: Model not available
- **Solution**: Ensure you have access to `gpt-4o` or update model names in `agents.py`

Happy coding! 🎉


