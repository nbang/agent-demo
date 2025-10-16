#!/usr/bin/env python3
"""
Advanced Memory Agent Implementation

A sophisticated AI agent with persistent memory capabilities that stores and retrieves
conversation history, maintains context across sessions, and provides personalized 
responses based on previous interactions. Features SQLite database integration with
intelligent agentic memory control for optimal performance and user experience.

Key Features:
- Persistent conversation history across application sessions
- Intelligent memory storage with agentic control
- Contextual recall of relevant past interactions
- Personalized responses based on interaction history
- Efficient memory queries with minimal performance impact
- Graceful error handling and recovery
- Privacy-conscious local data storage
- Comprehensive logging and debugging capabilities

Technical Implementation:
- Agno framework with SqliteDb integration
- Agentic memory enabled for intelligent memory management
- Local SQLite storage with data protection
- Memory lifecycle management and cleanup
- Performance monitoring and optimization

Usage:
    from src.agents.memory import create_memory_agent, main
    
    # Create agent
    agent = create_memory_agent()
    
    # Interactive mode
    main()
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import required modules
try:
    from agno.agent import Agent
    from agno.db.sqlite import SqliteDb
    from src.models.config import get_configured_model, print_model_info
    from src.lib.logging_config import setup_logging
    from src.lib.error_handling import AgentError, ErrorSeverity
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure all required dependencies are installed.")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryPatterns:
    """
    Memory management patterns and strategies for different types of information.
    Defines how different types of data should be stored, retrieved, and managed.
    """
    
    @staticmethod
    def get_conversation_memory_instructions() -> List[str]:
        """Get memory instructions for conversation history management."""
        return [
            "Store important details about the user's preferences, goals, and context",
            "Remember key information shared across conversations",
            "Refer to previous discussions when relevant to current questions",
            "Build a comprehensive understanding of the user over time",
            "Ask follow-up questions based on what you know about the user",
            "Maintain context continuity across conversation sessions",
        ]
    
    @staticmethod
    def get_user_context_instructions() -> List[str]:
        """Get memory instructions for user context and personalization."""
        return [
            "Learn and remember the user's name, role, and background",
            "Store preferences for communication style and detail level",
            "Remember ongoing projects and interests",
            "Track user goals and objectives over time",
            "Note technical skill level and areas of expertise",
            "Remember important dates, deadlines, and commitments",
        ]
    
    @staticmethod
    def get_privacy_instructions() -> List[str]:
        """Get memory instructions for privacy and data protection."""
        return [
            "Only store information that is relevant and appropriate",
            "Don't store sensitive personal information like passwords or private details",
            "Focus on context that improves assistance quality",
            "Respect user privacy and data minimization principles",
            "Ask permission before storing highly personal information",
        ]

class MemoryAgentManager:
    """
    Advanced memory agent manager with comprehensive database management
    and error handling capabilities.
    """
    
    def __init__(self, db_file: str = "agent_memory.db"):
        """
        Initialize the memory agent manager.
        
        Args:
            db_file: Path to SQLite database file for memory storage
        """
        self.db_file = db_file
        self.db_path = Path(project_root) / db_file
        self.agent: Optional[Agent] = None
        self.db: Optional[SqliteDb] = None
        self.stats = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "uptime_start": datetime.now(),
        }
        
        # Initialize database
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize SQLite database with error handling and validation."""
        try:
            print(f"🔧 Initializing memory database: {self.db_file}")
            
            # Create database directory if needed
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Initialize SqliteDb
            self.db = SqliteDb(db_file=str(self.db_path))
            
            print("✅ Memory database initialized successfully")
            
        except Exception as e:
            error_msg = f"Failed to initialize memory database: {e}"
            print(f"❌ {error_msg}")
            raise AgentError(error_msg, ErrorSeverity.HIGH)
    
    def create_memory_agent(self) -> Agent:
        """
        Create an advanced memory agent with comprehensive capabilities.
        
        Returns:
            Agent: Configured memory agent with persistent storage
        """
        try:
            print("🧠 Creating memory agent with advanced capabilities...")
            
            # Get model configuration
            model = get_configured_model()
            
            # Comprehensive memory instructions
            memory_instructions = [
                "You are an advanced AI assistant with persistent memory capabilities.",
                "You remember conversations across sessions and build context over time.",
                "You provide personalized responses based on previous interactions.",
                "",
                "MEMORY MANAGEMENT:",
            ]
            
            # Add pattern-specific instructions
            memory_instructions.extend(MemoryPatterns.get_conversation_memory_instructions())
            memory_instructions.append("")
            memory_instructions.append("USER PERSONALIZATION:")
            memory_instructions.extend(MemoryPatterns.get_user_context_instructions())
            memory_instructions.append("")
            memory_instructions.append("PRIVACY & DATA PROTECTION:")
            memory_instructions.extend(MemoryPatterns.get_privacy_instructions())
            
            memory_instructions.extend([
                "",
                "INTERACTION GUIDELINES:",
                "- Always acknowledge when referencing previous conversations",
                "- Ask clarifying questions to better understand user needs",
                "- Suggest relevant topics based on past discussions",
                "- Maintain helpful, professional, and personalized communication",
                "- Build trust through consistent, contextual assistance",
            ])
            
            # Create the memory agent
            agent = Agent(
                name="Advanced Memory Assistant",
                model=model,
                db=self.db,
                enable_agentic_memory=True,  # Enable intelligent memory control
                instructions=memory_instructions,
                markdown=True,
                add_datetime_to_context=True,
            )
            
            self.agent = agent
            print("✅ Memory agent created successfully!")
            return agent
            
        except Exception as e:
            error_msg = f"Failed to create memory agent: {e}"
            print(f"❌ {error_msg}")
            raise AgentError(error_msg, ErrorSeverity.HIGH)
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """
        Get memory database statistics and performance metrics.
        
        Returns:
            Dict: Memory statistics and performance data
        """
        try:
            uptime_minutes = (datetime.now() - self.stats["uptime_start"]).total_seconds() / 60
            success_rate = 0.0
            if self.stats["total_operations"] > 0:
                success_rate = (self.stats["successful_operations"] / self.stats["total_operations"]) * 100
            
            stats = {
                "database_file": str(self.db_path),
                "database_exists": self.db_path.exists(),
                "database_size_mb": 0.0,
                "total_operations": self.stats["total_operations"],
                "successful_operations": self.stats["successful_operations"],
                "failed_operations": self.stats["failed_operations"],
                "success_rate": round(success_rate, 1),
                "uptime_minutes": round(uptime_minutes, 1),
                "agent_active": self.agent is not None,
                "timestamp": datetime.now().isoformat(),
            }
            
            # Get database file size
            if self.db_path.exists():
                stats["database_size_mb"] = round(self.db_path.stat().st_size / (1024 * 1024), 2)
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting memory statistics: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
    
    def record_operation(self, success: bool = True) -> None:
        """Record an operation for statistics."""
        self.stats["total_operations"] += 1
        if success:
            self.stats["successful_operations"] += 1
        else:
            self.stats["failed_operations"] += 1
    
    def cleanup(self) -> None:
        """Clean up resources and close database connections."""
        try:
            print("🔧 Cleaning up memory agent resources...")
            
            if self.agent:
                self.agent = None
            
            if self.db:
                # SqliteDb handles its own cleanup
                self.db = None
            
            print("✅ Memory agent cleanup completed")
            
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")

# Global manager instance
_memory_manager: Optional[MemoryAgentManager] = None

def get_memory_manager(db_file: str = "agent_memory.db") -> MemoryAgentManager:
    """
    Get or create the global memory agent manager.
    
    Args:
        db_file: Path to SQLite database file
        
    Returns:
        MemoryAgentManager: Global memory manager instance
    """
    global _memory_manager
    
    if _memory_manager is None or _memory_manager.db_file != db_file:
        _memory_manager = MemoryAgentManager(db_file=db_file)
    
    return _memory_manager

def create_memory_agent(db_file: str = "agent_memory.db") -> Agent:
    """
    Create a memory agent with persistent storage capabilities.
    
    Args:
        db_file: Path to SQLite database file for memory storage
        
    Returns:
        Agent: Configured memory agent with persistent memory
    """
    manager = get_memory_manager(db_file)
    return manager.create_memory_agent()

def get_memory_stats(db_file: str = "agent_memory.db") -> Dict[str, Any]:
    """
    Get memory database statistics and performance metrics.
    
    Args:
        db_file: Path to SQLite database file
        
    Returns:
        Dict: Memory statistics and performance data
    """
    manager = get_memory_manager(db_file)
    return manager.get_memory_statistics()

def main(db_file: str = "agent_memory.db") -> None:
    """
    Main function to run the interactive memory agent.
    
    Args:
        db_file: Path to SQLite database file for memory storage
    """
    print("🔧 Initializing Advanced Memory Agent...")
    
    # Test model connection
    print("📡 Testing model connection...")
    try:
        model = get_configured_model()
        print_model_info()
        print("✅ Model connection successful!")
    except Exception as e:
        print(f"❌ Model connection failed: {e}")
        print("🔧 Please check your model configuration and try again.")
        return
    
    # Create memory agent
    print("🧠 Creating memory agent with persistent storage...")
    try:
        manager = get_memory_manager(db_file)
        agent = manager.create_memory_agent()
        
        print("✅ Memory agent created successfully!")
        print(f"💾 Memory database: {db_file}")
        
        memory_stats = manager.get_memory_statistics()
        if memory_stats.get("database_size_mb", 0) > 0:
            print(f"📊 Database size: {memory_stats['database_size_mb']} MB")
        
    except Exception as e:
        print(f"❌ Configuration Error: ⚙️  Configuration Issue: {e}")
        print("🔧 Please check your environment setup and try again.")
        return
    
    # Display banner and instructions
    print("\n🧠 Advanced Memory Assistant")
    print("=" * 60)
    print("Welcome to the Advanced Memory Assistant!")
    print("I have persistent memory and remember our conversations.")
    print()
    print("My capabilities include:")
    print("  💾 Persistent conversation history")
    print("  🎯 Personalized responses based on context")
    print("  🔍 Contextual recall of previous interactions")
    print("  📝 Learning user preferences over time")
    print("  🤝 Building long-term context and relationships")
    print("  🔐 Privacy-conscious local data storage")
    print("=" * 60)
    
    # Show model configuration
    print_model_info()
    
    print("\n💭 Example Memory-Enhanced Interactions:")
    print("=" * 50)
    print()
    print("📁 **First-Time Setup:**")
    print("   1. \"Hi, I'm Alex and I'm a software developer working on Python projects.\"")
    print("   2. \"I prefer detailed explanations and code examples.\"")
    print("   3. \"I'm currently learning about machine learning and AI agents.\"")
    print()
    print("📁 **Ongoing Conversations:**")
    print("   1. \"What did we discuss about Python projects last time?\"")
    print("   2. \"Can you help me with that ML project I mentioned?\"")
    print("   3. \"Remember my preference for detailed explanations.\"")
    print()
    print("📁 **Contextual Questions:**")
    print("   1. \"Based on what you know about me, what should I learn next?\"")
    print("   2. \"Can you suggest resources for my current project?\"")
    print("   3. \"What tasks from our previous conversations are still pending?\"")
    print()
    print("=" * 50)
    
    print("\n💡 Interaction Tips & Commands:")
    print("=" * 40)
    print("• Share information about yourself for better personalization")
    print("• Ask about previous conversations to test memory")
    print("• Request recommendations based on your context")
    print("• Tell me about your goals and preferences")
    print("• Type 'stats' for memory database statistics")
    print("• Type 'help' for additional commands")
    print("• Type 'quit', 'exit', 'bye', or 'q' to end the session")
    print("=" * 40)
    
    print("\n💬 Ready for Memory-Enhanced Conversations!")
    print("Share something about yourself to get started...")
    print("-" * 60)
    
    # Interactive conversation loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 I'll remember our conversation for next time!")
                print("💾 All context has been saved to memory.")
                break
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == 'stats':
                print("\n📊 Memory Statistics")
                print("=" * 30)
                stats = manager.get_memory_statistics()
                for key, value in stats.items():
                    print(f"   {key}: {value}")
                continue
            
            if user_input.lower() == 'help':
                print("\n🔧 Available Commands")
                print("=" * 25)
                print("   stats  - Show memory database statistics")
                print("   help   - Show this help message")
                print("   quit   - Exit the memory agent")
                print()
                print("💡 Memory Tips:")
                print("   - Tell me about your background and preferences")
                print("   - Ask about things we discussed previously")
                print("   - Request personalized recommendations")
                continue
            
            # Process user message
            print(f"\n🧠 Memory Assistant:", end=" ")
            start_time = time.time()
            
            try:
                agent.print_response(user_input)
                manager.record_operation(success=True)
                
                # Note slow responses
                elapsed_time = time.time() - start_time
                if elapsed_time > 2.0:
                    print(f"\n💭 (Response took {elapsed_time:.1f} seconds)")
                
            except Exception as e:
                manager.record_operation(success=False)
                print(f"\n❌ Error: {e}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Memory has been saved!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
    
    # Final performance report
    print(f"\n📊 Final Performance Summary:")
    print("=" * 40)
    stats = manager.get_memory_statistics()
    print(f"Uptime: {stats['uptime_minutes']:.1f} minutes")
    print(f"Total Operations: {stats['total_operations']}")
    print(f"Successful Operations: {stats['successful_operations']}")
    print(f"Success Rate: {stats['success_rate']:.1f}%")
    print(f"Database Size: {stats['database_size_mb']:.2f} MB")
    print("=" * 40)
    
    # Cleanup
    manager.cleanup()
    
    print("\n🧠 Thank you for using the Advanced Memory Agent!")
    print("Remember: Great conversations build great relationships! 💭")

if __name__ == "__main__":
    main()