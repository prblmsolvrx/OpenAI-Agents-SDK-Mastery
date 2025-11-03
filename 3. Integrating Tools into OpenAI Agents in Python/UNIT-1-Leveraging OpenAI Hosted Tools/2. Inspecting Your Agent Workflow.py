"""
Use the to_input_list() method on the result object to get a structured
list of all actions the agent performed. To make this easy to read,
use Python’s json.dumps() function with indentation to display the list in a clear,
formatted JSON structure.
Seeing the agent’s workflow step by step helps you understand how it uses tools and builds its answers.
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


async def main():
    # Run the agent to gather the latest information
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Suggest me one place to go skiing this month"
    )
    
    # Display the output
    print("Final Output:\n" + result.final_output + "\n")
    
    # TODO: Print the detailed input list using result.to_input_list() and json.dumps
    print(json.dumps(result.to_input_list(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())