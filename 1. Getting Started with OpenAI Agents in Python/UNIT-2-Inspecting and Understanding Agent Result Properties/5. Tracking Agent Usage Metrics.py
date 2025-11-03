"""
Your task is to update the code so that, instead of printing the entire response,
it prints only the usage attribute from each response in result.raw_responses.
This attribute contains important details about token counts and API usage.
To complete this exercise, change the loop so that it prints only the usage
information for each response by accessing response.usage.
Understanding usage metrics is important for keeping track of costs and
optimizing your agent’s performance.
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

# TODO: Change the print statement below to print only the usage attribute from each response
for response in result.raw_responses:
    print(response.usage)