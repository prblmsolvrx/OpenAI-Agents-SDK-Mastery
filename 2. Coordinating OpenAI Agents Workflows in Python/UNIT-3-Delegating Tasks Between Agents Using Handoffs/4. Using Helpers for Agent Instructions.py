"""
In this exercise, refactor the code so that the triage agent’s
specific instructions are stored in a separate variable. Follow these steps:

Move the triage agent’s specific instructions into their own variable.
Use the prompt_with_handoff_instructions to create the full instructions.
Update the triage agent to use the new combined instructions.
This approach helps keep your code clean and ensures that your
agents always have the right context for handling handoffs.
"""

import asyncio
from agents import Agent, Runner
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

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

# TODO: Extract the triage agent's specific instructions to a separate variable
# TODO: Use prompt_with_handoff_instructions to combine the recommended prompt prefix with the instructions
# TODO: Update the triage agent to use the combined instructions
agent_instructions = ("You are a travel triage agent. Given a request:\n"
                      "- For destination or itinerary questions, transfer to Travel Genie\n"
                      "- For safety or health concerns, transfer to the Travel Safety Expert")
full_instructions = prompt_with_handoff_instructions(agent_instructions)
triage = Agent(
    name="Travel Triage",
    instructions=full_instructions,
    handoffs=[
        travel_genie,
        safety_expert
    ],
    model="gpt-4.1"
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

# Print triage agent's instructions to verify system context is included
print(triage.instructions + "\n")

if __name__ == "__main__":
    asyncio.run(main())