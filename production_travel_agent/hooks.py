"""
Hooks for monitoring and controlling agent execution.
This module demonstrates RunHooks and AgentHooks for workflow monitoring and dynamic context injection.
"""

import time
from typing import Dict, Any, List
from agents.lifecycle import RunHooks, AgentHooks
from models import UserContext


# ============================================================================
# Global Run Hooks (Monitor entire workflow)
# ============================================================================

class GlobalMonitoringHooks(RunHooks):
    """
    Global hooks that monitor the entire agent workflow execution.
    Demonstrates tracking handoffs, agent starts, and overall workflow.
    """
    
    def __init__(self, enable_verbose: bool = True):
        self.enable_verbose = enable_verbose
        self.workflow_start_time = None
        self.agent_executions = []
    
    async def on_start(self, context):
        """Called when the entire workflow starts."""
        self.workflow_start_time = time.time()
        if self.enable_verbose:
            print(f"\n{'='*60}")
            print(f"[WORKFLOW] Starting execution...")
            print(f"{'='*60}\n")
    
    async def on_end(self, context, result):
        """Called when the entire workflow completes."""
        if self.workflow_start_time:
            total_time = time.time() - self.workflow_start_time
            if self.enable_verbose:
                print(f"\n{'='*60}")
                print(f"[WORKFLOW] Completed in {total_time:.2f}s")
                print(f"[WORKFLOW] Total agents executed: {len(self.agent_executions)}")
                print(f"[WORKFLOW] Final output length: {len(result.final_output)} characters")
                print(f"{'='*60}\n")
    
    async def on_agent_start(self, context, agent):
        """Called when any agent starts execution."""
        agent_start = {
            "agent_name": agent.name,
            "start_time": time.time()
        }
        self.agent_executions.append(agent_start)
        
        if self.enable_verbose:
            print(f"[GLOBAL] Agent '{agent.name}' starting execution")
    
    async def on_agent_end(self, context, agent, output):
        """Called when any agent completes execution."""
        if self.agent_executions:
            last_execution = self.agent_executions[-1]
            if last_execution["agent_name"] == agent.name:
                execution_time = time.time() - last_execution["start_time"]
                if self.enable_verbose:
                    print(f"[GLOBAL] Agent '{agent.name}' completed in {execution_time:.2f}s")
                    print(f"[GLOBAL] Output preview: {output[:100]}...")
    
    async def on_handoff(self, context, from_agent, to_agent):
        """Called when a handoff occurs between agents."""
        if self.enable_verbose:
            print(f"[GLOBAL] Handoff: '{from_agent.name}' → '{to_agent.name}'")
    
    async def on_error(self, context, error):
        """Called when an error occurs during workflow execution."""
        if self.enable_verbose:
            print(f"[GLOBAL] ERROR occurred: {type(error).__name__}: {str(error)}")


# ============================================================================
# Agent-Specific Hooks
# ============================================================================

class TravelGenieHooks(AgentHooks):
    """
    Agent-specific hooks for the Travel Genie agent.
    Demonstrates tool monitoring, context injection, and agent-specific behavior.
    """
    
    def __init__(self, enable_tool_monitoring: bool = True):
        self.enable_tool_monitoring = enable_tool_monitoring
        self.tool_invocations = []
    
    async def on_start(self, context, agent):
        """Called when Travel Genie agent starts."""
        print(f"[AGENT HOOK] {agent.name} starting execution")
        
        # Dynamic context injection example
        # In production, this could fetch user data from a database
        if not hasattr(context, 'context') or context.context is None:
            # Example: Inject default context if none exists
            print(f"[AGENT HOOK] No user context found, using default context")
    
    async def on_end(self, context, agent, output):
        """Called when Travel Genie agent completes."""
        print(f"[AGENT HOOK] {agent.name} completed execution")
        print(f"[AGENT HOOK] Tools used: {len(self.tool_invocations)}")
        if output:
            print(f"[AGENT HOOK] Output length: {len(output)} characters")
    
    async def on_tool_start(self, context, agent, tool):
        """Called when Travel Genie is about to call a tool."""
        tool_info = {
            "tool_name": tool.name,
            "start_time": time.time()
        }
        self.tool_invocations.append(tool_info)
        
        if self.enable_tool_monitoring:
            print(f"[AGENT HOOK] {agent.name} → Calling tool: {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        """Called when Travel Genie finishes calling a tool."""
        if self.tool_invocations:
            last_tool = self.tool_invocations[-1]
            if last_tool["tool_name"] == tool.name:
                execution_time = time.time() - last_tool["start_time"]
                if self.enable_tool_monitoring:
                    result_preview = str(result)[:100] if result else "None"
                    print(f"[AGENT HOOK] {agent.name} → Tool '{tool.name}' completed in {execution_time:.3f}s")
                    print(f"[AGENT HOOK] Result preview: {result_preview}...")


class BookingAgentHooks(AgentHooks):
    """
    Hooks for booking-related agents.
    Focuses on secure context validation and booking tracking.
    """
    
    async def on_start(self, context, agent):
        """Validate that secure context is available for booking operations."""
        print(f"[BOOKING HOOK] {agent.name} starting")
        
        if hasattr(context, 'context') and context.context:
            user_context = context.context
            if isinstance(user_context, UserContext):
                print(f"[BOOKING HOOK] User context loaded for user: {user_context.user_id}")
            else:
                print(f"[BOOKING HOOK] Warning: Context type mismatch")
        else:
            print(f"[BOOKING HOOK] Warning: No secure context available")
    
    async def on_tool_start(self, context, agent, tool):
        """Log booking tool invocations."""
        if "book" in tool.name.lower():
            print(f"[BOOKING HOOK] Secure booking operation initiated: {tool.name}")


class ResearchAgentHooks(AgentHooks):
    """
    Hooks for research agents.
    Tracks research operations and data collection.
    """
    
    def __init__(self):
        self.research_queries = []
    
    async def on_tool_start(self, context, agent, tool):
        """Track research tool usage."""
        if "search" in tool.name.lower() or "research" in tool.name.lower():
            print(f"[RESEARCH HOOK] Research operation: {tool.name}")
            self.research_queries.append(tool.name)
    
    async def on_end(self, context, agent, output):
        """Summarize research activities."""
        print(f"[RESEARCH HOOK] {agent.name} completed {len(self.research_queries)} research operations")


class ItineraryAgentHooks(AgentHooks):
    """
    Hooks for itinerary generation agents.
    Tracks itinerary creation and validation.
    """
    
    async def on_start(self, context, agent):
        """Initialize itinerary generation tracking."""
        print(f"[ITINERARY HOOK] {agent.name} starting itinerary generation")
    
    async def on_end(self, context, agent, output):
        """Validate and log itinerary completion."""
        print(f"[ITINERARY HOOK] {agent.name} itinerary generation completed")
        # Could add validation logic here


# ============================================================================
# Specialized Hooks for Metrics Collection
# ============================================================================

class MetricsCollectionHooks(RunHooks):
    """
    Hooks specialized for collecting detailed execution metrics.
    """
    
    def __init__(self):
        self.metrics = {
            "workflow_start": None,
            "workflow_end": None,
            "agents": [],
            "handoffs": [],
            "tools_used": [],
            "errors": []
        }
    
    async def on_start(self, context):
        """Record workflow start."""
        self.metrics["workflow_start"] = time.time()
    
    async def on_end(self, context, result):
        """Record workflow completion and compile metrics."""
        self.metrics["workflow_end"] = time.time()
        if self.metrics["workflow_start"]:
            duration = self.metrics["workflow_end"] - self.metrics["workflow_start"]
            self.metrics["total_duration"] = duration
        
        # Add token usage if available
        if hasattr(result, 'usage'):
            self.metrics["token_usage"] = {
                "prompt_tokens": getattr(result.usage, 'prompt_tokens', 0),
                "completion_tokens": getattr(result.usage, 'completion_tokens', 0),
                "total_tokens": getattr(result.usage, 'total_tokens', 0)
            }
    
    async def on_agent_start(self, context, agent):
        """Track agent execution."""
        self.metrics["agents"].append({
            "name": agent.name,
            "start_time": time.time()
        })
    
    async def on_agent_end(self, context, agent, output):
        """Complete agent metrics."""
        for agent_metric in reversed(self.metrics["agents"]):
            if agent_metric["name"] == agent.name and "end_time" not in agent_metric:
                agent_metric["end_time"] = time.time()
                agent_metric["duration"] = agent_metric["end_time"] - agent_metric["start_time"]
                break
    
    async def on_handoff(self, context, from_agent, to_agent):
        """Track handoffs."""
        self.metrics["handoffs"].append({
            "from": from_agent.name,
            "to": to_agent.name,
            "timestamp": time.time()
        })
    
    async def on_tool_end(self, context, agent, tool, result):
        """Track tool usage."""
        self.metrics["tools_used"].append({
            "agent": agent.name,
            "tool": tool.name,
            "timestamp": time.time()
        })
    
    async def on_error(self, context, error):
        """Track errors."""
        self.metrics["errors"].append({
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": time.time()
        })
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get collected metrics."""
        return self.metrics.copy()


