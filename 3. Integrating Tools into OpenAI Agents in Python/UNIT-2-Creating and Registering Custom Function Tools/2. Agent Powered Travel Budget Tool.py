"""Transform the provided estimate_budget function into a custom
function tool and integrate it with the Travel Genie agent.
This will allow the agent to calculate travel budgets on demand, just as in the lesson example.

To complete this task:

Import the function_tool decorator from the agents module.
Add the @function_tool decorator above the estimate_budget function to register it as a tool.
Update the agent’s instructions so they mention the ability to estimate budgets using tools.
Add the decorated estimate_budget function to the agent’s tools list, alongside the web search tool.
Run the script to see your agent call the new tool and provide a real
budget estimate in its response. This is a key step in making your agents more helpful and interactive!

"""

import json
import asyncio
# TODO: Import function_tool from agents
from agents import Agent, Runner, WebSearchTool, function_tool

@function_tool
# TODO: Register this function as a tool using the @function_tool decorator
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
    

# Define the Travel Genie agent
travel_genie = Agent(
    name="Travel Genie",
    # TODO: Update the instructions to mention budget estimation using your tools
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend destinations and offer travel tips."
        "Calculate the budget of the trip aswell"
    ),
    tools=[
        WebSearchTool(),
        # TODO: Add estimate_budget to the tools list
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
    
    # Display the input list to see how it used the tool
    print("Input List:\n" + json.dumps(result.to_input_list(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())