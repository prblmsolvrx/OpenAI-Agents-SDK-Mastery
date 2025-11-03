"""
Manual control can be just as important as automation! In the last exercises,
you saw how easy it is to manage MCP server connections using an async with block.
Now, let’s explore how to handle the connection process yourself using a try-except-finally pattern.

Refactor the code so that it no longer uses an async with block to manage the MCP server connection.
Instead, take charge by manually connecting to and cleaning up the server using try, except, and finally. Remember to:

Before creating or running the agent, call await mcp_server.connect() to open the connection.
Make sure the agent receives the MCP server connection in its mcp_servers list.
Once the agent has finished running and you’ve printed the results, call await mcp_server.cleanup() to close the connection.
Use a try-except-finally block to ensure that cleanup() is always called, even if an error occurs.
This exercise will help you understand how to manage resources safely and flexibly, even without
a context manager. Give it a try and see how manual connection management works in practice!
"""

import asyncio
import json
from agents import Agent, Runner
from agents.mcp import MCPServerSse

# Setup the SSE server parameters
SERVER_PARAMS = {"url": "http://localhost:8000/sse"}


async def main():
    # Initialize the MCP server (no async with block)
    mcp_server = MCPServerSse(
        params=SERVER_PARAMS,
        name="Museum Booking Server",
        cache_tools_list=True
    )

    try:
        # Manually open the connection
        await mcp_server.connect()
        print("✅ Connected to MCP server.")

        # Create the agent providing the MCP server connection
        travel_genie = Agent(
            name="Travel Genie",
            instructions=(
                "You are Travel Genie, a friendly and knowledgeable travel assistant. "
                "Always use the available tools to help users plan their trips, such "
                "as booking museum visits. Whenever you complete a booking or reservation, "
                "be sure to provide the user with all relevant confirmation details."
            ),
            mcp_servers=[mcp_server],
            model="gpt-4.1"
        )

        # Run the agent
        result = await Runner.run(
            starting_agent=travel_genie,
            input="Book 3 tickets to the Louvre for June 10, 2025"
        )

        # Print the final output
        print("\nFinal output:\n" + result.final_output + "\n")

        # Print input list to see tool use
        print("Input list:\n", json.dumps(result.to_input_list(), indent=2))

    except Exception as e:
        # Handle any errors that occur
        print(f"❌ An error occurred: {e}")

    finally:
        # Always ensure cleanup happens
        await mcp_server.cleanup()
        print("🧹 Cleaned up MCP server connection.")


if __name__ == "__main__":
    asyncio.run(main())
