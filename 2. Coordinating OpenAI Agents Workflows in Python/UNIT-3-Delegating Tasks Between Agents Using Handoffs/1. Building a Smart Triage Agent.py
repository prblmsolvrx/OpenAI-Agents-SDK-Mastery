"""
In this exercise, write clear instructions for the triage agent so
it knows when to hand off a request to the Travel Genie or the Travel Safety Expert. The triage agent should:

Send destination or itinerary questions to the Travel Genie.
Send safety or health concerns to the Travel Safety Expert.
Add both specialist agents to the handoffs parameter of the triage agent so it can delegate requests properly.

This will help you practice configuring agent roles and using the handoffs parameter for dynamic delegation.    
"""

import asyncio
from agents import Agent, Runner

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

# Define the triage agent that delegates tasks
triage = Agent(
    name="Travel Triage",
    # TODO: Write clear instructions for the triage agent to delegate:
    # - Destination or itinerary questions to Travel Genie
    # - Safety or health concerns to Travel Safety Expert
    instructions=(
        "You are a travel triage agent. Given a request:\n"
        "- For destination or itinerary questions, transfer to Travel Genie\n"
        "- For safety or health concerns, transfer to the Travel Safety Expert"
        ),
        handoffs=[
            travel_genie,
            safety_expert
           ],
    model="gpt-4.1",
    # TODO: Add both specialist agents to the handoffs parameter
)

# Example requests to demonstrate delegation
requests = [
    "Suggest in few words a place for a beach vacation?",  # destination
    "Briefly tell me if it's safe to travel to Peru"       # safety
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