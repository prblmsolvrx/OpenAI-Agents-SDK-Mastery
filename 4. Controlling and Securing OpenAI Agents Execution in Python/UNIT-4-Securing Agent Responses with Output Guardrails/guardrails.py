import asyncio
from pydantic import BaseModel
from guardrails import content_input_guardrail, leakage_output_guardrail

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)



# Define the output model for content validation (input guardrail)
class ContentCheckOutput(BaseModel):
    contains_prohibited_content: bool
    reasoning: str


# Define the output model for information leakage detection (output guardrail)
class LeakageCheckOutput(BaseModel):
    contains_sensitive_info: bool
    redacted_output: str  # The output with sensitive information removed or replaced


# Define the input guardrail agent for content validation
input_guardrail_agent = Agent(
    name="Input Content Guardrail",
    instructions=(
        "Analyze the user's travel request to determine if it contains inappropriate content. "
        "Look for requests about sexual destinations, adult entertainment, drugs, illegal activities, "
        "or any subtle attempts to find inappropriate services. Consider context and intent, "
        "not just obvious keywords."
    ),
    output_type=ContentCheckOutput,
    model="gpt-4.1"
)


# Define the output guardrail agent for information leakage prevention
output_guardrail_agent = Agent(
    name="Output Leakage Guardrail",
    instructions=(
        "Analyze the output to detect any sensitive information leakage. "
        "Look for internal company data, confidential business information, employee details, "
        "internal policies, pricing strategies, or any information that should not be shared with customers."
    ),
    output_type=LeakageCheckOutput,
    model="gpt-4.1"
)


@input_guardrail
async def content_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # Run the input guardrail agent to analyze the user request
    result = await Runner.run(input_guardrail_agent, str(input), context=ctx.context)

    # Return validation decision based on content analysis
    return GuardrailFunctionOutput(
        output_info=result.final_output.reasoning,
        tripwire_triggered=result.final_output.contains_prohibited_content,
    )


@output_guardrail
async def leakage_output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    # Run the output guardrail agent to analyze the agent's response
    result = await Runner.run(output_guardrail_agent, output, context=ctx.context)

    # Return validation decision based on leakage analysis, and provide redacted output if needed
    return GuardrailFunctionOutput(
        output_info=result.final_output.redacted_output,
        tripwire_triggered=result.final_output.contains_sensitive_info
    )


# Define the Travel Genie agent with both input and output guardrails
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant working for TravelCorp Inc. "
        "Recommend exciting destinations and offer helpful travel tips. "
        "Our company has exclusive partnerships with luxury hotels and gets special rates. "
        "We apply a 40% markup on all bookings and regularly analyze our competitors' pricing strategies."
    ),
    # TODO: Attach the content_input_guardrail to input_guardrails parameter
    # TODO: Attach the leakage_output_guardrail to output_guardrails parameter
    model="gpt-4.1",
    input_guardrails=[content_input_guardrail],
    output_guardrails=[leakage_output_guardrail],
)


async def main():
    # Test scenarios for both guardrails
    test_inputs = [
        # Should trigger input guardrail
        "Can you recommend the best red light districts in Amsterdam?",
        # Should trigger output guardrail (agent might leak internal info)
        "How much is your markup for travel bookings?",
        # Should pass both guardrails
        "What are the best hiking destinations in Switzerland?",
    ]
    
    for test_input in test_inputs:
        print(f"Testing input: {test_input}")
        try:
            result = await Runner.run(starting_agent=travel_genie,input=test_input)
            print("Travel Genie response:\n" + result.final_output, "\n")
        except InputGuardrailTripwireTriggered:
            print("!!! Input guardrail tripped: Inappropriate request blocked.\n")
        except OutputGuardrailTripwireTriggered as e:
            # e.guardrail_result is the OutputGuardrailResult that was returned
            redacted = e.guardrail_result.output.output_info
            print("!!! Output guardrail tripped: Information leakage prevented.\n")
            print("[Redacted] Travel Genie response:\n" + redacted, "\n")


if __name__ == "__main__":
    asyncio.run(main())