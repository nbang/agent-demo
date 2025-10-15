#!/usr/bin/env python3
"""
Research Team Launcher

A simple menu to choose between different research team examples.
"""

import os
import sys
import subprocess
import pathlib

def display_menu():
    """Display the main menu options."""
    print("\n🔬 Agno Research Team Examples")
    print("=" * 50)
    print("Choose a research team to run:")
    print()
    print("1. Simple Research Team (Recommended)")
    print("   • 2-agent team (Web Researcher + Analysis Coordinator)")
    print("   • Reliable sync execution")
    print("   • Interactive topic selection")
    print("   • Best for: Quick, focused research")
    print()
    print("2. Advanced Research Team")
    print("   • 4-agent collaborative team")
    print("   • Full async collaboration features")
    print("   • Interactive topic selection")
    print("   • Best for: Comprehensive, multi-perspective research")
    print()
    print("3. Topic Selector (Test)")
    print("   • Test the interactive topic selection menu")
    print("   • No research execution")
    print()
    print("4. Exit")
    print()

def run_simple_research():
    """Run the simple research team."""
    print("\n🚀 Launching Simple Research Team...")
    print("-" * 40)
    
    try:
        # Run the simple research team script
        script_path = pathlib.Path(__file__).parent / "simple_research_team.py"
        subprocess.run([sys.executable, str(script_path)], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running simple research team: {e}")
    except KeyboardInterrupt:
        print("\n👋 Research cancelled by user")

def run_advanced_research():
    """Run the advanced research team."""
    print("\n🚀 Launching Advanced Research Team...")
    print("-" * 40)
    print("⚠️  Note: This uses a complex 4-agent async team which may encounter issues")
    print("   If you experience problems, try the Simple Research Team instead.")
    print()
    
    try:
        # Run the research team script
        script_path = pathlib.Path(__file__).parent / "research_team.py"
        
        # Run the advanced research team (always async)
        subprocess.run([sys.executable, str(script_path)], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running advanced research team: {e}")
    except KeyboardInterrupt:
        print("\n👋 Research cancelled by user")

def test_topic_selector():
    """Test the topic selector."""
    print("\n🧪 Testing Topic Selector...")
    print("-" * 40)
    
    try:
        # Run the topic selector script
        script_path = pathlib.Path(__file__).parent / "topic_selector.py"
        subprocess.run([sys.executable, str(script_path)], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running topic selector: {e}")
    except KeyboardInterrupt:
        print("\n👋 Topic selection cancelled by user")

def main():
    """Main menu loop."""
    while True:
        try:
            display_menu()
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                run_simple_research()
                
            elif choice == '2':
                run_advanced_research()
                
            elif choice == '3':
                test_topic_selector()
                
            elif choice == '4':
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-4.")
                continue
                
            # Ask if user wants to run another example
            print("\n" + "=" * 50)
            again = input("Would you like to run another example? (y/n): ").strip().lower()
            if again not in ['y', 'yes']:
                print("\n👋 Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue

if __name__ == "__main__":
    main()