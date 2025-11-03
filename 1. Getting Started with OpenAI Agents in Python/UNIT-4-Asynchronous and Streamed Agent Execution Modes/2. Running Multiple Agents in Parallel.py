"""
Suppose you want to get travel tips for both Japan and Italy.
The current code runs the two agent calls one after the other,
which means you have to wait for the first answer before starting
the second request. Your task is to update the code so that both
agent calls happen in parallel, making your program faster.

To run multiple agent calls at the same time, use asyncio.gather().
It starts both calls in parallel and returns their results together.

Example:

Python
Copy to clipboard
result1, result2 = await asyncio.gather(
    Runner.run(...),
    Runner.run(...)
)
This will help you see how running tasks in parallel can make your programs more efficient and responsive.    
    """

import asyncio
from agents import Agent, Runner

# Define the agent
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips. "
        "Be enthusiastic and tailor suggestions to the user's interests."
    ),
    model="gpt-4.1"
)


async def main():
    first_input = "What are the best travel tips for solo travelers in Japan?"
    second_input = "What are the best travel tips for families visiting Italy?"
    
    result1, result2 = await asyncio.gather(
        Runner.run(starting_agent=agent,
                   input=first_input),
        Runner.run(starting_agent=agent,
                   input=second_input)
    )
    
    print("First Output:")
    print(result1.final_output)
    
    print("\nSecond Output:")
    print(result2.final_output)

if __name__ == "__main__":
    asyncio.run(main())