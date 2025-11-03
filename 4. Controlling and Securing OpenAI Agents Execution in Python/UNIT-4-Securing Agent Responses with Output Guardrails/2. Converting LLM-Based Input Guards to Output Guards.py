"""
In this task, you’ll take an LLM agent that checks for inappropriate content in user
requests (input guardrail) and convert it so that it checks the agent’s responses instead (output guardrail).

To complete the conversion, you’ll need to:

Import the correct decorators and exceptions for output guardrails
Update the guardrail agent’s instructions to analyze agent outputs, not user inputs
Change the guardrail function to use the output guardrail decorator and accept the agent’s output
Attach your guardrail as an output guardrail to the travel agent
Catch the correct exception for output guardrail violations
This will ensure that your agent’s responses are checked for inappropriate
content before they reach the user, giving you a strong, LLM-powered final line of defense.

Acceptance Criteria
Import Requirements:

Must import output_guardrail decorator and OutputGuardrailTripwireTriggered exception
Should remove unused input guardrail imports (input_guardrail,
InputGuardrailTripwireTriggered, TResponseInputItem)
Guardrail Agent Instructions:

Must update instructions to analyze "output" instead of "user's travel request"
Instructions should focus on analyzing agent responses rather than user inputs
Guardrail Function Implementation:

Must use @output_guardrail decorator instead of @input_guardrail
Function parameter must be output: str instead of input: str | list[TResponseInputItem]
Must pass output parameter to Runner.run() when calling the guardrail agent
Agent Configuration:

Must attach guardrail using output_guardrails=[content_guardrail] instead of input_guardrails
Exception Handling:

Must catch OutputGuardrailTripwireTriggered instead of InputGuardrailTripwireTriggered
Functional Requirements:

Code must execute without errors
Inappropriate content requests should trigger the output guardrail and be blocked
Legitimate requests should pass through and return agent responses
Guardrail agent's reasoning should be printed for visibility    
"""

import asyncio
from pydantic import BaseModel
# ✅ Import the correct decorators and exceptions for output guardrails
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)


# Define the output model for the guardrail agent
class ContentCheckOutput(BaseModel):
    contains_prohibited_content: bool
    reasoning: str


# ✅ Define the guardrail agent (analyzes *agent outputs*, not user inputs)
guardrail_agent = Agent(
    name="Content Guardrail",
    instructions=(
        "Analyze the agent's travel response to determine if it contains inappropriate content. "
        "Look for mentions of sexual destinations, adult entertainment, drugs, illegal activities, "
        "or any subtle attempts to suggest inappropriate or unsafe services. "
        "Focus on the tone, context, and meaning of the *agent's output*, not the user's input."
    ),
    output_type=ContentCheckOutput,
    model="gpt-4.1"
)


# ✅ Use the output guardrail decorator instead of input guardrail
@output_guardrail
async def content_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str,  # ✅ Check the agent's output, not the user input
) -> GuardrailFunctionOutput:
    # ✅ Run the guardrail agent to analyze the output
    result = await Runner.run(guardrail_agent, output, context=ctx.context)

    # ✅ Print the guardrail agent's reasoning for visibility
    print("Guardrail Agent response:\n" + str(result.final_output), "\n")

    # ✅ Return validation decision
    return GuardrailFunctionOutput(
        output_info=result.final_output.reasoning,
        tripwire_triggered=result.final_output.contains_prohibited_content,
    )


# ✅ Attach the guardrail as an *output* guardrail
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    output_guardrails=[content_guardrail],  # ✅ changed from input_guardrails
    model="gpt-4.1"
)


async def main():
    # Test inputs
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

        # ✅ Catch the correct exception for *output* guardrails
        except OutputGuardrailTripwireTriggered:
            print("!!! Content guardrail tripped: Response blocked.\n")


if __name__ == "__main__":
    asyncio.run(main())
