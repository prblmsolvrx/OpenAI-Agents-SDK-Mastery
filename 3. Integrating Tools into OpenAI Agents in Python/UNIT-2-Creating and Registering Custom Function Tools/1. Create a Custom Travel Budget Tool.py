"""
Building on your understanding of how custom function tools work,
it's time to create your very own travel budget estimator!

In this exercise, write a Python function to calculate a budget and
return a float representing the estimated budget, given two parameters with type annotations:

destination (a str)
days (an int)
This function should:

Include a docstring that explains what this tool does, documents the parameters and the return value.
If the destination is "Norway" or "Switzerland" (case-insensitive), use a multiplier of 2.0; otherwise, use 1.0.
Calculate and return the total budget using the formula with a base cost of $150.0 per day:
budget = 150.0 × days × multiplier budget=150.0×days×multiplier
This is your chance to put your new skills into practice and see how easy it
is to extend an agent’s abilities with your own logic!    
"""

# TODO: Define the function with appropriate type annotations
    # TODO: Write a docstring explaining the tool, its parameters, and return value
    # TODO: Implement the budget calculation logic with the correct multiplier.
    # TODO: Return the calculated budget as a float.

from agents import function_tool

@function_tool
def estimate_budget(destination: str, days: int) -> float:
        """
        Estimate the travel budget for a given destination and number of days.

        Args:
            destination: The travel destination.
            days: Number of days for the trip.

        Returns:
            The estimated budget in USD.
        """
        base_cost = 150.0
        multiplier = 2.0 if destination.lower() in ["switzerland", "norway"] else 1.0
        return base_cost * days * multiplier