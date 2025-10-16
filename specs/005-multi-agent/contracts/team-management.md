# Multi-Agent Team API Contract

**Functional Requirement**: Team formation and management capabilities  
**Contract Type**: Core Team Management API  
**Version**: 1.0

## Contract Overview

This contract defines the API for creating, managing, and operating multi-agent teams within the Agno framework.

## API Operations

### CREATE_TEAM

**Purpose**: Initialize a new multi-agent team with specified roles and configuration

**Input Specification**:
```python
{
    "team_name": str,           # Human-readable team name
    "team_type": str,           # "research" | "content_creation" | "problem_solving"
    "agent_roles": [            # List of agent role definitions
        {
            "role_name": str,         # "researcher" | "analyst" | "writer" | "editor"
            "agent_config": {
                "model": str,         # OpenAI model specification
                "tools": [str],       # List of tool identifiers
                "instructions": str   # Role-specific instructions
            }
        }
    ],
    "workflow_config": {
        "type": str,            # "sequential" | "parallel" | "hybrid"
        "max_iterations": int,  # Maximum collaboration rounds
        "timeout_minutes": int  # Team operation timeout
    }
}
```

**Output Specification**:
```python
{
    "success": bool,
    "team_id": str,             # Unique team identifier
    "team_status": str,         # "created" | "initializing" | "ready"
    "agents": [                 # List of initialized agents
        {
            "agent_id": str,
            "role": str,
            "status": str       # "ready" | "initializing" | "error"
        }
    ],
    "error": str | None         # Error message if success=false
}
```

**Validation Rules**:
- `team_name` must be 1-100 characters
- `team_type` must be supported collaboration type  
- `agent_roles` must contain 2-5 unique roles
- Each role must have valid `agent_config`
- `workflow_config` must specify valid workflow type

### START_COLLABORATION

**Purpose**: Begin collaborative work on a specific task or objective

**Input Specification**:
```python
{
    "team_id": str,             # Target team identifier
    "task_description": str,    # Detailed task description
    "expected_output": str,     # Description of expected deliverable
    "context": dict,            # Initial shared context
    "constraints": {
        "max_duration_minutes": int,
        "quality_threshold": float,  # 0.0-1.0 quality score requirement
        "resource_limits": dict
    }
}
```

**Output Specification**:
```python
{
    "success": bool,
    "collaboration_id": str,    # Unique collaboration session ID
    "workflow_status": str,     # "started" | "planning" | "executing"
    "estimated_completion": str, # ISO timestamp
    "initial_assignments": [    # Initial task assignments
        {
            "agent_id": str,
            "task": str,
            "priority": int
        }
    ],
    "error": str | None
}
```

**Validation Rules**:
- `team_id` must reference existing, ready team
- `task_description` must be 10-1000 characters
- `expected_output` must be specified
- `constraints.quality_threshold` must be 0.0-1.0
- `constraints.max_duration_minutes` must be positive

### GET_COLLABORATION_STATUS

**Purpose**: Retrieve current status and progress of ongoing collaboration

**Input Specification**:
```python
{
    "collaboration_id": str,    # Collaboration session identifier
    "include_details": bool     # Whether to include detailed progress
}
```

**Output Specification**:
```python
{
    "success": bool,
    "collaboration_id": str,
    "status": str,              # "executing" | "completed" | "failed" | "paused"
    "progress": {
        "completed_tasks": int,
        "total_tasks": int,
        "completion_percentage": float,
        "current_phase": str
    },
    "agents_status": [          # Individual agent status
        {
            "agent_id": str,
            "role": str,
            "current_task": str,
            "status": str       # "working" | "waiting" | "completed" | "blocked"
        }
    ],
    "shared_context": dict,     # Current shared context (if include_details=true)
    "partial_results": dict,    # Intermediate results (if include_details=true)
    "error": str | None
}
```

**Validation Rules**:
- `collaboration_id` must reference existing collaboration
- Status must reflect actual collaboration state
- Progress percentages must be accurate

### STOP_COLLABORATION

**Purpose**: Terminate ongoing collaboration and retrieve final results

**Input Specification**:
```python
{
    "collaboration_id": str,    # Collaboration session identifier
    "force_stop": bool,         # Whether to stop immediately or wait for current tasks
    "save_partial": bool        # Whether to save partial results
}
```

**Output Specification**:
```python
{
    "success": bool,
    "collaboration_id": str,
    "final_status": str,        # "completed" | "terminated" | "failed"
    "results": {
        "output": str,          # Final collaborative output
        "quality_score": float, # Automated quality assessment
        "completion_time": str, # ISO timestamp
        "contributions": [      # Individual agent contributions
            {
                "agent_id": str,
                "role": str,
                "contribution": str,
                "effort_score": float
            }
        ]
    },
    "metrics": {
        "total_duration_minutes": int,
        "messages_exchanged": int,
        "iterations_completed": int
    },
    "error": str | None
}
```

**Validation Rules**:
- `collaboration_id` must reference existing collaboration
- Final results must be complete if status is "completed"
- Quality score must be 0.0-1.0 range
- Metrics must accurately reflect collaboration activity

## Error Handling

**Standard Error Codes**:
- `TEAM_NOT_FOUND`: Referenced team does not exist
- `INVALID_TEAM_CONFIG`: Team configuration violates validation rules
- `AGENT_INITIALIZATION_FAILED`: One or more agents failed to initialize
- `COLLABORATION_IN_PROGRESS`: Team is already engaged in collaboration
- `INSUFFICIENT_RESOURCES`: System resources unavailable for operation
- `TIMEOUT_EXCEEDED`: Operation exceeded specified timeout
- `QUALITY_THRESHOLD_NOT_MET`: Results do not meet quality requirements

**Error Response Format**:
```python
{
    "success": false,
    "error_code": str,          # Standardized error code
    "error_message": str,       # Human-readable error description
    "details": dict,            # Additional error context
    "retry_after": int | None   # Seconds to wait before retry (if applicable)
}
```

## Contract Compliance

This contract ensures:

1. **Functional Requirement F1**: Team formation through CREATE_TEAM operation
2. **Functional Requirement F2**: Role specialization via agent_config parameters
3. **Functional Requirement F3**: Workflow orchestration through START_COLLABORATION
4. **Functional Requirement F4**: Communication coordination (implicit in collaboration flow)
5. **Functional Requirement F6**: Quality control through quality_threshold constraints
6. **Functional Requirement F7**: Result integration in STOP_COLLABORATION output

The API design maintains consistency with Agno framework patterns while providing comprehensive multi-agent collaboration capabilities.