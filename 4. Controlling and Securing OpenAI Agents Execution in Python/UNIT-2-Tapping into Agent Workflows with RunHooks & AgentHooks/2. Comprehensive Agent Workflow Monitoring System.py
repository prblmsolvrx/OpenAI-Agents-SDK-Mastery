"""
Building on your success with basic agent monitoring, it's time to create a comprehensive
workflow observer that captures every important event in your agent system!
Your previous exercise gave you visibility into when agents start, but real production
systems need much more detailed monitoring to understand what's happening under the hood.

You currently have a GlobalHooks class with a working on_agent_start method,
but it's missing two critical monitoring capabilities. Your task is to expand this
monitoring system by implementing the remaining hook methods:

Implement the on_tool_end method to log tool execution results, showing which agent used
which tool and what result was returned.
Implement the on_handoff method to track agent transitions, displaying when control passes
from one agent to another.
When you finish implementing these methods, you'll have a complete monitoring system that
provides real-time visibility into agent starts, tool executions, and handoffs across your
entire workflow. This comprehensive observability is exactly what you need to debug complex
agent interactions and understand how your AI system behaves in production!
"""

import asyncio
from agents import Agent, Runner
from agents.lifecycle import RunHooks
from utils import UserData, fetch_user_data, book_hotel


class GlobalHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print(f"[GLOBAL] {agent.name} agent starting")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"[GLOBAL] {agent.name} -> {tool.name} returned: {result}")

    async def on_handoff(self, context, from_agent, to_agent):
        print(f"[GLOBAL] {from_agent.name} handed to {to_agent.name}")


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

safety_expert = Agent(
    name="Travel Safety Expert",
    instructions=(
        "You are a travel safety expert. "
        "Provide safety advice and important precautions for travelers."
    ),
    model="gpt-4.1"
)

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

user_context = UserData(
    name="Alice Smith",
    passport_number="P123456789"
)


async def main():
    result = await Runner.run(
        starting_agent=triage,
        input="Please book me a room at the Grand Plaza Hotel.",
        context=user_context,
        hooks=GlobalHooks()
    )
    print("\nFinal output:\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
