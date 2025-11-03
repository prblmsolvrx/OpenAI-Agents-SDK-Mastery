"""
Currently, the given book_hotel function takes name and passport_number as separate parameters,
which means the LLM can see and potentially expose this sensitive information. You'll need to:

Create a UserData Pydantic model to structure the sensitive information with name and passport_number fields.
Modify the book_hotel function to use RunContextWrapper[UserData] as its first parameter and only
hotel_name: str as the second parameter.
Update the function body to access sensitive data from wrapper.context instead of using the
separate parameters.
    
"""

import json
import uuid
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, function_tool, RunContextWrapper


# ✅ Create a UserData Pydantic model with 'name' and 'passport_number' fields
class UserData(BaseModel):
    name: str
    passport_number: str


# ✅ Updated function signature and implementation
@function_tool
def book_hotel(wrapper: RunContextWrapper[UserData], hotel_name: str) -> dict:
    """
    Books a hotel using sensitive data from the context wrapper.

    Args:
        wrapper: RunContextWrapper that provides user data (name, passport_number)
        hotel_name: The hotel to book

    Returns:
        dict: Confirmation details including a unique booking ID
    """
    # ✅ Access sensitive data from wrapper.context
    user_data = wrapper.context

    # Process sensitive data (for debugging/demo purposes)
    print(f"DEBUG: Booking for {user_data.name}")
    print(f"DEBUG: Passport number is {user_data.passport_number}")

    # ✅ Return booking confirmation
    return {
        "hotel_name": hotel_name,
        "guest_name": user_data.name,
        "confirmation_success": True,
        "confirmation_id": str(uuid.uuid4())
    }


# ✅ Define the Travel Genie agent with the booking tool
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


# ✅ Display agent tools (for inspection)
print("How the agent sees the tool:")
for tool in travel_genie.tools:
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Params JSON schema: {json.dumps(tool.params_json_schema, indent=2)}")
