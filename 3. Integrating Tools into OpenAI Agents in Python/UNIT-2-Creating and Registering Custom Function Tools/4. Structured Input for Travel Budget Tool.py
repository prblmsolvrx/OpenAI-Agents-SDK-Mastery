"""
To complete this task:

Define a TripInfo class that inherits from TypedDict, with two keys: destination (type str) and days (type int).
Update the estimate_budget function so that it takes one argument, trip_info:
TripInfo, and uses this dictionary to access the destination and days.
Adjust the function's docstring to describe the new structured input and the return value.
Update the function's implementation to access properties from the trip_info dictionary.
After your changes, the agent will automatically use your updated tool to estimate
travel budgets. Using structured input with TypedDict makes your tool interface clearer,
easier to extend, and helps the agent reliably provide all necessary information in an organized way.
"""

import json
import asyncio
from typing_extensions import TypedDict
from agents import Agent, Runner, WebSearchTool, function_tool


# ✅ Define a TypedDict for trip details
class TripInfo(TypedDict):
    destination: str
    days: int


# ✅ Modify the function to take TripInfo instead of separate parameters
@function_tool
def estimate_budget(trip: TripInfo) -> float:
    """
    Estimate the travel budget for a given trip.

    Args:
        trip: A dictionary containing 'destination' and 'days'.

    Returns:
        The estimated budget in USD.
    """
    destination = trip["destination"]
    days = trip["days"]

    # Simple mock logic for demonstration
    base_cost = 150.0
    multiplier = 2.0 if destination.lower() in ["switzerland", "norway"] else 1.0
    return base_cost * days * multiplier


# ✅ Define the Travel Genie agent with the tool
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


async def main():
    # Run the agent asking to calculate a budget
    result = await Runner.run(
        starting_agent=travel_genie,
        input="What would be the estimated budget for a 5-day trip to Norway?"
    )
    
    # Display the output
    print("Final Output:\n" + result.final_output + "\n")
    
    # Display how the agent processed it
    print("Input List:\n" + json.dumps(result.to_input_list(), indent=2))
    

if __name__ == "__main__":
    asyncio.run(main())
