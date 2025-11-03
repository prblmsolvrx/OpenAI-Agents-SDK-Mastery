"""
In this exercise, you'll build a conversation_history list from scratch,
adding each message as the conversation unfolds. Instead of relying on helper
methods like to_input_list(), you'll construct the proper message format
yourself - dictionaries with "role" and "content" fields.

Your task is to:

Create an empty conversation history list
Add the user's first question as a properly formatted message
Run the agent with this history and capture its response
Store the agent's response in the history (with "role": "assistant")
Display the conversation so far
Add a follow-up question to the history
Run the agent again with the complete history
Print the agent's new response
This practice will give you a deeper understanding of conversation
structure and how to maintain context across multiple turns of dialogue—manually,
without relying on helper methods or including extra metadata.    
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
    # ✅ Create an empty conversation history list
    conversation_history = []

    # First user question
    user_input_1 = "Can you suggest a unique destination for a food lover?"

    # ✅ Add the user's first question as a properly formatted message
    conversation_history.append({
        "role": "user",
        "content": user_input_1
    })

    # ✅ Run the agent with this history and capture its response
    result_1 = await Runner.run(
        starting_agent=agent,
        input=conversation_history
    )

    # ✅ Store the agent's response in the history (with "role": "assistant")
    conversation_history.append({
        "role": "assistant",
        "content": result_1.final_output
    })

    # ✅ Display the conversation so far
    print("\n--- Conversation So Far ---")
    print(json.dumps(conversation_history, indent=2))

    # Follow-up user question
    user_input_2 = "What is the best time of year to visit?"

    # ✅ Add the follow-up question to the history
    conversation_history.append({"role": "user", "content": user_input_2})

    # ✅ Run the agent again with the complete history
    result_2 = await Runner.run(
        starting_agent=agent,
        input=conversation_history
    )

    # ✅ Print the agent's new response
    print("\n--- Agent’s New Response ---")
    print(result_2.final_output)


if __name__ == "__main__":
    asyncio.run(main())
