"""
In this exercise, your goal is to build a callback that keeps track of how
often the safety expert is called and what types of concerns are reported for each destination.

To complete this task:

Write a new callback function that updates the existing tracking variables:
safety_expert_call_count and safety_concerns_by_destination.
Use global variables to track call count and concerns by destination
Increment the counter each time the safety expert is called
Extract destination and concern from the validated input
Initialize the set for this destination if it doesn't exist yet
Add the new concern to the set for this destination
Update the handoff configuration so that your new analytics callback
is used when handing off to the safety expert.
At the end of the workflow, a summary of analytics will be printed for you.
Observe the displayed summary to verify that your callback is correctly tracking
the safety expert usage and concerns by destination.    
"""

import asyncio
from typing import Any
from pydantic import BaseModel, Field
from agents import Agent, Runner, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


# Typed request schemas (validated before the next agent runs)
class SafetyRequest(BaseModel):
    destination: str = Field(..., description="The travel destination in question")
    concern: str = Field(..., description="The specific safety or health concern")


# Define the travel genie agent
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
)

# Define the travel safety expert agent
safety_expert = Agent(
    name="Travel Safety Expert",
    instructions=(
        "You are a travel safety expert. "
        "Provide safety advice and important precautions for travelers."
    ),
    model="gpt-4.1",
)

# Analytics tracking variables
safety_expert_call_count = 0
safety_concerns_by_destination = {}


# ✅ Async analytics callback function
async def safety_analytics_callback(validated_input: SafetyRequest, **kwargs: Any):
    """
    Asynchronous callback triggered whenever the safety expert is called.
    Updates analytics counters and concern lists by destination.
    """
    global safety_expert_call_count, safety_concerns_by_destination

    # Increment the call counter
    safety_expert_call_count += 1

    # Extract destination and concern from the validated input
    destination = validated_input.destination
    concern = validated_input.concern

    # Initialize set if this destination hasn't been tracked yet
    if destination not in safety_concerns_by_destination:
        safety_concerns_by_destination[destination] = set()

    # Add the concern to the set for that destination
    safety_concerns_by_destination[destination].add(concern)


# Triage agent that decides which specialized agent to hand off to
triage = Agent(
    name="Travel triage",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a travel triage agent. Given a request:\n"
        "- For destination or itinerary questions, transfer to Travel Genie\n"
        "- For safety or health concerns, transfer to the Travel Safety Expert"
    ),
    handoffs=[
        travel_genie,
        handoff(
            agent=safety_expert,
            tool_name_override="ask_safety_expert",
            tool_description_override="Ask the travel safety expert for advice",
            input_type=SafetyRequest,
            on_handoff=safety_analytics_callback,  # ✅ async callback attached here
        ),
    ],
    model="gpt-4.1",
)


# Example requests to demonstrate delegation
requests = [
    "In a few words, what's the food safety situation in Thailand?",
    "Briefly suggest a city for art lovers in Europe.",
    "Is it safe to drink tap water in Mexico? Answer very briefly.",
]


async def main():
    # Run each request through the triage agent
    for req in requests:
        result = await Runner.run(
            starting_agent=triage,
            input=req,
        )
        print("Request:", req)
        print("Delegated to:", result.last_agent.name)
        print("Response:\n" + result.final_output + "\n")

    # Print analytics summary at the end
    print("\n=== Analytics Summary ===")
    print(f"Safety expert was called {safety_expert_call_count} times.")
    print("Concerns by destination:")
    for dest, concerns in safety_concerns_by_destination.items():
        print(f"  - {dest}: {', '.join(concerns)}")


if __name__ == "__main__":
    asyncio.run(main())
