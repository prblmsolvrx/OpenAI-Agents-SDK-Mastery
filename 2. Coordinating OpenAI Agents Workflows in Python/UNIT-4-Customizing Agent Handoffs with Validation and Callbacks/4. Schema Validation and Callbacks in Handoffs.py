"""
In this exercise, the code already includes a Pydantic model called SafetyRequest and
a callback function named announce_safety. The goal is to connect these components to
the handoff for the safety expert so that:

The handoff uses the input_type parameter to enforce the SafetyRequest schema,
ensuring all safety requests include both a destination and a concern.
The handoff uses the on_handoff parameter to run the announce_safety
callback whenever a safety concern is handed off.
This will help you see how validation and callbacks can make your agent
workflows safer and more flexible.
"""

import asyncio
from typing import Any, Literal
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
    model="gpt-4.1"
)

# Define the travel safety expert agent
safety_expert = Agent(
    name="Travel Safety Expert",
    instructions=(
        "You are a travel safety expert. "
        "Provide safety advice and important precautions for travelers."
    ),
    model="gpt-4.1"
)

# Callback that runs the moment we hand off to the safety expert
async def announce_safety(_: Any, args: SafetyRequest):
    print(f"[ANNOUNCE] Safety concern for {args.destination}: {args.concern}")

# Triage agent that chooses which customised tool to call
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
            # TODO: Add the input_type parameter to enforce the SafetyRequest schema
            # TODO: Add the on_handoff parameter to use the announce_safety callback
            input_type=SafetyRequest,          # ✅ Enforces structured validation
            on_handoff=announce_safety          # ✅ Calls callback before delegation
        )
    ],
    model="gpt-4.1",
)

# Example requests to demonstrate delegation
requests = [
    "I'm worried about food safety in Thailand.",
    "Can you suggest a city for art lovers in Europe?"
]


async def main():
    # Run each request through the triage agent
    for req in requests:
        result = await Runner.run(
            starting_agent=triage,
            input=req
        )
        print("Request:", req)
        print("Delegated to:", result.last_agent.name)
        print("Response:\n" + result.final_output + "\n")

if __name__ == "__main__":
    asyncio.run(main())