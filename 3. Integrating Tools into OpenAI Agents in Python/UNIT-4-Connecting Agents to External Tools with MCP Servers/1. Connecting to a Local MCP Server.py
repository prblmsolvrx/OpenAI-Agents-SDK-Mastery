"""You have access to a Python MCP server script at mcp_server.py.
Your task is to configure the SERVER_PARAMS dictionary so that your code launches this script as a subprocess using Python.
This setup should happen inside the async with block, just as demonstrated in the lesson.
When your code runs, it should connect to the MCP server and display the details of each tool the server offers.
This will give you a clear, practical view of how your code interacts with the MCP server and retrieves tool
information—demonstrating the concepts you just learned in action.
"""

import asyncio
from agents.mcp import MCPServerStdio

# TODO: Fill in the correct parameters to launch the MCP server as a subprocess
SERVER_PARAMS = {
    "command": "python",
    "args": ["mcp_server.py"],
}


async def main():
    # Connect to the MCP server via stdio
    async with MCPServerStdio(
        params=SERVER_PARAMS,
        name="Museum Booking Server",
        cache_tools_list=True
    ) as mcp_server:
        # List all the available tools from the server
        tools = await mcp_server.list_tools()

        # Print each tool's details
        for tool in tools:
            print("Name:", tool.name)
            print("Description:\n" + tool.description)
            print("Input Schema:\n" + str(tool.inputSchema))

if __name__ == "__main__":
    asyncio.run(main())