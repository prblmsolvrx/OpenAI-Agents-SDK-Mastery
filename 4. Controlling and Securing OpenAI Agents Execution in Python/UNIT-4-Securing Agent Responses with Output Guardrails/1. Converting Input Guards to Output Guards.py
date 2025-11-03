"""Your starter code contains a working travel assistant with a keyword-based
       input guardrail that blocks inappropriate requests. Your mission
       is to transform this into an output guardrail that analyzes the agent's
       generated responses instead of the user's input.

Here's what you need to update:
  
Change the decorator from @input_guardrail to @output_guardrail.
Update the function signature to accept output: str instead of input: str | list[TResponseInputItem].
Modify the agent configuration to use output_guardrails instead of input_guardrails.
Update the exception handling to catch OutputGuardrailTripwireTriggered instead of InputGuardrailTripwireTriggered.
Import the correct decorators and exceptions for output guardrails.
The validation logic itself can stay the same — you're just moving from checking what goes into your agent to checking what comes out of it. This shift creates your final line of defense, ensuring that even if an inappropriate request slips through, any problematic response gets caught before reaching the user.
"""

import asyncio
# ✅ Import the correct decorators and exceptions for output guardrails
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)


# ✅ Use @output_guardrail instead of @input_guardrail
@output_guardrail
async def content_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    # ✅ Accept output: str instead of input: str | list[TResponseInputItem]
    output: str
) -> GuardrailFunctionOutput:
    # List of prohibited terms for travel requests
    prohibited_terms = ["prostitution", "drugs", "strip club"]
    
    # Convert output to lowercase for case-insensitive matching
    output_lower = output.lower()
    
    # Check for prohibited terms
    for term in prohibited_terms:
        if term in output_lower:
            return GuardrailFunctionOutput(
                output_info=f"Blocked: inappropriate content containing '{term}'",
                tripwire_triggered=True
            )
    
    # Allow output if no prohibited terms found
    return GuardrailFunctionOutput(
        output_info="Content approved",
        tripwire_triggered=False
    )


# ✅ Define the Travel Genie agent with output_guardrails
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    output_guardrails=[content_guardrail],
    model="gpt-4.1"
)


async def main():
    # Test inputs - one prohibited and one acceptable
    test_inputs = [
        "Where can I find drugs in Amsterdam?",
        "What are the best beaches in Europe?"
    ]
    
    for test_input in test_inputs:
        print(f"Testing input: {test_input}")
        try:
            # Run the agent with the current input
            result = await Runner.run(
                starting_agent=travel_genie,
                input=test_input
            )
            # If content is allowed, print the agent's response
            print("Travel Genie response:\n" + result.final_output, "\n")
        # ✅ Catch OutputGuardrailTripwireTriggered instead of InputGuardrailTripwireTriggered
        except OutputGuardrailTripwireTriggered:
            print("!!! Content guardrail tripped: Response blocked.\n")


if __name__ == "__main__":
    asyncio.run(main())
