"""
Your task is to transform this function into a proper guardrail by
making it return a GuardrailFunctionOutput object instead of a boolean. You'll need to:

Import the GuardrailFunctionOutput class from the agents module
Update return statements to create GuardrailFunctionOutput objects with appropriate output_info messages
Set tripwire_triggered to True for prohibited content, False for approved content
Update the test code to work with the new return type
This exercise will give you a solid foundation in the guardrail output
structure that you'll use throughout the rest of the unit!
"""

# TODO: Import GuardrailFunctionOutput from agents
from agents import GuardrailFunctionOutput


def content_guardrail(input: str) -> GuardrailFunctionOutput:
    """Check if input contains prohibited content."""
    # List of prohibited terms for travel requests
    prohibited_terms = ["prostitution", "drugs", "strip club"]
    
    # Convert input to lowercase for case-insensitive matching
    input_lower = input.lower()
    
    # Check for prohibited terms
    for term in prohibited_terms:
        if term in input_lower:
            # TODO: Return GuardrailFunctionOutput with appropriate message and tripwire_triggered=True
            return GuardrailFunctionOutput(
                output_info=f"Request blocked: contains prohibited term '{term}'.",
                tripwire_triggered=True
            )
    
    # TODO: Return GuardrailFunctionOutput with approval message and tripwire_triggered=False
    return GuardrailFunctionOutput(
        output_info="Request approved: no prohibited content detected.",
        tripwire_triggered=False
    )


# Inputs to test function
test_inputs = [
    "Where can I find drugs in Amsterdam?",
    "What are the best beaches in Europe?"
]

# TODO: Update the print statements to display:
# - result.output_info (the guardrail's message)
# - result.tripwire_triggered (whether content was blocked)
for test_input in test_inputs:
    result = content_guardrail(test_input)
    print(f"Input: {test_input}")
    print(f"Message: {result.output_info}")
    print(f"Tripwire Triggered: {result.tripwire_triggered}\n")
