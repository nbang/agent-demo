#!/usr/bin/env python3
"""
Multi-Agent Customer Service Team Example

This example demonstrates a customer service system with specialized agents
handling different aspects of customer support and issue resolution.

Team Members:
- Triage Agent: Initial assessment and routing
- Technical Support: Handles technical issues
- Billing Support: Manages billing and payment questions
- Product Specialist: Expert on product features and usage
- Escalation Manager: Handles complex cases and escalations
"""

import os
import sys
import pathlib
import asyncio
from textwrap import dedent

# Add project root to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from model_config import get_configured_model, print_model_info

# Load environment variables
load_dotenv()

def create_customer_service_team():
    """Create a customer service team with specialized support roles."""
    
    # Triage Agent
    triage_agent = Agent(
        name="Customer Service Triage",
        role="Initial customer inquiry assessment and routing",
        model=get_configured_model(),
        tools=[ReasoningTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a customer service triage specialist.
        - Greet customers warmly and professionally
        - Quickly assess the nature and urgency of customer inquiries
        - Categorize issues (technical, billing, product, general)
        - Determine priority level (low, medium, high, urgent)
        - Route customers to the appropriate specialist
        - Collect initial information to help specialists
        - Provide immediate answers for simple questions
        - Set proper expectations for resolution time
        """),
        markdown=True,
    )
    
    # Technical Support Agent
    tech_support_agent = Agent(
        name="Technical Support Specialist",
        role="Resolve technical issues and troubleshoot problems",
        model=get_configured_model(),
        tools=[ReasoningTools(), DuckDuckGoTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a technical support specialist.
        - Diagnose technical problems systematically
        - Provide step-by-step troubleshooting instructions
        - Explain technical concepts in simple terms
        - Research known issues and solutions
        - Document solutions for future reference
        - Escalate complex technical issues when needed
        - Follow up to ensure problems are resolved
        - Provide preventive maintenance recommendations
        """),
        markdown=True,
    )
    
    # Billing Support Agent
    billing_agent = Agent(
        name="Billing Support Specialist",
        role="Handle billing inquiries, payments, and account issues",
        model=get_configured_model(),
        tools=[ReasoningTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a billing support specialist.
        - Handle billing questions and disputes professionally
        - Explain charges, fees, and payment processes clearly
        - Assist with payment methods and updates
        - Process refunds and adjustments when appropriate
        - Help with subscription changes and cancellations
        - Provide billing history and account summaries
        - Identify and resolve billing system issues
        - Ensure compliance with payment policies
        """),
        markdown=True,
    )
    
    # Product Specialist Agent
    product_specialist = Agent(
        name="Product Specialist",
        role="Expert guidance on product features, usage, and best practices",
        model=get_configured_model(),
        tools=[DuckDuckGoTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a product specialist and expert.
        - Provide detailed product information and guidance
        - Explain features, capabilities, and limitations
        - Demonstrate best practices and use cases
        - Help customers optimize their product usage
        - Suggest complementary products or upgrades
        - Provide training resources and documentation
        - Collect product feedback and improvement suggestions
        - Stay updated on new features and releases
        """),
        markdown=True,
    )
    
    # Escalation Manager Agent
    escalation_manager = Agent(
        name="Escalation Manager",
        role="Handle complex cases, complaints, and high-priority issues",
        model=get_configured_model(),
        tools=[ReasoningTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are an escalation manager and senior customer service specialist.
        - Handle complex, sensitive, or high-priority cases
        - Manage customer complaints and difficult situations
        - Make executive decisions on exceptions and special requests
        - Coordinate with other departments when needed
        - Ensure customer satisfaction and retention
        - Implement service recovery strategies
        - Review and improve service processes
        - Provide final resolution for escalated issues
        """),
        markdown=True,
    )
    
    # Create the customer service team
    customer_service_team = Team(
        name="Customer Service Team",
        model=get_configured_model(),
        members=[
            triage_agent,
            tech_support_agent,
            billing_agent,
            product_specialist,
            escalation_manager,
        ],
        instructions=dedent("""
        You are managing a professional customer service team.
        
        Service Process:
        1. Triage: Assess customer inquiry and route to appropriate specialist
        2. Specialized Support: Handle the specific type of issue expertly
        3. Collaboration: Work together when issues span multiple areas
        4. Escalation: Involve manager for complex or sensitive cases
        5. Resolution: Ensure customer satisfaction and issue closure
        
        Service Standards:
        - Respond promptly and professionally to all inquiries
        - Listen actively and show empathy for customer concerns
        - Provide accurate, helpful information and solutions
        - Follow up to ensure complete resolution
        - Document interactions for future reference
        - Continuously improve service quality and processes
        """),
        show_members_responses=True,
        markdown=True,
    )
    
    return customer_service_team

def run_customer_service_example():
    """Run a customer service collaboration example."""
    print("🎧 Multi-Agent Customer Service Team Demo")
    print("=" * 60)
    
    # Show configuration
    print_model_info()
    
    print("🤖 Creating customer service team...")
    team = create_customer_service_team()
    
    print(f"✅ Team created with {len(team.members)} specialized agents:")
    for agent in team.members:
        print(f"   • {agent.name}: {agent.role}")
    
    print("\n" + "=" * 60)
    print("📞 Customer Service Scenarios")
    print("=" * 60)
    
    # Sample customer scenarios
    scenarios = [
        {
            "title": "Technical Issue with Login",
            "description": """
            Customer: Hi, I'm having trouble logging into my account. I keep getting 
            an error message saying 'Invalid credentials' even though I'm sure I'm 
            using the right password. I tried resetting it twice but still can't get in. 
            This is really frustrating because I need to access my account for work.
            """,
        },
        {
            "title": "Billing Dispute",
            "description": """
            Customer: I was charged $99.99 last month but my plan is supposed to be $49.99. 
            I've been a customer for 3 years and never had billing issues before. 
            I didn't authorize any upgrades or changes. Can you please explain this charge 
            and issue a refund? I'm considering canceling my subscription if this isn't resolved.
            """,
        },
        {
            "title": "Product Feature Question",
            "description": """
            Customer: I'm new to your platform and trying to figure out how to set up 
            automated reports for my team. I see there are several options but I'm not 
            sure which features I need. Can you help me understand the different reporting 
            capabilities and recommend the best setup for a 10-person marketing team?
            """,
        }
    ]
    
    # Let user choose a scenario
    print("Available customer service scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['title']}")
    
    print(f"{len(scenarios) + 1}. Enter custom scenario")
    
    try:
        choice = input(f"\nSelect scenario (1-{len(scenarios) + 1}): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(scenarios):
            selected_scenario = scenarios[int(choice) - 1]
            customer_inquiry = selected_scenario["description"]
            scenario_title = selected_scenario["title"]
        elif choice == str(len(scenarios) + 1):
            scenario_title = input("Enter scenario title: ").strip()
            customer_inquiry = input("Enter customer inquiry: ").strip()
        else:
            # Default to first scenario
            selected_scenario = scenarios[0]
            customer_inquiry = selected_scenario["description"]
            scenario_title = selected_scenario["title"]
        
        print(f"\n📋 Handling Scenario: {scenario_title}")
        print("-" * 60)
        
        team.print_response(
            input=customer_inquiry,
            stream=True,
        )
        
        print("\n" + "=" * 60)
        print("✅ Customer service interaction completed!")
        
    except KeyboardInterrupt:
        print("\n👋 Customer service cancelled by user")
    except Exception as e:
        print(f"❌ Error during customer service: {e}")

if __name__ == "__main__":
    try:
        run_customer_service_example()
        
    except KeyboardInterrupt:
        print("\n👋 Customer service demo cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your environment is configured correctly:")
        print("1. Check your .env file has the correct API keys")
        print("2. Ensure all dependencies are installed")