"""
Your goal is to build a joke-telling agent—an AI that always has a funny quip ready.
Give your agent a unique name and write clear, detailed instructions that explain its job: to tell short,
lighthearted jokes whenever someone asks. You can also choose a specific model for your agent if you want to experiment.
Here’s what to do:

Define an agent with a creative name and instructions that make it clear the agent’s job is to tell jokes.
(Optional) Pick a model for your agent.
Run your agent synchronously using Runner.run_sync with a prompt asking for a joke.
Print the agent’s final output.
"""

from agents import Agent, Runner, ModelSettings

# TODO: Define an agent for a joke-telling role
agent = Agent(
    name="Joke Teller",
    instructions=(
        "Your job is to tell funny good jokes which will make people laugh"
    ),
    model="gpt-4.1",
    model_settings=ModelSettings(
        temperature=0.9,
        max_tokens=100
    )
)
# TODO: Run the agent synchronously with an appropriate input
result = Runner.run_sync(
    starting_agent=agent,
    input="Tell Jokes"
)
# TODO: Print the agent's final output
print(result.final_output)