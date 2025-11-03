"""
Example usage scripts demonstrating various features of the Travel Agent System.
These examples can be run independently to understand specific features.
"""

import asyncio
from agents import Runner

# Import agents (adjust import path as needed)
try:
    from travel_agents import create_agent_system
    from models import UserContext
except ImportError:
    import sys
    sys.path.insert(0, '.')
    from travel_agents import create_agent_system
    from models import UserContext


# ============================================================================
# Example 1: Basic Agent Usage with Structured Output
# ============================================================================

async def example_structured_output():
    """Example: Using agents with structured Pydantic outputs."""
    print("\n=== Example 1: Structured Output ===")
    
    agents = create_agent_system()
    recommender = agents["recommender"]
    
    result = await Runner.run(
        starting_agent=recommender,
        input="Recommend a destination for someone who loves mountain hiking and photography."
    )
    
    # Access structured output
    if hasattr(result.final_output, 'destination'):
        rec = result.final_output
        print(f"\nDestination: {rec.destination}")
        print(f"Country: {rec.country}")
        print(f"Reason: {rec.reason}")
        print(f"Best Season: {rec.best_season}")
        print(f"Top Tip: {rec.top_tip}")
    else:
        print(f"\nRecommendation: {result.final_output}")


# ============================================================================
# Example 2: Agent Chaining
# ============================================================================

async def example_agent_chaining():
    """Example: Chaining multiple agents in sequence."""
    print("\n=== Example 2: Agent Chaining ===")
    
    agents = create_agent_system()
    
    # Step 1: Get recommendation
    print("\nStep 1: Getting destination recommendation...")
    recommender = agents["recommender"]
    rec_result = await Runner.run(
        starting_agent=recommender,
        input="Suggest a destination for a romantic getaway."
    )
    
    # Step 2: Create itinerary based on recommendation
    print("\nStep 2: Creating itinerary...")
    itinerary_input = rec_result.to_input_list() + [
        {"role": "user", "content": "Create a 3-day itinerary for this destination."}
    ]
    
    itinerary_agent = agents["itinerary_agent"]
    itin_result = await Runner.run(
        starting_agent=itinerary_agent,
        input=itinerary_input
    )
    
    print(f"\nItinerary created successfully!")
    print(f"Output preview: {str(itin_result.final_output)[:200]}...")


# ============================================================================
# Example 3: Using Tools
# ============================================================================

async def example_tool_usage():
    """Example: Agents using custom function tools."""
    print("\n=== Example 3: Tool Usage ===")
    
    agents = create_agent_system()
    travel_genie = agents["travel_genie"]
    
    result = await Runner.run(
        starting_agent=travel_genie,
        input="What's the weather like in Switzerland right now, and estimate the budget for a 7-day trip?"
    )
    
    print(f"\nAgent Response: {result.final_output[:300]}...")


# ============================================================================
# Example 4: Handoffs
# ============================================================================

async def example_handoffs():
    """Example: Agent handoffs and delegation."""
    print("\n=== Example 4: Agent Handoffs ===")
    
    agents = create_agent_system()
    triage = agents["triage"]
    
    requests = [
        "What are the safety considerations for traveling to Peru?",
        "Research the best time to visit Japan.",
        "Book me a hotel in Paris for next week."
    ]
    
    for request in requests:
        print(f"\nRequest: {request}")
        result = await Runner.run(
            starting_agent=triage,
            input=request
        )
        print(f"Handled by: {result.last_agent.name}")
        print(f"Response preview: {result.final_output[:150]}...")


# ============================================================================
# Example 5: Secure Context
# ============================================================================

async def example_secure_context():
    """Example: Secure context injection for sensitive data."""
    print("\n=== Example 5: Secure Context Injection ===")
    
    agents = create_agent_system()
    booking_agent = agents["booking_agent"]
    
    # Create user context with sensitive information
    user_context = UserContext(
        user_id="user_example_123",
        name="John Doe",
        email="john.doe@example.com",
        passport_number="P987654321",
        preferences={"accommodation": "luxury", "room_type": "suite"}
    )
    
    print("\nMaking booking with secure context...")
    result = await Runner.run(
        starting_agent=booking_agent,
        input="Book a hotel room at the Grand Plaza from 2024-06-15 to 2024-06-18 for 2 guests, deluxe room",
        context=user_context
    )
    
    print(f"\nBooking Result: {result.final_output[:300]}...")


# ============================================================================
# Example 6: Multi-turn Conversation
# ============================================================================

async def example_conversation():
    """Example: Multi-turn conversation with history."""
    print("\n=== Example 6: Multi-turn Conversation ===")
    
    agents = create_agent_system()
    agent = agents["travel_genie"]
    
    # First turn
    print("\nTurn 1: Initial request")
    result1 = await Runner.run(
        starting_agent=agent,
        input="I'm planning a trip to Iceland."
    )
    print(f"Agent: {result1.final_output[:200]}...")
    
    # Second turn - with conversation history
    print("\nTurn 2: Follow-up question")
    conversation_input = result1.to_input_list() + [
        {"role": "user", "content": "What's the best time of year to visit?"}
    ]
    
    result2 = await Runner.run(
        starting_agent=agent,
        input=conversation_input
    )
    print(f"Agent: {result2.final_output[:200]}...")


# ============================================================================
# Example 7: Result Inspection
# ============================================================================

async def example_result_inspection():
    """Example: Inspecting agent result properties."""
    print("\n=== Example 7: Result Inspection ===")
    
    agents = create_agent_system()
    researcher = agents["researcher"]
    
    result = await Runner.run(
        starting_agent=researcher,
        input="Research current travel advisories for Japan."
    )
    
    print(f"\nResult Properties:")
    print(f"- Final Output Length: {len(result.final_output)} characters")
    print(f"- Last Agent: {result.last_agent.name}")
    print(f"- Number of Steps: {len(result.steps)}")
    
    # Show steps
    print(f"\nAgent Steps:")
    for i, step in enumerate(result.steps[:5], 1):  # Show first 5 steps
        print(f"  {i}. {step.type}")
    
    # Show conversation history structure
    history = result.to_input_list()
    print(f"\nConversation History Messages: {len(history)}")
    for i, msg in enumerate(history[:3], 1):  # Show first 3 messages
        print(f"  {i}. {msg['role']}: {msg['content'][:50]}...")


# ============================================================================
# Example 8: Streaming
# ============================================================================

async def example_streaming():
    """Example: Streaming agent responses in real-time."""
    print("\n=== Example 8: Streaming Responses ===")
    
    agents = create_agent_system()
    recommender = agents["recommender"]
    
    print("\nStreaming response events:")
    result = Runner.run_streamed(
        starting_agent=recommender,
        input="Recommend a destination for adventure travel."
    )
    
    event_count = 0
    async for event in result.stream_events():
        event_count += 1
        print(f"  Event {event_count}: {type(event).__name__}")
        if event_count >= 5:  # Limit output
            print("  ... (more events)")
            break
    
    print(f"\nTotal events received: {event_count}+")


# ============================================================================
# Main Runner
# ============================================================================

async def run_all_examples():
    """Run all example functions."""
    examples = [
        example_structured_output,
        example_agent_chaining,
        example_tool_usage,
        example_handoffs,
        example_secure_context,
        example_conversation,
        example_result_inspection,
        example_streaming,
    ]
    
    for example_func in examples:
        try:
            await example_func()
            print("\n" + "-"*70)
        except Exception as e:
            print(f"\nExample '{example_func.__name__}' failed: {str(e)}")
            import traceback
            traceback.print_exc()
            print("-"*70)


if __name__ == "__main__":
    print("="*70)
    print("TRAVEL AGENT SYSTEM - USAGE EXAMPLES")
    print("="*70)
    
    # Run all examples
    asyncio.run(run_all_examples())
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)

