"""
In this exercise, the triage agent currently delegates tasks
by directly listing both the travel genie and the safety expert in its handoffs.
The goal is to update the handoffs so that the safety expert is
included using the handoff() function, but with only the required agent parameter.

To complete this task:

Remove the direct reference to the safety expert from the handoffs list.
Replace it with a call to handoff() that wraps the safety expert agent, using only the basic agent argument.
Make sure the workflow still delegates requests to the correct agent.
This step will help you become comfortable with the handoff object before adding more advanced features later.    
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
        # TODO: Remove the direct reference to safety_expert below and replace it with a call to handoff() that only uses the agent parameter.
        handoff(agent=safety_expert),
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