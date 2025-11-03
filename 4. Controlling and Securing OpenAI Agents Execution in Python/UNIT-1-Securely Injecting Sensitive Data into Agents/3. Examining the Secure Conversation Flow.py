"""
Time to peek behind the curtain and see how your secure context injection works!
Your agent is booking hotels with sensitive data while keeping that information
hidden from the LLM—but can you prove it?

Print the complete conversation flow using result.to_input_list() (formatted with json.dumps())
to inspect what was actually exchanged between the user, the LLM, and your tools.
Look closely: you’ll see that only the hotel_name parameter is passed in function calls, and sensitive data like the passport number never appears in the conversation.

This is especially important if you plan to chain agents or build multi-step conversations.
By examining the output of to_input_list(), you can confirm that your context remains secure at every step.    
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

# Create an object with sensitive data
user_context = UserData(
    name="Alice Smith",
    passport_number="P123456789"
)


async def main():
    # Run the agent passing the sensitive data as context (context is NOT sent to the LLM)
    result = await Runner.run(
        starting_agent=travel_genie,
        input="Please book me a room at the Grand Plaza Hotel.",
        context=user_context
    )

    # Print the final output
    print("Final output:\n" + result.final_output)

    # TODO: Add a print statement to display the complete conversation flow using json.dumps(result.to_input_list(), indent=2)
    print(json.dumps(result.to_input_list(), indent=2))
     
if __name__ == "__main__":
    asyncio.run(main())