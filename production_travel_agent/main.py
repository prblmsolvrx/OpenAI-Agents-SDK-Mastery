"""
Production-Ready Comprehensive Travel Agent System
===================================================

This is a comprehensive, production-ready AI agent system that demonstrates all aspects
of OpenAI Agents SDK Mastery covering materials 1-4.

Features demonstrated:
- Structured outputs with Pydantic
- Custom function tools with typed inputs
- Agent chaining and handoffs
- Agents as tools
- Secure context injection
- RunHooks and AgentHooks
- Input and output guardrails
- Multi-turn conversations
- Async execution and streaming
- Result inspection and metrics
- OpenAI hosted tools (WebSearchTool)
"""

import asyncio
import json
import sys
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will rely on environment variables

from agents import Agent, Runner, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

try:
    from .models import UserContext
    from .travel_agents import create_agent_system
    from .hooks import GlobalMonitoringHooks, MetricsCollectionHooks
except ImportError:
    from models import UserContext
    from travel_agents import create_agent_system
    from hooks import GlobalMonitoringHooks, MetricsCollectionHooks
# Note: Guardrails are applied via decorators on agents when configured


# ============================================================================
# Configuration
# ============================================================================

class Config:
    """Application configuration."""
    ENABLE_HOOKS = True
    ENABLE_GUARDRAILS = True
    ENABLE_METRICS = True
    VERBOSE_OUTPUT = True


# ============================================================================
# Main Application Class
# ============================================================================

class TravelAgentSystem:
    """
    Main application class that orchestrates the comprehensive travel agent system.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.agents = create_agent_system(enable_hooks=self.config.ENABLE_HOOKS)
        self.conversation_history = []
        self.metrics_hooks = MetricsCollectionHooks() if self.config.ENABLE_METRICS else None
    
    def get_hooks(self) -> Optional[GlobalMonitoringHooks]:
        """Get global hooks for workflow monitoring."""
        if self.config.ENABLE_HOOKS:
            return GlobalMonitoringHooks(enable_verbose=self.config.VERBOSE_OUTPUT)
        return None
    
    async def run_interactive(self):
        """Run interactive conversation mode."""
        print("\n" + "="*70)
        print("COMPREHENSIVE TRAVEL AGENT SYSTEM")
        print("="*70)
        print("\nWelcome! I'm your comprehensive travel assistant.")
        print("I can help with recommendations, research, bookings, safety advice, and more.")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nThank you for using the Travel Agent System. Safe travels!")
                    break
                
                if not user_input:
                    continue
                
                # Run with triage agent (routes to appropriate specialist)
                result = await self.process_request(
                    user_input,
                    starting_agent=self.agents["triage"],
                    context=None
                )
                
                print(f"\nAssistant: {result.final_output}")
                
                # Store conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": result.final_output
                })
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                if self.config.VERBOSE_OUTPUT:
                    import traceback
                    traceback.print_exc()
    
    async def process_request(
        self,
        user_input: str,
        starting_agent: Agent,
        context: Optional[UserContext] = None,
        use_history: bool = True
    ):
        """
        Process a single request through the agent system.
        
        Demonstrates:
        - Request processing with hooks
        - Guardrails
        - Context injection
        - Conversation history
        """
        hooks_list = []
        
        # Add global monitoring hooks
        global_hooks = self.get_hooks()
        if global_hooks:
            hooks_list.append(global_hooks)
        
        # Add metrics hooks
        if self.metrics_hooks:
            hooks_list.append(self.metrics_hooks)
        
        # Note: Guardrails are applied via decorators on agents when ENABLE_GUARDRAILS is True
        # The guardrails will be automatically checked during agent execution
        
        # Build input with conversation history if enabled
        input_data = user_input
        if use_history and self.conversation_history:
            # Convert conversation history to input list format
            input_list = self.conversation_history.copy()
            input_list.append({"role": "user", "content": user_input})
            input_data = input_list
        
        # Run the agent
        result = await Runner.run(
            starting_agent=starting_agent,
            input=input_data,
            context=context,
            hooks=hooks_list[0] if len(hooks_list) == 1 else None
        )
        
        # Output guardrails are applied via decorators on agents
        # They will automatically be checked during agent execution
        
        return result
    
    async def demo_structured_output(self):
        """Demonstrate structured output with Pydantic models."""
        print("\n" + "="*70)
        print("DEMO: Structured Output with Pydantic")
        print("="*70)
        
        recommender = self.agents["recommender"]
        
        result = await Runner.run(
            starting_agent=recommender,
            input="Recommend a destination for a food lover interested in street food and local cuisine."
        )
        
        print("\nStructured Output:")
        print(json.dumps(result.final_output.dict() if hasattr(result.final_output, 'dict') else result.final_output, indent=2))
    
    async def demo_agent_chaining(self):
        """Demonstrate agent chaining for sequential workflows."""
        print("\n" + "="*70)
        print("DEMO: Agent Chaining")
        print("="*70)
        
        # Step 1: Get recommendation
        print("\nStep 1: Getting destination recommendation...")
        recommender = self.agents["recommender"]
        rec_result = await Runner.run(
            starting_agent=recommender,
            input="Suggest a destination for a romantic honeymoon."
        )
        print(f"Recommendation: {rec_result.final_output.destination if hasattr(rec_result.final_output, 'destination') else rec_result.final_output}")
        
        # Step 2: Create itinerary
        print("\nStep 2: Creating itinerary...")
        itinerary_input = rec_result.to_input_list() + [
            {"role": "user", "content": "Create a 5-day itinerary for this destination."}
        ]
        itinerary_agent = self.agents["itinerary_agent"]
        itin_result = await Runner.run(
            starting_agent=itinerary_agent,
            input=itinerary_input
        )
        print(f"Itinerary created: {itin_result.final_output.destination if hasattr(itin_result.final_output, 'destination') else 'Success'}")
        
        # Step 3: Generate packing list
        print("\nStep 3: Generating packing list...")
        packing_input = itin_result.to_input_list() + [
            {"role": "user", "content": "Create a detailed packing list for this trip."}
        ]
        packing_agent = self.agents["packing_agent"]
        packing_result = await Runner.run(
            starting_agent=packing_agent,
            input=packing_input
        )
        print(f"Packing list generated: {packing_result.final_output.destination if hasattr(packing_result.final_output, 'destination') else 'Success'}")
    
    async def demo_handoffs(self):
        """Demonstrate agent handoffs and delegation."""
        print("\n" + "="*70)
        print("DEMO: Agent Handoffs")
        print("="*70)
        
        requests = [
            ("I need safety advice for traveling to Peru", self.agents["triage"]),
            ("Book me a hotel in Paris", self.agents["travel_genie"]),
            ("Research current weather in Tokyo", self.agents["travel_genie"])
        ]
        
        for request, agent in requests:
            print(f"\nRequest: {request}")
            result = await self.process_request(request, starting_agent=agent)
            print(f"Handled by: {result.last_agent.name}")
            print(f"Response: {result.final_output[:200]}...")
    
    async def demo_secure_context(self):
        """Demonstrate secure context injection."""
        print("\n" + "="*70)
        print("DEMO: Secure Context Injection")
        print("="*70)
        
        # Create user context with sensitive data
        user_context = UserContext(
            user_id="user_12345",
            name="Alice Smith",
            email="alice@example.com",
            passport_number="P123456789",
            preferences={"preferred_accommodation": "luxury", "dietary_restrictions": ["vegetarian"]}
        )
        
        booking_agent = self.agents["booking_agent"]
        
        print("\nMaking a booking with secure context...")
        result = await Runner.run(
            starting_agent=booking_agent,
            input="Book me a room at the Grand Plaza Hotel from 2024-06-01 to 2024-06-05 for 2 guests, deluxe room",
            context=user_context
        )
        
        print(f"\nBooking Result: {result.final_output}")
    
    async def demo_streaming(self):
        """Demonstrate streaming agent responses."""
        print("\n" + "="*70)
        print("DEMO: Streaming Agent Responses")
        print("="*70)
        
        agent = self.agents["recommender"]
        
        print("\nStreaming response:")
        result = Runner.run_streamed(
            starting_agent=agent,
            input="Recommend a destination for adventure seekers."
        )
        
        async for event in result.stream_events():
            print(f"Event: {event}")
    
    async def demo_result_inspection(self):
        """Demonstrate inspecting agent result properties."""
        print("\n" + "="*70)
        print("DEMO: Result Inspection")
        print("="*70)
        
        agent = self.agents["researcher"]
        result = await Runner.run(
            starting_agent=agent,
            input="Research the best time to visit Iceland."
        )
        
        print("\nResult Properties:")
        print(f"- Final Output Length: {len(result.final_output)} characters")
        print(f"- Last Agent: {result.last_agent.name}")
        print(f"- Steps Count: {len(result.steps)}")
        
        # Show steps
        print(f"\nAgent Steps ({len(result.steps)}):")
        for i, step in enumerate(result.steps, 1):
            print(f"  Step {i}: {step.type}")
        
        # Show usage metrics
        if hasattr(result, 'usage') and result.usage:
            print(f"\nToken Usage:")
            print(f"  Prompt Tokens: {result.usage.prompt_tokens}")
            print(f"  Completion Tokens: {result.usage.completion_tokens}")
            print(f"  Total Tokens: {result.usage.total_tokens}")
        
        # Show conversation history
        print(f"\nConversation History:")
        history = result.to_input_list()
        print(json.dumps(history, indent=2))
    
    async def demo_agents_as_tools(self):
        """Demonstrate using agents as callable tools."""
        print("\n" + "="*70)
        print("DEMO: Agents as Tools")
        print("="*70)
        
        comprehensive_agent = self.agents["comprehensive_agent"]
        
        result = await Runner.run(
            starting_agent=comprehensive_agent,
            input="I want to plan a trip to Japan. Research current travel conditions and get safety advice."
        )
        
        print(f"\nResponse from comprehensive agent using other agents as tools:")
        print(result.final_output)
    
    async def run_all_demos(self):
        """Run all demonstration scenarios."""
        demos = [
            ("Structured Output", self.demo_structured_output),
            ("Agent Chaining", self.demo_agent_chaining),
            ("Handoffs", self.demo_handoffs),
            ("Secure Context", self.demo_secure_context),
            ("Result Inspection", self.demo_result_inspection),
            ("Agents as Tools", self.demo_agents_as_tools),
        ]
        
        for name, demo_func in demos:
            try:
                await demo_func()
                print("\n" + "-"*70)
            except Exception as e:
                print(f"\nDemo '{name}' failed: {str(e)}")
                if self.config.VERBOSE_OUTPUT:
                    import traceback
                    traceback.print_exc()
        
        # Show metrics if enabled
        if self.metrics_hooks:
            print("\n" + "="*70)
            print("COLLECTED METRICS")
            print("="*70)
            metrics = self.metrics_hooks.get_metrics()
            print(json.dumps(metrics, indent=2, default=str))


# ============================================================================
# CLI Interface
# ============================================================================

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Travel Agent System")
    parser.add_argument(
        "--mode",
        choices=["interactive", "demo", "all-demos"],
        default="interactive",
        help="Run mode: interactive, demo, or all-demos"
    )
    parser.add_argument(
        "--no-hooks",
        action="store_true",
        help="Disable hooks"
    )
    parser.add_argument(
        "--no-guardrails",
        action="store_true",
        help="Disable guardrails"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Quiet mode (less verbose output)"
    )
    
    args = parser.parse_args()
    
    # Configure
    config = Config()
    config.ENABLE_HOOKS = not args.no_hooks
    config.ENABLE_GUARDRAILS = not args.no_guardrails
    config.VERBOSE_OUTPUT = not args.quiet
    
    # Create system
    system = TravelAgentSystem(config)
    
    # Run based on mode
    if args.mode == "interactive":
        await system.run_interactive()
    elif args.mode == "demo":
        await system.demo_structured_output()
    elif args.mode == "all-demos":
        await system.run_all_demos()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)

