"""
Right after the agent is created, add a loop that goes
through the tools list in your travel_genie agent and prints each tool. For example:
for tool in my_agent.tools:
    print(tool)
By inspecting the tools list of your agent, you can verify which tools
are available and see how each one is represented.
This helps ensure your agent is configured correctly and
gives you insight into how the agent will "see" and use its
tools when deciding how to answer user queries.
"""

import json
import asyncio
from agents import Agent, Runner, WebSearchTool

# Define the Travel Genie agent with WebSearchTool
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    tools=[WebSearchTool()],
    model="gpt-4.1"
)

# TODO: Write a loop that iterates over travel_genie.tools and prints each tool
for tool in travel_genie.tools:
    print(tool)
