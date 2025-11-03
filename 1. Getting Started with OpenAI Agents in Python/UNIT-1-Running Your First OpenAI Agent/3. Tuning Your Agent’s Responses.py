"""
Import the ModelSettings class from the agents module.
Add a model_settings parameter to your agent.
Set the temperature to 0.9 to encourage the agent
to suggest different destinations each time, making its answers less repetitive.
Set max_tokens to 100 to keep responses short and help control API costs.
Note: The model does not know in advance that it must finish
its answer within the max_tokens limit. If its response is too long,
it may get cut off mid-sentence. This is a trade-off for
keeping answers brief and costs predictable.

After updating your agent, run it with the travel prompt and print
the final output. Observe how these settings make the agent's responses
more varied and concise, but also notice if the output ever gets truncated.
"""

from agents import Agent, Runner, ModelSettings

# TODO: Import ModelSettings from the agents module

# Define the agent
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
    # TODO: Add model_settings with temperature=0.9 and max_tokens=100
    model_settings=ModelSettings(
        temperature=0.9,  # Controls creativity (0-2)
        max_tokens=100    # Limits response length
    )
)

# Run the agent synchronously with an input prompt
result = Runner.run_sync(
    starting_agent=agent,
    input="Can you suggest a unique place for a quick weekend adventure?"
)

# Print the agent's final output
print(result.final_output)