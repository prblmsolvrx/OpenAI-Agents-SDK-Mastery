"""
Your task:
Filter the items in result.new_items to only show those with type "message_output_item"
For each message item you find, extract and display:
The agent's name (available at item.agent.name)
The message content (available at item.raw_item.content[0].text)
This filtering technique is particularly useful when working with
complex agent runs that might include tool calls, thinking steps, and other non-message items.
"""

from agents import Agent, Runner

# Define the agent
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1"
)

# Run the agent synchronously with an input prompt
result = Runner.run_sync(
    starting_agent=agent,
    input="What's your top recommendation for adventure seekers?"
)

# TODO: For each message_output_item, print the agent's name and the message content
for item in result.new_items:
    if item.type == "message_output_item":
        agent_name = item.agent.name
        message_text = item.raw_item.content[0].text
        print(f"Agent: {agent_name}\nMessage: {message_text}\n")