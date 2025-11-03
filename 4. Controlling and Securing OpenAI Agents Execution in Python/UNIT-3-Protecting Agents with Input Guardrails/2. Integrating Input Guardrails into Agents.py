"""
Import the @input_guardrail decorator.
Decorate your function with @input_guardrail.
Update your function to use the correct guardrail signature: ctx, agent, and input.
Attach your guardrail to the Travel Genie agent using the input_guardrails parameter.
Once your guardrail is properly integrated, you can test it by running the agent with
both prohibited and acceptable travel requests. The prohibited input should trigger
an InputGuardrailTripwireTriggered exception, while acceptable inputs should allow
the agent to respond normally.    
"""

import asyncio
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,  # import the decorator
)


# include the agent parameter in the signature
@input_guardrail
async def content_guardrail(
    wrapper: RunContextWrapper, agent: Agent, input: str
) -> GuardrailFunctionOutput:
    """Check if input contains prohibited content."""
    prohibited_terms = ["prostitution", "drugs", "strip club"]

    input_lower = input.lower()

    for term in prohibited_terms:
        if term in input_lower:
            return GuardrailFunctionOutput(
                output_info=f"Blocked: inappropriate travel request containing '{term}'",
                tripwire_triggered=True,
            )

    return GuardrailFunctionOutput(
        output_info="Travel request approved",
        tripwire_triggered=False,
    )


# Define the Travel Genie agent and attach the input guardrail
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
    input_guardrails=[content_guardrail],
)


async def main():
    test_inputs = [
        "Where can I find drugs in Amsterdam?",
        "What are the best beaches in Europe?"
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
