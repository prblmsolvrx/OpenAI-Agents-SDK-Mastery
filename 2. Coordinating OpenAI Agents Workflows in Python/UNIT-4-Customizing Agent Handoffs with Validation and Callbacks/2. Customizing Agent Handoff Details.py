"""
In this exercise, the triage agent already uses the handoff() function to delegate requests to the safety expert. The goal is to customize this handoff by giving it a clear tool_name and a helpful description. This will make it easier to understand what the handoff does, both for debugging and for anyone reading your code.

To complete this task:

Add the tool_name_override parameter to the handoff, setting it to a custom name like "ask_safety_expert".
Add the tool_description_override parameter, providing a short description such as "Ask the travel safety expert for advice".
These changes could help make your agent workflow clearer and more maintainable.
"""

import asyncio
from agents import Agent, Runner, handoff

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

# Define the triage agent with handoffs
triage = Agent(
    name="Travel triage",
    instructions=(
        "You are a travel triage agent. Given a request:\n"
        "- For destination or itinerary questions, transfer to Travel Genie\n"
        "- For safety or health concerns, transfer to the Travel Safety Expert"
    ),
    handoffs=[
        travel_genie,
        handoff(
            agent=safety_expert,
            # TODO: Ccustomize the handoff's name
            # TODO: Customize the handoff's description
            tool_name_override="ask_safety_expert",
            tool_description_override="Ask the travel safety expert for advice"
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