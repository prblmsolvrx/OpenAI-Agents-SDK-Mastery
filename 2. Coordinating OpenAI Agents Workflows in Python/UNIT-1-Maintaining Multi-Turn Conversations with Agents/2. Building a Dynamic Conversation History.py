"""
Start by creating a new list by adding a follow-up user message to the end of the input
list, preserving the correct order and structure.
Print the updated conversation list, again using JSON formatting for clarity.
This task will help you practice managing and extending the conversation history,
ensuring your agent can handle multi-turn dialogues naturally and contextually.    
"""

import asyncio
from agents import Agent, Runner
import json

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
    # Run the agent with an initial input
    result = await Runner.run(
        starting_agent=agent,
        input="Can you suggest a unique destination for a food lover?"
    )
    
    # Print the first response
    print("First answer:\n" + result.final_output + "\n")
    
    # Get the conversation history as a list
    input_list = result.to_input_list()
    
    # Print the input list formatted as JSON for readability
    print("Input list:\n" + json.dumps(input_list, indent=2) + "\n")
    
    # TODO: Create a new list by appending a follow-up user message
    follow_up_input = result.to_input_list() + [
      {
        "role": "user",
        "content": "What is the best time of year to visit?"
      }
    ]
    # TODO: Print the updated input list with the follow-up message
    print("Input list with follow up message:\n" + json.dumps(follow_up_input, indent=2) + "\n")
    
if __name__ == "__main__":
    asyncio.run(main())