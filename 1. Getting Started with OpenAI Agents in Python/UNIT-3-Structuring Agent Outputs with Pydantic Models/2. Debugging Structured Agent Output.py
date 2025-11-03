"""
Let’s see what happens when the model’s type annotations do not match the agent’s output.
"""

from agents import Agent, Runner
from pydantic import BaseModel, Field


# Define a Pydantic model for the desired output format
class TravelRecommendation(BaseModel):
    destination: str = Field(..., description="The recommended travel destination.")
    reason: str = Field(..., description="Why this destination is great for the user.")
    top_tip: str = Field(..., description="A top travel tip for this destination.")


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