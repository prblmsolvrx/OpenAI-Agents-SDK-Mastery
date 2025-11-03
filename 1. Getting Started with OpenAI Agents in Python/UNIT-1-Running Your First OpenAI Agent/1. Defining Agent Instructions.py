"""
    In this exercise, you'll update the agent's instructions to create a travel
    assistant that recommends destinations only in Italy.
    This will help you see firsthand how changing the instructions directly shapes the agent's behavior—even when you use the same input prompt.
"""

from agents import Agent, Runner

# TODO: Modify the agent instructions to recommend only Italian destinations
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie who recommends destinations only in Italy, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    )
)

# Run the agent synchronously with an input prompt
result = Runner.run_sync(
    starting_agent=agent,
    input="What's your top recommendation for adventure seekers?"
)

# Print the agent's final output
print(result.final_output)