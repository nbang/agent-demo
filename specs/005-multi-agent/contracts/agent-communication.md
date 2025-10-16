# Agent Communication API Contract

**Functional Requirement**: Agent-to-agent communication and coordination  
**Contract Type**: Inter-Agent Communication API  
**Version**: 1.0

## Contract Overview

This contract defines the API for agents within a team to communicate, share information, and coordinate their activities during collaborative work.

## API Operations

### SEND_MESSAGE

**Purpose**: Send a message from one agent to other team members

**Input Specification**:
```python
{
    "sender_agent_id": str,     # ID of the sending agent
    "recipient_agent_ids": [str], # List of recipient agent IDs (or ["ALL"] for broadcast)
    "message_type": str,        # "information" | "request" | "response" | "coordination"
    "content": {
        "text": str,            # Human-readable message content
        "data": dict,           # Structured data payload (optional)
        "attachments": [dict]   # File or resource attachments (optional)
    },
    "priority": str,            # "low" | "normal" | "high" | "urgent"
    "requires_response": bool,  # Whether message expects a response
    "context_reference": str    # Reference to shared context item (optional)
}
```

**Output Specification**:
```python
{
    "success": bool,
    "message_id": str,          # Unique message identifier
    "timestamp": str,           # ISO timestamp when message was sent
    "delivery_status": {
        "delivered_to": [str],   # Agent IDs that received the message
        "failed_delivery": [str], # Agent IDs that failed to receive message
        "pending_delivery": [str] # Agent IDs with pending delivery
    },
    "error": str | None
}
```

**Validation Rules**:

- `sender_agent_id` must be valid team member
- `recipient_agent_ids` cannot include sender
- `message_type` must be from allowed set
- `content.text` must be 1-2000 characters
- `priority` must be valid priority level

### GET_MESSAGES

**Purpose**: Retrieve messages for a specific agent, with filtering options

**Input Specification**:
```python
{
    "agent_id": str,            # Agent requesting messages
    "filters": {
        "message_types": [str], # Filter by message types (optional)
        "senders": [str],       # Filter by sender agents (optional)
        "priority": str,        # Filter by priority level (optional)
        "unread_only": bool,    # Only unread messages (optional)
        "since_timestamp": str  # Messages after timestamp (optional)
    },
    "limit": int,               # Maximum messages to return (default: 50)
    "sort_order": str           # "newest_first" | "oldest_first"
}
```

**Output Specification**:
```python
{
    "success": bool,
    "messages": [
        {
            "message_id": str,
            "sender_agent_id": str,
            "sender_role": str,
            "message_type": str,
            "content": {
                "text": str,
                "data": dict,
                "attachments": [dict]
            },
            "priority": str,
            "timestamp": str,
            "read_status": bool,
            "requires_response": bool,
            "response_deadline": str,  # ISO timestamp (if applicable)
            "context_reference": str
        }
    ],
    "total_count": int,         # Total messages matching filter
    "unread_count": int,        # Count of unread messages
    "error": str | None
}
```

**Validation Rules**:

- `agent_id` must be valid team member
- `limit` must be 1-100
- Filter values must be valid for their types
- Sort order must be supported option

### MARK_MESSAGE_READ

**Purpose**: Mark specific messages as read by an agent

**Input Specification**:
```python
{
    "agent_id": str,            # Agent marking messages as read
    "message_ids": [str]        # List of message IDs to mark as read
}
```

**Output Specification**:
```python
{
    "success": bool,
    "marked_read": [str],       # Successfully marked message IDs
    "not_found": [str],         # Message IDs that were not found
    "already_read": [str],      # Message IDs that were already read
    "error": str | None
}
```

**Validation Rules**:

- `agent_id` must be valid team member
- `message_ids` must contain valid message IDs
- Agent can only mark messages intended for them

### RESPOND_TO_MESSAGE

**Purpose**: Send a response to a message that requested a response

**Input Specification**:
```python
{
    "responder_agent_id": str,  # Agent sending the response
    "original_message_id": str, # ID of message being responded to
    "response_content": {
        "text": str,            # Response text
        "data": dict,           # Structured response data (optional)
        "status": str           # "completed" | "partial" | "unable" | "delegated"
    },
    "additional_recipients": [str] # Additional agents to include in response (optional)
}
```

**Output Specification**:
```python
{
    "success": bool,
    "response_message_id": str, # ID of the response message
    "original_message_updated": bool, # Whether original message was updated
    "timestamp": str,           # Response timestamp
    "error": str | None
}
```

**Validation Rules**:

- `responder_agent_id` must be valid recipient of original message
- `original_message_id` must reference message requiring response
- `response_content.text` must be 1-2000 characters
- `response_content.status` must be valid status

## Specialized Communication Patterns

### BROADCAST_UPDATE

**Purpose**: Send important updates to all team members simultaneously

**Input Specification**:
```python
{
    "sender_agent_id": str,     # Agent broadcasting the update
    "update_type": str,         # "progress" | "discovery" | "issue" | "completion"
    "content": {
        "summary": str,         # Brief update summary
        "details": str,         # Detailed update information
        "impact": str,          # Impact on team objectives
        "action_required": bool # Whether team members need to take action
    },
    "urgency": str              # "info" | "attention" | "action_required" | "critical"
}
```

**Output Specification**:
```python
{
    "success": bool,
    "broadcast_id": str,        # Unique broadcast identifier
    "recipients": [str],        # All team member agent IDs
    "timestamp": str,
    "error": str | None
}
```

### REQUEST_ASSISTANCE

**Purpose**: Request help or collaboration from specific team members

**Input Specification**:
```python
{
    "requester_agent_id": str,  # Agent requesting assistance
    "assistance_type": str,     # "expertise" | "resources" | "review" | "collaboration"
    "target_agents": [str],     # Specific agents to request from (optional)
    "required_capabilities": [str], # Capabilities needed for assistance
    "request_details": {
        "description": str,     # What assistance is needed
        "context": str,         # Background context
        "deadline": str,        # When assistance is needed by
        "priority": str         # Request priority level
    }
}
```

**Output Specification**:
```python
{
    "success": bool,
    "request_id": str,          # Unique assistance request ID
    "potential_responders": [   # Agents that might be able to help
        {
            "agent_id": str,
            "role": str,
            "capability_match": float, # 0.0-1.0 capability match score
            "availability": str        # "available" | "busy" | "unavailable"
        }
    ],
    "broadcast_sent": bool,     # Whether request was broadcast to team
    "error": str | None
}
```

## Error Handling

**Standard Error Codes**:

- `AGENT_NOT_FOUND`: Referenced agent does not exist in team
- `MESSAGE_NOT_FOUND`: Referenced message does not exist
- `INVALID_RECIPIENT`: Recipient agent is not valid team member
- `MESSAGE_TOO_LONG`: Message content exceeds length limits
- `RESPONSE_NOT_REQUIRED`: Attempted to respond to message not requiring response
- `RESPONSE_DEADLINE_PASSED`: Response sent after deadline
- `COMMUNICATION_DISABLED`: Agent communication is temporarily disabled

**Error Response Format**:
```python
{
    "success": false,
    "error_code": str,
    "error_message": str,
    "details": dict,
    "suggested_action": str     # Recommended action to resolve error
}
```

## Contract Compliance

This contract ensures:

1. **Functional Requirement F4**: Agent coordination through structured messaging
2. **Functional Requirement F5**: Information sharing via message content and attachments
3. **Functional Requirement F8**: Progress tracking through broadcast updates
4. **Functional Requirement F9**: Performance monitoring via communication metrics

The communication API integrates seamlessly with the Agno Team framework while providing rich inter-agent coordination capabilities.