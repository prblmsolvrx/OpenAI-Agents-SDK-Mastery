"""
In real-world agent workflows, sensitive context often needs to flow securely across multiple agent handoffs.
In this exercise, you'll observe how the OpenAI Agents SDK maintains secure context sharing as
requests are routed between agents.
Currently, the code runs the Travel Genie agent directly, bypassing the triage system. Change the starting_agent
in Runner.run() from travel_genie to triage. This will route the booking request through the triage agent first,
which will recognize it as a booking task and hand it off to Travel Genie.
The remarkable part? The same sensitive user_context will still be available to Travel Genie when
it calls the book_hotel function, even though it has traveled through a handoff chain!
This demonstrates how the OpenAI Agents SDK maintains secure context across the entire agent workflow,
ensuring your sensitive data remains protected while enabling sophisticated multi-agent architectures.
"""

import json
import uuid
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, function_tool, RunContextWrapper


# Define a context model to hold sensitive user data
class UserData(BaseModel):
    name: str
    passport_number: str


# Define a function tool that uses context data
@function_tool
def book_hotel(wrapper: RunContextWrapper[UserData], hotel_name: str) -> str:
    # Access sensitive data from the context
    user = wrapper.context

    # Process sensitive data...
    print(f"DEBUG: Booking for {user.name}\n")
    print(f"DEBUG: Passport number is {user.passport_number}\n")
    
    # Return confirmation
    return {
        "hotel_name": hotel_name,
        "guest_name": user.name,
        "confirmation_success": True,
        "confirmation_id": str(uuid.uuid4())
    }


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
    # TODO: Change starting_agent from travel_genie to triage to see context sharing across handoffs
    result = await Runner.run(
        starting_agent=triage,
        input="Please book me a room at the Grand Plaza Hotel.",
        context=user_context
    )

    # Print the final output
    print("Final output:\n" + result.final_output)

    # Print input list to see tool use
    print("Input list:\n", json.dumps(result.to_input_list(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())