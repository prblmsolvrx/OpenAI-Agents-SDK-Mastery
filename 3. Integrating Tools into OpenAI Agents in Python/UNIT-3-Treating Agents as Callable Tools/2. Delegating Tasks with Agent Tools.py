"""
In this task, you’ll add the Travel Researcher agent as a tool to the
travel_genie agent, along with the estimate_budget function tool.
Then, run the main agent with a question that requires both research and budget estimation.
This will let you see how the main agent delegates tasks to the researcher agent-tool and combines the results.
"""

import asyncio
import json
from agents import Agent, Runner, WebSearchTool, function_tool


# Define a function tool for travel budget calculation
@function_tool
def estimate_budget(destination: str, days: int) -> float:
    """
    Estimate the travel budget for a given destination and number of days.

    Args:
        destination: The travel destination.
        days: Number of days for the trip.

    Returns:
        The estimated budget in USD.
    """
    base_cost = 150.0
    multiplier = 2.0 if destination.lower() in ["switzerland", "norway"] else 1.0
    return base_cost * days * multiplier


# Define the Researcher agent with WebSearchTool
researcher = Agent(
    name="Travel Researcher",
    instructions=(
        "You are a travel researcher. "
        "Search for the latest travel news and summarize your findings."
    ),
    tools=[WebSearchTool()],
    model="gpt-4.1"
)

# Convert the researcher agent into a callable tool
researcher_tool = researcher.as_tool(
    tool_name="research_information",
    tool_description="Research the web for travel information",
)

# Define the Travel Genie agent with tools
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Always use your tools to research destinations and estimate budgets."
    ),
    # TODO: Include researcher_tool and estimate_budget in its tools list
    tools=[
        estimate_budget,
        researcher_tool
    ],
    model="gpt-4.1"
)


async def main():
    # Run the Travel Genie agent
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Is there snow in Switzerland now, and how much would a 7-day trip cost?"
    )
    
    # Print the Travel Genie's response
    print("Travel Genie response:\n" + result.final_output)
    
    # Print input list to see tool use
    print("Input list:\n", json.dumps(result.to_input_list(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())