"""
In this task, you should make sure your agent can access the MCP server
by passing the connection in the agent’s mcp_servers list.
This exercise will let you see the entire workflow in action—from connecting
to the server, using a tool, and returning the results to the user!
"""

import asyncio
import json
from agents import Agent, Runner
from agents.mcp import MCPServerSse

# Setup the SSE server parameters
SERVER_PARAMS = {"url": "http://localhost:8000/sse"}
    

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
            instructions=(
                "You are Travel Genie, a friendly and knowledgeable travel assistant. "
                "Always use the available tools to help users plan their trips, such "
                "as booking museum visits. Whenever you complete a booking or reservation, "
                "be sure to provide the user with all relevant confirmation details."
            ),
            model="gpt-4.1",
            # TODO: Add the MCP server connection to the agent's mcp servers list
            mcp_servers=[mcp_server]
        )

        # Run the agent
        result = await Runner.run(
            starting_agent=travel_genie,
            input="Book 3 tickets to the Louvre for June 10, 2025"
        )

        # Print the final output
        print("Final output:\n" + result.final_output + "\n")

        # Print input list to see tool use
        print("Input list:\n", json.dumps(result.to_input_list(), indent=2))
        
if __name__ == "__main__":
    asyncio.run(main())