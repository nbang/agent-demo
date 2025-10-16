"""Shared Context Management

Manages shared information and state accessible to all agents in a collaboration.
"""

import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from .exceptions import MultiAgentError
from .logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("shared_context")


@dataclass
class ContextUpdate:
    """Record of a context update."""
    
    timestamp: float
    updated_by: str
    key: str
    action: str  # "set", "update", "delete"
    previous_value: Any
    new_value: Any


class SharedContext:
    """Manages shared context for multi-agent collaboration."""
    
    def __init__(self, team_id: str):
        self.team_id = team_id
        self.context_id = f"context_{team_id}_{int(time.time())}"
        self._data: Dict[str, Any] = {}
        self._version = 0
        self._last_updated = time.time()
        self._updated_by: Optional[str] = None
        self._access_log: List[ContextUpdate] = []
        
        logger.info(f"Created shared context {self.context_id} for team {team_id}")
    
    def set(self, key: str, value: Any, updated_by: str) -> None:
        """Set a value in the shared context.
        
        Args:
            key: The key to set
            value: The value to set
            updated_by: ID of the agent making the update
        """
        previous_value = self._data.get(key)
        self._data[key] = value
        self._version += 1
        self._last_updated = time.time()
        self._updated_by = updated_by
        
        # Log the update
        update = ContextUpdate(
            timestamp=self._last_updated,
            updated_by=updated_by,
            key=key,
            action="set",
            previous_value=previous_value,
            new_value=value
        )
        self._access_log.append(update)
        
        logger.debug(f"Context {self.context_id}: {updated_by} set {key}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the shared context.
        
        Args:
            key: The key to get
            default: Default value if key not found
            
        Returns:
            The value or default if not found
        """
        return self._data.get(key, default)
    
    def update(self, key: str, value: Any, updated_by: str) -> None:
        """Update an existing value in the shared context.
        
        Args:
            key: The key to update
            value: The new value
            updated_by: ID of the agent making the update
            
        Raises:
            MultiAgentError: If key doesn't exist
        """
        if key not in self._data:
            raise MultiAgentError(f"Key {key} not found in shared context")
        
        previous_value = self._data[key]
        self._data[key] = value
        self._version += 1
        self._last_updated = time.time()
        self._updated_by = updated_by
        
        # Log the update
        update = ContextUpdate(
            timestamp=self._last_updated,
            updated_by=updated_by,
            key=key,
            action="update",
            previous_value=previous_value,
            new_value=value
        )
        self._access_log.append(update)
        
        logger.debug(f"Context {self.context_id}: {updated_by} updated {key}")
    
    def delete(self, key: str, updated_by: str) -> Any:
        """Delete a value from the shared context.
        
        Args:
            key: The key to delete
            updated_by: ID of the agent making the update
            
        Returns:
            The deleted value
            
        Raises:
            MultiAgentError: If key doesn't exist
        """
        if key not in self._data:
            raise MultiAgentError(f"Key {key} not found in shared context")
        
        previous_value = self._data.pop(key)
        self._version += 1
        self._last_updated = time.time()
        self._updated_by = updated_by
        
        # Log the update
        update = ContextUpdate(
            timestamp=self._last_updated,
            updated_by=updated_by,
            key=key,
            action="delete",
            previous_value=previous_value,
            new_value=None
        )
        self._access_log.append(update)
        
        logger.debug(f"Context {self.context_id}: {updated_by} deleted {key}")
        return previous_value
    
    def has(self, key: str) -> bool:
        """Check if a key exists in the shared context.
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists, False otherwise
        """
        return key in self._data
    
    def keys(self) -> List[str]:
        """Get all keys in the shared context.
        
        Returns:
            List of all keys
        """
        return list(self._data.keys())
    
    def items(self) -> Dict[str, Any]:
        """Get all items in the shared context.
        
        Returns:
            Dictionary of all key-value pairs
        """
        return self._data.copy()
    
    def clear(self, updated_by: str) -> None:
        """Clear all data from the shared context.
        
        Args:
            updated_by: ID of the agent clearing the context
        """
        previous_data = self._data.copy()
        self._data.clear()
        self._version += 1
        self._last_updated = time.time()
        self._updated_by = updated_by
        
        # Log the clear operation
        update = ContextUpdate(
            timestamp=self._last_updated,
            updated_by=updated_by,
            key="*",
            action="clear",
            previous_value=previous_data,
            new_value={}
        )
        self._access_log.append(update)
        
        logger.info(f"Context {self.context_id}: {updated_by} cleared all data")
    
    def get_version(self) -> int:
        """Get the current version of the context.
        
        Returns:
            Current version number
        """
        return self._version
    
    def get_last_updated(self) -> float:
        """Get timestamp of last update.
        
        Returns:
            Timestamp of last update
        """
        return self._last_updated
    
    def get_updated_by(self) -> Optional[str]:
        """Get ID of agent that made the last update.
        
        Returns:
            Agent ID or None if no updates yet
        """
        return self._updated_by
    
    def get_access_log(self) -> List[ContextUpdate]:
        """Get the access log.
        
        Returns:
            List of all context updates
        """
        return self._access_log.copy()
    
    def export_data(self) -> Dict[str, Any]:
        """Export context data for persistence or sharing.
        
        Returns:
            Dictionary containing all context data and metadata
        """
        return {
            "context_id": self.context_id,
            "team_id": self.team_id,
            "data": self._data.copy(),
            "version": self._version,
            "last_updated": self._last_updated,
            "updated_by": self._updated_by,
            "access_log": [asdict(update) for update in self._access_log]
        }
    
    def import_data(self, data: Dict[str, Any]) -> None:
        """Import context data from exported format.
        
        Args:
            data: Dictionary containing context data and metadata
        """
        self.context_id = data.get("context_id", self.context_id)
        self.team_id = data.get("team_id", self.team_id)
        self._data = data.get("data", {})
        self._version = data.get("version", 0)
        self._last_updated = data.get("last_updated", time.time())
        self._updated_by = data.get("updated_by")
        
        # Import access log
        access_log_data = data.get("access_log", [])
        self._access_log = [
            ContextUpdate(**update_data) for update_data in access_log_data
        ]
        
        logger.info(f"Imported context data for {self.context_id}")
    
    def to_json(self) -> str:
        """Convert context to JSON string.
        
        Returns:
            JSON representation of the context
        """
        return json.dumps(self.export_data(), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SharedContext':
        """Create SharedContext from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            SharedContext instance
        """
        data = json.loads(json_str)
        team_id = data.get("team_id", "unknown")
        context = cls(team_id)
        context.import_data(data)
        return context
    
    def __str__(self) -> str:
        """String representation of the context."""
        return f"SharedContext(id={self.context_id}, team={self.team_id}, version={self._version}, keys={len(self._data)})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"SharedContext(context_id='{self.context_id}', team_id='{self.team_id}', data={self._data}, version={self._version})"