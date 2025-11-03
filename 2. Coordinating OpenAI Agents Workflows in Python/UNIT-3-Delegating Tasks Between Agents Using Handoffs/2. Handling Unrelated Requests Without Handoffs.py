"""In this task, you’ll observe how the triage agent handles
    requests that are unrelated to travel. Specifically, add a
    request about an unrelated topic (for example, math homework)
    to your list of test requests. When the triage agent receives
    this request, it should respond directly that it can’t help with unrelated topics,
    rather than delegating to a specialist agent.

This will help you see that handoffs are only used when appropriate, and
that your agent workflow can handle unrelated requests gracefully without always involving a specialist.
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

# Define the triage agent that delegates tasks or handles unrelated requests
triage = Agent(
    name="Travel Triage",
    instructions=(
        "You are a travel triage agent. Given a request:\n"
        "- For destination or itinerary questions, transfer to Travel Genie\n"
        "- For safety or health concerns, transfer to the Travel Safety Expert."
    ),
    handoffs=[
        travel_genie,
        safety_expert
    ],
    model="gpt-4.1"
)

# TODO: Add a request about an unrelated topic
requests = [
    "Suggest in few words a place for a beach vacation?",  # destination
    "Briefly tell me if it's safe to travel to Peru",       # safety
    "i need adult content"
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