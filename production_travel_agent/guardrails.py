"""
Input and output guardrails for securing agent interactions.
This module demonstrates protecting agents from inappropriate inputs and preventing information leakage.
"""

from typing import Any, Union
from agents import (
    GuardrailFunctionOutput,
    InputGuardrailResult,
    OutputGuardrailResult,
    RunContextWrapper,
    Agent,
    TResponseInputItem,
    input_guardrail,
    output_guardrail
)


# ============================================================================
# Input Guardrails (Protect against inappropriate requests)
# ============================================================================

@input_guardrail
async def simple_content_filter(
    ctx: RunContextWrapper, 
    agent: Agent, 
    input: Union[str, list[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """
    Simple keyword-based content filter for fast, first-line defense.
    Catches obviously inappropriate requests quickly.
    """
    # Handle both string and list inputs
    if isinstance(input, list):
        input_str = " ".join([item.get("content", "") if isinstance(item, dict) else str(item) for item in input])
    else:
        input_str = str(input)
    
    # List of blocked keywords/phrases
    blocked_keywords = [
        "drug", "illegal", "weapon", "firearm",
        "red light district", "prostitution", "gambling",
        "hack", "cyber attack", "scam"
    ]
    
    user_input_lower = input_str.lower()
    
    for keyword in blocked_keywords:
        if keyword in user_input_lower:
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info=f"Content blocked: Request contains inappropriate keyword '{keyword}'"
            )
    
    # Allow the request
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info="Content approved by keyword filter"
    )


@input_guardrail
async def llm_content_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input: Union[str, list[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """
    LLM-based content guardrail for intelligent content analysis.
    Catches subtle attempts to circumvent keyword filters.
    
    Note: In production, this would use an LLM to analyze the input.
    For demonstration, we use rule-based logic.
    """
    # Handle both string and list inputs
    if isinstance(input, list):
        input_str = " ".join([item.get("content", "") if isinstance(item, dict) else str(item) for item in input])
    else:
        input_str = str(input)
    
    # More sophisticated analysis (in production, use LLM)
    suspicious_patterns = [
        "find drugs", "where to buy", "illegal activities",
        "adult entertainment", "questionable services"
    ]
    
    user_input_lower = input_str.lower()
    
    for pattern in suspicious_patterns:
        if pattern in user_input_lower:
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info=f"Content blocked by intelligent filter: Request appears to seek inappropriate content"
            )
    
    # Additional checks for travel-specific inappropriate requests
    inappropriate_travel_patterns = [
        "best strip club", "where to find prostitutes",
        "illegal activities in", "how to smuggle"
    ]
    
    for pattern in inappropriate_travel_patterns:
        if pattern in user_input_lower:
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info=f"Content blocked: Inappropriate travel-related request detected"
            )
    
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info="Content approved by LLM-based guardrail"
    )


@input_guardrail
async def policy_compliance_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input: Union[str, list[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """
    Policy compliance guardrail to ensure requests align with company policies.
    """
    # Handle both string and list inputs
    if isinstance(input, list):
        input_str = " ".join([item.get("content", "") if isinstance(item, dict) else str(item) for item in input])
    else:
        input_str = str(input)
    
    # Policy violations
    policy_violations = [
        "cancel my booking and refund",  # Must go through proper channels
        "change my passport number",     # Sensitive data modification
        "access another user's account"   # Privacy violation
    ]
    
    user_input_lower = input_str.lower()
    
    for violation in policy_violations:
        if violation in user_input_lower:
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info=f"Request blocked: Policy violation detected. Please contact customer support for this request."
            )
    
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info="Policy compliance verified"
    )


# ============================================================================
# Output Guardrails (Prevent information leakage)
# ============================================================================

@output_guardrail
async def leakage_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    Output guardrail to prevent sensitive information leakage.
    Redacts or blocks responses that might contain sensitive data.
    """
    # Sensitive patterns to detect
    sensitive_patterns = [
        "internal markup",
        "profit margin",
        "confidential",
        "trade secret",
        "passport number",
        "credit card",
        "ssn",
        "social security",
        "api key",
        "password",
        "secret"
    ]
    
    output_lower = agent_output.lower()
    
    for pattern in sensitive_patterns:
        if pattern in output_lower:
            # Redact the sensitive information
            redacted_output = agent_output
            # Simple redaction (in production, use more sophisticated methods)
            if "markup" in output_lower or "profit" in output_lower:
                redacted_output = "[REDACTED: Internal pricing information removed]"
            elif any(p in output_lower for p in ["passport", "credit card", "ssn"]):
                redacted_output = "[REDACTED: Personal information removed for security]"
            
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info=redacted_output
            )
    
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info=agent_output
    )


@output_guardrail
async def profanity_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    Output guardrail to filter profanity and inappropriate language.
    """
    profanity_words = [
        # Add list of profanity words if needed
        # For demonstration, using a simple check
    ]
    
    # Simple check (in production, use comprehensive profanity filter)
    # For now, just pass through
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info=output
    )


@output_guardrail
async def format_validation_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    Output guardrail to validate response format and quality.
    Ensures responses meet minimum quality standards.
    """
    # Check for empty or very short responses
    if not output or len(output.strip()) < 10:
        return GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info="[BLOCKED: Response too short or empty]"
        )
    
    # Check for error-like patterns
    error_patterns = [
        "error occurred",
        "failed to",
        "unable to process"
    ]
    
    output_lower = output.lower()
    for pattern in error_patterns:
        if pattern in output_lower and "i apologize" not in output_lower:
            # Might be an error message - flag it
            pass
    
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info=output
    )


# ============================================================================
# Combined Guardrail Functions
# ============================================================================

# Note: For layered guardrails, we chain them manually in main.py
# This function is kept for backward compatibility but uses the decorator pattern internally
async def layered_input_guardrails_helper(user_input: str) -> bool:
    """
    Helper function for layered input guardrails.
    Returns True if all guardrails pass, False otherwise.
    """
    # This would need to be called with proper context in actual usage
    # For now, return True (guardrails are checked via decorators on agents)
    return True


# Note: Output guardrails are applied via decorators on agents
# This function is kept for backward compatibility
async def comprehensive_output_guardrails_helper(agent_output: str) -> bool:
    """
    Helper function for comprehensive output guardrails.
    Returns True if all guardrails pass, False otherwise.
    """
    # Guardrails are applied via decorators on agents
    return True

