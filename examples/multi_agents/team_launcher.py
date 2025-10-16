#!/usr/bin/env python3
"""
Unified Multi-Agent Team Launcher

A unified interface to launch and interact with any of the available
multi-agent teams with consistent UI/UX.

Available Teams:
1. Research Team - Collaborative research and analysis
2. Content Creation Team - Content development and refinement
3. Problem-Solving Team - Systematic problem analysis and solutions

Features:
- Interactive team selection
- Consistent input/output formatting
- Session management
- Performance tracking
- Export capabilities
"""

import io
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import team modules
try:
    # Import research team
    sys.path.insert(0, str(Path(__file__).parent))
    from research_team import create_research_team
    
    # Import content team
    from content_creation_team import ContentCreationTeam, ContentRequirements, ContentType
    
    # Import problem-solving team
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
    from agents.multi_agent.problem_solving_integration import (
        create_problem_solving_team,
        ProblemSolvingTeamManager
    )
    
    IMPORTS_OK = True
except ImportError as e:
    print(f"⚠️  Warning: Some team modules could not be imported: {e}")
    print("   Some features may not be available.")
    IMPORTS_OK = False


class TeamChoice(Enum):
    """Available team types."""
    RESEARCH = "research"
    CONTENT = "content"
    PROBLEM_SOLVING = "problem_solving"
    EXIT = "exit"


@dataclass
class SessionConfig:
    """Configuration for a launcher session."""
    
    save_results: bool = True
    export_format: str = "json"  # json, markdown, text
    output_dir: Path = Path("./output")
    show_timing: bool = True
    verbose: bool = False
    

@dataclass
class SessionResult:
    """Results from a team execution session."""
    
    team_type: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    input_params: Dict[str, Any]
    output_data: Any
    success: bool
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "team_type": self.team_type,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": self.duration_seconds,
            "input_params": self.input_params,
            "output_data": str(self.output_data),
            "success": self.success,
            "error_message": self.error_message
        }


class UnifiedTeamLauncher:
    """Unified launcher for all multi-agent teams."""
    
    def __init__(self, config: Optional[SessionConfig] = None):
        """Initialize the launcher.
        
        Args:
            config: Session configuration (uses defaults if not provided)
        """
        self.config = config or SessionConfig()
        self.session_history: List[SessionResult] = []
        
        # Ensure output directory exists
        if self.config.save_results:
            self.config.output_dir.mkdir(parents=True, exist_ok=True)
    
    def display_banner(self):
        """Display welcome banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           🤖 MULTI-AGENT TEAM LAUNCHER 🤖                        ║
║                                                                  ║
║              Unified Interface for AI Team Collaboration         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def display_menu(self) -> TeamChoice:
        """Display team selection menu and get user choice.
        
        Returns:
            Selected team choice
        """
        menu = """
┌──────────────────────────────────────────────────────────────────┐
│ Available Teams:                                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. 🔍 Research Team                                             │
│     → Collaborative research and comprehensive analysis          │
│     → Web search, academic research, trend analysis              │
│                                                                  │
│  2. ✍️  Content Creation Team                                    │
│     → Professional content development and refinement            │
│     → Writing, editing, review, and publishing workflows         │
│                                                                  │
│  3. 🧩 Problem-Solving Team                                      │
│     → Systematic problem analysis and solution development       │
│     → Multi-perspective analysis, strategy evaluation            │
│                                                                  │
│  4. 🚪 Exit                                                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
"""
        print(menu)
        
        choice_map = {
            "1": TeamChoice.RESEARCH,
            "2": TeamChoice.CONTENT,
            "3": TeamChoice.PROBLEM_SOLVING,
            "4": TeamChoice.EXIT
        }
        
        while True:
            choice = input("\n👉 Select a team (1-4): ").strip()
            if choice in choice_map:
                return choice_map[choice]
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def launch_research_team(self):
        """Launch the research team."""
        print("\n" + "="*70)
        print("🔍 LAUNCHING RESEARCH TEAM")
        print("="*70)
        
        # Get research topic
        topic = input("\n📝 Enter research topic: ").strip()
        if not topic:
            print("❌ No topic provided. Returning to menu.")
            return
        
        print(f"\n⏳ Researching: {topic}")
        print("\n" + "-"*70)
        
        # Execute research
        start_time = datetime.now()
        try:
            # Create research team
            team = create_research_team()
            
            # Show team info
            print("\n📊 Research Team Assembled:")
            print(f"   ✅ Team created with {len(team.members)} agents")
            for agent in team.members:
                print(f"      • {agent.name}: {agent.role}")
            
            # Execute actual research
            print(f"\n🚀 Executing research workflow...")
            print("-" * 70)
            research_prompt = f"""Conduct comprehensive research on: {topic}
            
Please provide:
1. Key findings and insights
2. Different perspectives on the topic
3. Supporting data and evidence
4. Practical implications

Coordinate among the research team to provide a thorough analysis."""
            
            team.print_response(
                input=research_prompt,
                stream=True
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Record session
            result = SessionResult(
                team_type="research",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                input_params={"topic": topic},
                output_data={"status": "execution_complete", "team_size": len(team.members)},
                success=True
            )
            self.session_history.append(result)
            
            if self.config.show_timing:
                print(f"\n⏱️  Duration: {duration:.2f} seconds")
            
            # Save results
            if self.config.save_results:
                self._save_session_result(result)
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"\n❌ Error: {str(e)}")
            
            result = SessionResult(
                team_type="research",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                input_params={"topic": topic},
                output_data=None,
                success=False,
                error_message=str(e)
            )
            self.session_history.append(result)
    
    def launch_content_team(self):
        """Launch the content creation team."""
        print("\n" + "="*70)
        print("✍️  LAUNCHING CONTENT CREATION TEAM")
        print("="*70)
        
        # Get content requirements
        print("\n📝 Content Specifications:")
        title = input("   Content title/topic: ").strip()
        if not title:
            print("❌ No title provided. Returning to menu.")
            return
        
        content_type = input("   Content type (article/blog_post/technical/marketing) [article]: ").strip() or "article"
        
        print(f"\n⏳ Creating content: {title}")
        print(f"   Type: {content_type}")
        print("\n" + "-"*70)
        
        # Execute content creation
        start_time = datetime.now()
        try:
            # Create content requirements
            requirements = ContentRequirements(
                topic=title,
                content_type=ContentType(content_type.lower()) if content_type.lower() in [t.value for t in ContentType] else ContentType.ARTICLE,
                target_audience="General audience",
                word_count_range=(800, 1200),
                tone="professional"
            )
            
            # Create content team
            team = ContentCreationTeam(requirements)
            
            # Show team info
            print("\n✍️ Content Creation Team Assembled:")
            print(f"   ✅ Team created with {team.team_size} specialized agents")
            print(f"   ✅ Topic: {title}")
            print(f"   ✅ Type: {content_type}")
            
            # Execute actual content creation
            print(f"\n🚀 Executing content creation workflow...")
            print("-" * 70)
            result_content = team.create_content()
            
            if result_content and result_content.success:
                print("\n✅ Content Created Successfully!")
                print(f"   📄 Length: {len(result_content.content)} characters")
                if result_content.quality_metrics:
                    avg_quality = sum(result_content.quality_metrics.values()) / len(result_content.quality_metrics)
                    print(f"   ⭐ Average Quality Score: {avg_quality:.2f}")
            else:
                error_msg = result_content.error if result_content else "Unknown error"
                print(f"\n⚠️  Content creation failed: {error_msg}")
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Record session
            result = SessionResult(
                team_type="content",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                input_params={"title": title, "type": content_type},
                output_data={
                    "status": "execution_complete" if result_content and result_content.success else "failed",
                    "team_size": team.team_size,
                    "content_length": len(result_content.content) if result_content else 0
                },
                success=result_content.success if result_content else False
            )
            self.session_history.append(result)
            
            if self.config.show_timing:
                print(f"\n⏱️  Duration: {duration:.2f} seconds")
            
            # Save results
            if self.config.save_results:
                self._save_session_result(result)
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"\n❌ Error: {str(e)}")
            
            result = SessionResult(
                team_type="content",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                input_params={"title": title, "type": content_type},
                output_data=None,
                success=False,
                error_message=str(e)
            )
            self.session_history.append(result)
    
    def launch_problem_solving_team(self):
        """Launch the problem-solving team."""
        print("\n" + "="*70)
        print("🧩 LAUNCHING PROBLEM-SOLVING TEAM")
        print("="*70)
        
        # Get problem description
        print("\n📝 Problem Definition:")
        problem_id = input("   Problem ID (e.g., PROB-001): ").strip() or f"PROB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        description = input("   Problem description: ").strip()
        
        if not description:
            print("❌ No description provided. Returning to menu.")
            return
        
        context = input("   Additional context (optional): ").strip() or "No additional context provided"
        perspectives = input("   Perspectives to include (technical/business/ux/legal) [technical,business,ux]: ").strip()
        perspectives = perspectives or "technical,business,ux"
        
        print(f"\n⏳ Analyzing problem: {problem_id}")
        print(f"   Description: {description[:50]}...")
        print(f"   Perspectives: {perspectives}")
        print("\n" + "-"*70)
        
        # Execute problem-solving
        start_time = datetime.now()
        try:
            # Create and run problem-solving team
            manager = ProblemSolvingTeamManager()
            team_result = manager.create_team()
            
            # Execute actual problem-solving workflow
            print("\n� Executing problem-solving workflow...")
            print("-" * 70)
            
            solution = team_result.solve_problem(
                problem=description,
                context={"additional_context": context, "perspectives": perspectives}
            )
            
            if solution and solution.success:
                print("\n✅ Problem Analysis Complete!")
                print(f"   🎯 Strategies Generated: {len(solution.strategies)}")
                print(f"   💡 Key Insights: {len(solution.analysis.key_insights) if hasattr(solution.analysis, 'key_insights') else 'N/A'}")
                print(f"   ⭐ Confidence: {solution.confidence_score:.2%}")
            else:
                error_msg = solution.error if solution else "Unknown error"
                print(f"\n⚠️  Problem-solving failed: {error_msg}")
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Record session
            result = SessionResult(
                team_type="problem_solving",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                input_params={
                    "problem_id": problem_id,
                    "description": description,
                    "context": context,
                    "perspectives": perspectives
                },
                output_data={
                    "status": "execution_complete" if solution and solution.success else "failed",
                    "strategies_count": len(solution.strategies) if solution else 0,
                    "confidence": solution.confidence_score if solution else 0
                },
                success=solution.success if solution else False
            )
            self.session_history.append(result)
            
            if self.config.show_timing:
                print(f"\n⏱️  Duration: {duration:.2f} seconds")
            
            # Save results
            if self.config.save_results:
                self._save_session_result(result)
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"\n❌ Error: {str(e)}")
            
            result = SessionResult(
                team_type="problem_solving",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                input_params={
                    "problem_id": problem_id,
                    "description": description,
                    "context": context,
                    "perspectives": perspectives
                },
                output_data=None,
                success=False,
                error_message=str(e)
            )
            self.session_history.append(result)
    
    def _save_session_result(self, result: SessionResult):
        """Save session result to file.
        
        Args:
            result: Session result to save
        """
        try:
            timestamp = result.start_time.strftime("%Y%m%d_%H%M%S")
            filename = f"{result.team_type}_{timestamp}.{self.config.export_format}"
            filepath = self.config.output_dir / filename
            
            if self.config.export_format == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(result.to_dict(), f, indent=2)
            elif self.config.export_format == "markdown":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {result.team_type.title()} Team Session\n\n")
                    f.write(f"**Start Time:** {result.start_time.isoformat()}\n")
                    f.write(f"**Duration:** {result.duration_seconds:.2f}s\n")
                    f.write(f"**Success:** {result.success}\n\n")
                    f.write(f"## Input Parameters\n\n")
                    for key, value in result.input_params.items():
                        f.write(f"- **{key}:** {value}\n")
                    f.write(f"\n## Output\n\n```\n{result.output_data}\n```\n")
            else:  # text
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"{result.team_type.upper()} TEAM SESSION\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(f"Start: {result.start_time.isoformat()}\n")
                    f.write(f"Duration: {result.duration_seconds:.2f}s\n")
                    f.write(f"Success: {result.success}\n\n")
                    f.write(f"INPUT:\n{result.input_params}\n\n")
                    f.write(f"OUTPUT:\n{result.output_data}\n")
            
            print(f"\n💾 Results saved to: {filepath}")
            
        except Exception as e:
            print(f"\n⚠️  Warning: Could not save results: {str(e)}")
    
    def display_session_summary(self):
        """Display summary of current session."""
        if not self.session_history:
            return
        
        print("\n" + "="*70)
        print("📊 SESSION SUMMARY")
        print("="*70)
        
        total_sessions = len(self.session_history)
        successful = sum(1 for r in self.session_history if r.success)
        failed = total_sessions - successful
        total_time = sum(r.duration_seconds for r in self.session_history)
        
        print(f"\nTotal Sessions: {total_sessions}")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  ⏱️  Total Time: {total_time:.2f}s")
        
        # Team breakdown
        team_counts = {}
        for result in self.session_history:
            team_counts[result.team_type] = team_counts.get(result.team_type, 0) + 1
        
        print("\nTeam Usage:")
        for team, count in team_counts.items():
            print(f"  • {team.title()}: {count} session(s)")
    
    def run(self):
        """Run the unified team launcher."""
        self.display_banner()
        
        print("\n💡 Welcome! This launcher provides unified access to all")
        print("   multi-agent teams with consistent interface and features.\n")
        
        while True:
            choice = self.display_menu()
            
            if choice == TeamChoice.EXIT:
                self.display_session_summary()
                print("\n👋 Thank you for using Multi-Agent Team Launcher!")
                print("   Your session data has been saved to:", self.config.output_dir)
                break
            
            elif choice == TeamChoice.RESEARCH:
                self.launch_research_team()
            
            elif choice == TeamChoice.CONTENT:
                self.launch_content_team()
            
            elif choice == TeamChoice.PROBLEM_SOLVING:
                self.launch_problem_solving_team()
            
            # Pause before returning to menu
            input("\n⏸️  Press Enter to return to main menu...")


def main():
    """Main entry point."""
    # Parse command-line arguments (optional)
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Unified Multi-Agent Team Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Disable automatic saving of results"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Directory for saving results (default: ./output)"
    )
    parser.add_argument(
        "--export-format",
        choices=["json", "markdown", "text"],
        default="json",
        help="Export format for results (default: json)"
    )
    parser.add_argument(
        "--no-timing",
        action="store_true",
        help="Disable timing information display"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Create session configuration
    config = SessionConfig(
        save_results=not args.no_save,
        export_format=args.export_format,
        output_dir=Path(args.output_dir),
        show_timing=not args.no_timing,
        verbose=args.verbose
    )
    
    # Create and run launcher
    launcher = UnifiedTeamLauncher(config)
    launcher.run()


if __name__ == "__main__":
    main()
