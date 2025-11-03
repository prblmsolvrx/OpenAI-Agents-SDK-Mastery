"""
Take the existing specialized agent focused on travel restrictions (currently used as a handoff).
Convert this agent into a callable tool using the .as_tool() method, giving it a clear name and description.
Update the main agent: remove the handoff, and add the new agent-tool to its tools list instead.
This hands-on challenge will show you how easy it is to swap out handoffs for agent-tools,
making your system more modular and letting your main agent orchestrate everything for a seamless user experience!
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


# Define a specialized Restrictions Agent
restrictions_agent = Agent(
    name="Travel Restrictions Agent",
    instructions=(
        "You are an expert on travel restrictions. "
        "Search for the latest travel restrictions and summarize them clearly."
    ),
    tools=[WebSearchTool()],
    model="gpt-4.1"
)


# ✅ Updated Travel Genie — uses tools only (no handoffs)
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Always use your tools to estimate budgets and check travel restrictions."
    ),
    tools=[
        estimate_budget,
        restrictions_agent.as_tool(
            tool_name="check_restrictions",
            tool_description="Use this tool to look up and summarize travel restrictions for any destination."
        ),
    ],
    model="gpt-4.1"
)


async def main():
    # Run the Travel Genie agent
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Do American tourists need a visa to visit China?"
    )
    
    # Print the Travel Genie's response
    print("Travel Genie response:\n" + result.final_output)
    
    # Print input list to see tool use
    print("Input list:\n", json.dumps(result.to_input_list(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
