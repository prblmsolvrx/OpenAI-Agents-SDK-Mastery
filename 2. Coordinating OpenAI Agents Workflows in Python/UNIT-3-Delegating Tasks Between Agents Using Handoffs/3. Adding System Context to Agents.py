"""
In this exercise, prepend the RECOMMENDED_PROMPT_PREFIX to the triage agent’s instructions using string concatenation.
This will help the agent understand its role in a multi-agent system and handle handoffs more reliably.

Find the triage agent’s definition in the code.
Combine the RECOMMENDED_PROMPT_PREFIX and the agent’s specific instructions so that the full context is included.
Use string concatenation (such as an f-string) to join the prefix and the instructions.
Observe how the triage agent's instructions now include the recommended prompt prefix,
making its behavior more consistent and effective when delegating tasks.
"""

import asyncio
from agents import Agent, Runner
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

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
    # TODO: Prepend RECOMMENDED_PROMPT_PREFIX to the instructions using string concatenation
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a travel triage agent. Given a request:\n"
        "- For destination or itinerary questions, transfer to Travel Genie\n"
        "- For safety or health concerns, transfer to the Travel Safety Expert"
    ),
    handoffs=[
        travel_genie,
        safety_expert
    ],
    model="gpt-4.1"
)

# Print triage agent's instructions
print(triage.instructions)