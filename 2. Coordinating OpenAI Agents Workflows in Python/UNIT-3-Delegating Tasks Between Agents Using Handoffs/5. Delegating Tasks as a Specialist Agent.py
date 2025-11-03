"""
In this exercise, update the Travel Genie agent so it can handle
travel suggestions and recommendations itself, but delegate any
safety- or health-related questions to the Travel Safety Expert.
This shows that handoffs are not just for triage agents —
any agent can pass a request to another expert when it makes sense.

To complete this task:

Update the Travel Genie’s instructions so they explain when it will
answer directly and when it will delegate to the Travel Safety Expert.
Add the Safety Expert agent to the Travel Genie’s handoffs parameter.
Run two test requests: one asking for a travel suggestion
(which Travel Genie should answer), and one asking about travel
safety (which should be delegated to the Safety Expert).
This will help you see how agents can work together and delegate tasks, even when they are not triage agents.
"""

import asyncio
from agents import Agent, Runner

# Define the travel safety expert agent
safety_expert = Agent(
    name="Travel Safety Expert",
    instructions=(
        "You are a travel safety expert. "
        "Provide safety advice and important precautions for travelers."
    ),
    model="gpt-4.1"
)

# Define the travel genie agent
# TODO: Update the instructions so Travel Genie answers travel suggestions directly,
# and delegates safety or health questions to the Travel Safety Expert.
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
        "Delegate to Safety Expert, For safety or health concerns"
    ),
    # TODO: Add the handoffs parameter with the Safety Expert agent
    model="gpt-4.1",
    handoffs=[
        safety_expert,
    ]
)

# Example requests to demonstrate delegation
requests = [
    "Suggest in few words a place for a beach vacation?",  # destination
    "Briefly tell me if it's safe to travel to Peru"       # safety
]


async def main():
    # Run each request through the travel genie agent
    for req in requests:
        result = await Runner.run(
            starting_agent=travel_genie,
            input=req
        )
        print("Request:", req)
        print("Handled by:", result.last_agent.name)
        print("Response:\n" + result.final_output + "\n")

if __name__ == "__main__":
    asyncio.run(main())