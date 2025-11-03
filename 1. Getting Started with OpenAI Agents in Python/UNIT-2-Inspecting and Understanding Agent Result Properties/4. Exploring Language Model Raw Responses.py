"""
Your task is to examine the raw_responses list in the result object. To do this:
Write a for loop that goes through each response in result.raw_responses.
For each response, print it as a whole using a simple print statement.
This will help you see the detailed outputs from the language model and better understand what happens behind the scenes during an agent’s run.
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

# TODO: Write a for loop that goes through result.raw_responses and prints each response
for i in result.raw_responses:
    print(i)