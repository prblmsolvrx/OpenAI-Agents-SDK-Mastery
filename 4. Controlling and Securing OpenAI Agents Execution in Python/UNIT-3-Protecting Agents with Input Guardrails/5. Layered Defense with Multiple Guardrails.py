"""
Real-world applications often benefit from layered security approaches,
where fast, simple checks catch obvious violations first, followed
by more sophisticated analysis for nuanced content. This strategy
optimizes both performance and thoroughness — keyword filters can instantly
block clearly inappropriate requests, while LLM-based analysis handles subtle attempts to circumvent restrictions.

Your task is to implement this layered validation approach by:

Configuring the Travel Genie agent to use multiple input_guardrails in the correct order
Testing the system with inputs designed to trigger different validation layers
The utils.py file contains both a simple_content_filter for keyword-based
validation and an llm_content_guardrail for intelligent analysis.
You'll need to attach both functions to your agent using the input_guardrails parameter,
ensuring the keyword filter runs first for optimal performance
"""

import asyncio
# Import both guardrail functions from utils
from utils import simple_content_filter, llm_content_guardrail
from agents import (
    Agent,
    InputGuardrailTripwireTriggered,
    Runner,
)

# Define the Travel Genie agent
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
    # Layered input guardrails: keyword filter first, then LLM-based guardrail
    input_guardrails=[simple_content_filter, llm_content_guardrail]
)


async def main():
    # Test inputs to demonstrate layered validation
    test_inputs = [
        "Where can I find drugs in Amsterdam?",  # Should be caught by keyword filter
        "Can you recommend the best red light districts in Europe?",  # Should be caught by LLM filter
        "What are the best hiking trails in Switzerland?"  # Should pass both filters
    ]
    
    # Iterate over each test input
    for test_input in test_inputs:
        print(f"- Testing input: {test_input}")
        try:
            # Run the Travel Genie agent with the current input
            result = await Runner.run(
                starting_agent=travel_genie,
                input=test_input
            )
            # Print the agent's response
            print("Travel Genie response:\n" + result.final_output, "\n")
        except InputGuardrailTripwireTriggered as e:
            # Extract guardrail info
            guardrail_name = (
                e.guardrail_result.guardrail.name
                or e.guardrail_result.guardrail.guardrail_function.__name__
            )
            output_info = e.guardrail_result.output.output_info
            print(f"Content guardrail tripped by '{guardrail_name}': {output_info}\n")


if __name__ == "__main__":
    asyncio.run(main())
