"""
In this task, your mission is to add an agent-specific
layer that shows you exactly what an individual agent produces when it finishes its work.
For that, you'll need to:
Create a class that inherits from AgentHooks
Implement the on_end method to capture and display the agent's name and completion output
Attach this agent-specific hooks to the Travel Genie agent instance
When you complete this exercise, you'll see both monitoring systems working
in harmony — global events showing the big picture and agent-specific events showing
detailed insights for individual agents. This combination gives you the complete observability
toolkit you need for sophisticated AI agent systems!
"""

import asyncio
from agents import Agent, Runner
from agents.lifecycle import AgentHooks, RunHooks
from utils import UserData, fetch_user_data, book_hotel


# Global hooks for monitoring the entire run lifecycle
class GlobalHooks(RunHooks):
    # Called when any agent starts
    async def on_agent_start(self, context, agent):
        print(f"[GLOBAL] {agent.name} agent starting")

    # Called when any tool finishes execution
    async def on_tool_end(self, context, agent, tool, result):
        print(f"[GLOBAL] {agent.name} -> {tool.name} returned: {result}")

    # Called when a handoff occurs between agents
    async def on_handoff(self, context, from_agent, to_agent):
        print(f"[GLOBAL] {from_agent.name} handed to {to_agent.name}")


# TODO: Create a new class that inherits from AgentHooks
    # TODO: Implement the on_end method to print the agent's name and its output
# Agent-specific hooks
class TravelGenieHooks(AgentHooks):
    async def on_end(self, context, agent, output):
        print(f"[AGENT HOOK] {agent.name} finished with output: {output}")


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
    # TODO: Add the hooks parameter to attach your AgentHooks
    hooks=TravelGenieHooks()  # <-- attach the agent hooks here
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

# Create an object with sensitive data
user_context = UserData(
    name="Alice Smith",
    passport_number="P123456789"
)


async def main():
    # Run the agent
    result = await Runner.run(
        starting_agent=triage,
        input="Please book me a room at the Grand Plaza Hotel.",
        context=user_context,
        hooks=GlobalHooks()
    )

    # Print the final output
    print("Final output:\n" + result.final_output)

if __name__ == "__main__":
    asyncio.run(main())