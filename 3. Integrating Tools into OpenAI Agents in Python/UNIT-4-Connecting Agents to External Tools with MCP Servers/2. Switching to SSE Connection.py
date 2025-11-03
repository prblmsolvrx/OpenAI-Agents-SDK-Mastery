"""
Your task is to update the code so that it connects to this remote MCP server using SSE instead of Stdio.
Here’s what you need to do:

Change the import to use MCPServerSse instead of MCPServerStdio.
Update the SERVER_PARAMS dictionary to use the URL "http://localhost:8000/sse" (as shown in the lesson).
Update the async with block to use MCPServerSse instead of MCPServerStdio.
Leave the rest of the code unchanged so that it still lists and prints the available tools from the server.
This hands-on task will help you get comfortable switching between local and remote
MCP server connections, and reinforce how easy it is to adapt your code for different environments.    
"""

import asyncio
# TODO: Change the import to use MCPServerSse instead of MCPServerStdio
from agents.mcp import  MCPServerSse

# TODO: Change the parameters to connect to the SSE endpoint at http://localhost:8000/sse
SERVER_PARAMS = {
   "url" : "http://localhost:8000/sse"
}


async def main():
    # TODO: Change the class to MCPServerSse to use SSE transport
    async with  MCPServerSse(
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