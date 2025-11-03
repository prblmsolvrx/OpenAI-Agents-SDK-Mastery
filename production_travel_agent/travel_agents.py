"""
Agent definitions for the comprehensive Travel Agent system.
This module demonstrates various agent patterns: standalone agents, chaining, handoffs, and agents as tools.
"""

from agents import Agent, WebSearchTool
from agents.lifecycle import AgentHooks, RunHooks

try:
    from .models import (
        TravelRecommendation,
        TravelItinerary,
        PackingList,
        SafetyAdvice,
        BookingConfirmation
    )
    from .tools import (
        estimate_budget,
        get_detailed_budget_breakdown,
        book_hotel,
        check_hotel_availability,
        get_destination_weather,
        get_local_currency_info,
        get_travel_restrictions,
        suggest_activities
    )
    from .hooks import (
        TravelGenieHooks,
        BookingAgentHooks,
        ResearchAgentHooks,
        ItineraryAgentHooks
    )
except ImportError:
    from models import (
        TravelRecommendation,
        TravelItinerary,
        PackingList,
        SafetyAdvice,
        BookingConfirmation
    )
    from tools import (
        estimate_budget,
        get_detailed_budget_breakdown,
        book_hotel,
        check_hotel_availability,
        get_destination_weather,
        get_local_currency_info,
        get_travel_restrictions,
        suggest_activities
    )
    from hooks import (
        TravelGenieHooks,
        BookingAgentHooks,
        ResearchAgentHooks,
        ItineraryAgentHooks
    )


# ============================================================================
# Core Specialized Agents
# ============================================================================

def create_travel_recommender_agent(hooks: AgentHooks = None) -> Agent:
    """
    Creates a travel recommendation agent with structured output.
    Demonstrates: Structured output with Pydantic, model selection, instructions tuning.
    """
    return Agent(
        name="Travel Recommender",
        instructions=(
            "You are Travel Recommender, an expert in recommending travel destinations. "
            "You provide detailed, personalized travel recommendations based on user preferences. "
            "Always consider factors like travel interests, budget, season, and accessibility. "
            "Be enthusiastic but realistic in your recommendations. "
            "When recommending destinations, provide specific reasons why each destination matches the user's interests."
        ),
        model="gpt-4o",  # Using high-quality model for recommendations
        output_type=TravelRecommendation,  # Structured output
        hooks=hooks
    )


def create_research_agent(hooks: AgentHooks = None) -> Agent:
    """
    Creates a research agent with web search capabilities.
    Demonstrates: OpenAI hosted tools (WebSearchTool), tool integration.
    """
    return Agent(
        name="Travel Researcher",
        instructions=(
            "You are Travel Researcher, an expert in gathering and synthesizing travel information. "
            "Use web search to find the latest information about destinations, weather, events, "
            "and travel conditions. Summarize your findings clearly and cite important details. "
            "Always verify current information and note any time-sensitive data."
        ),
        tools=[WebSearchTool()],
        model="gpt-4o",
        hooks=hooks or ResearchAgentHooks()
    )


def create_itinerary_agent(hooks: AgentHooks = None) -> Agent:
    """
    Creates an itinerary generation agent with structured output.
    Demonstrates: Structured outputs, tool usage for budget calculations.
    """
    return Agent(
        name="Itinerary Generator",
        instructions=(
            "You are Itinerary Generator, an expert in creating detailed travel itineraries. "
            "Given a destination and trip requirements, create a comprehensive day-by-day itinerary. "
            "Include activities, accommodations, meal suggestions, and transportation. "
            "Use the budget estimation tools to provide accurate cost estimates. "
            "Consider practical factors like travel time, opening hours, and logical activity sequencing."
        ),
        tools=[estimate_budget, get_detailed_budget_breakdown, suggest_activities],
        model="gpt-4o",
        output_type=TravelItinerary,  # Structured output
        hooks=hooks or ItineraryAgentHooks()
    )


def create_packing_list_agent(hooks: AgentHooks = None) -> Agent:
    """
    Creates a packing list generation agent.
    Demonstrates: Structured output, context from previous agents.
    """
    return Agent(
        name="Packing List Generator",
        instructions=(
            "You are Packing List Generator, an expert in creating comprehensive packing lists. "
            "Based on destination, duration, season, and planned activities, create a detailed packing list. "
            "Consider climate, cultural considerations, and activity-specific needs. "
            "Categorize items logically (clothing, toiletries, electronics, documents, etc.)."
        ),
        model="gpt-4o",
        output_type=PackingList,  # Structured output
        hooks=hooks
    )


def create_safety_expert_agent(hooks: AgentHooks = None) -> Agent:
    """
    Creates a travel safety expert agent.
    Demonstrates: Specialized agent for specific domain expertise.
    """
    return Agent(
        name="Travel Safety Expert",
        instructions=(
            "You are Travel Safety Expert, a specialist in travel safety and health. "
            "Provide comprehensive safety advice, health precautions, and risk assessments for destinations. "
            "Include information about travel advisories, health requirements, local laws, "
            "and emergency procedures. Always prioritize traveler safety and well-being."
        ),
        tools=[get_travel_restrictions, WebSearchTool()],
        model="gpt-4o",
        output_type=SafetyAdvice,  # Structured output
        hooks=hooks
    )


def create_booking_agent(hooks: AgentHooks = None) -> Agent:
    """
    Creates a booking agent with secure context access.
    Demonstrates: Secure context injection, booking tools with RunContextWrapper.
    """
    return Agent(
        name="Booking Specialist",
        instructions=(
            "You are Booking Specialist, an expert in handling travel bookings. "
            "You can book hotels, check availability, and provide booking confirmations. "
            "Always verify booking details before confirming. "
            "Use secure user information from context when making bookings. "
            "Provide clear booking confirmations with all relevant details."
        ),
        tools=[book_hotel, check_hotel_availability],
        model="gpt-4o",
        output_type=BookingConfirmation,  # Structured output
        hooks=hooks or BookingAgentHooks()
    )


# ============================================================================
# Multi-Purpose Agents (with Handoffs)
# ============================================================================

def create_travel_genie_agent(
    recommender: Agent,
    researcher: Agent,
    booking_agent: Agent,
    hooks: AgentHooks = None
) -> Agent:
    """
    Creates the main Travel Genie agent with handoff capabilities.
    Demonstrates: Handoffs, delegation, agent coordination.
    """
    return Agent(
        name="Travel Genie",
        instructions=(
            "You are Travel Genie, a comprehensive travel assistant and the primary point of contact for travelers. "
            "You coordinate with specialized agents to provide complete travel assistance.\n\n"
            "Your responsibilities:\n"
            "- For destination recommendations: Delegate to Travel Recommender\n"
            "- For research and current information: Delegate to Travel Researcher\n"
            "- For bookings and reservations: Delegate to Booking Specialist\n"
            "- For general travel questions: Answer directly using your knowledge\n\n"
            "Always provide friendly, helpful service and ensure users get complete answers to their questions."
        ),
        tools=[estimate_budget, get_destination_weather, get_local_currency_info],
        handoffs=[recommender, researcher, booking_agent],
        model="gpt-4o",
        hooks=hooks or TravelGenieHooks()
    )


def create_triage_agent(
    travel_genie: Agent,
    safety_expert: Agent,
    itinerary_agent: Agent
) -> Agent:
    """
    Creates a triage agent that routes requests to appropriate specialists.
    Demonstrates: Triage pattern, smart routing, handoff coordination.
    """
    return Agent(
        name="Travel Triage",
        instructions=(
            "You are Travel Triage, the intelligent routing system for travel requests.\n\n"
            "Route requests as follows:\n"
            "- General travel planning, recommendations, research, bookings → Travel Genie\n"
            "- Safety concerns, health questions, travel advisories → Travel Safety Expert\n"
            "- Itinerary creation and detailed trip planning → Itinerary Generator\n\n"
            "Analyze the user's request and route to the most appropriate specialist. "
            "If a request involves multiple aspects, route to the primary concern first."
        ),
        handoffs=[travel_genie, safety_expert, itinerary_agent],
        model="gpt-4o"
    )


# ============================================================================
# Agents as Tools
# ============================================================================

def create_comprehensive_agent_with_tools(
    researcher: Agent,
    safety_expert: Agent,
    hooks: AgentHooks = None
) -> Agent:
    """
    Creates a comprehensive agent that uses other agents as tools.
    Demonstrates: Agents as callable tools, agent tool integration.
    """
    # Convert agents to tools
    researcher_tool = researcher.as_tool(
        tool_name="research_travel_info",
        tool_description="Research current travel information, weather, events, and destination details from the web"
    )
    
    safety_tool = safety_expert.as_tool(
        tool_name="get_safety_advice",
        tool_description="Get comprehensive safety advice, health precautions, and travel advisories for destinations"
    )
    
    return Agent(
        name="Comprehensive Travel Assistant",
        instructions=(
            "You are a Comprehensive Travel Assistant that coordinates all aspects of travel planning. "
            "You have access to research and safety tools (which are actually specialized agents). "
            "Use these tools when users need current information or safety advice. "
            "For other tasks, use your own knowledge and the available function tools. "
            "Provide complete, well-researched travel guidance."
        ),
        tools=[
            estimate_budget,
            get_detailed_budget_breakdown,
            suggest_activities,
            get_destination_weather,
            get_local_currency_info,
            researcher_tool,  # Agent as tool
            safety_tool       # Agent as tool
        ],
        model="gpt-4o",
        hooks=hooks
    )


# ============================================================================
# Agent Factory Functions
# ============================================================================

def create_agent_system(enable_hooks: bool = True) -> dict:
    """
    Factory function to create the complete agent system.
    Returns all agents configured and ready to use.
    """
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

