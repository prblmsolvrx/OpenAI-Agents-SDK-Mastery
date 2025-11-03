"""
In the given code there is an issue that affects how requests are routed to the specialist agents.
Carefully review the handoff configurations in the triage agent's handoffs list.
Once you've identified the problem, make the necessary adjustment so
that requests are properly routed to the appropriate agent.
This task will help you appreciate the impact of precise naming and configuration in multi-agent workflows.
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
            tool_name_override="safety",
            tool_description_override="Safety or health concerns Expert"
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