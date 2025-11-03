"""
modify the code by following the TODO comment to add the WebSearchTool to the agent's tools list.
Run the updated agent with the same skiing question and observe how the response changes
when the agent can access current information from the web

This hands-on comparison will demonstrate how adding a hosted tool enables your agent
to provide more current, specific, and useful information by supplementing its built-in
knowledge with real-time data from external sources.   
"""

import json
import asyncio
from agents import Agent, Runner, WebSearchTool

# TODO: Add the WebSearchTool to the agent's tool list
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
    tools=[WebSearchTool()]
)


async def main():
    # Run the agent to gather the latest information
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Suggest me one place to go skiing this month"
    )
    
    # Display the output
    print("Final Output:\n" + result.final_output)

if __name__ == "__main__":
    asyncio.run(main())