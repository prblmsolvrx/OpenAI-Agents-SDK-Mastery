"""
In this exercise, you’ll work with a code snippet that isn’t working as expected.
Your task is to carefully review
the code, spot what’s wrong, and make the necessary changes so that
the agent runs successfully and displays its final output.
This is a great chance to practice your debugging skills and become
comfortable with the basics of running agents.
"""
from agents import Agent, Runner, ModelSettings

# Define the agent
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
    model_settings=ModelSettings(
        temperature=0.9,  # Controls creativity (0-2)
        max_tokens=100    # Limits response length
    )
)

# Run the agent synchronously with an input prompt
result = Runner.run_sync(
    starting_agent=agent,
    input="What's your top recommendation for adventure seekers?"
)

# Print the agent's final output
print(result.final_output)