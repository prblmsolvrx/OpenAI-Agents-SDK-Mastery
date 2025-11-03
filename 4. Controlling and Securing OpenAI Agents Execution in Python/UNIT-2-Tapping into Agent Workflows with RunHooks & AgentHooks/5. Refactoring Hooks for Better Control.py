"""
Currently, your monitoring system uses a "one-size-fits-all" approach,
where global RunHooks track everything, including tool executions across all agents.
But what if you want more granular control? What if you need detailed tool monitoring
for specific agents while keeping global monitoring lightweight?

Your mission is to refactor the existing hook system by moving tool monitoring from
the global scope to the agent-specific scope:

Remove the on_tool_end method from the GlobalHooks class, since tool monitoring will become agent-specific.
Add an on_tool_start method to TravelGenieHooks that prints when the Travel Genie agent is about to call a tool.
Add an on_tool_end method to TravelGenieHooks that prints the tool execution results specifically
 for the Travel Genie agent.
This refactoring demonstrates that hook architecture isn't set in stone —
you can reorganize monitoring responsibilities as your system grows and requirements change.
Master this flexibility, and you'll be ready to build adaptable agent systems that evolve with your needs!    
"""

import asyncio
from agents import Agent, Runner
from agents.lifecycle import AgentHooks, RunHooks
from utils import fetch_user_data, book_hotel


# ------------------------------
# Global hooks for monitoring the entire run lifecycle
# ------------------------------
class GlobalHooks(RunHooks):
    # Called when any agent starts
    async def on_agent_start(self, context, agent):
        print(f"[GLOBAL] {agent.name} agent starting")

    # Called when a handoff occurs between agents
    async def on_handoff(self, context, from_agent, to_agent):
        print(f"[GLOBAL] {from_agent.name} handed to {to_agent.name}")


# ------------------------------
# Per-agent hooks for Travel Genie
# ------------------------------
class TravelGenieHooks(AgentHooks):
    # Called when agent starts
    async def on_start(self, context, agent):
        # Inject user data into context
        context.context = fetch_user_data()
        print(f"[AGENT HOOKS] {agent.name} starting with context: {context.context}")
        
    # Called when agent finishes
    async def on_end(self, context, agent, output):
        print(f"[AGENT] {agent.name} completed with output:\n{output}")
    
    # Called when this agent is about to call a tool
    async def on_tool_start(self, context, agent, tool):
        print(f"[AGENT HOOKS] {agent.name} is about to run tool: {tool.name}")
    
    # Called when this agent finishes running a tool
    async def on_tool_end(self, context, agent, tool, result):
        print(f"[AGENT HOOKS] {agent.name} -> {tool.name} returned: {result}")


# ------------------------------
# Agents
# ------------------------------
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
    hooks=TravelGenieHooks()  # Attach agent hooks
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


# ------------------------------
# Main runner
# ------------------------------
async def main():
    # Run the agent
    result = await Runner.run(
        starting_agent=triage,
        input="Please book me a room at the Grand Plaza Hotel.",
        hooks=GlobalHooks()  # Attach run hooks
    )

    # Print the final output
    print("Final output:\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
