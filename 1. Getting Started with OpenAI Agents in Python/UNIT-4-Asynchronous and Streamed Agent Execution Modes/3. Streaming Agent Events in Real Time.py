"""
Your task is to update the code so that it uses streaming mode instead of
the standard asynchronous approach. This will allow you to iterate over
the agent’s execution events as they arrive and print each event.
Here’s what you need to do:

Replace the regular asynchronous agent call with Runner.run_streamed to enable streaming.
Use an async for loop to go through each event from result.stream_events().
For each event, print the whole event.
This exercise will help you understand how to work with streamed agent
responses and see the structure of the events as they are generated.
"""

import asyncio
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


async def main():
    # ✅ Use streaming mode
    result = Runner.run_streamed(
        starting_agent=agent,
        input="What are the best travel tips for solo travelers in Japan?",
    )

    # ✅ Iterate over and print each streaming event
    async for event in result.stream_events():
        print("Event:", event)


if __name__ == "__main__":
    asyncio.run(main())
