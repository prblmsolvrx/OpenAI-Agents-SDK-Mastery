"""
the goal is to extend the conversation history by appending a new user message before
passing it to the Itinerary Writer agent. This will show how you can layer new requests
onto the existing dialogue, making the workflow more dynamic.

Follow these steps:

Use the to_input_list() method on the result from the Travel Genie agent to get the full conversation as a list.
Create a new list that adds a user message asking for a "3-day itinerary" to the end of this conversation.
Run the Itinerary Writer agent using this new list as input.
Print the Itinerary Writer’s response.
This approach helps you see how to build more complex agent workflows by adding extra instructions at each step.    
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

    # TODO: Get the full conversation context as a list using result.to_input_list()
    conversation = result.to_input_list()

    # TODO: Create a new list that adds a user message requesting a 3-day itinerary
    conversation.append({
        "role": "user",
        "content": "Can you create a 3-day itinerary for that destination?"
    })
    # TODO: Run the Itinerary Writer agent with this new input
    itinerary_result = await Runner.run(
        starting_agent=itinerary_writer,
        input=conversation
    )
    # TODO: Print the Itinerary Writer's response
    print("Itinerary Writer response:\n" + itinerary_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())