"""
This file aliases travel_agents.py to avoid naming conflicts with the 'agents' package.
"""
from . import travel_agents as agents_module

# Re-export all functions
create_agent_system = agents_module.create_agent_system if hasattr(agents_module, 'create_agent_system') else None

# If create_agent_system doesn't exist in travel_agents.py, define it here
if create_agent_system is None:
    from .travel_agents import (
        create_travel_recommender_agent,
        create_research_agent,
        create_itinerary_agent,
        create_packing_list_agent,
        create_safety_expert_agent,
        create_booking_agent,
        create_travel_genie_agent,
        create_triage_agent,
        create_comprehensive_agent_with_tools
    )
    
    def create_agent_system(enable_hooks: bool = True) -> dict:
        """Factory function to create the complete agent system."""
        # Create specialized agents
        recommender = create_travel_recommender_agent()
        researcher = create_research_agent()
        itinerary_agent = create_itinerary_agent()
        packing_agent = create_packing_list_agent()
        safety_expert = create_safety_expert_agent()
        booking_agent = create_booking_agent()
        
        # Create multi-purpose agents
        travel_genie = create_travel_genie_agent(recommender, researcher, booking_agent)
        triage = create_triage_agent(travel_genie, safety_expert, itinerary_agent)
        
        # Create comprehensive agent with tools
        comprehensive_agent = create_comprehensive_agent_with_tools(researcher, safety_expert)
        
        return {
            "triage": triage,
            "travel_genie": travel_genie,
            "recommender": recommender,
            "researcher": researcher,
            "itinerary_agent": itinerary_agent,
            "packing_agent": packing_agent,
            "safety_expert": safety_expert,
            "booking_agent": booking_agent,
            "comprehensive_agent": comprehensive_agent
        }

