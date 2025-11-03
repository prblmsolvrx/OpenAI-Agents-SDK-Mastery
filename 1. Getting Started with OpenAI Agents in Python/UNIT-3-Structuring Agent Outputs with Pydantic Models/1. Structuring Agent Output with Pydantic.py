"""
Your task is to update the agent definition so that it returns its
output as a TravelRecommendation object, not just free-form text.
The model is already defined for you. All you need to do is to
specify the TravelRecommendation class as the output_type when you create the agent.

This small change will help you see how easy it is to shape your
agent’s responses for use in your own programs.    
"""

from agents import Agent, Runner
from pydantic import BaseModel, Field


# Define a Pydantic model for the desired output format
class TravelRecommendation(BaseModel):
    destination: str = Field(..., description="The recommended travel destination.")
    reason: str = Field(..., description="Why this destination is great for the user.")
    top_tip: str = Field(..., description="A top travel tip for this destination.")


# TODO: Set the output type to TravelRecommendation
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