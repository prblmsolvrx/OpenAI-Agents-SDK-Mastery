"""
In the code, the Travel Genie agent has already been run and its response has been printed.
The next step is to pass the Travel Genie’s output to the Itinerary Writer agent, but this time,
only the raw text output (not the full conversation or any extra context) should be used as input.
Run the Itinerary Writer agent using only result.final_output as the input.
Print the Itinerary Writer’s response immediately after.
This exercise will help you see what happens when agents are chained without sharing the full context.
"""

import asyncio
from agents import Agent, Runner

# Define the first agent (Travel Genie)
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1"
)

# Define the second agent (Itinerary Writer)
itinerary_writer = Agent(
    name="Itinerary Writer",
    instructions=(
        "You are an expert travel itinerary writer. "
        "Given a destination and user interests, create a concise itinerary."
    ),
    model="o4-mini"
)


async def main():
    # Run the first agent
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Suggest a single destination for a honeymoon."
    )
    print("Travel Genie response:\n" + result.final_output + "\n")

    # Use ONLY the raw output from Travel Genie as input
    itinerary_result = await Runner.run(
        starting_agent=itinerary_writer,
        input=result.final_output
    )

    print("Itinerary Writer response:\n" + itinerary_result.final_output + "\n")


if __name__ == "__main__":
    asyncio.run(main())
