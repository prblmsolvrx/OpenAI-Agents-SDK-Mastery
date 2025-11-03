"""
You have a complete travel agent system with three agents
(Travel Triage, Travel Genie, and Travel Safety Expert)
that can handle hotel bookings and handoffs between agents.
However, this system currently runs without any visibility into what is happening behind the scenes.

Your task is to add global monitoring by:

Creating a new class that inherits from RunHooks
Implementing the on_agent_start method to print a message showing which agent is starting
Attaching your hook class to the Runner.run() call using the hooks parameter
When you run the completed code, you'll see real-time messages showing exactly
when each agent becomes active during the workflow.
This is your first step toward building sophisticated agent monitoring
systems that give you complete visibility into your AI workflows!    
"""

import asyncio
from agents import Agent, Runner
from agents.lifecycle import RunHooks
from utils import UserData, fetch_user_data, book_hotel


# ✅ Corrected: first parameter after self is context, then agent
class TravelHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        """Called when an agent starts running."""
        print(f"🚀 Starting agent: {agent.name}")


# Travel Genie agent with the booking tool
travel_genie = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Always use the available tools to help users plan their trips, such "
        "as booking hotels. Whenever you complete a booking or reservation, "
        "be sure to provide the user with all relevant confirmation details."
    ),
    tools=[book_hotel],
    model="gpt-4.1"
)

# Travel safety expert agent
safety_expert = Agent(
    name="Travel Safety Expert",
    instructions=(
        "You are a travel safety expert. "
        "Provide safety advice and important precautions for travelers."
    ),
    model="gpt-4.1"
)

# Triage agent that delegates tasks
triage = Agent(
    name="Travel Triage",
    instructions=(
        "You are a travel triage agent. Given a request:\n"
        "- For destination or itinerary questions, transfer to Travel Genie\n"
        "- For safety or health concerns, transfer to the Travel Safety Expert"
    ),
    handoffs=[travel_genie, safety_expert],
    model="gpt-4.1"
)

# Create an object with sensitive data
user_context = UserData(
    name="Alice Smith",
    passport_number="P123456789"
)


async def main():
    # Attach the hooks parameter here
    result = await Runner.run(
        starting_agent=triage,
        input="Please book me a room at the Grand Plaza Hotel.",
        context=user_context,
        hooks=TravelHooks()  # attach custom lifecycle hooks
    )

    # Print the final output
    print("\n✅ Final output:\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
