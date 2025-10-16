"""Agent Communication Protocols

Handles message passing and communication between agents in a multi-agent team.
"""

import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from .constants import MessageType, MessagePriority
from .exceptions import CommunicationError
from .logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("communication")


@dataclass
class Message:
    """A message between agents."""
    
    message_id: str
    sender_agent_id: str
    recipient_agent_ids: List[str]
    message_type: MessageType
    content: Dict[str, Any]
    priority: MessagePriority
    requires_response: bool
    timestamp: float
    context_reference: Optional[str] = None
    response_deadline: Optional[float] = None
    
    def __post_init__(self):
        """Validate message after initialization."""
        if not self.content.get("text"):
            raise CommunicationError("Message must have text content")
        
        if len(self.content.get("text", "")) > 2000:
            raise CommunicationError("Message text cannot exceed 2000 characters")


@dataclass
class MessageDelivery:
    """Status of message delivery to recipients."""
    
    message_id: str
    delivered_to: List[str]
    failed_delivery: List[str]
    pending_delivery: List[str]
    timestamp: float


class AgentCommunication:
    """Manages communication between agents in a team."""
    
    def __init__(self, team_id: str):
        self.team_id = team_id
        self._messages: Dict[str, Message] = {}
        self._agent_inboxes: Dict[str, List[str]] = {}  # agent_id -> list of message_ids
        self._message_read_status: Dict[str, Dict[str, bool]] = {}  # message_id -> agent_id -> read
        self._delivery_log: List[MessageDelivery] = []
        
        logger.info(f"Initialized communication system for team {team_id}")
    
    def register_agent(self, agent_id: str) -> None:
        """Register an agent for communication.
        
        Args:
            agent_id: ID of the agent to register
        """
        if agent_id not in self._agent_inboxes:
            self._agent_inboxes[agent_id] = []
            logger.debug(f"Registered agent {agent_id} for communication")
    
    def send_message(
        self,
        sender_agent_id: str,
        recipient_agent_ids: List[str],
        message_type: MessageType,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        requires_response: bool = False,
        context_reference: Optional[str] = None,
        response_deadline_seconds: Optional[int] = None
    ) -> str:
        """Send a message from one agent to others.
        
        Args:
            sender_agent_id: ID of the sending agent
            recipient_agent_ids: List of recipient agent IDs
            message_type: Type of the message
            content: Message content including text and optional data
            priority: Message priority level
            requires_response: Whether message expects a response
            context_reference: Reference to shared context item
            response_deadline_seconds: Deadline for response in seconds
            
        Returns:
            Message ID
            
        Raises:
            CommunicationError: If message sending fails
        """
        # Validate sender is registered
        if sender_agent_id not in self._agent_inboxes:
            raise CommunicationError(f"Sender agent {sender_agent_id} not registered")
        
        # Handle broadcast (ALL recipients)
        if len(recipient_agent_ids) == 1 and recipient_agent_ids[0] == "ALL":
            recipient_agent_ids = [aid for aid in self._agent_inboxes.keys() if aid != sender_agent_id]
        
        # Validate recipients
        for recipient_id in recipient_agent_ids:
            if recipient_id not in self._agent_inboxes:
                raise CommunicationError(f"Recipient agent {recipient_id} not registered")
        
        if sender_agent_id in recipient_agent_ids:
            raise CommunicationError("Sender cannot be in recipient list")
        
        # Create message
        message_id = str(uuid.uuid4())
        current_time = time.time()
        response_deadline = None
        if response_deadline_seconds:
            response_deadline = current_time + response_deadline_seconds
        
        message = Message(
            message_id=message_id,
            sender_agent_id=sender_agent_id,
            recipient_agent_ids=recipient_agent_ids,
            message_type=message_type,
            content=content,
            priority=priority,
            requires_response=requires_response,
            timestamp=current_time,
            context_reference=context_reference,
            response_deadline=response_deadline
        )
        
        # Store message
        self._messages[message_id] = message
        
        # Deliver to recipients
        delivered_to = []
        failed_delivery = []
        pending_delivery = []
        
        for recipient_id in recipient_agent_ids:
            try:
                self._agent_inboxes[recipient_id].append(message_id)
                self._message_read_status.setdefault(message_id, {})[recipient_id] = False
                delivered_to.append(recipient_id)
            except Exception as e:
                logger.error(f"Failed to deliver message {message_id} to {recipient_id}: {e}")
                failed_delivery.append(recipient_id)
        
        # Log delivery
        delivery = MessageDelivery(
            message_id=message_id,
            delivered_to=delivered_to,
            failed_delivery=failed_delivery,
            pending_delivery=pending_delivery,
            timestamp=current_time
        )
        self._delivery_log.append(delivery)
        
        logger.info(f"Message {message_id} sent from {sender_agent_id} to {len(delivered_to)} recipients")
        
        if failed_delivery:
            raise CommunicationError(
                f"Failed to deliver message to {len(failed_delivery)} recipients",
                context={"failed_recipients": failed_delivery}
            )
        
        return message_id
    
    def get_messages(
        self,
        agent_id: str,
        message_types: Optional[List[MessageType]] = None,
        senders: Optional[List[str]] = None,
        priority: Optional[MessagePriority] = None,
        unread_only: bool = False,
        since_timestamp: Optional[float] = None,
        limit: int = 50
    ) -> List[Message]:
        """Get messages for a specific agent with filtering.
        
        Args:
            agent_id: Agent requesting messages
            message_types: Filter by message types
            senders: Filter by sender agents
            priority: Filter by priority level
            unread_only: Only return unread messages
            since_timestamp: Messages after this timestamp
            limit: Maximum messages to return
            
        Returns:
            List of messages matching the filters
        """
        if agent_id not in self._agent_inboxes:
            raise CommunicationError(f"Agent {agent_id} not registered")
        
        message_ids = self._agent_inboxes[agent_id]
        messages = []
        
        for message_id in message_ids:
            message = self._messages.get(message_id)
            if not message:
                continue
            
            # Apply filters
            if message_types and message.message_type not in message_types:
                continue
            
            if senders and message.sender_agent_id not in senders:
                continue
            
            if priority and message.priority != priority:
                continue
            
            if unread_only:
                read_status = self._message_read_status.get(message_id, {})
                if read_status.get(agent_id, False):
                    continue
            
            if since_timestamp and message.timestamp <= since_timestamp:
                continue
            
            messages.append(message)
        
        # Sort by timestamp (newest first) and limit
        messages.sort(key=lambda m: m.timestamp, reverse=True)
        return messages[:limit]
    
    def mark_message_read(self, agent_id: str, message_ids: List[str]) -> Dict[str, List[str]]:
        """Mark messages as read by an agent.
        
        Args:
            agent_id: Agent marking messages as read
            message_ids: List of message IDs to mark as read
            
        Returns:
            Dict with lists of: marked_read, not_found, already_read
        """
        if agent_id not in self._agent_inboxes:
            raise CommunicationError(f"Agent {agent_id} not registered")
        
        marked_read = []
        not_found = []
        already_read = []
        
        for message_id in message_ids:
            if message_id not in self._messages:
                not_found.append(message_id)
                continue
            
            # Check if agent is a recipient
            agent_inbox = self._agent_inboxes[agent_id]
            if message_id not in agent_inbox:
                not_found.append(message_id)
                continue
            
            # Check current read status
            read_status = self._message_read_status.get(message_id, {})
            if read_status.get(agent_id, False):
                already_read.append(message_id)
                continue
            
            # Mark as read
            read_status[agent_id] = True
            self._message_read_status[message_id] = read_status
            marked_read.append(message_id)
        
        logger.debug(f"Agent {agent_id} marked {len(marked_read)} messages as read")
        
        return {
            "marked_read": marked_read,
            "not_found": not_found,
            "already_read": already_read
        }
    
    def respond_to_message(
        self,
        responder_agent_id: str,
        original_message_id: str,
        response_content: Dict[str, Any],
        additional_recipients: Optional[List[str]] = None
    ) -> str:
        """Send a response to a message.
        
        Args:
            responder_agent_id: Agent sending the response
            original_message_id: ID of message being responded to
            response_content: Response content
            additional_recipients: Additional agents to include in response
            
        Returns:
            Response message ID
            
        Raises:
            CommunicationError: If response fails
        """
        original_message = self._messages.get(original_message_id)
        if not original_message:
            raise CommunicationError(f"Original message {original_message_id} not found")
        
        if not original_message.requires_response:
            raise CommunicationError("Original message does not require a response")
        
        if responder_agent_id not in original_message.recipient_agent_ids:
            raise CommunicationError("Responder was not a recipient of the original message")
        
        # Check response deadline
        if original_message.response_deadline and time.time() > original_message.response_deadline:
            raise CommunicationError("Response deadline has passed")
        
        # Determine recipients (sender + additional recipients)
        recipients = [original_message.sender_agent_id]
        if additional_recipients:
            recipients.extend(additional_recipients)
        
        # Send response
        response_id = self.send_message(
            sender_agent_id=responder_agent_id,
            recipient_agent_ids=recipients,
            message_type=MessageType.RESPONSE,
            content=response_content,
            priority=original_message.priority,
            requires_response=False,
            context_reference=f"response_to:{original_message_id}"
        )
        
        logger.info(f"Response {response_id} sent to message {original_message_id}")
        return response_id
    
    def broadcast_update(
        self,
        sender_agent_id: str,
        update_type: str,
        content: Dict[str, Any],
        urgency: str = "info"
    ) -> str:
        """Send a broadcast update to all team members.
        
        Args:
            sender_agent_id: Agent broadcasting the update
            update_type: Type of update (progress, discovery, issue, completion)
            content: Update content
            urgency: Urgency level (info, attention, action_required, critical)
            
        Returns:
            Broadcast message ID
        """
        priority_map = {
            "info": MessagePriority.LOW,
            "attention": MessagePriority.NORMAL,
            "action_required": MessagePriority.HIGH,
            "critical": MessagePriority.URGENT
        }
        
        broadcast_content = {
            "text": f"[{update_type.upper()}] {content.get('summary', '')}",
            "update_type": update_type,
            "details": content.get("details", ""),
            "impact": content.get("impact", ""),
            "action_required": content.get("action_required", False)
        }
        
        return self.send_message(
            sender_agent_id=sender_agent_id,
            recipient_agent_ids=["ALL"],
            message_type=MessageType.BROADCAST,
            content=broadcast_content,
            priority=priority_map.get(urgency, MessagePriority.NORMAL),
            requires_response=content.get("action_required", False)
        )
    
    def get_unread_count(self, agent_id: str) -> int:
        """Get count of unread messages for an agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Number of unread messages
        """
        if agent_id not in self._agent_inboxes:
            return 0
        
        unread_count = 0
        for message_id in self._agent_inboxes[agent_id]:
            read_status = self._message_read_status.get(message_id, {})
            if not read_status.get(agent_id, False):
                unread_count += 1
        
        return unread_count
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics.
        
        Returns:
            Dictionary with communication statistics
        """
        total_messages = len(self._messages)
        total_agents = len(self._agent_inboxes)
        
        # Count messages by type
        message_type_counts = {}
        for message in self._messages.values():
            msg_type = message.message_type.value
            message_type_counts[msg_type] = message_type_counts.get(msg_type, 0) + 1
        
        # Count messages by priority
        priority_counts = {}
        for message in self._messages.values():
            priority = message.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        return {
            "total_messages": total_messages,
            "total_agents": total_agents,
            "message_types": message_type_counts,
            "priorities": priority_counts,
            "total_deliveries": len(self._delivery_log)
        }