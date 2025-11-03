"""
Instead of printing the entire output object, your task is to
extract each field from the result and print it one by one with clear labels.
This will help you become comfortable accessing specific pieces of information from a Pydantic model.
This exercise will help you prepare for real-world scenarios in
which you need to use or display only certain parts of the agent’s response. 
"""

from agents import Agent, Runner
from pydantic import BaseModel, Field


# Define a Pydantic model for the desired output format
class TravelRecommendation(BaseModel):
    destination: str = Field(..., description="The recommended travel destination.")
    reason: str = Field(..., description="Why this destination is great for the user.")
    top_tip: str = Field(..., description="A top travel tip for this destination.")
    best_season: str = Field(..., description="The best season to visit this destination.")


# Define the agent with a specific output type
agent = Agent(
    name="Travel Genie",
    instructions=(
        "You are Travel Genie, a friendly and knowledgeable travel assistant. "
        "Recommend exciting destinations and offer helpful travel tips."
    ),
    model="gpt-4.1",
    output_type=TravelRecommendation
)

# Run the agent synchronously
result = Runner.run_sync(
    starting_agent=agent,
    input="Suggest a once-in-a-lifetime hiking destination.",
)

# TODO: Extract and print each field individually with clear labels:
output = result.final_output
print(f"🏔️ Destination: {output.destination}")
print(f"💬 Reason: {output.reason}")
print(f"💡 Top Tip: {output.top_tip}")
print(f"🌤️ Best Season: {output.best_season}")