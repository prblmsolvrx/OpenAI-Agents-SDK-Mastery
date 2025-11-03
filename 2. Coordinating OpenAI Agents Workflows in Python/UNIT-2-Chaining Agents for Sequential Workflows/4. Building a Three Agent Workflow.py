"""
Your task is to:
Define a new Packing List Generator agent using a reasoning model (since it receives input from o4-mini).
Chain it by passing the updated conversation history with a user message requesting a packing list.
Print the response from the Packing List Generator agent.
This exercise demonstrates chaining multiple agents while understanding compatibility requirements between reasoning and non-reasoning models.
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

# TODO: Define the third agent (Packing List Generator)
# Note: Use a reasoning model since it receives input from o4-mini
# Define the third agent (Packing List Generator)
packing_list_generator = Agent(
    name="Packing List Generator",
    instructions=(
        "You are an expert in creating detailed packing lists based on a travel itinerary."
    ),
    model="o4-mini"
)

async def main():
    # Step 1: Run the Travel Genie agent
    genie_result = await Runner.run(
        starting_agent=travel_genie,
        input="Suggest a single destination for a honeymoon."
    )
    print("Travel Genie response:\n" + genie_result.final_output + "\n")

    # Step 2: Prepare input for the Itinerary Writer
    itinerary_input = genie_result.to_input_list() + [
        {
            "role": "user",
            "content": "Write a 3-day itinerary."
        }
    ]
    itinerary_result = await Runner.run(
        starting_agent=itinerary_writer,
        input=itinerary_input
    )
    print("Itinerary Writer response:\n" + itinerary_result.final_output + "\n")

    # Step 3: Prepare input for the Packing List Generator
    packing_input = itinerary_result.to_input_list() + [
        {
            "role": "user",
            "content": "Please create a detailed packing list for this trip."
        }
    ]

    # Step 4: Run the Packing List Generator agent
    packing_result = await Runner.run(
        starting_agent=packing_list_generator,
        input=packing_input
    )

    print("Packing List Generator response:\n" + packing_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())