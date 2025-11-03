"""In this exercise:
Use the to_input_list() method on the result from the Travel Genie agent to get the full conversation as a list.
Print this list to confirm that it contains both the original honeymoon request and the Travel Genie’s response.
Run the Itinerary Writer agent using this input list so that it receives the complete context.
Print the Itinerary Writer’s response.
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
        input="Suggest a single destination for a honey moon."
    )
    print("Travel Genie response:\n" + result.final_output + "\n")

    # TODO: Get the full conversation as a list using result.to_input_list()
    input_list = result.to_input_list()
    # TODO: Run the Itinerary Writer agent with the input list as input
    itinerary_result = await Runner.run(
        starting_agent = itinerary_writer,
        input = input_list
    )
    # TODO: Print the Itinerary Writer's response
    # ✅ Print the Itinerary Writer's response
    print("Itinerary Writer response:\n" + itinerary_result.final_output + "\n")

if __name__ == "__main__":
    asyncio.run(main())