"""
Run the code and see how the agent handles the updated input list.
Once you spot the issue, make the necessary correction so the agent can reply properly.

This will help you practice debugging multi-turn conversations
and ensure your agent-powered applications work smoothly.    
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
    # Run the agent with an initial input
    result = await Runner.run(
        starting_agent=agent,
        input="Can you suggest a unique destination for a food lover?"
    )
    
    # Print the first response
    print("First answer:\n" + result.final_output + "\n")
    
    # Create a follow-up input with conversation history
    follow_up_input = result.to_input_list() + [
        {
            "role": "user",
            "content": "What is the best time of year to visit?"
        }
    ]

    # Run the agent with the follow-up input
    follow_up_result = await Runner.run(
        starting_agent=agent,
        input=follow_up_input
    )
    
    # Print the second response
    print("Second answer:\n" + follow_up_result.final_output + "\n")

if __name__ == "__main__":
    asyncio.run(main())