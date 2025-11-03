"""
Your task is to extend the given script so that, in addition to printing the agent's final output, it also prints:

The original input provided to the agent
The name of the last agent that ran
Add two print statements after the existing one, each with a clear label for what is being displayed.
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

# Print the agent's final output
print("Final Output:", result.final_output)

# TODO: Print the original input provided to the agent
print("original input ", result.input)
# TODO: Print the last agent that ran
print("last agent ", result.last_agent.name)