#!/usr/bin/env python3
"""
Research Topic Selection Module

This module provides interactive topic selection for research team examples.
"""

def get_predefined_topics():
    """Return a list of predefined research topics."""
    return [
        {
            "title": "AI Impact on Job Markets",
            "description": "The impact of artificial intelligence on job markets in 2024",
            "category": "Technology & Employment"
        },
        {
            "title": "Remote Work Evolution", 
            "description": "The benefits and challenges of remote work in 2024",
            "category": "Workplace Trends"
        },
        {
            "title": "Climate Change Solutions",
            "description": "Innovative solutions and technologies for addressing climate change",
            "category": "Environment & Sustainability"
        },
        {
            "title": "Cryptocurrency Market Trends",
            "description": "Current trends and future outlook for cryptocurrency markets",
            "category": "Finance & Technology"
        },
        {
            "title": "Mental Health in Digital Age",
            "description": "Mental health challenges and solutions in the digital age",
            "category": "Health & Society"
        },
        {
            "title": "Space Technology Advances",
            "description": "Recent advances in space technology and commercial space industry",
            "category": "Science & Technology"
        },
        {
            "title": "Electric Vehicle Adoption",
            "description": "Global trends in electric vehicle adoption and infrastructure",
            "category": "Transportation & Environment"
        },
        {
            "title": "Social Media Impact on Youth",
            "description": "The impact of social media on youth mental health and behavior",
            "category": "Technology & Society"
        },
        {
            "title": "Renewable Energy Transition",
            "description": "Global transition to renewable energy sources and challenges",
            "category": "Energy & Environment"
        },
        {
            "title": "Cybersecurity Threats 2024",
            "description": "Emerging cybersecurity threats and defense strategies in 2024",
            "category": "Technology & Security"
        }
    ]

def select_research_topic():
    """Interactive function to select a research topic."""
    topics = get_predefined_topics()
    
    print("\n🔍 Research Topic Selection")
    print("=" * 50)
    print("Choose from predefined topics or enter your own:")
    print()
    
    # Display predefined topics
    for i, topic in enumerate(topics, 1):
        print(f"{i:2d}. {topic['title']}")
        print(f"     {topic['description']}")
        print(f"     Category: {topic['category']}")
        print()
    
    print(f"{len(topics) + 1:2d}. Enter custom topic")
    print()
    
    while True:
        try:
            choice = input(f"Select option (1-{len(topics) + 1}): ").strip()
            
            if not choice:
                print("❌ Please enter a valid number")
                continue
                
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(topics):
                selected_topic = topics[choice_num - 1]
                print(f"\n✅ Selected: {selected_topic['title']}")
                print(f"📝 Description: {selected_topic['description']}")
                return selected_topic['description']
                
            elif choice_num == len(topics) + 1:
                # Custom topic
                print("\n📝 Enter Custom Research Topic:")
                custom_topic = input("Topic: ").strip()
                
                if custom_topic:
                    print(f"\n✅ Custom topic: {custom_topic}")
                    return custom_topic
                else:
                    print("❌ Please enter a valid topic")
                    continue
            else:
                print(f"❌ Please enter a number between 1 and {len(topics) + 1}")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Topic selection cancelled")
            return None

def get_research_prompt(topic):
    """Generate a comprehensive research prompt for the given topic."""
    return f"""
    Conduct comprehensive research on the following topic:
    
    **Topic:** {topic}
    
    **Research Requirements:**
    - Current state and recent developments
    - Key statistics and data points
    - Expert opinions and analysis
    - Public sentiment and social discussions
    - Future projections and implications
    - Challenges and opportunities
    
    **Deliverable:**
    Provide a comprehensive research report with findings from multiple perspectives,
    including web sources, academic research, and social trends analysis.
    """

def get_simple_research_prompt(topic):
    """Generate a simple research prompt for basic research."""
    return f"Research the topic: {topic}. Provide a brief summary with key points, current trends, and important insights."

if __name__ == "__main__":
    # Test the topic selection
    topic = select_research_topic()
    if topic:
        print("\n" + "=" * 50)
        print("Generated Research Prompt:")
        print("=" * 50)
        print(get_research_prompt(topic))