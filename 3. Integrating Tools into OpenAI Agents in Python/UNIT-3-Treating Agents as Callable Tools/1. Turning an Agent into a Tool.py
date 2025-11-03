"""
In this exercise, take the provided researcher agent and convert it into a callable tool using the
.as_tool() method. Give your tool a custom name and description so it’s easy to identify and use later.
Once the tool is created, print it to see its key attributes.
Follow these steps:
Use the .as_tool() method on the researcher agent, setting the tool name to "research_information" and
the description to "Research the web for travel information".
Assign the result to a variable.
Print the resulting tool object to inspect its details.
This hands-on task will help you understand how agents can be wrapped and reused as tools, making
your AI systems more organized and powerful.
"""

from agents import Agent, WebSearchTool

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

# TODO: Convert the researcher agent into a callable tool using .as_tool(...)

# TODO: Print the resulting tool object

# ✅ Convert the researcher agent into a callable tool
research_tool = researcher.as_tool(
    tool_name="research_information",
    tool_description="Research the web for travel information"
)

# ✅ Print the resulting tool object
print(research_tool)