"""
Continue the conversation by running the agent with the new list that now includes a follow-up question.
After the agent responds, observe how it maintains context from the previous messages.
To complete this task:

Run the agent again, this time passing in the full conversation history
(including the follow-up message).
Print the agent’s second response.
This will help you see how the agent understands and responds to
follow-up questions based on the context established in earlier messages, creating a more natural and coherent conversation flow.
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
    
    # Get the conversation history after the first turn
    input_list = result.to_input_list()
    
    # Create a follow-up input with conversation history
    follow_up_input = input_list + [
        {
            "role": "user",
            "content": "What is the best time of year to visit?"
        }
    ]
    
    # TODO: Run the agent with the follow up input that includes the conversation history
    # TODO: Print the second response
    # ✅ Run the agent again with conversation history
    follow_up_result = await Runner.run(
        starting_agent=agent,
        input=follow_up_input
    )
    
    # ✅ Print the second response
    print("Second answer:\n" + follow_up_result.final_output + "\n")

if __name__ == "__main__":
    asyncio.run(main())