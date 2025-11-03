"""
    Suppose you need your agent to plan a complex group trip—comparing destinations, balancing costs,
    and building a detailed itinerary. For this, you’ll want a reasoning-optimized model.
    The OpenAI Agents SDK lets you set the model parameter when creating your agent. In this exercise, update the agent’s
    configuration to use the "o4-mini" model, which is designed for strong reasoning and efficiency.
"""

from agents import Agent, Runner

# TODO: Add the model parameter and set it to "o4-mini"
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="o4-mini"
)

# Run the agent synchronously with an input prompt
result = Runner.run_sync(
    starting_agent=agent,
    input=(
        "We’re a group of four friends with a $2,000 per-person budget "
        "and two weeks off. We love hiking and water sports, but want to "
        "manage costs and safety. Which single destination would you "
        "recommend under these constraints? Please compare at least two "
        "options on cost, climate, and activity variety, then outline a "
        "7-day itinerary with daily activities and rough budgets."
    )
)

# Print the agent's final output
print(result.final_output)