# Workflow Orchestration API Contract

**Functional Requirement**: Workflow management and task coordination  
**Contract Type**: Workflow Orchestration API  
**Version**: 1.0

## Contract Overview

This contract defines the API for orchestrating workflows, managing task assignments, and coordinating the sequence of activities within multi-agent collaborations.

## API Operations

### CREATE_WORKFLOW

**Purpose**: Define a new workflow template for multi-agent collaboration

**Input Specification**:
```python
{
    "workflow_name": str,       # Human-readable workflow name
    "workflow_type": str,       # "sequential" | "parallel" | "hybrid"
    "description": str,         # Workflow purpose and objectives
    "steps": [
        {
            "step_id": str,     # Unique step identifier
            "step_name": str,   # Human-readable step name
            "step_type": str,   # "task" | "decision" | "synchronization" | "review"
            "required_role": str, # Agent role required for this step
            "estimated_duration": int, # Minutes
            "dependencies": [str], # Step IDs that must complete first
            "success_criteria": str, # How to determine step completion
            "failure_handling": str  # What to do if step fails
        }
    ],
    "quality_gates": [
        {
            "gate_id": str,
            "gate_type": str,   # "approval" | "quality_check" | "milestone"
            "criteria": str,    # Gate passing criteria
            "required_score": float # Minimum score to pass (0.0-1.0)
        }
    ]
}
```

**Output Specification**:
```python
{
    "success": bool,
    "workflow_id": str,         # Unique workflow template ID
    "validation_status": {
        "is_valid": bool,
        "warnings": [str],      # Non-critical issues
        "errors": [str]         # Critical issues preventing use
    },
    "estimated_total_duration": int, # Total estimated minutes
    "error": str | None
}
```

**Validation Rules**:

- Workflow must have at least one step
- All step dependencies must reference valid steps
- No circular dependencies allowed
- Each step must specify required role and success criteria

### EXECUTE_WORKFLOW

**Purpose**: Start executing a workflow with a specific team

**Input Specification**:
```python
{
    "workflow_id": str,         # Workflow template to execute
    "team_id": str,             # Team that will execute the workflow
    "input_parameters": dict,   # Initial parameters and context
    "execution_config": {
        "max_iterations": int,  # Maximum workflow execution attempts
        "timeout_minutes": int, # Overall execution timeout
        "auto_retry": bool,     # Whether to auto-retry failed steps
        "quality_enforcement": str # "strict" | "lenient" | "advisory"
    },
    "notifications": {
        "milestone_alerts": bool,
        "error_alerts": bool,
        "completion_alerts": bool
    }
}
```

**Output Specification**:
```python
{
    "success": bool,
    "execution_id": str,        # Unique execution instance ID
    "initial_assignments": [    # First round of task assignments
        {
            "agent_id": str,
            "step_id": str,
            "task_description": str,
            "estimated_start": str, # ISO timestamp
            "deadline": str         # ISO timestamp
        }
    ],
    "workflow_status": str,     # "starting" | "executing" | "waiting"
    "next_milestone": {
        "milestone_name": str,
        "estimated_completion": str
    },
    "error": str | None
}
```

**Validation Rules**:

- `workflow_id` must reference valid workflow template
- `team_id` must reference team with required roles
- Team must have all roles required by workflow steps
- Execution config values must be within allowed ranges

### GET_WORKFLOW_STATUS

**Purpose**: Get current status and progress of workflow execution

**Input Specification**:
```python
{
    "execution_id": str,        # Workflow execution instance ID
    "include_details": bool,    # Whether to include step-level details
    "include_metrics": bool     # Whether to include performance metrics
}
```

**Output Specification**:
```python
{
    "success": bool,
    "execution_id": str,
    "workflow_status": str,     # "executing" | "completed" | "failed" | "paused"
    "overall_progress": {
        "completed_steps": int,
        "total_steps": int,
        "completion_percentage": float,
        "current_phase": str
    },
    "active_steps": [           # Currently executing steps
        {
            "step_id": str,
            "step_name": str,
            "assigned_agent": str,
            "status": str,      # "in_progress" | "blocked" | "review_pending"
            "progress_percentage": float,
            "estimated_completion": str
        }
    ],
    "completed_steps": [        # If include_details=true
        {
            "step_id": str,
            "completion_time": str,
            "quality_score": float,
            "agent_feedback": str
        }
    ],
    "performance_metrics": {    # If include_metrics=true
        "total_duration": int,  # Minutes elapsed
        "average_step_duration": float,
        "quality_trend": [float], # Quality scores over time
        "resource_utilization": dict
    },
    "next_steps": [             # Upcoming steps ready to start
        {
            "step_id": str,
            "step_name": str,
            "required_role": str,
            "dependencies_met": bool
        }
    ],
    "error": str | None
}
```

### ASSIGN_TASK

**Purpose**: Assign a specific workflow step to an agent

**Input Specification**:
```python
{
    "execution_id": str,        # Workflow execution instance
    "step_id": str,             # Step to assign
    "agent_id": str,            # Agent to assign step to
    "assignment_config": {
        "priority": str,        # "low" | "normal" | "high" | "critical"
        "deadline": str,        # ISO timestamp (optional override)
        "resources": dict,      # Additional resources for the task
        "context": dict         # Step-specific context
    },
    "override_role_check": bool # Whether to bypass role requirement check
}
```

**Output Specification**:
```python
{
    "success": bool,
    "assignment_id": str,       # Unique task assignment ID
    "agent_notified": bool,     # Whether agent was notified of assignment
    "estimated_start": str,     # When agent is expected to start
    "estimated_completion": str, # When task should be completed
    "dependencies_status": {
        "all_met": bool,
        "pending": [str]        # Step IDs still pending
    },
    "error": str | None
}
```

**Validation Rules**:

- `execution_id` must reference active workflow execution
- `step_id` must be valid step in the workflow
- `agent_id` must be team member with compatible role
- Step dependencies must be satisfied before assignment

### COMPLETE_STEP

**Purpose**: Mark a workflow step as completed and provide results

**Input Specification**:
```python
{
    "execution_id": str,        # Workflow execution instance
    "assignment_id": str,       # Task assignment being completed
    "completion_data": {
        "status": str,          # "completed" | "partial" | "failed"
        "output": str,          # Step output or results
        "quality_self_assessment": float, # Agent's self-assessment (0.0-1.0)
        "duration_minutes": int, # Actual time taken
        "challenges_encountered": str, # Issues faced during execution
        "recommendations": str   # Suggestions for future improvements
    },
    "handoff_data": dict        # Data to pass to dependent steps
}
```

**Output Specification**:
```python
{
    "success": bool,
    "step_completed": bool,     # Whether step was successfully marked complete
    "quality_score": float,     # System-calculated quality score
    "triggers_next_steps": [str], # Step IDs that can now start
    "workflow_impact": {
        "progress_change": float, # Change in overall progress percentage
        "timeline_impact": str,   # "on_track" | "ahead" | "delayed"
        "quality_impact": str     # Impact on overall quality trend
    },
    "next_assignments": [       # Immediate next assignments created
        {
            "agent_id": str,
            "step_id": str,
            "assignment_id": str
        }
    ],
    "error": str | None
}
```

**Validation Rules**:

- `assignment_id` must reference active task assignment
- Completion status must be valid
- Quality self-assessment must be 0.0-1.0
- Output must meet step success criteria

## Workflow Control Operations

### PAUSE_WORKFLOW

**Purpose**: Temporarily pause workflow execution

**Input Specification**:
```python
{
    "execution_id": str,        # Workflow execution to pause
    "pause_reason": str,        # Reason for pausing
    "pause_type": str,          # "graceful" | "immediate"
    "estimated_resume": str     # Expected resume time (optional)
}
```

**Output Specification**:
```python
{
    "success": bool,
    "paused_at": str,           # ISO timestamp when paused
    "active_steps_handled": [   # How active steps were handled
        {
            "step_id": str,
            "action": str       # "completed" | "paused" | "cancelled"
        }
    ],
    "resume_token": str,        # Token needed to resume workflow
    "error": str | None
}
```

### RESUME_WORKFLOW

**Purpose**: Resume a paused workflow execution

**Input Specification**:
```python
{
    "execution_id": str,        # Workflow execution to resume
    "resume_token": str,        # Token from pause operation
    "resume_config": {
        "restart_failed_steps": bool,
        "update_deadlines": bool,    # Whether to adjust deadlines
        "reset_timeout": bool        # Whether to reset execution timeout
    }
}
```

**Output Specification**:
```python
{
    "success": bool,
    "resumed_at": str,          # ISO timestamp when resumed
    "steps_restarted": [str],   # Step IDs that were restarted
    "new_assignments": [        # New assignments created on resume
        {
            "agent_id": str,
            "step_id": str,
            "assignment_id": str
        }
    ],
    "error": str | None
}
```

## Error Handling

**Standard Error Codes**:

- `WORKFLOW_NOT_FOUND`: Referenced workflow does not exist  
- `EXECUTION_NOT_FOUND`: Referenced execution does not exist
- `INVALID_WORKFLOW_DEFINITION`: Workflow definition has errors
- `MISSING_REQUIRED_ROLES`: Team lacks roles needed for workflow
- `STEP_DEPENDENCIES_NOT_MET`: Cannot assign step due to unmet dependencies
- `ASSIGNMENT_NOT_FOUND`: Referenced task assignment does not exist
- `QUALITY_GATE_FAILED`: Step output does not meet quality criteria
- `WORKFLOW_TIMEOUT`: Execution exceeded configured timeout

**Error Response Format**:
```python
{
    "success": false,
    "error_code": str,
    "error_message": str,
    "execution_context": {
        "execution_id": str,
        "current_step": str,
        "affected_agents": [str]
    },
    "recovery_options": [str]   # Suggested recovery actions
}
```

## Contract Compliance

This contract ensures:

1. **Functional Requirement F3**: Workflow orchestration through structured step execution
2. **Functional Requirement F6**: Quality control via quality gates and assessments  
3. **Functional Requirement F8**: Progress tracking through workflow status monitoring
4. **Functional Requirement F9**: Performance monitoring via execution metrics
5. **Functional Requirement F10**: Scalability through configurable workflow patterns

The workflow orchestration API provides comprehensive control over multi-agent collaboration sequences while maintaining flexibility and quality standards.