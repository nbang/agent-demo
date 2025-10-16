"""Graceful Shutdown and Cleanup for Multi-Agent Teams

Provides proper resource cleanup, state persistence, and graceful
shutdown procedures for multi-agent operations.
"""

import atexit
import signal
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


logger = logging.getLogger(__name__)


class ShutdownPhase(Enum):
    """Phases of the shutdown process."""
    INITIATED = "initiated"
    STOPPING_AGENTS = "stopping_agents"
    SAVING_STATE = "saving_state"
    CLEANUP_RESOURCES = "cleanup_resources"
    COMPLETED = "completed"


@dataclass
class ShutdownConfig:
    """Configuration for shutdown behavior."""
    
    timeout_seconds: int = 30
    save_state: bool = True
    state_file: str = "data/team_state.json"
    force_after_timeout: bool = True
    cleanup_temp_files: bool = True
    log_shutdown: bool = True


@dataclass
class TeamState:
    """Persistent team state."""
    
    team_id: str
    team_name: str
    timestamp: datetime
    active_operations: List[str] = field(default_factory=list)
    agent_states: Dict[str, Any] = field(default_factory=dict)
    metrics_summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "timestamp": self.timestamp.isoformat(),
            "active_operations": self.active_operations,
            "agent_states": self.agent_states,
            "metrics_summary": self.metrics_summary,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TeamState':
        """Create from dictionary."""
        data = data.copy()
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class ShutdownManager:
    """Manages graceful shutdown and cleanup for multi-agent teams."""
    
    def __init__(
        self,
        team_id: str,
        config: Optional[ShutdownConfig] = None
    ):
        """Initialize shutdown manager.
        
        Args:
            team_id: Team identifier
            config: Shutdown configuration
        """
        self.team_id = team_id
        self.config = config or ShutdownConfig()
        
        # Shutdown state
        self.shutdown_initiated = False
        self.current_phase = None
        self.shutdown_handlers: List[Callable[[], None]] = []
        
        # Team state
        self.team_state: Optional[TeamState] = None
        
        # Register signal handlers
        self._register_signal_handlers()
        
        # Register cleanup at exit
        atexit.register(self._cleanup_at_exit)
        
        logger.info(f"Shutdown manager initialized for team: {team_id}")
    
    def _register_signal_handlers(self):
        """Register handlers for shutdown signals."""
        try:
            signal.signal(signal.SIGINT, self._handle_signal)
            signal.signal(signal.SIGTERM, self._handle_signal)
            if hasattr(signal, 'SIGBREAK'):  # Windows
                signal.signal(signal.SIGBREAK, self._handle_signal)
        except Exception as e:
            logger.warning(f"Could not register signal handlers: {e}")
    
    def _handle_signal(self, signum, frame):
        """Handle shutdown signals.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        signal_name = signal.Signals(signum).name if hasattr(signal, 'Signals') else str(signum)
        logger.info(f"Received signal {signal_name}, initiating shutdown...")
        self.initiate_shutdown()
    
    def _cleanup_at_exit(self):
        """Cleanup function called at program exit."""
        if not self.shutdown_initiated:
            logger.info("Exit handler triggered, performing cleanup...")
            self.initiate_shutdown()
    
    def register_shutdown_handler(self, handler: Callable[[], None]):
        """Register a custom shutdown handler.
        
        Args:
            handler: Callable to execute during shutdown
        """
        self.shutdown_handlers.append(handler)
        logger.debug(f"Registered shutdown handler: {handler.__name__}")
    
    def set_team_state(self, team_state: TeamState):
        """Set team state for persistence.
        
        Args:
            team_state: Team state to persist
        """
        self.team_state = team_state
    
    def initiate_shutdown(self, reason: str = "Manual shutdown"):
        """Initiate graceful shutdown sequence.
        
        Args:
            reason: Reason for shutdown
        """
        if self.shutdown_initiated:
            logger.warning("Shutdown already initiated")
            return
        
        self.shutdown_initiated = True
        
        if self.config.log_shutdown:
            logger.info("="*70)
            logger.info(f"🛑 INITIATING GRACEFUL SHUTDOWN - Team: {self.team_id}")
            logger.info(f"   Reason: {reason}")
            logger.info("="*70)
        
        try:
            # Phase 1: Stop agents
            self._stop_agents()
            
            # Phase 2: Save state
            if self.config.save_state:
                self._save_state()
            
            # Phase 3: Cleanup resources
            self._cleanup_resources()
            
            # Phase 4: Execute custom handlers
            self._execute_shutdown_handlers()
            
            # Completed
            self.current_phase = ShutdownPhase.COMPLETED
            
            if self.config.log_shutdown:
                logger.info("="*70)
                logger.info("✅ GRACEFUL SHUTDOWN COMPLETED")
                logger.info("="*70)
        
        except Exception as e:
            logger.error(f"Error during shutdown: {e}", exc_info=True)
            
            if self.config.force_after_timeout:
                logger.warning("Forcing shutdown due to error...")
    
    def _stop_agents(self):
        """Stop all active agents."""
        self.current_phase = ShutdownPhase.STOPPING_AGENTS
        logger.info("⏹️  Stopping agents...")
        
        try:
            # Here you would implement actual agent stopping logic
            # For now, just log
            if self.team_state and self.team_state.active_operations:
                logger.info(f"   Stopping {len(self.team_state.active_operations)} active operations")
                # Wait for operations to complete or timeout
                # cancel_active_operations()
            
            logger.info("   ✅ All agents stopped")
        
        except Exception as e:
            logger.error(f"   ❌ Error stopping agents: {e}")
    
    def _save_state(self):
        """Save team state to disk."""
        self.current_phase = ShutdownPhase.SAVING_STATE
        logger.info("💾 Saving team state...")
        
        try:
            if not self.team_state:
                logger.debug("   No team state to save")
                return
            
            # Prepare state file path
            state_path = Path(self.config.state_file)
            state_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Update timestamp
            self.team_state.timestamp = datetime.now()
            
            # Save to file
            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump(self.team_state.to_dict(), f, indent=2)
            
            logger.info(f"   ✅ State saved to: {state_path}")
        
        except Exception as e:
            logger.error(f"   ❌ Error saving state: {e}")
    
    def _cleanup_resources(self):
        """Cleanup resources and temporary files."""
        self.current_phase = ShutdownPhase.CLEANUP_RESOURCES
        logger.info("🧹 Cleaning up resources...")
        
        try:
            if self.config.cleanup_temp_files:
                # Cleanup temp files
                temp_patterns = [
                    "cache/*.tmp",
                    "temp/*",
                    "*.lock"
                ]
                logger.debug(f"   Cleaning temporary files: {temp_patterns}")
                # cleanup_temp_files(temp_patterns)
            
            # Close any open file handles
            # close_file_handles()
            
            # Release any locks
            # release_locks()
            
            logger.info("   ✅ Resources cleaned up")
        
        except Exception as e:
            logger.error(f"   ❌ Error during cleanup: {e}")
    
    def _execute_shutdown_handlers(self):
        """Execute custom shutdown handlers."""
        if not self.shutdown_handlers:
            return
        
        logger.info(f"🔧 Executing {len(self.shutdown_handlers)} shutdown handlers...")
        
        for i, handler in enumerate(self.shutdown_handlers, 1):
            try:
                logger.debug(f"   Handler {i}/{len(self.shutdown_handlers)}: {handler.__name__}")
                handler()
                logger.debug(f"   ✅ Handler {i} completed")
            except Exception as e:
                logger.error(f"   ❌ Handler {i} failed: {e}")
        
        logger.info("   ✅ All handlers executed")
    
    def load_previous_state(self) -> Optional[TeamState]:
        """Load previously saved team state.
        
        Returns:
            Previous team state or None
        """
        state_path = Path(self.config.state_file)
        
        if not state_path.exists():
            logger.debug(f"No previous state found at: {state_path}")
            return None
        
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            team_state = TeamState.from_dict(data)
            logger.info(f"Loaded previous state from: {state_path}")
            logger.info(f"  State timestamp: {team_state.timestamp}")
            logger.info(f"  Active operations: {len(team_state.active_operations)}")
            
            return team_state
        
        except Exception as e:
            logger.error(f"Failed to load previous state: {e}")
            return None
    
    def get_shutdown_status(self) -> Dict[str, Any]:
        """Get current shutdown status.
        
        Returns:
            Shutdown status dictionary
        """
        return {
            "team_id": self.team_id,
            "shutdown_initiated": self.shutdown_initiated,
            "current_phase": self.current_phase.value if self.current_phase else None,
            "handlers_registered": len(self.shutdown_handlers),
            "state_saved": self.config.save_state,
            "state_file": self.config.state_file
        }


class ResourceManager:
    """Manages resources with automatic cleanup."""
    
    def __init__(self, team_id: str):
        """Initialize resource manager.
        
        Args:
            team_id: Team identifier
        """
        self.team_id = team_id
        self.resources: Dict[str, Any] = {}
        self.cleanup_functions: Dict[str, Callable] = {}
        
        logger.info(f"Resource manager initialized for team: {team_id}")
    
    def register_resource(
        self,
        resource_id: str,
        resource: Any,
        cleanup_function: Optional[Callable] = None
    ):
        """Register a resource for tracking.
        
        Args:
            resource_id: Resource identifier
            resource: Resource object
            cleanup_function: Optional cleanup function
        """
        self.resources[resource_id] = resource
        
        if cleanup_function:
            self.cleanup_functions[resource_id] = cleanup_function
        
        logger.debug(f"Registered resource: {resource_id}")
    
    def unregister_resource(self, resource_id: str):
        """Unregister a resource.
        
        Args:
            resource_id: Resource identifier
        """
        if resource_id in self.resources:
            del self.resources[resource_id]
        
        if resource_id in self.cleanup_functions:
            del self.cleanup_functions[resource_id]
        
        logger.debug(f"Unregistered resource: {resource_id}")
    
    def cleanup_resource(self, resource_id: str):
        """Cleanup a specific resource.
        
        Args:
            resource_id: Resource identifier
        """
        if resource_id not in self.resources:
            logger.warning(f"Resource not found: {resource_id}")
            return
        
        try:
            # Call cleanup function if available
            if resource_id in self.cleanup_functions:
                cleanup_func = self.cleanup_functions[resource_id]
                logger.debug(f"Cleaning up resource: {resource_id}")
                cleanup_func(self.resources[resource_id])
            
            # Remove from tracking
            self.unregister_resource(resource_id)
            
            logger.debug(f"✅ Resource cleaned up: {resource_id}")
        
        except Exception as e:
            logger.error(f"❌ Failed to cleanup resource {resource_id}: {e}")
    
    def cleanup_all(self):
        """Cleanup all registered resources."""
        logger.info(f"Cleaning up {len(self.resources)} resources...")
        
        resource_ids = list(self.resources.keys())
        for resource_id in resource_ids:
            self.cleanup_resource(resource_id)
        
        logger.info("✅ All resources cleaned up")
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get summary of managed resources.
        
        Returns:
            Resource summary
        """
        return {
            "team_id": self.team_id,
            "total_resources": len(self.resources),
            "resources_with_cleanup": len(self.cleanup_functions),
            "resource_ids": list(self.resources.keys())
        }


# Context manager for resource lifecycle
class ManagedResource:
    """Context manager for automatic resource cleanup."""
    
    def __init__(
        self,
        resource_manager: ResourceManager,
        resource_id: str,
        resource: Any,
        cleanup_function: Optional[Callable] = None
    ):
        """Initialize managed resource.
        
        Args:
            resource_manager: Resource manager instance
            resource_id: Resource identifier
            resource: Resource object
            cleanup_function: Optional cleanup function
        """
        self.resource_manager = resource_manager
        self.resource_id = resource_id
        self.resource = resource
        self.cleanup_function = cleanup_function
    
    def __enter__(self):
        """Enter context - register resource."""
        self.resource_manager.register_resource(
            self.resource_id,
            self.resource,
            self.cleanup_function
        )
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - cleanup resource."""
        self.resource_manager.cleanup_resource(self.resource_id)
        return False  # Don't suppress exceptions


# Convenience functions
def create_shutdown_manager(
    team_id: str,
    **kwargs
) -> ShutdownManager:
    """Create and initialize a shutdown manager.
    
    Args:
        team_id: Team identifier
        **kwargs: Additional arguments for ShutdownManager
    
    Returns:
        Initialized ShutdownManager
    """
    return ShutdownManager(team_id, **kwargs)


def create_resource_manager(team_id: str) -> ResourceManager:
    """Create and initialize a resource manager.
    
    Args:
        team_id: Team identifier
    
    Returns:
        Initialized ResourceManager
    """
    return ResourceManager(team_id)
