"""
In this exercise, update the code so that it prints out only the
custom function tools registered with your travel_genie agent. To do this:
Loop through the tools list of your travel_genie agent.
For each tool, check whether it is an instance of FunctionTool.
If it is, print the tool’s name, description and params_json_schema.
This will help you clearly see which custom tools your agent can
use and reinforce your understanding of how to inspect and filter
different types of tools. Give it a try and see your custom tool stand out!
"""

from agents import Agent, WebSearchTool, function_tool, FunctionTool


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
    

# Define the Travel Genie agent with the budget estimation tool
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend destinations, offer travel tips, and estimate budgets using your tools."
    ),
    tools=[
        WebSearchTool(),
        estimate_budget
    ],
    model="gpt-4.1"
)

# TODO: Iterate over travel_genie.tools
    # TODO: Check if each tool is a FunctionTool
    # TODO: If so, print its name, description and params_json_schema
for tool in travel_genie.tools:
    if isinstance(tool, FunctionTool):
        print(tool.name, tool.description, tool.params_json_schema)