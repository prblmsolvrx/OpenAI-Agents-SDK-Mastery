"""
Here’s what you need to do:
Wrap the agent execution code inside an async function.
Replace the synchronous agent call with the asynchronous version by using await Runner.run().
Update the program’s entry point to use asyncio.run to start your async function.
Don’t forget to import asyncio at the top of the file.
This exercise will help you become comfortable with async/await and prepare you to build more interactive applications.  
"""

from agents import Agent, Runner
# TODO: Import the asyncio package
import asyncio
# Define the agent
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1"
)

# TODO: Wrap the agent execution into an async function and run it asynchronously
async def main():
    result = await Runner.run(
    starting_agent=agent,
    input="What are the best travel tips for solo travelers in Japan?",
    )# Print the agent's final output
    print(result.final_output)



# TODO: Use asyncio.run to start the async function
if __name__ == "__main__":
    asyncio.run(main())