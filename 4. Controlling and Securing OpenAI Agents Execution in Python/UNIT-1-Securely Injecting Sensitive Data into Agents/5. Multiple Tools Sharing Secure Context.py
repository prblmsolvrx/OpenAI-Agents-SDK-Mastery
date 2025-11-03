"""
Building on your mastery of secure context injection with a single tool,
it's time to expand your agent's capabilities by adding multiple tools that
can all safely share the same sensitive data!

Your current book_hotel function is working perfectly with secure context injection,
but real travel agents need to handle more than just hotels.
You'll create a second tool function called book_flight that follows
the same secure pattern as your hotel booking function.

Your tasks are:

Implement the book_flight function with RunContextWrapper[UserData] and flight_number: str parameters.
Access the user's sensitive data from wrapper.context and print debug messages showing
the name and passport number being used for flight booking.
Return a dictionary with flight booking details, including the passenger name,
flight number, booking success status, and a generated confirmation ID.
Add the new book_flight tool to the Travel Genie agent's tools list.
Update the agent's instructions to mention that it can now book both hotels and flights for users.
Modify the user input to request both a hotel booking and a flight booking in a single prompt with specific details.
This exercise demonstrates how multiple tools can securely access the same sensitive
context without any risk of data exposure to the LLM. You're building the foundation for
sophisticated multi-tool agents that handle complex workflows while keeping user data completely secure!
    
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
    print(f"DEBUG: Booking hotel for {user.name}\n")
    print(f"DEBUG: Passport number is {user.passport_number}\n")
    
    # Return confirmation
    return {
        "hotel_name": hotel_name,
        "guest_name": user.name,
        "confirmation_success": True,
        "confirmation_id": str(uuid.uuid4())
    }


# TODO: Create a book_flight function that takes wrapper: RunContextWrapper[UserData] and flight_number: str
@function_tool
def book_flight(wrapper: RunContextWrapper[UserData], flight_number: str) -> dict:
    # Access sensitive data from the context
    user = wrapper.context

    # Process sensitive data...
    print(f"DEBUG: Booking flight for {user.name}")
    print(f"DEBUG: Passport number is {user.passport_number}")

    # Return confirmation
    return {
        "flight_number": flight_number,
        "passenger_name": user.name,
        "confirmation_success": True,
        "confirmation_id": str(uuid.uuid4())
    }

# Define the Travel Genie agent with both booking tools
travel_genie = Agent(
    name="Travel Genie",
    # TODO: Update the agent's instructions to mention that it can now book both hotels and flights
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Always use the available tools to help users plan their trips, such "
        "as booking hotels. Whenever you complete a booking or reservation, "
        "be sure to provide the user with all relevant confirmation details."
    ),
    # TODO: Add book_flight to the tools list
    tools=[book_hotel, book_flight],
    model="gpt-4.1"
)

# Create an object with sensitive data
user_context = UserData(
    name="Alice Smith",
    passport_number="P123456789"
)


async def main():
    # Run the agent passing the sensitive data as context (context is NOT sent to the LLM)
    result = await Runner.run(
        starting_agent=travel_genie,
        # TODO: Modify the input to request both hotel and flight booking with specific details
        input="Please book me a room at the Grand Plaza Hotel and a flight with number AI203 ",
        context=user_context
    )

    # Print the final output
    print("Final output:\n" + result.final_output)

    # Print input list to see tool use
    print("Input list:\n", json.dumps(result.to_input_list(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())