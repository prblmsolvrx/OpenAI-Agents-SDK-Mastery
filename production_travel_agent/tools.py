"""
Custom function tools for the Travel Agent system.
This module demonstrates creating and registering custom function tools with structured inputs.
"""

import uuid
import json
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
from agents import function_tool, RunContextWrapper
from models import (
    TripInfo, 
    BudgetEstimateRequest, 
    HotelBookingRequest,
    UserContext,
    BookingConfirmation
)


# ============================================================================
# Budget and Cost Estimation Tools
# ============================================================================

@function_tool
def estimate_budget(trip: TripInfo) -> float:
    """
    Estimate the travel budget for a given trip.
    
    This tool calculates an estimated budget based on destination,
    duration, number of travelers, and accommodation preferences.
    
    Args:
        trip: A TripInfo object containing destination, days, travelers, and accommodation_level
        
    Returns:
        The estimated total budget in USD
    """
    destination = trip.destination.lower()
    days = trip.days
    travelers = trip.travelers
    acc_level = trip.accommodation_level.lower()
    
    # Base daily cost per person (varies by destination)
    destination_multipliers = {
        "switzerland": 250.0,
        "norway": 220.0,
        "japan": 180.0,
        "iceland": 200.0,
        "singapore": 160.0,
        "default": 120.0
    }
    
    base_cost = destination_multipliers.get(destination, destination_multipliers["default"])
    
    # Accommodation level multipliers
    acc_multipliers = {
        "budget": 0.7,
        "moderate": 1.0,
        "luxury": 2.5
    }
    
    multiplier = acc_multipliers.get(acc_level, 1.0)
    
    # Calculate total
    daily_cost = base_cost * multiplier
    total_cost = daily_cost * days * travelers
    
    # Add flight estimates (rough)
    flight_costs = {
        "switzerland": 1200,
        "norway": 1100,
        "japan": 1300,
        "iceland": 900,
        "singapore": 1400,
        "default": 800
    }
    flight_cost = flight_costs.get(destination, flight_costs["default"]) * travelers
    
    return round(total_cost + flight_cost, 2)


@function_tool
def get_detailed_budget_breakdown(request: BudgetEstimateRequest) -> Dict[str, Any]:
    """
    Get a detailed budget breakdown including accommodation, food, activities, and transport.
    
    Args:
        request: BudgetEstimateRequest with destination, days, travelers, accommodation_level, include_flights
        
    Returns:
        Dictionary with detailed budget breakdown
    """
    destination = request.destination.lower()
    days = request.days
    travelers = request.travelers
    acc_level = request.accommodation_level.lower()
    include_flights = request.include_flights
    
    # Cost components
    acc_costs = {"budget": 50, "moderate": 120, "luxury": 400}
    food_costs = {"budget": 30, "moderate": 60, "luxury": 150}
    activity_costs = {"budget": 40, "moderate": 80, "luxury": 200}
    transport_costs = {"budget": 20, "moderate": 40, "luxury": 100}
    
    acc_daily = acc_costs.get(acc_level, 120)
    food_daily = food_costs.get(acc_level, 60)
    activity_daily = activity_costs.get(acc_level, 80)
    transport_daily = transport_costs.get(acc_level, 40)
    
    # Destination multipliers
    dest_mult = 1.5 if destination in ["switzerland", "norway", "iceland"] else 1.0
    
    breakdown = {
        "accommodation": round(acc_daily * days * travelers * dest_mult, 2),
        "food": round(food_daily * days * travelers * dest_mult, 2),
        "activities": round(activity_daily * days * travelers * dest_mult, 2),
        "local_transport": round(transport_daily * days * travelers * dest_mult, 2),
        "flights": round(800 * travelers, 2) if include_flights else 0.0,
        "travel_insurance": round(50 * travelers, 2),
        "miscellaneous": round(100 * travelers, 2)
    }
    
    breakdown["total"] = sum(breakdown.values())
    
    return breakdown


# ============================================================================
# Booking Tools (with Secure Context)
# ============================================================================

@function_tool
def book_hotel(
    wrapper: RunContextWrapper[UserContext], 
    booking: HotelBookingRequest
) -> Dict[str, Any]:
    """
    Book a hotel room using sensitive user data from the secure context wrapper.
    
    This tool demonstrates secure context injection - sensitive user information
    is passed through RunContextWrapper to prevent LLM exposure.
    
    Args:
        wrapper: RunContextWrapper containing UserContext with sensitive user data
        booking: HotelBookingRequest with hotel details and dates
        
    Returns:
        Booking confirmation dictionary with booking ID and details
    """
    user_data = wrapper.context
    
    # Simulate hotel booking process
    booking_id = f"HTL-{uuid.uuid4().hex[:8].upper()}"
    
    # Calculate nights
    check_in = datetime.strptime(booking.check_in, "%Y-%m-%d")
    check_out = datetime.strptime(booking.check_out, "%Y-%m-%d")
    nights = (check_out - check_in).days
    
    # Pricing (mock)
    base_rate = 150.0
    rate_multiplier = {"standard": 1.0, "deluxe": 1.5, "suite": 2.5}
    rate = base_rate * rate_multiplier.get(booking.room_type, 1.0)
    total_cost = rate * nights * booking.guests
    
    confirmation = {
        "booking_id": booking_id,
        "hotel_name": booking.hotel_name,
        "guest_name": user_data.name,
        "guest_email": user_data.email,
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "guests": booking.guests,
        "room_type": booking.room_type,
        "nights": nights,
        "total_cost": round(total_cost, 2),
        "status": "confirmed",
        "confirmation_sent_to": user_data.email
    }
    
    # In production, this would actually book the hotel
    print(f"[BOOKING] Hotel booking created for {user_data.name} (ID: {user_data.user_id})")
    
    return confirmation


@function_tool
def check_hotel_availability(
    destination: str,
    check_in: str,
    check_out: str,
    guests: int = 1
) -> List[Dict[str, Any]]:
    """
    Check hotel availability for a given destination and dates.
    
    Args:
        destination: Travel destination
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
        guests: Number of guests
        
    Returns:
        List of available hotels with pricing
    """
    # Mock hotel data
    mock_hotels = [
        {
            "name": f"{destination.title()} Grand Hotel",
            "rating": 4.5,
            "price_per_night": 180.0,
            "available_rooms": 5,
            "amenities": ["WiFi", "Breakfast", "Pool", "Gym"]
        },
        {
            "name": f"{destination.title()} Central Inn",
            "rating": 4.0,
            "price_per_night": 120.0,
            "available_rooms": 8,
            "amenities": ["WiFi", "Breakfast"]
        },
        {
            "name": f"Luxury {destination.title()} Resort",
            "rating": 5.0,
            "price_per_night": 350.0,
            "available_rooms": 2,
            "amenities": ["WiFi", "Breakfast", "Pool", "Spa", "Concierge"]
        }
    ]
    
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days
    
    for hotel in mock_hotels:
        hotel["total_cost"] = round(hotel["price_per_night"] * nights * guests, 2)
        hotel["nights"] = nights
    
    return mock_hotels


# ============================================================================
# Destination Information Tools
# ============================================================================

@function_tool
def get_destination_weather(destination: str, month: str = None) -> Dict[str, Any]:
    """
    Get weather information for a destination.
    
    Args:
        destination: Travel destination
        month: Month name (optional, defaults to current month)
        
    Returns:
        Weather information dictionary
    """
    # Mock weather data
    weather_data = {
        "destination": destination,
        "month": month or datetime.now().strftime("%B"),
        "temperature_avg": "22°C",
        "temperature_range": "18°C - 26°C",
        "conditions": "Sunny with occasional clouds",
        "rainfall": "Low",
        "humidity": "65%",
        "recommendation": "Perfect weather for outdoor activities"
    }
    
    return weather_data


@function_tool
def get_local_currency_info(destination: str) -> Dict[str, Any]:
    """
    Get currency information for a destination.
    
    Args:
        destination: Travel destination
        
    Returns:
        Currency information dictionary
    """
    # Mock currency data
    currency_map = {
        "switzerland": {"currency": "CHF", "usd_rate": 1.10, "symbol": "Fr"},
        "norway": {"currency": "NOK", "usd_rate": 0.095, "symbol": "kr"},
        "japan": {"currency": "JPY", "usd_rate": 0.0067, "symbol": "¥"},
        "iceland": {"currency": "ISK", "usd_rate": 0.0072, "symbol": "kr"},
        "singapore": {"currency": "SGD", "usd_rate": 0.74, "symbol": "S$"}
    }
    
    dest_key = destination.lower()
    currency_info = currency_map.get(dest_key, {
        "currency": "USD",
        "usd_rate": 1.0,
        "symbol": "$",
        "note": "Currency information not available for this destination"
    })
    
    currency_info["destination"] = destination
    return currency_info


# ============================================================================
# Research and Planning Tools
# ============================================================================

@function_tool
def get_travel_restrictions(destination: str) -> Dict[str, Any]:
    """
    Get travel restrictions and visa requirements for a destination.
    
    Args:
        destination: Travel destination
        
    Returns:
        Travel restrictions and visa information
    """
    # Mock data
    restrictions = {
        "destination": destination,
        "visa_required": destination.lower() in ["japan", "singapore"],
        "visa_type": "Tourist Visa" if destination.lower() in ["japan", "singapore"] else "No visa required for US citizens",
        "passport_validity": "6 months",
        "vaccination_requirements": [],
        "entry_restrictions": "None currently",
        "additional_info": f"Check official {destination} embassy website for latest updates"
    }
    
    return restrictions


@function_tool
def suggest_activities(destination: str, interests: List[str] = None) -> List[Dict[str, Any]]:
    """
    Suggest activities based on destination and user interests.
    
    Args:
        destination: Travel destination
        interests: List of interests (e.g., ["hiking", "culture", "food"])
        
    Returns:
        List of suggested activities with details
    """
    interests = interests or ["general"]
    
    # Mock activity data
    all_activities = {
        "hiking": [
            {"name": "Mountain Trail Expedition", "duration": "Full day", "cost": "$80", "difficulty": "Moderate"},
            {"name": "Scenic Nature Walk", "duration": "Half day", "cost": "$40", "difficulty": "Easy"}
        ],
        "culture": [
            {"name": "Museum Tour", "duration": "3-4 hours", "cost": "$30", "difficulty": "Easy"},
            {"name": "Historical District Walking Tour", "duration": "2 hours", "cost": "$25", "difficulty": "Easy"}
        ],
        "food": [
            {"name": "Culinary Experience Tour", "duration": "4 hours", "cost": "$90", "difficulty": "Easy"},
            {"name": "Local Market Visit", "duration": "2 hours", "cost": "$20", "difficulty": "Easy"}
        ],
        "general": [
            {"name": "City Sightseeing Tour", "duration": "Full day", "cost": "$60", "difficulty": "Easy"},
            {"name": "Sunset Viewpoint Visit", "duration": "2 hours", "cost": "Free", "difficulty": "Easy"}
        ]
    }
    
    suggested = []
    for interest in interests:
        if interest.lower() in all_activities:
            suggested.extend(all_activities[interest.lower()])
    
    if not suggested:
        suggested = all_activities["general"]
    
    # Add destination context
    for activity in suggested:
        activity["destination"] = destination
    
    return suggested[:5]  # Limit to 5 suggestions


