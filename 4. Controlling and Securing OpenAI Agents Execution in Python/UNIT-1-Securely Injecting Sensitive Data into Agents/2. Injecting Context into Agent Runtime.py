"""
    You have a perfectly secure book_hotel function that expects sensitive
    user data through a RunContextWrapper[UserData], but if you run the current code,
    it will fail because no context is being provided to the agent. The function is
    ready to receive secure data, but there is nothing to receive.

Your mission is to:

Create a UserData object containing sample sensitive information.
Pass this sensitive data to the Runner.run() method using the context parameter.
Once you complete these steps, you'll see the agent successfully book a hotel
using the sensitive data without ever exposing it to the LLM.
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
def book_hotel(wrapper: RunContextWrapper[UserData], hotel_name: str) -> dict:
    # Access sensitive data from the context
    user = wrapper.context

    # Process sensitive data...
    print(f"DEBUG: Booking for {user.name}")
    print(f"DEBUG: Passport number is {user.passport_number}")
    
    # Return confirmation
    return {
        "hotel_name": hotel_name,
        "guest_name": user.name,
        "confirmation_success": True,
        "confirmation_id": str(uuid.uuid4())
    }


# Define the Travel Genie agent with the booking tool
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


# Create a UserData object with sample sensitive data
user_context = UserData(
    name="Soumik Ghosh",
    passport_number="A1234567"
)


async def main():
    # Add the context parameter to pass the sensitive user data
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Please book me a room at the Grand Plaza Hotel.",
        context=user_context
    )

    # Print the final output
    print("Final output:\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
