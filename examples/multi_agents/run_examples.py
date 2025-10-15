#!/usr/bin/env python3
"""
Multi-Agent Examples Runner

This script provides an interactive menu to run different multi-agent examples
demonstrating various collaboration patterns with the Agno framework.
"""

import os
import sys
import pathlib
import asyncio
from textwrap import dedent

# Add project root to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from model_config import print_model_info

def show_menu():
    """Display the multi-agent examples menu."""
    print("🤖 Multi-Agent Examples with Agno Framework")
    print("=" * 60)
    
    examples = [
        {
            "title": "Research Team",
            "description": "Collaborative research with web, academic, social media, and analysis specialists",
            "file": "research_team.py"
        },
        {
            "title": "Content Creation Team", 
            "description": "Content pipeline from research to final optimized publication",
            "file": "content_creation_team.py"
        },
        {
            "title": "Customer Service Team",
            "description": "Multi-tier customer support with triage, technical, billing, and product specialists",
            "file": "customer_service_team.py"
        }
    ]
    
    print("Available Multi-Agent Examples:")
    print("-" * 30)
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['title']}")
        print(f"   {example['description']}")
        print()
    
    print(f"{len(examples) + 1}. Show Model Configuration")
    print(f"{len(examples) + 2}. Exit")
    
    return examples

async def run_example(example_file):
    """Run the selected multi-agent example."""
    try:
        # Import and run the example
        if example_file == "research_team.py":
            from research_team import run_research_example
            await run_research_example()
        elif example_file == "content_creation_team.py":
            from content_creation_team import run_content_creation_example
            run_content_creation_example()
        elif example_file == "customer_service_team.py":
            from customer_service_team import run_customer_service_example
            run_customer_service_example()
        else:
            print(f"❌ Unknown example: {example_file}")
            
    except ImportError as e:
        print(f"❌ Error importing example: {e}")
        print("💡 Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error running example: {e}")

async def main():
    """Main interactive menu."""
    while True:
        try:
            examples = show_menu()
            
            choice = input(f"Select option (1-{len(examples) + 2}): ").strip()
            
            if not choice.isdigit():
                print("❌ Please enter a valid number")
                continue
                
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(examples):
                selected_example = examples[choice_num - 1]
                print(f"\n🚀 Running: {selected_example['title']}")
                print("=" * 60)
                
                await run_example(selected_example['file'])
                
                print("\n" + "=" * 60)
                input("Press Enter to return to menu...")
                print("\n")
                
            elif choice_num == len(examples) + 1:
                print("\n🔧 Model Configuration:")
                print("-" * 30)
                print_model_info()
                input("\nPress Enter to return to menu...")
                print("\n")
                
            elif choice_num == len(examples) + 2:
                print("👋 Goodbye!")
                break
                
            else:
                print(f"❌ Please enter a number between 1 and {len(examples) + 2}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except ValueError:
            print("❌ Please enter a valid number")
        except Exception as e:
            print(f"❌ Error: {e}")

def show_examples_info():
    """Show information about all available examples."""
    print(dedent("""
    📚 Multi-Agent Examples Overview
    ===============================
    
    1. Research Team
    ----------------
    Demonstrates collaborative research with specialized agents:
    • Web Researcher: Real-time information gathering
    • Academic Researcher: Scholarly sources and citations  
    • Social Media Researcher: Trends and public sentiment
    • Analysis Coordinator: Synthesis and insights
    
    Use case: Market research, competitive analysis, trend investigation
    
    2. Content Creation Team
    ------------------------
    Shows content production pipeline with quality control:
    • Research Specialist: Information gathering and fact-checking
    • Content Strategist: Planning and structure development
    • Content Writer: Creative writing and composition
    • Content Editor: Review, editing, and improvement
    • SEO Specialist: Optimization for search and engagement
    
    Use case: Blog posts, articles, marketing content, documentation
    
    3. Customer Service Team
    ------------------------
    Illustrates multi-tier customer support system:
    • Triage Agent: Initial assessment and routing
    • Technical Support: Technical troubleshooting
    • Billing Support: Payment and account issues
    • Product Specialist: Feature guidance and training
    • Escalation Manager: Complex cases and complaints
    
    Use case: Customer support, help desk, service management
    
    🎯 Key Multi-Agent Patterns Demonstrated:
    ----------------------------------------
    • Specialization: Each agent has a specific role and expertise
    • Collaboration: Agents work together towards common goals
    • Workflow: Structured processes with handoffs between agents
    • Quality Control: Multiple review stages and validation
    • Escalation: Hierarchical handling of complex cases
    • Knowledge Sharing: Agents build on each other's work
    
    💡 Getting Started:
    ------------------
    1. Make sure your .env file is configured with API keys
    2. Run this script and select an example
    3. Follow the interactive prompts
    4. Observe how agents collaborate and specialize
    """))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        show_examples_info()
    else:
        asyncio.run(main())