"""
Your task is explore the contents of the new_items list in the result
object by displaying each item in result.new_items as a whole.
This will help you see the full structure of each step the agent took during its run.
Write a for loop that goes through each item in result.new_items.
For each item, print the item itself.
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

# TODO: Write a for loop that goes through result.new_items and prints each item
for r in result.new_items:
    print("Result : new items ", r)