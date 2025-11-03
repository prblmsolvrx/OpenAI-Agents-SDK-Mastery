"""
Pydantic models for structured inputs and outputs in the Travel Agent system.
This module demonstrates structured agent outputs and typed function tool inputs.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# Structured Output Models (Agent Output Types)
# ============================================================================

class TravelRecommendation(BaseModel):
    """Structured output for travel destination recommendations."""
    destination: str = Field(..., description="The recommended travel destination")
    country: str = Field(..., description="The country where the destination is located")
    reason: str = Field(..., description="Why this destination is great for the user")
    best_season: str = Field(..., description="Best time of year to visit")
    top_tip: str = Field(..., description="A top travel tip for this destination")
    estimated_cost_range: str = Field(..., description="Estimated cost range (e.g., 'Budget', 'Moderate', 'Luxury')")


class ItineraryDay(BaseModel):
    """Model for a single day in an itinerary."""
    day_number: int = Field(..., description="Day number in the itinerary")
    date: Optional[str] = Field(None, description="Specific date if provided")
    activities: List[str] = Field(..., description="List of activities for this day")
    accommodations: Optional[str] = Field(None, description="Where to stay this night")
    meals: List[str] = Field(default_factory=list, description="Meal recommendations")


class TravelItinerary(BaseModel):
    """Structured output for complete travel itineraries."""
    destination: str = Field(..., description="Travel destination")
    duration_days: int = Field(..., description="Number of days for the trip")
    itinerary: List[ItineraryDay] = Field(..., description="Day-by-day itinerary breakdown")
    total_estimated_budget: float = Field(..., description="Total estimated budget in USD")
    packing_suggestions: List[str] = Field(default_factory=list, description="Essential items to pack")


class PackingList(BaseModel):
    """Structured output for travel packing lists."""
    destination: str = Field(..., description="Travel destination")
    duration_days: int = Field(..., description="Trip duration")
    season: str = Field(..., description="Travel season/climate")
    essential_items: List[str] = Field(..., description="Essential items to pack")
    optional_items: List[str] = Field(default_factory=list, description="Optional but recommended items")
    climate_specific_items: List[str] = Field(default_factory=list, description="Items specific to climate/activities")
    weight_estimate: str = Field(..., description="Estimated luggage weight")


class SafetyAdvice(BaseModel):
    """Structured output for travel safety advice."""
    destination: str = Field(..., description="Travel destination")
    safety_level: str = Field(..., description="Overall safety level (e.g., 'Safe', 'Caution Required', 'High Risk')")
    health_precautions: List[str] = Field(..., description="Health-related precautions")
    security_precautions: List[str] = Field(..., description="Security-related precautions")
    emergency_contacts: List[str] = Field(default_factory=list, description="Important emergency contact numbers")
    travel_advisories: List[str] = Field(default_factory=list, description="Relevant travel advisories")


class BookingConfirmation(BaseModel):
    """Structured output for booking confirmations."""
    booking_type: str = Field(..., description="Type of booking (hotel, flight, activity, etc.)")
    confirmation_id: str = Field(..., description="Unique confirmation/reference number")
    details: Dict[str, Any] = Field(..., description="Booking details")
    status: str = Field(..., description="Booking status (confirmed, pending, etc.)")
    total_cost: Optional[float] = Field(None, description="Total cost in USD")
    cancellation_policy: Optional[str] = Field(None, description="Cancellation policy information")


# ============================================================================
# Structured Input Models (Function Tool Inputs)
# ============================================================================

class TripInfo(BaseModel):
    """Structured input for trip information."""
    destination: str = Field(..., description="Travel destination")
    days: int = Field(..., description="Number of days for the trip", gt=0)
    travelers: int = Field(default=1, description="Number of travelers", gt=0)
    accommodation_level: str = Field(default="moderate", description="Accommodation level: budget, moderate, luxury")


class BudgetEstimateRequest(BaseModel):
    """Structured input for budget estimation."""
    destination: str = Field(..., description="Travel destination")
    days: int = Field(..., description="Number of days", gt=0)
    travelers: int = Field(default=1, description="Number of travelers", gt=0)
    accommodation_level: str = Field(default="moderate", description="budget, moderate, luxury")
    include_flights: bool = Field(default=True, description="Whether to include flight costs")


class HotelBookingRequest(BaseModel):
    """Structured input for hotel booking requests."""
    hotel_name: str = Field(..., description="Name of the hotel")
    check_in: str = Field(..., description="Check-in date (YYYY-MM-DD)")
    check_out: str = Field(..., description="Check-out date (YYYY-MM-DD)")
    guests: int = Field(default=1, description="Number of guests", gt=0)
    room_type: str = Field(default="standard", description="Room type preference")


class UserContext(BaseModel):
    """Model for user context data (sensitive information)."""
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    passport_number: Optional[str] = Field(None, description="Passport number (sensitive)")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")


# ============================================================================
# Response Metadata Models
# ============================================================================

class AgentMetrics(BaseModel):
    """Model for tracking agent execution metrics."""
    agent_name: str
    execution_time: float
    token_usage: Dict[str, int]
    steps_count: int
    tools_used: List[str]


class ConversationSummary(BaseModel):
    """Model for conversation summary."""
    message_count: int
    user_messages: int
    agent_messages: int
    topics_discussed: List[str]
    tools_invoked: List[str]


