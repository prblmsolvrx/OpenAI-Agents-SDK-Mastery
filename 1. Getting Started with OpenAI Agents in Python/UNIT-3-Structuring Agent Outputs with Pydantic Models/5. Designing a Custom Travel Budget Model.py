"""
Your task is to create a new Pydantic model called TravelBudget that will help the agent return a detailed budget plan for a trip. This model should include the following string fields, each with a helpful description:

total_cost: the estimated total cost for the trip
accommodation: details and cost of accommodation
food_estimate: estimated cost for food during the trip
must_include_activity: a must-do activity to include in the plan
Once you’ve defined your model:

Set up an agent called "Budget Travel Planner" that uses your TravelBudget model as its output_type.
Run the agent with the prompt: Plan a week in Bali on a mid-range budget.
Extract each field from the agent’s structured output and print them one by one with clear labels.
This exercise will help you become comfortable designing your own output
formats and using them to get exactly the information you need from your agent.
"""

from agents import Agent, Runner
from pydantic import BaseModel, Field

# TODO: Create a Pydantic model called TravelBudget with the following string fields:
# - total_cost: The estimated total cost for the trip.
# - accommodation: Details and cost of accommodation.
# - food_estimate: Estimated cost for food during the trip.
# - must_include_activity: A must-do activity to include in the plan.
class TravelBudget(BaseModel):
    total_cost: str = Field(..., description="The estimated total cost for the trip.")
    accommodation: str = Field(..., description="Details and cost of accommodation.") 
    food_estimate: str = Field(..., description="Estimated cost for food during the trip.") 
    must_include_activity: str = Field(..., description="A must-do activity to include in the plan.") 

# Define the agent
agent = Agent(
    name="Budget Travel Planner",
    instructions=(
        "You are a budget travel planner. Provide a clear breakdown of costs for a trip, "
        "including total cost, accommodation, food estimate, and a must-include activity."
    ),
    model="gpt-4.1",
    # TODO: Set output_type to your TravelBudget model
    output_type=TravelBudget
)

# Run the agent synchronously
result = Runner.run_sync(
    starting_agent=agent,
    input="Plan a week in Bali on a mid-range budget.",
)

# TODO: Extract and print each field from the result.final_output individually with clear labels
output = result.final_output
print("total_cost", output.total_cost)
print("accommodation", output.accommodation)
print("food_estimate", output.food_estimate)
print("must_include_activity", output.must_include_activity)