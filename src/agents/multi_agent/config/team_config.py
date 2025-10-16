"""Centralized Configuration Management for Multi-Agent Teams

Provides centralized configuration for teams, agents, and system settings
with validation, defaults, and environment variable support.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


logger = logging.getLogger(__name__)


class ConfigSource(Enum):
    """Source of configuration values."""
    DEFAULT = "default"
    FILE = "file"
    ENVIRONMENT = "environment"
    OVERRIDE = "override"


@dataclass
class ModelConfig:
    """Configuration for AI models."""
    
    provider: str = "openai"  # openai, anthropic, google, etc.
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout_seconds: int = 30
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    
    def __post_init__(self):
        """Load API key from environment if not provided."""
        if not self.api_key:
            env_var = f"{self.provider.upper()}_API_KEY"
            self.api_key = os.getenv(env_var)


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    
    agent_id: str
    agent_name: str
    role: str
    model_config: ModelConfig
    max_iterations: int = 10
    timeout_seconds: int = 300
    enable_memory: bool = True
    enable_tools: bool = True
    verbose: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TeamConfig:
    """Configuration for multi-agent teams."""
    
    team_id: str
    team_name: str
    team_type: str  # research, content, problem_solving
    max_agents: int = 10
    collaboration_timeout: int = 1800  # 30 minutes
    enable_monitoring: bool = True
    enable_metrics: bool = True
    enable_error_handling: bool = True
    quality_threshold: float = 0.7
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringConfig:
    """Configuration for performance monitoring."""
    
    enable_memory_tracking: bool = True
    enable_api_tracking: bool = True
    enable_timing: bool = True
    snapshot_interval_seconds: float = 5.0
    max_history_size: int = 1000
    log_level: str = "INFO"


@dataclass
class ErrorHandlingConfig:
    """Configuration for error handling."""
    
    max_retries: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    exponential_backoff: bool = True
    backoff_factor: float = 2.0
    enable_fallbacks: bool = True
    enable_logging: bool = True


@dataclass
class MetricsConfig:
    """Configuration for collaboration metrics."""
    
    enable_interaction_tracking: bool = True
    enable_pattern_detection: bool = True
    enable_network_analysis: bool = True
    track_response_times: bool = True
    export_network_graph: bool = False


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    
    log_level: str = "INFO"
    log_to_file: bool = True
    log_file_path: str = "logs/multi_agent.log"
    log_to_console: bool = True
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    max_file_size_mb: int = 10
    backup_count: int = 5


@dataclass
class SystemConfig:
    """Overall system configuration."""
    
    # Core settings
    environment: str = "development"  # development, staging, production
    debug: bool = False
    
    # Component configurations
    default_model_config: ModelConfig = field(default_factory=ModelConfig)
    monitoring_config: MonitoringConfig = field(default_factory=MonitoringConfig)
    error_handling_config: ErrorHandlingConfig = field(default_factory=ErrorHandlingConfig)
    metrics_config: MetricsConfig = field(default_factory=MetricsConfig)
    logging_config: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Storage
    data_dir: str = "data"
    cache_dir: str = "cache"
    output_dir: str = "output"
    
    # Performance
    max_concurrent_operations: int = 5
    operation_timeout_seconds: int = 600
    
    # Feature flags
    enable_experimental_features: bool = False


class ConfigurationManager:
    """Manages configuration for multi-agent teams."""
    
    def __init__(
        self,
        config_file: Optional[Union[str, Path]] = None,
        auto_load: bool = True
    ):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file (JSON)
            auto_load: Automatically load configuration on init
        """
        self.config_file = Path(config_file) if config_file else None
        self.system_config = SystemConfig()
        self.team_configs: Dict[str, TeamConfig] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        
        # Track configuration sources
        self.config_sources: Dict[str, ConfigSource] = {}
        
        if auto_load and self.config_file and self.config_file.exists():
            self.load_from_file(self.config_file)
        
        # Load from environment variables
        self.load_from_environment()
        
        logger.info("Configuration manager initialized")
    
    def load_from_file(self, config_file: Union[str, Path]):
        """Load configuration from JSON file.
        
        Args:
            config_file: Path to configuration file
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            logger.warning(f"Configuration file not found: {config_path}")
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Load system config
            if "system" in config_data:
                self._update_system_config(config_data["system"])
            
            # Load team configs
            if "teams" in config_data:
                for team_data in config_data["teams"]:
                    team_config = self._create_team_config(team_data)
                    self.team_configs[team_config.team_id] = team_config
                    self.config_sources[f"team.{team_config.team_id}"] = ConfigSource.FILE
            
            # Load agent configs
            if "agents" in config_data:
                for agent_data in config_data["agents"]:
                    agent_config = self._create_agent_config(agent_data)
                    self.agent_configs[agent_config.agent_id] = agent_config
                    self.config_sources[f"agent.{agent_config.agent_id}"] = ConfigSource.FILE
            
            logger.info(f"Configuration loaded from: {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_path}: {e}")
    
    def load_from_environment(self):
        """Load configuration from environment variables."""
        # System environment
        if env := os.getenv("MULTI_AGENT_ENVIRONMENT"):
            self.system_config.environment = env
            self.config_sources["system.environment"] = ConfigSource.ENVIRONMENT
        
        if debug := os.getenv("MULTI_AGENT_DEBUG"):
            self.system_config.debug = debug.lower() in ("true", "1", "yes")
            self.config_sources["system.debug"] = ConfigSource.ENVIRONMENT
        
        # Logging level
        if log_level := os.getenv("MULTI_AGENT_LOG_LEVEL"):
            self.system_config.logging_config.log_level = log_level.upper()
            self.config_sources["logging.log_level"] = ConfigSource.ENVIRONMENT
        
        # Model configuration
        if model_provider := os.getenv("MULTI_AGENT_MODEL_PROVIDER"):
            self.system_config.default_model_config.provider = model_provider
            self.config_sources["model.provider"] = ConfigSource.ENVIRONMENT
        
        if model_name := os.getenv("MULTI_AGENT_MODEL_NAME"):
            self.system_config.default_model_config.model_name = model_name
            self.config_sources["model.model_name"] = ConfigSource.ENVIRONMENT
        
        logger.debug("Environment variables loaded")
    
    def _update_system_config(self, config_data: Dict[str, Any]):
        """Update system configuration from dictionary."""
        if "environment" in config_data:
            self.system_config.environment = config_data["environment"]
        
        if "debug" in config_data:
            self.system_config.debug = config_data["debug"]
        
        if "default_model" in config_data:
            model_data = config_data["default_model"]
            self.system_config.default_model_config = ModelConfig(**model_data)
        
        if "monitoring" in config_data:
            mon_data = config_data["monitoring"]
            self.system_config.monitoring_config = MonitoringConfig(**mon_data)
        
        if "error_handling" in config_data:
            err_data = config_data["error_handling"]
            self.system_config.error_handling_config = ErrorHandlingConfig(**err_data)
        
        if "metrics" in config_data:
            met_data = config_data["metrics"]
            self.system_config.metrics_config = MetricsConfig(**met_data)
        
        if "logging" in config_data:
            log_data = config_data["logging"]
            self.system_config.logging_config = LoggingConfig(**log_data)
    
    def _create_team_config(self, team_data: Dict[str, Any]) -> TeamConfig:
        """Create team configuration from dictionary."""
        return TeamConfig(**team_data)
    
    def _create_agent_config(self, agent_data: Dict[str, Any]) -> AgentConfig:
        """Create agent configuration from dictionary."""
        # Handle nested model config
        if "model_config" in agent_data and isinstance(agent_data["model_config"], dict):
            agent_data["model_config"] = ModelConfig(**agent_data["model_config"])
        elif "model_config" not in agent_data:
            # Use default model config
            agent_data["model_config"] = self.system_config.default_model_config
        
        return AgentConfig(**agent_data)
    
    def register_team_config(
        self,
        team_config: TeamConfig,
        source: ConfigSource = ConfigSource.OVERRIDE
    ):
        """Register a team configuration.
        
        Args:
            team_config: Team configuration to register
            source: Source of configuration
        """
        self.team_configs[team_config.team_id] = team_config
        self.config_sources[f"team.{team_config.team_id}"] = source
        logger.debug(f"Registered team config: {team_config.team_id}")
    
    def register_agent_config(
        self,
        agent_config: AgentConfig,
        source: ConfigSource = ConfigSource.OVERRIDE
    ):
        """Register an agent configuration.
        
        Args:
            agent_config: Agent configuration to register
            source: Source of configuration
        """
        self.agent_configs[agent_config.agent_id] = agent_config
        self.config_sources[f"agent.{agent_config.agent_id}"] = source
        logger.debug(f"Registered agent config: {agent_config.agent_id}")
    
    def get_team_config(self, team_id: str) -> Optional[TeamConfig]:
        """Get team configuration by ID.
        
        Args:
            team_id: Team identifier
        
        Returns:
            Team configuration or None
        """
        return self.team_configs.get(team_id)
    
    def get_agent_config(self, agent_id: str) -> Optional[AgentConfig]:
        """Get agent configuration by ID.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            Agent configuration or None
        """
        return self.agent_configs.get(agent_id)
    
    def get_system_config(self) -> SystemConfig:
        """Get system configuration.
        
        Returns:
            System configuration
        """
        return self.system_config
    
    def save_to_file(self, config_file: Union[str, Path]):
        """Save configuration to JSON file.
        
        Args:
            config_file: Path to save configuration
        """
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build configuration dictionary
        config_data = {
            "system": {
                "environment": self.system_config.environment,
                "debug": self.system_config.debug,
                "default_model": asdict(self.system_config.default_model_config),
                "monitoring": asdict(self.system_config.monitoring_config),
                "error_handling": asdict(self.system_config.error_handling_config),
                "metrics": asdict(self.system_config.metrics_config),
                "logging": asdict(self.system_config.logging_config),
                "data_dir": self.system_config.data_dir,
                "cache_dir": self.system_config.cache_dir,
                "output_dir": self.system_config.output_dir
            },
            "teams": [
                asdict(team_config)
                for team_config in self.team_configs.values()
            ],
            "agents": [
                asdict(agent_config)
                for agent_config in self.agent_configs.values()
            ]
        }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Configuration saved to: {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration to {config_path}: {e}")
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate model configuration
        if not self.system_config.default_model_config.api_key:
            errors.append(
                f"API key not configured for provider: "
                f"{self.system_config.default_model_config.provider}"
            )
        
        # Validate directories
        for dir_name in ["data_dir", "cache_dir", "output_dir"]:
            dir_path = getattr(self.system_config, dir_name)
            if not Path(dir_path).exists():
                logger.warning(f"Directory does not exist: {dir_path}")
        
        # Validate team configs
        for team_id, team_config in self.team_configs.items():
            if team_config.max_agents < 1:
                errors.append(f"Team {team_id}: max_agents must be >= 1")
            
            if team_config.quality_threshold < 0 or team_config.quality_threshold > 1:
                errors.append(f"Team {team_id}: quality_threshold must be 0-1")
        
        # Validate agent configs
        for agent_id, agent_config in self.agent_configs.items():
            if agent_config.max_iterations < 1:
                errors.append(f"Agent {agent_id}: max_iterations must be >= 1")
            
            if agent_config.timeout_seconds < 1:
                errors.append(f"Agent {agent_id}: timeout_seconds must be >= 1")
        
        return errors
    
    def print_config_summary(self):
        """Print configuration summary to console."""
        print("\n" + "="*70)
        print("⚙️  CONFIGURATION SUMMARY")
        print("="*70)
        
        print(f"\n🌍 Environment: {self.system_config.environment}")
        print(f"🐛 Debug Mode: {self.system_config.debug}")
        
        print(f"\n🤖 Default Model:")
        print(f"   Provider: {self.system_config.default_model_config.provider}")
        print(f"   Model: {self.system_config.default_model_config.model_name}")
        print(f"   Temperature: {self.system_config.default_model_config.temperature}")
        
        print(f"\n📊 Monitoring: {'Enabled' if self.system_config.monitoring_config.enable_memory_tracking else 'Disabled'}")
        print(f"   Memory Tracking: {self.system_config.monitoring_config.enable_memory_tracking}")
        print(f"   API Tracking: {self.system_config.monitoring_config.enable_api_tracking}")
        print(f"   Timing: {self.system_config.monitoring_config.enable_timing}")
        
        print(f"\n⚠️  Error Handling:")
        print(f"   Max Retries: {self.system_config.error_handling_config.max_retries}")
        print(f"   Exponential Backoff: {self.system_config.error_handling_config.exponential_backoff}")
        print(f"   Fallbacks: {self.system_config.error_handling_config.enable_fallbacks}")
        
        print(f"\n📝 Logging:")
        print(f"   Level: {self.system_config.logging_config.log_level}")
        print(f"   To File: {self.system_config.logging_config.log_to_file}")
        print(f"   File Path: {self.system_config.logging_config.log_file_path}")
        
        if self.team_configs:
            print(f"\n👥 Registered Teams: {len(self.team_configs)}")
            for team_id in list(self.team_configs.keys())[:5]:
                config = self.team_configs[team_id]
                print(f"   • {config.team_name} ({config.team_type})")
        
        if self.agent_configs:
            print(f"\n🤖 Registered Agents: {len(self.agent_configs)}")
            for agent_id in list(self.agent_configs.keys())[:5]:
                config = self.agent_configs[agent_id]
                print(f"   • {config.agent_name} ({config.role})")
        
        # Validation
        errors = self.validate_config()
        if errors:
            print(f"\n❌ Configuration Issues:")
            for error in errors:
                print(f"   • {error}")
        else:
            print(f"\n✅ Configuration Valid")
        
        print("\n" + "="*70)
    
    def create_default_config_file(self, output_path: Union[str, Path]):
        """Create a default configuration file template.
        
        Args:
            output_path: Path to save default configuration
        """
        default_config = {
            "system": {
                "environment": "development",
                "debug": False,
                "default_model": {
                    "provider": "openai",
                    "model_name": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "timeout_seconds": 30
                },
                "monitoring": {
                    "enable_memory_tracking": True,
                    "enable_api_tracking": True,
                    "enable_timing": True,
                    "snapshot_interval_seconds": 5.0
                },
                "error_handling": {
                    "max_retries": 3,
                    "initial_delay_seconds": 1.0,
                    "exponential_backoff": True,
                    "enable_fallbacks": True
                },
                "metrics": {
                    "enable_interaction_tracking": True,
                    "enable_pattern_detection": True,
                    "enable_network_analysis": True
                },
                "logging": {
                    "log_level": "INFO",
                    "log_to_file": True,
                    "log_file_path": "logs/multi_agent.log",
                    "log_to_console": True
                }
            },
            "teams": [
                {
                    "team_id": "research_team_01",
                    "team_name": "Research Team",
                    "team_type": "research",
                    "max_agents": 10,
                    "collaboration_timeout": 1800,
                    "enable_monitoring": True,
                    "quality_threshold": 0.7
                }
            ],
            "agents": [
                {
                    "agent_id": "researcher_01",
                    "agent_name": "Research Agent",
                    "role": "researcher",
                    "max_iterations": 10,
                    "timeout_seconds": 300,
                    "enable_memory": True,
                    "enable_tools": True
                }
            ]
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        logger.info(f"Default configuration template created: {output_path}")
        print(f"✅ Default configuration template created: {output_path}")


# Global configuration manager instance
_global_config_manager: Optional[ConfigurationManager] = None


def get_config_manager(
    config_file: Optional[Union[str, Path]] = None
) -> ConfigurationManager:
    """Get the global configuration manager instance.
    
    Args:
        config_file: Optional configuration file to load
    
    Returns:
        Global ConfigurationManager instance
    """
    global _global_config_manager
    
    if _global_config_manager is None:
        _global_config_manager = ConfigurationManager(config_file)
    
    return _global_config_manager


def reset_config_manager():
    """Reset the global configuration manager."""
    global _global_config_manager
    _global_config_manager = None


# Convenience functions
def get_system_config() -> SystemConfig:
    """Get system configuration."""
    return get_config_manager().get_system_config()


def get_team_config(team_id: str) -> Optional[TeamConfig]:
    """Get team configuration."""
    return get_config_manager().get_team_config(team_id)


def get_agent_config(agent_id: str) -> Optional[AgentConfig]:
    """Get agent configuration."""
    return get_config_manager().get_agent_config(agent_id)
