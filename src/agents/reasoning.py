#!/usr/bin/env python3
"""
Advanced Reasoning Agent

A sophisticated AI agent that performs structured, step-by-step problem analysis with 
comprehensive reasoning capabilities. This agent breaks down complex problems, shows 
detailed reasoning steps, provides logical analysis, and presents solutions in a clear, 
structured format with real-time reasoning visibility.

Key Features:
- Step-by-step structured problem analysis
- Multi-perspective consideration and evaluation  
- Assumption identification and uncertainty handling
- Evidence-based reasoning and evaluation
- Real-time intermediate step streaming
- Comprehensive problem decomposition
- Different reasoning patterns (deductive, inductive, abductive)
- Clear presentation of logic and supporting evidence

Usage:
    python reasoning_agent.py
    
or

    python -m src.agents.reasoning
"""

import os
import sys
import signal
from typing import Optional, List, Dict, Any
from textwrap import dedent

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckduckgo import DuckDuckGoTools
from src.models.config import get_reasoning_model, print_model_info, test_model_connection
from src.services.error_handling import ErrorHandler
from src.services.monitoring import PerformanceMonitor
from src.services.logging import setup_logging, get_agent_logger

# Initialize logging
setup_logging()
logger = get_agent_logger(__name__)

class ReasoningPatterns:
    """Defines different reasoning patterns and approaches."""
    
    PROBLEM_DECOMPOSITION = """
    When analyzing complex problems:
    1. Break down the problem into its fundamental components
    2. Identify the relationships between different parts
    3. Determine which components are most critical to address
    4. Consider how solving one part affects the others
    5. Establish a logical sequence for addressing each component
    """
    
    ASSUMPTION_ANALYSIS = """
    For thorough assumption identification:
    1. State what information you're taking as given
    2. Identify unstated assumptions underlying the problem
    3. Evaluate how reasonable these assumptions are
    4. Consider what changes if assumptions prove incorrect
    5. Highlight which assumptions are most critical to validate
    """
    
    EVIDENCE_EVALUATION = """
    When assessing evidence and arguments:
    1. Identify the sources and types of evidence available
    2. Evaluate the credibility and reliability of each source
    3. Look for both supporting and contradicting evidence
    4. Assess the strength of causal relationships claimed
    5. Consider what additional evidence would strengthen the analysis
    """
    
    PERSPECTIVE_ANALYSIS = """
    For multi-perspective consideration:
    1. Identify key stakeholders and their interests
    2. Consider how different groups might view the problem
    3. Analyze potential conflicts between perspectives
    4. Look for common ground and shared interests
    5. Evaluate which perspectives have the strongest foundation
    """
    
    UNCERTAINTY_HANDLING = """
    When dealing with uncertainty:
    1. Clearly identify what is known vs. unknown
    2. Distinguish between different types of uncertainty
    3. Assess the potential impact of unknown factors
    4. Consider scenarios with different uncertainty outcomes
    5. Recommend strategies for reducing uncertainty where possible
    """

def create_reasoning_agent() -> Agent:
    """Create an advanced reasoning agent with comprehensive analytical capabilities."""
    try:
        model = get_reasoning_model()
        
        # Comprehensive instructions for structured reasoning
        reasoning_instructions = dedent("""\
            You are an **Expert Reasoning Assistant** with exceptional analytical and problem-solving capabilities! 🧠
            
            ## Your Core Mission
            Help users tackle complex problems through structured, systematic analysis that reveals deep insights and actionable solutions.
            
            ## Your Reasoning Philosophy
            **Structure + Logic + Clarity = Powerful Analysis**
            
            ## Your Standard Approach to Complex Problems:
            
            ### 1. **Problem Understanding & Decomposition** 📊
            - Break complex questions into manageable component parts
            - Identify the core issue beneath surface-level questions  
            - Map relationships between different problem elements
            - Establish clear boundaries and scope for analysis
            
            ### 2. **Assumption Analysis** 🔍
            - **Always** explicitly state your key assumptions
            - Identify unstated assumptions in the problem or context
            - Evaluate the reasonableness of these assumptions
            - Consider how conclusions change if assumptions prove incorrect
            
            ### 3. **Multi-Perspective Analysis** 👁️
            - Consider multiple stakeholder viewpoints and interests
            - Analyze how different groups might approach the problem
            - Look for hidden biases or blind spots in reasoning
            - Identify areas of consensus vs. disagreement
            
            ### 4. **Evidence-Based Reasoning** ⚖️
            - Gather and evaluate available evidence systematically
            - Distinguish between strong, moderate, and weak evidence
            - Look for both supporting AND contradicting information
            - Identify gaps where additional evidence is needed
            
            ### 5. **Uncertainty & Risk Assessment** ⚠️
            - **Explicitly highlight** areas of uncertainty or doubt
            - Distinguish between different types of uncertainty
            - Assess potential consequences of unknown factors
            - Recommend strategies for managing or reducing uncertainty
            
            ### 6. **Solution Development & Evaluation** 💡
            - Generate multiple potential approaches or solutions
            - Evaluate trade-offs and implications of each option
            - Consider both short-term and long-term consequences
            - Provide clear reasoning for recommended approaches
            
            ## Your Reasoning Patterns:
            
            **For Quantitative Problems:**
            - Show all calculations step-by-step
            - Explain the significance and meaning of numbers
            - Consider margins of error and confidence levels
            - Identify data reliability and source limitations
            
            **For Qualitative Analysis:**
            - Examine how different factors interact and influence each other
            - Consider psychological, social, and cultural dynamics
            - Evaluate practical implementation constraints
            - Address ethical considerations and value trade-offs
            
            **For Strategic Decisions:**
            - Analyze both opportunities and threats
            - Consider resource requirements and constraints
            - Evaluate timing and sequencing factors
            - Assess potential unintended consequences
            
            ## Your Communication Style:
            - **Use clear, logical structure** with numbered steps or bullet points
            - **Show your thought process** transparently
            - **Use specific examples** to illustrate abstract concepts
            - **Employ visual organization** (headers, lists, emphasis) for clarity
            - **Acknowledge limitations** in your analysis honestly
            
            ## Quality Standards:
            - Every major claim should have supporting reasoning
            - Identify and address potential counterarguments
            - Provide actionable recommendations where appropriate
            - Ensure conclusions logically follow from the analysis
            - Make complex ideas accessible without oversimplifying
            
            Remember: Your goal is not just to provide answers, but to demonstrate **how** to think through complex problems systematically and thoroughly.
        """)
        
        # Create the reasoning agent
        agent = Agent(
            name="Advanced Reasoning Assistant",
            model=model,
            tools=[
                ReasoningTools(
                    enable_think=True,       # Enable structured thinking
                    enable_analyze=True,     # Enable analytical capabilities  
                    add_instructions=True,   # Add reasoning instructions
                    add_few_shot=True,      # Include reasoning examples
                ),
                DuckDuckGoTools(enable_search=True),  # Enable web search for evidence gathering
            ],
            instructions=reasoning_instructions,
            markdown=True,
            add_datetime_to_context=True,
            stream_intermediate_steps=True,  # Show reasoning steps as they happen
        )
        
        return agent
        
    except Exception as e:
        logger.error(f"Error creating reasoning agent: {str(e)}")
        raise ValueError(f"Failed to create reasoning agent: {str(e)}")

def display_reasoning_banner():
    """Display welcome banner for the reasoning agent."""
    try:
        print("🧠 Advanced Reasoning Agent")
    except UnicodeEncodeError:
        print("Advanced Reasoning Agent")
    print("=" * 60)
    print("Welcome to the Advanced Reasoning Agent!")
    print("I specialize in structured, step-by-step problem analysis.")
    print()
    print("My capabilities include:")
    try:
        print("  🔍 Complex problem decomposition")
        print("  📊 Multi-perspective analysis")
        print("  ⚖️ Evidence evaluation and assessment")
        print("  🎯 Assumption identification and testing")
        print("  ⚠️ Uncertainty analysis and risk assessment")
        print("  💡 Structured solution development")
        print("  📈 Strategic decision analysis")
        print("  🌐 Web research for evidence gathering")
    except UnicodeEncodeError:
        print("  - Complex problem decomposition")
        print("  - Multi-perspective analysis")
        print("  - Evidence evaluation and assessment")
        print("  - Assumption identification and testing")
        print("  - Uncertainty analysis and risk assessment")
        print("  - Structured solution development")
        print("  - Strategic decision analysis")
        print("  - Web research for evidence gathering")
    print("=" * 60)

def display_reasoning_examples():
    """Display example problems suitable for reasoning analysis."""
    print("\n💭 Example Complex Problems for Analysis:")
    print("=" * 50)
    
    examples = [
        {
            "category": "Strategic Decision Making",
            "problems": [
                "Should a company implement a 4-day work week? Analyze comprehensively.",
                "How should a city address its housing affordability crisis?",
                "What factors should a startup consider when choosing between growth strategies?"
            ]
        },
        {
            "category": "Ethical & Social Analysis", 
            "problems": [
                "What are the ethical implications of AI in healthcare decision-making?",
                "How should society balance individual privacy with public safety?",
                "Analyze the fairness and effectiveness of universal basic income."
            ]
        },
        {
            "category": "Problem-Solving & Design",
            "problems": [
                "How would you solve traffic congestion in a major metropolitan area?",
                "Design a system to reduce food waste in restaurants and grocery stores.",
                "What's the best approach to combat climate change at the city level?"
            ]
        },
        {
            "category": "Comparative Analysis",
            "problems": [
                "Compare electric cars vs. public transportation for environmental impact.",
                "Analyze remote work vs. office work for productivity and wellbeing.",
                "Evaluate different education models for preparing students for the future."
            ]
        },
        {
            "category": "Logic Puzzles & Scenarios",
            "problems": [
                "A trolley problem variation: analyze the ethical dimensions thoroughly.",
                "You have limited resources to save multiple endangered species - how do you prioritize?",
                "Design a fair system for distributing limited medical resources during a crisis."
            ]
        }
    ]
    
    for example in examples:
        try:
            print(f"\n📁 **{example['category']}:**")
        except UnicodeEncodeError:
            print(f"\n{example['category']}:")
        
        for i, problem in enumerate(example['problems'], 1):
            print(f"   {i}. {problem}")
    
    print("\n" + "=" * 50)

def display_reasoning_commands():
    """Display available commands and interaction tips.""" 
    print("\n💡 Interaction Tips & Commands:")
    print("=" * 40)
    print("• Ask complex, multi-faceted questions for best results")
    print("• Request specific reasoning approaches (e.g., 'analyze pros and cons')")
    print("• Ask for assumption analysis: 'What assumptions are you making?'")
    print("• Request multiple perspectives: 'Consider different stakeholder views'")
    print("• Ask about uncertainty: 'What are the main uncertainties here?'")
    print("• Type 'examples' for more problem examples")
    print("• Type 'patterns' to see reasoning pattern explanations")
    print("• Type 'stats' for performance information")
    print("• Type 'quit', 'exit', 'bye', or 'q' to end the session")
    print("=" * 40)

def display_reasoning_patterns():
    """Display information about different reasoning patterns."""
    print("\n🧠 Reasoning Patterns & Approaches:")
    print("=" * 50)
    
    patterns = [
        ("Problem Decomposition", "Breaking complex issues into manageable components"),
        ("Assumption Analysis", "Identifying and evaluating underlying assumptions"),  
        ("Evidence Evaluation", "Assessing the quality and reliability of information"),
        ("Perspective Analysis", "Considering multiple viewpoints and stakeholder interests"),
        ("Uncertainty Handling", "Managing and communicating areas of doubt"),
        ("Deductive Reasoning", "Drawing specific conclusions from general principles"),
        ("Inductive Reasoning", "Forming general principles from specific observations"),
        ("Abductive Reasoning", "Finding the best explanation for observed phenomena"),
    ]
    
    for pattern, description in patterns:
        try:
            print(f"🔹 **{pattern}**: {description}")
        except UnicodeEncodeError:
            print(f"- {pattern}: {description}")
    
    print("\nI automatically apply these patterns based on the type of problem you present.")
    print("=" * 50)

def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        print("\n\n👋 Shutting down Reasoning Agent. Thank you for thinking with me!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def validate_reasoning_input(user_input: str) -> bool:
    """Validate user input for reasoning tasks."""
    if not user_input or not user_input.strip():
        return False
    
    if len(user_input) > 15000:  # Longer limit for complex reasoning problems
        return False
    
    # Allow reasoning-related content
    return True

def classify_problem_type(user_input: str) -> str:
    """Classify the type of reasoning problem for appropriate approach."""
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ['should', 'ought', 'ethical', 'moral', 'right', 'wrong']):
        return "ethical_analysis"
    elif any(word in input_lower for word in ['compare', 'versus', 'vs', 'better', 'difference']):
        return "comparative_analysis"  
    elif any(word in input_lower for word in ['how', 'solve', 'fix', 'address', 'improve']):
        return "problem_solving"
    elif any(word in input_lower for word in ['why', 'because', 'cause', 'reason', 'explain']):
        return "causal_analysis"
    elif any(word in input_lower for word in ['decide', 'choose', 'option', 'alternative', 'strategy']):
        return "decision_analysis"
    elif any(word in input_lower for word in ['predict', 'future', 'forecast', 'will', 'outcome']):
        return "predictive_analysis"
    else:
        return "general_analysis"

def provide_reasoning_context(problem_type: str) -> str:
    """Provide additional context based on problem type."""
    contexts = {
        "ethical_analysis": "Focus on multiple ethical frameworks, stakeholder impacts, and value trade-offs.",
        "comparative_analysis": "Ensure balanced evaluation with clear criteria and systematic comparison.",
        "problem_solving": "Emphasize root cause analysis, alternative solutions, and implementation considerations.",
        "causal_analysis": "Focus on evidence quality, alternative explanations, and causal mechanisms.",
        "decision_analysis": "Highlight decision criteria, trade-offs, risks, and implementation factors.",
        "predictive_analysis": "Emphasize uncertainty, scenarios, assumptions, and confidence levels.",
        "general_analysis": "Apply comprehensive structured reasoning appropriate to the problem."
    }
    return contexts.get(problem_type, contexts["general_analysis"])

def main():
    """Main function to run the advanced reasoning agent."""
    # Setup
    setup_signal_handlers()
    performance_monitor = PerformanceMonitor()
    
    try:
        # Validate environment and create agent
        print("🔧 Initializing Advanced Reasoning Agent...")
        
        # Test model connection
        print("📡 Testing reasoning model connection...")
        connection_result = test_model_connection()
        if not connection_result:
            raise ValueError("Model connection failed. Please check your configuration.")
        
        print("✅ Model connection successful!")
        
        # Create and configure agent
        print("🧠 Creating reasoning agent with advanced capabilities...")
        agent = create_reasoning_agent()
        print("✅ Reasoning agent created successfully!")
        
        # Display information
        display_reasoning_banner()
        print_model_info()
        display_reasoning_examples()
        display_reasoning_commands()
        
        print("\n💬 Ready for Complex Problem Analysis!")
        print("Ask me any complex question that requires structured thinking...")
        print("-" * 60)
        
        # Main reasoning loop
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Thank you for exploring complex problems with me!")
                    break
                elif user_input.lower() == 'help':
                    display_reasoning_commands()
                    continue
                elif user_input.lower() == 'examples':
                    display_reasoning_examples()
                    continue
                elif user_input.lower() == 'patterns':
                    display_reasoning_patterns()
                    continue
                elif user_input.lower() in ['stats', 'performance', 'perf']:
                    print("\n📊 Performance Statistics:")
                    stats = performance_monitor.get_summary_stats()
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                    continue
                
                # Validate input
                if not validate_reasoning_input(user_input):
                    print("❌ Please provide a clear question or problem for analysis.")
                    print("💡 Try asking about complex decisions, ethical dilemmas, or strategic questions.")
                    continue
                
                # Classify problem and provide context
                problem_type = classify_problem_type(user_input)
                context = provide_reasoning_context(problem_type)
                
                print(f"\n🧠 Reasoning Assistant: ")
                print(f"📋 Analyzing as: {problem_type.replace('_', ' ').title()}")
                print(f"🎯 Focus: {context}")
                print("\n" + "🔄 Starting structured analysis..." + "\n")
                print("-" * 50)
                
                # Process with reasoning agent 
                try:
                    # Enhanced prompt with reasoning context
                    enhanced_prompt = f"""
                    **Problem Type**: {problem_type.replace('_', ' ').title()}
                    **Analysis Focus**: {context}
                    
                    **Question**: {user_input}
                    
                    Please provide a comprehensive, structured analysis using your full reasoning capabilities.
                    """
                    
                    agent.print_response(
                        enhanced_prompt,
                        stream=True,
                        stream_intermediate_steps=True,
                        show_full_reasoning=True
                    )
                    
                    print("\n" + "-" * 50)
                    print("✅ Analysis complete!")
                    
                    # Log successful interaction
                    logger.info(f"Reasoning analysis completed for problem type: {problem_type}")
                    
                except Exception as e:
                    print(f"\n❌ Error during reasoning analysis: {str(e)}")
                    logger.error(f"Error during reasoning analysis: {e}", exc_info=True)
                    
                    if "network" in str(e).lower() or "timeout" in str(e).lower() or "api" in str(e).lower():
                        print("🔄 You can try rephrasing your question or asking a different one.")
                    else:
                        print("⚠️ This error may require restarting the reasoning agent.")
                        
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Thank you for thinking through complex problems with me!")
                break
            except Exception as e:
                error_message = f"Unexpected error: {e}"
                logger.error(f"Unexpected error in reasoning loop: {e}")
                print(f"\n❌ {error_message}")
                
                if "network" in str(e).lower() or "timeout" in str(e).lower() or "api" in str(e).lower():
                    print("🔄 You can try again with a different question.")
                else:
                    print("⚠️ This error may require restarting the agent.")
    
    except ValueError as e:
        error_message = f"Configuration error: {e}"
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {error_message}")
        print("\n🔧 Please check your environment setup and try again.")
        sys.exit(1)
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected Error: {error_message}")
        logger.debug(f"Error details: {e}", exc_info=True)
        sys.exit(1)
    
    # Final performance report
    print("\n📊 Final Performance Summary:")
    stats = performance_monitor.get_summary_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n🧠 Thank you for using the Advanced Reasoning Agent!")
    print("Remember: Great reasoning is the foundation of great decisions! 💡")

if __name__ == "__main__":
    main()