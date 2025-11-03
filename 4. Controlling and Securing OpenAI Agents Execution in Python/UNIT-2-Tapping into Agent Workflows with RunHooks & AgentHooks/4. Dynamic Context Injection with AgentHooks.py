"""
Currently, your system uses the "old-school" approach of creating a static
UserData object and passing it to Runner.run() at the beginning.
This works, but what if user data changes between when you start the
workflow and when the Travel Genie agent actually needs it? Dynamic context
injection solves this by fetching the latest data right before the agent executes.

Your mission is to transform this static system into a dynamic one by:

Implementing the on_start method in the TravelGenieHooks class to call
fetch_user_data() and assign the result to context.context
Delete the creation of the UserData object and do not pass the context
parameter to Runner.run(), since you'll be injecting it dynamically instead    
"""

import asyncio
from agents import Agent, Runner
from agents.lifecycle import AgentHooks, RunHooks
from utils import UserData, fetch_user_data, book_hotel


# Global hooks for monitoring the entire run lifecycle
class GlobalHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print(f"[GLOBAL] {agent.name} agent starting")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"[GLOBAL] {agent.name} -> {tool.name} returned: {result}")

    async def on_handoff(self, context, from_agent, to_agent):
        print(f"[GLOBAL] {from_agent.name} handed to {to_agent.name}")


# Per-agent hooks for Travel Genie
class TravelGenieHooks(AgentHooks):
    async def on_start(self, context, agent):
        # Dynamically fetch user data and assign it to the context
        context.context = fetch_user_data()
        print(f"[AGENT] {agent.name} context initialized: {context.context}")

    async def on_end(self, context, agent, output):
        print(f"[AGENT] {agent.name} completed with output:\n{output}")


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
    model="gpt-4.1",
    hooks=TravelGenieHooks()  # Attach the agent hooks
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
    handoffs=[
        travel_genie,
        safety_expert
    ],
    model="gpt-4.1"
)


async def main():
    result = Runner.run(
        starting_agent=triage,
        input="Please book me a room at the Grand Plaza Hotel.",
        # context removed to allow dynamic context injection by TravelGenieHooks
        hooks=GlobalHooks()
    )

    print("Final output:\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
