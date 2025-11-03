"""
Your task is to extend the TravelRecommendation
model by adding a new field called best_season
(as a string) with a helpful description. This will allow the
agent to include the best time of year to visit the recommended destination.
"""

from agents import Agent, Runner
from pydantic import BaseModel, Field


# TODO: Add a new field called best_season: str with an appropriate description
class TravelRecommendation(BaseModel):
    destination: str = Field(..., description="The recommended travel destination.")
    reason: str = Field(..., description="Why this destination is great for the user.")
    top_tip: str = Field(..., description="A top travel tip for this destination.")
    best_season: str = Field(..., description="Best Season to visit the Destination")


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

# Print the agent's final output
print(result.final_output)