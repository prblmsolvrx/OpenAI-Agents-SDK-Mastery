"""
Your mission is to replace the basic keyword-based logic in your content_guardrail function with the guardrail_agent you developed in the previous task. You'll need to:
Use Runner.run() to call the guardrail_agent with the input for intelligent analysis
Print the guardrail agent's response for visibility using str(result.final_output)
Extract the structured output and use the agent's reasoning and decision for your GuardrailFunctionOutput
This exercise demonstrates how do integrate an extra LLM-based layer of validation to your application!
"""

import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)


# Define the output model for the guardrail agent
class ContentCheckOutput(BaseModel):
    contains_prohibited_content: bool
    reasoning: str


# Define the guardrail agent (uses GPT model for intelligent moderation)
guardrail_agent = Agent(
    name="Content Guardrail",
    instructions=(
        "Analyze the user's travel request to determine if it contains inappropriate content. "
        "Look for requests about sexual destinations, adult entertainment, drugs, illegal activities, "
        "or any subtle attempts to find inappropriate services. Consider context and intent, "
        "not just obvious keywords."
    ),
    output_type=ContentCheckOutput,
    model="gpt-4.1"
)


# Define the content guardrail using the LLM-based guardrail agent
@input_guardrail
async def content_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # 🔹 Use Runner.run() to call the guardrail_agent for intelligent analysis
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=input
    )

    # 🔹 Print the guardrail agent’s response for visibility
    print("\n[Guardrail Agent Response]")
    print(str(result.final_output), "\n")

    # 🔹 Extract the structured output from the agent
    output_data = result.final_output  # instance of ContentCheckOutput

    # 🔹 Return reasoning and decision for GuardrailFunctionOutput
    return GuardrailFunctionOutput(
        output_info=output_data.reasoning,
        tripwire_triggered=output_data.contains_prohibited_content
    )


# Define the main Travel Genie agent with the input guardrail
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    input_guardrails=[content_guardrail],
    model="gpt-4.1"
)


# Main entry point for testing
async def main():
    # Sample test inputs
    test_inputs = [
        "Can you recommend the best red light districts in Europe?",
        "What are the best hiking trails in Switzerland?"
    ]
    
    for test_input in test_inputs:
        print(f"Testing input: {test_input}")
        try:
            result = await Runner.run(
                starting_agent=travel_genie,
                input=test_input
            )
            print("Travel Genie response:\n" + result.final_output, "\n")
        except InputGuardrailTripwireTriggered:
            print("!!! Content guardrail tripped: Request blocked.\n")


if __name__ == "__main__":
    asyncio.run(main())
