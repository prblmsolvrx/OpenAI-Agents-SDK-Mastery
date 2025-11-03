"""
In this exercise, a function tool called get_date_plus_days is already provided.
It returns today’s date plus a number of days you specify.
Your task is to help the agent use this tool to figure out the correct visit date before booking a museum trip.

To complete this exercise:

Add the get_date_plus_days function to the agent’s tools list so it becomes available for use.
Update the agent’s instructions so it first uses the date tool to determine the
correct booking date, and then uses the museum booking tool from the MCP server.
Leave the rest of the code as it is.
This will show how an agent can use both MCP-provided tools and extra helper tools you define — all in one workflow.
"""

import asyncio
import json
from datetime import date, timedelta
from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

# Setup the SSE server parameters
SERVER_PARAMS = {"url": "http://localhost:8000/sse"}


@function_tool
def get_date_plus_days(days: int) -> date:
    """
    Returns the current date plus the specified number of days.

    Args:
        days: The number of days to add to today's date.

    Returns:
        The resulting date.
    """
    return date.today() + timedelta(days=days)
    

async def main():
    # Connect to the MCP server via SSE
    async with MCPServerSse(
        params=SERVER_PARAMS,
        name="Museum Booking Server",
        cache_tools_list=True
    ) as mcp_server:
        # Create the agent
        travel_genie = Agent(
            name="Travel Genie",
            # TODO: Update the instructions so the agent first uses the date tool to determine the visit date before booking
            instructions=(
                "You are Travel Genie, a friendly and knowledgeable travel assistant. "
                "Always use the available tools to help users plan their trips, such "
                "as booking museum visits. Whenever you complete a booking or reservation, "
                "be sure to provide the user with all relevant confirmation details."
                "first uses the date tool to determine the visit date before booking"
            ),
            mcp_servers=[mcp_server],
            model="gpt-4.1",
            # TODO: Add the get_date_plus_days function to the agent's tools list
            tools=[get_date_plus_days]
        )

        # Run the agent
        result = await Runner.run(
            starting_agent=travel_genie,
            input="Book 3 tickets to the Louvre for tomorrow"
        )

        # Print the final output
        print("Final output:\n" + result.final_output + "\n")

        # Print input list to see tool use
        print("Input list:\n", json.dumps(result.to_input_list(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())