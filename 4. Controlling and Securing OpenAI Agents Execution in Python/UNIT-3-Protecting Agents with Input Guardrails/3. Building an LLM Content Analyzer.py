"""
Your mission is to create a content analysis agent. You'll need to:

Define a structured output model that captures both the validation decision and reasoning.
Write clear instructions that guide the agent to identify problematic travel requests.
Configure the agent to use your output model for structured responses.
Implement the test logic to run your analyzer directly with various inputs.
Display the results to see how the agent reasons about different types of requests.    
"""

import asyncio
from pydantic import BaseModel
from agents import Agent, Runner


# ✅ Define an output model for content analysis
class ContentAnalysisOutput(BaseModel):
    is_inappropriate: bool
    reason: str


# ✅ Create a content analysis agent
content_analyzer = Agent(
    name="ContentAnalyzer",
    instructions=(
        "Analyze the given travel-related request and determine if it contains "
        "inappropriate or prohibited content such as references to prostitution, "
        "drugs, or adult entertainment. Explain your reasoning clearly."
    ),
    output_type=ContentAnalysisOutput,
)


async def main():
    # Test inputs
    test_inputs = [
        "What are the best beaches in Thailand?",
        "Where can I find red light districts?"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        
        # ✅ Correct static call to Runner.run
        result = await Runner.run(content_analyzer, test_input)
        
        # ✅ Get structured output
        analysis = result.final_output
        print(f"Contains prohibited content: {analysis.is_inappropriate}")
        print(f"Reasoning: {analysis.reason}")


if __name__ == "__main__":
    asyncio.run(main())
