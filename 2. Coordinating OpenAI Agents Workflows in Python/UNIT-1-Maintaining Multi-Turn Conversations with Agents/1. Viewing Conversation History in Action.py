"""
Set up an initial conversation by running the agent with a simple user question.
Once you receive the agent's response, use the correct method to get the
conversation history as a list. Format this list using a JSON tool so that it is easy to read, and print it out.

Use the method that returns the full conversation so far.
Format the output with indentation for better readability.
Print the formatted conversation history to check that each message contains the expected keys.
This exercise will help you see exactly how the agent tracks the dialogue,
which is a key step in building more natural conversations.
"""

import json
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
    # Run the agent with an initial input
    result = await Runner.run(
        starting_agent=agent,
        input="Can you suggest a unique destination for a food lover?"
    )
    
    # Print the first response
    print("First answer:\n" + result.final_output + "\n")
    
    # TODO: Get the conversation history as a list using the correct method
    conversation_history = result.to_input_list()
    # TODO: Print the input list formatted as JSON for readability
    print("Conversation history:\n")
    print(json.dumps(conversation_history, indent=2))

if __name__ == "__main__":
    asyncio.run(main())