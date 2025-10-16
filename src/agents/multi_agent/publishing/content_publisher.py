"""Content Publishing Integration System

Integration components for publishing content to various platforms (CMS, social media,
documentation sites) with format conversion, scheduling, and multi-platform support.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
from abc import ABC, abstractmethod
import re

from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class PublishingPlatform(Enum):
    """Supported publishing platforms."""
    WORDPRESS = "wordpress"
    MEDIUM = "medium"
    GHOST = "ghost"
    HASHNODE = "hashnode"
    DEV_TO = "dev_to"
    SUBSTACK = "substack"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    GITHUB_PAGES = "github_pages"
    GITLAB_PAGES = "gitlab_pages"
    CONFLUENCE = "confluence"
    NOTION = "notion"
    CONTENTFUL = "contentful"
    STRAPI = "strapi"
    CUSTOM = "custom"


class ContentFormat(Enum):
    """Content format types."""
    MARKDOWN = "markdown"
    HTML = "html"
    PLAIN_TEXT = "plain_text"
    JSON = "json"
    XML = "xml"
    RST = "rst"
    ASCIIDOC = "asciidoc"
    LATEX = "latex"


class PublishStatus(Enum):
    """Publishing status."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class ScheduleFrequency(Enum):
    """Scheduling frequency options."""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


@dataclass
class PublishingCredentials:
    """Platform authentication credentials."""
    platform: PublishingPlatform
    api_key: Optional[str] = None
    access_token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    api_url: Optional[str] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishingConfig:
    """Configuration for publishing to a platform."""
    platform: PublishingPlatform
    target_format: ContentFormat
    credentials: PublishingCredentials
    
    # Platform-specific settings
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    visibility: str = "public"  # public, private, unlisted
    enable_comments: bool = True
    featured_image_url: Optional[str] = None
    
    # SEO settings
    meta_description: Optional[str] = None
    canonical_url: Optional[str] = None
    custom_slug: Optional[str] = None
    
    # Formatting options
    preserve_formatting: bool = True
    auto_add_metadata: bool = True
    code_highlighting: bool = True
    
    # Additional platform-specific options
    platform_options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishingSchedule:
    """Schedule for publishing content."""
    schedule_id: str
    content_id: str
    platforms: List[PublishingPlatform]
    
    # Timing
    scheduled_time: datetime
    frequency: ScheduleFrequency = ScheduleFrequency.ONCE
    repeat_until: Optional[datetime] = None
    timezone: str = "UTC"
    
    # Status
    status: PublishStatus = PublishStatus.PENDING
    last_published: Optional[datetime] = None
    next_publish_time: Optional[datetime] = None
    
    # Notifications
    notify_on_success: bool = True
    notify_on_failure: bool = True
    notification_emails: List[str] = field(default_factory=list)


@dataclass
class PublishingResult:
    """Result of a publishing operation."""
    platform: PublishingPlatform
    status: PublishStatus
    published_url: Optional[str] = None
    published_at: Optional[datetime] = None
    
    # Response data
    platform_response: Dict[str, Any] = field(default_factory=dict)
    platform_id: Optional[str] = None  # Platform-specific content ID
    
    # Error information
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    retry_count: int = 0
    
    # Metadata
    content_id: str = ""
    content_hash: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiPlatformPublishResult:
    """Result of publishing to multiple platforms."""
    content_id: str
    total_platforms: int
    successful_publishes: int
    failed_publishes: int
    results: List[PublishingResult]
    started_at: datetime
    completed_at: datetime
    duration: float  # seconds


class ContentFormatter(ABC):
    """Abstract base class for content formatters."""
    
    @abstractmethod
    def format(self, content: str, metadata: Dict[str, Any]) -> str:
        """Format content for target platform."""
        pass
    
    @abstractmethod
    def get_format_type(self) -> ContentFormat:
        """Get the output format type."""
        pass


class MarkdownFormatter(ContentFormatter):
    """Markdown content formatter."""
    
    def format(self, content: str, metadata: Dict[str, Any]) -> str:
        """Format content as Markdown."""
        # Content is already in Markdown, just ensure proper formatting
        formatted = content.strip()
        
        # Add front matter if metadata provided
        if metadata:
            front_matter = self._generate_front_matter(metadata)
            formatted = f"{front_matter}\n\n{formatted}"
        
        return formatted
    
    def get_format_type(self) -> ContentFormat:
        return ContentFormat.MARKDOWN
    
    def _generate_front_matter(self, metadata: Dict[str, Any]) -> str:
        """Generate YAML front matter."""
        lines = ["---"]
        
        if "title" in metadata:
            lines.append(f"title: \"{metadata['title']}\"")
        if "date" in metadata:
            lines.append(f"date: {metadata['date']}")
        if "author" in metadata:
            lines.append(f"author: {metadata['author']}")
        if "tags" in metadata and metadata["tags"]:
            tags_str = ", ".join(metadata["tags"])
            lines.append(f"tags: [{tags_str}]")
        if "description" in metadata:
            lines.append(f"description: \"{metadata['description']}\"")
        
        lines.append("---")
        return "\n".join(lines)


class HTMLFormatter(ContentFormatter):
    """HTML content formatter."""
    
    def format(self, content: str, metadata: Dict[str, Any]) -> str:
        """Convert Markdown to HTML."""
        # Simple Markdown to HTML conversion
        html = content
        
        # Convert headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Convert bold and italic
        html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
        html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
        
        # Convert links
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Convert images
        html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1" />', html)
        
        # Convert code blocks
        html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Convert lists
        html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Convert paragraphs
        paragraphs = html.split('\n\n')
        formatted_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<'):
                para = f'<p>{para}</p>'
            formatted_paragraphs.append(para)
        
        html = '\n\n'.join(formatted_paragraphs)
        
        # Add HTML structure if metadata provided
        if metadata:
            html = self._wrap_in_html(html, metadata)
        
        return html
    
    def get_format_type(self) -> ContentFormat:
        return ContentFormat.HTML
    
    def _wrap_in_html(self, content: str, metadata: Dict[str, Any]) -> str:
        """Wrap content in full HTML document."""
        title = metadata.get('title', 'Untitled')
        description = metadata.get('description', '')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
</head>
<body>
    <article>
        {content}
    </article>
</body>
</html>"""
        return html


class PlainTextFormatter(ContentFormatter):
    """Plain text formatter."""
    
    def format(self, content: str, metadata: Dict[str, Any]) -> str:
        """Convert to plain text."""
        # Remove Markdown formatting
        text = content
        
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove images
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
        
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        
        # Remove inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove formatting
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        
        # Remove headers markers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def get_format_type(self) -> ContentFormat:
        return ContentFormat.PLAIN_TEXT


class JSONFormatter(ContentFormatter):
    """JSON formatter."""
    
    def format(self, content: str, metadata: Dict[str, Any]) -> str:
        """Format content as JSON."""
        data = {
            "content": content,
            "metadata": metadata,
            "formatted_at": datetime.now().isoformat()
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def get_format_type(self) -> ContentFormat:
        return ContentFormat.JSON


class PlatformAdapter(ABC):
    """Abstract base class for platform adapters."""
    
    def __init__(self, config: PublishingConfig):
        self.config = config
        self.platform = config.platform
    
    @abstractmethod
    def publish(self, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Publish content to platform."""
        pass
    
    @abstractmethod
    def update(self, platform_id: str, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Update existing content on platform."""
        pass
    
    @abstractmethod
    def delete(self, platform_id: str) -> bool:
        """Delete content from platform."""
        pass
    
    @abstractmethod
    def get_published_url(self, platform_id: str) -> Optional[str]:
        """Get URL of published content."""
        pass


class WordPressAdapter(PlatformAdapter):
    """WordPress publishing adapter."""
    
    def publish(self, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Publish to WordPress."""
        logger.info(f"Publishing to WordPress: {metadata.get('title', 'Untitled')}")
        
        try:
            # Simulate WordPress API call
            # In production, use python-wordpress-xmlrpc or REST API
            
            post_data = {
                "title": metadata.get("title", "Untitled"),
                "content": content,
                "status": self.config.visibility,
                "categories": [self.config.category] if self.config.category else [],
                "tags": self.config.tags,
                "excerpt": metadata.get("description", ""),
                "featured_image": self.config.featured_image_url
            }
            
            # Simulate successful publish
            platform_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]
            published_url = f"https://example.wordpress.com/posts/{platform_id}"
            
            result = PublishingResult(
                platform=PublishingPlatform.WORDPRESS,
                status=PublishStatus.PUBLISHED,
                published_url=published_url,
                published_at=datetime.now(),
                platform_response=post_data,
                platform_id=platform_id,
                content_id=metadata.get("content_id", ""),
                content_hash=hashlib.sha256(content.encode()).hexdigest()
            )
            
            logger.info(f"Successfully published to WordPress: {published_url}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to publish to WordPress: {str(e)}")
            return PublishingResult(
                platform=PublishingPlatform.WORDPRESS,
                status=PublishStatus.FAILED,
                error_message=str(e),
                content_id=metadata.get("content_id", "")
            )
    
    def update(self, platform_id: str, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Update WordPress post."""
        logger.info(f"Updating WordPress post: {platform_id}")
        # Implementation would call WordPress API to update post
        return self.publish(content, metadata)
    
    def delete(self, platform_id: str) -> bool:
        """Delete WordPress post."""
        logger.info(f"Deleting WordPress post: {platform_id}")
        # Implementation would call WordPress API to delete post
        return True
    
    def get_published_url(self, platform_id: str) -> Optional[str]:
        """Get WordPress post URL."""
        return f"https://example.wordpress.com/posts/{platform_id}"


class MediumAdapter(PlatformAdapter):
    """Medium publishing adapter."""
    
    def publish(self, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Publish to Medium."""
        logger.info(f"Publishing to Medium: {metadata.get('title', 'Untitled')}")
        
        try:
            # Simulate Medium API call
            platform_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]
            published_url = f"https://medium.com/@user/{platform_id}"
            
            result = PublishingResult(
                platform=PublishingPlatform.MEDIUM,
                status=PublishStatus.PUBLISHED,
                published_url=published_url,
                published_at=datetime.now(),
                platform_id=platform_id,
                content_id=metadata.get("content_id", ""),
                content_hash=hashlib.sha256(content.encode()).hexdigest()
            )
            
            logger.info(f"Successfully published to Medium: {published_url}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to publish to Medium: {str(e)}")
            return PublishingResult(
                platform=PublishingPlatform.MEDIUM,
                status=PublishStatus.FAILED,
                error_message=str(e),
                content_id=metadata.get("content_id", "")
            )
    
    def update(self, platform_id: str, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Update Medium post (Medium doesn't support updates, create new)."""
        logger.warning("Medium doesn't support post updates, creating new post")
        return self.publish(content, metadata)
    
    def delete(self, platform_id: str) -> bool:
        """Delete Medium post (Medium doesn't support deletion via API)."""
        logger.warning("Medium doesn't support post deletion via API")
        return False
    
    def get_published_url(self, platform_id: str) -> Optional[str]:
        """Get Medium post URL."""
        return f"https://medium.com/@user/{platform_id}"


class DevToAdapter(PlatformAdapter):
    """DEV.to publishing adapter."""
    
    def publish(self, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Publish to DEV.to."""
        logger.info(f"Publishing to DEV.to: {metadata.get('title', 'Untitled')}")
        
        try:
            # Simulate DEV.to API call
            platform_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]
            slug = metadata.get("title", "untitled").lower().replace(" ", "-")
            published_url = f"https://dev.to/user/{slug}-{platform_id}"
            
            result = PublishingResult(
                platform=PublishingPlatform.DEV_TO,
                status=PublishStatus.PUBLISHED,
                published_url=published_url,
                published_at=datetime.now(),
                platform_id=platform_id,
                content_id=metadata.get("content_id", ""),
                content_hash=hashlib.sha256(content.encode()).hexdigest()
            )
            
            logger.info(f"Successfully published to DEV.to: {published_url}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to publish to DEV.to: {str(e)}")
            return PublishingResult(
                platform=PublishingPlatform.DEV_TO,
                status=PublishStatus.FAILED,
                error_message=str(e),
                content_id=metadata.get("content_id", "")
            )
    
    def update(self, platform_id: str, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Update DEV.to post."""
        logger.info(f"Updating DEV.to post: {platform_id}")
        return self.publish(content, metadata)
    
    def delete(self, platform_id: str) -> bool:
        """Delete DEV.to post."""
        logger.info(f"Deleting DEV.to post: {platform_id}")
        return True
    
    def get_published_url(self, platform_id: str) -> Optional[str]:
        """Get DEV.to post URL."""
        return f"https://dev.to/user/{platform_id}"


class GitHubPagesAdapter(PlatformAdapter):
    """GitHub Pages publishing adapter."""
    
    def publish(self, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Publish to GitHub Pages."""
        logger.info(f"Publishing to GitHub Pages: {metadata.get('title', 'Untitled')}")
        
        try:
            # Simulate GitHub Pages deployment
            slug = metadata.get("title", "untitled").lower().replace(" ", "-")
            platform_id = f"{slug}-{datetime.now().strftime('%Y%m%d')}"
            published_url = f"https://username.github.io/{slug}"
            
            result = PublishingResult(
                platform=PublishingPlatform.GITHUB_PAGES,
                status=PublishStatus.PUBLISHED,
                published_url=published_url,
                published_at=datetime.now(),
                platform_id=platform_id,
                content_id=metadata.get("content_id", ""),
                content_hash=hashlib.sha256(content.encode()).hexdigest()
            )
            
            logger.info(f"Successfully published to GitHub Pages: {published_url}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to publish to GitHub Pages: {str(e)}")
            return PublishingResult(
                platform=PublishingPlatform.GITHUB_PAGES,
                status=PublishStatus.FAILED,
                error_message=str(e),
                content_id=metadata.get("content_id", "")
            )
    
    def update(self, platform_id: str, content: str, metadata: Dict[str, Any]) -> PublishingResult:
        """Update GitHub Pages content."""
        logger.info(f"Updating GitHub Pages: {platform_id}")
        return self.publish(content, metadata)
    
    def delete(self, platform_id: str) -> bool:
        """Delete GitHub Pages content."""
        logger.info(f"Deleting from GitHub Pages: {platform_id}")
        return True
    
    def get_published_url(self, platform_id: str) -> Optional[str]:
        """Get GitHub Pages URL."""
        return f"https://username.github.io/{platform_id}"


class ContentPublisher:
    """Main content publishing system."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize content publisher.
        
        Args:
            storage_path: Path to store publishing data
        """
        self.storage_path = storage_path or Path("./publishing_data")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Formatters
        self.formatters: Dict[ContentFormat, ContentFormatter] = {
            ContentFormat.MARKDOWN: MarkdownFormatter(),
            ContentFormat.HTML: HTMLFormatter(),
            ContentFormat.PLAIN_TEXT: PlainTextFormatter(),
            ContentFormat.JSON: JSONFormatter()
        }
        
        # Platform adapters factory
        self.adapter_classes: Dict[PublishingPlatform, type] = {
            PublishingPlatform.WORDPRESS: WordPressAdapter,
            PublishingPlatform.MEDIUM: MediumAdapter,
            PublishingPlatform.DEV_TO: DevToAdapter,
            PublishingPlatform.GITHUB_PAGES: GitHubPagesAdapter
        }
        
        # Active schedules
        self.schedules: Dict[str, PublishingSchedule] = {}
        
        # Publishing history
        self.publishing_history: List[PublishingResult] = []
        
        logger.info("Content publisher initialized")
    
    def publish_to_platform(
        self,
        content: str,
        metadata: Dict[str, Any],
        config: PublishingConfig
    ) -> PublishingResult:
        """Publish content to a single platform.
        
        Args:
            content: Content to publish
            metadata: Content metadata
            config: Publishing configuration
            
        Returns:
            PublishingResult with publishing outcome
        """
        logger.info(f"Publishing to {config.platform.value}")
        
        try:
            # Format content
            formatter = self.formatters.get(config.target_format)
            if not formatter:
                raise ValueError(f"Unsupported format: {config.target_format}")
            
            formatted_content = formatter.format(content, metadata)
            
            # Get platform adapter
            adapter_class = self.adapter_classes.get(config.platform)
            if not adapter_class:
                raise ValueError(f"Unsupported platform: {config.platform}")
            
            adapter = adapter_class(config)
            
            # Publish
            result = adapter.publish(formatted_content, metadata)
            
            # Store result
            self.publishing_history.append(result)
            self._save_result(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Publishing failed: {str(e)}")
            result = PublishingResult(
                platform=config.platform,
                status=PublishStatus.FAILED,
                error_message=str(e),
                content_id=metadata.get("content_id", "")
            )
            self.publishing_history.append(result)
            return result
    
    def publish_to_multiple_platforms(
        self,
        content: str,
        metadata: Dict[str, Any],
        configs: List[PublishingConfig]
    ) -> MultiPlatformPublishResult:
        """Publish content to multiple platforms.
        
        Args:
            content: Content to publish
            metadata: Content metadata
            configs: List of publishing configurations
            
        Returns:
            MultiPlatformPublishResult with all outcomes
        """
        logger.info(f"Publishing to {len(configs)} platforms")
        
        started_at = datetime.now()
        results: List[PublishingResult] = []
        
        for config in configs:
            result = self.publish_to_platform(content, metadata, config)
            results.append(result)
        
        completed_at = datetime.now()
        duration = (completed_at - started_at).total_seconds()
        
        successful = sum(1 for r in results if r.status == PublishStatus.PUBLISHED)
        failed = sum(1 for r in results if r.status == PublishStatus.FAILED)
        
        multi_result = MultiPlatformPublishResult(
            content_id=metadata.get("content_id", ""),
            total_platforms=len(configs),
            successful_publishes=successful,
            failed_publishes=failed,
            results=results,
            started_at=started_at,
            completed_at=completed_at,
            duration=duration
        )
        
        logger.info(f"Multi-platform publish completed: {successful}/{len(configs)} successful")
        return multi_result
    
    def schedule_publish(
        self,
        content: str,
        metadata: Dict[str, Any],
        configs: List[PublishingConfig],
        scheduled_time: datetime,
        frequency: ScheduleFrequency = ScheduleFrequency.ONCE
    ) -> PublishingSchedule:
        """Schedule content publishing.
        
        Args:
            content: Content to publish
            metadata: Content metadata
            configs: Publishing configurations
            scheduled_time: When to publish
            frequency: Publishing frequency
            
        Returns:
            PublishingSchedule with schedule details
        """
        schedule_id = hashlib.md5(
            f"{metadata.get('content_id', '')}{scheduled_time}".encode()
        ).hexdigest()[:12]
        
        platforms = [config.platform for config in configs]
        
        schedule = PublishingSchedule(
            schedule_id=schedule_id,
            content_id=metadata.get("content_id", ""),
            platforms=platforms,
            scheduled_time=scheduled_time,
            frequency=frequency,
            status=PublishStatus.SCHEDULED
        )
        
        self.schedules[schedule_id] = schedule
        
        # Store content and configs for later publishing
        schedule_data = {
            "content": content,
            "metadata": metadata,
            "configs": [self._config_to_dict(c) for c in configs]
        }
        
        self._save_schedule(schedule_id, schedule_data)
        
        logger.info(f"Publishing scheduled: {schedule_id} for {scheduled_time}")
        return schedule
    
    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel a scheduled publish.
        
        Args:
            schedule_id: Schedule identifier
            
        Returns:
            True if cancelled successfully
        """
        if schedule_id not in self.schedules:
            return False
        
        schedule = self.schedules[schedule_id]
        schedule.status = PublishStatus.CANCELLED
        
        logger.info(f"Schedule cancelled: {schedule_id}")
        return True
    
    def get_publishing_history(
        self,
        content_id: Optional[str] = None,
        platform: Optional[PublishingPlatform] = None,
        limit: Optional[int] = None
    ) -> List[PublishingResult]:
        """Get publishing history.
        
        Args:
            content_id: Filter by content ID
            platform: Filter by platform
            limit: Maximum results to return
            
        Returns:
            List of publishing results
        """
        results = self.publishing_history
        
        if content_id:
            results = [r for r in results if r.content_id == content_id]
        
        if platform:
            results = [r for r in results if r.platform == platform]
        
        # Sort by most recent
        results = sorted(
            results,
            key=lambda r: r.published_at or datetime.min,
            reverse=True
        )
        
        if limit:
            results = results[:limit]
        
        return results
    
    def get_schedule(self, schedule_id: str) -> Optional[PublishingSchedule]:
        """Get a scheduled publish.
        
        Args:
            schedule_id: Schedule identifier
            
        Returns:
            PublishingSchedule if found
        """
        return self.schedules.get(schedule_id)
    
    def get_pending_schedules(self) -> List[PublishingSchedule]:
        """Get all pending/scheduled publishes.
        
        Returns:
            List of pending schedules
        """
        return [
            s for s in self.schedules.values()
            if s.status in [PublishStatus.PENDING, PublishStatus.SCHEDULED]
        ]
    
    def convert_format(
        self,
        content: str,
        from_format: ContentFormat,
        to_format: ContentFormat,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Convert content between formats.
        
        Args:
            content: Content to convert
            from_format: Source format
            to_format: Target format
            metadata: Optional metadata
            
        Returns:
            Converted content
        """
        metadata = metadata or {}
        
        # Get target formatter
        formatter = self.formatters.get(to_format)
        if not formatter:
            raise ValueError(f"Unsupported format: {to_format}")
        
        # Format content
        return formatter.format(content, metadata)
    
    # Private helper methods
    
    def _config_to_dict(self, config: PublishingConfig) -> Dict[str, Any]:
        """Convert PublishingConfig to dictionary."""
        return {
            "platform": config.platform.value,
            "target_format": config.target_format.value,
            "category": config.category,
            "tags": config.tags,
            "visibility": config.visibility,
            "platform_options": config.platform_options
        }
    
    def _save_result(self, result: PublishingResult) -> None:
        """Save publishing result to storage."""
        file_path = self.storage_path / "results" / f"{result.content_id}_{result.platform.value}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        result_data = {
            "platform": result.platform.value,
            "status": result.status.value,
            "published_url": result.published_url,
            "published_at": result.published_at.isoformat() if result.published_at else None,
            "platform_id": result.platform_id,
            "content_id": result.content_id,
            "error_message": result.error_message
        }
        
        with open(file_path, 'w') as f:
            json.dump(result_data, f, indent=2)
    
    def _save_schedule(self, schedule_id: str, schedule_data: Dict[str, Any]) -> None:
        """Save schedule data to storage."""
        file_path = self.storage_path / "schedules" / f"{schedule_id}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(schedule_data, f, indent=2)


# Demo function
def demo_publishing_integration():
    """Demonstrate content publishing integration."""
    print("Content Publishing Integration Demonstration")
    print("=" * 60)
    
    publisher = ContentPublisher()
    
    # Sample content
    sample_content = """# Getting Started with Python AI Development

Python has become the go-to language for AI and machine learning development. In this guide, we'll explore why Python is so popular for AI and how to get started.

## Why Python for AI?

- **Rich ecosystem**: NumPy, Pandas, TensorFlow, PyTorch
- **Easy to learn**: Clean syntax and readability
- **Large community**: Extensive resources and support

## Getting Started

First, install the essential packages:

```python
pip install numpy pandas scikit-learn
```

## Your First AI Model

Here's a simple example:

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

## Conclusion

Python makes AI development accessible and efficient. Start experimenting today!
"""
    
    metadata = {
        "content_id": "ai_python_guide_001",
        "title": "Getting Started with Python AI Development",
        "author": "Tech Writer",
        "description": "A beginner's guide to Python for AI development",
        "tags": ["python", "ai", "machine-learning", "tutorial"],
        "date": datetime.now().isoformat()
    }
    
    # Test 1: Single platform publishing
    print("\n1. Publishing to WordPress")
    print("-" * 40)
    
    wp_credentials = PublishingCredentials(
        platform=PublishingPlatform.WORDPRESS,
        api_key="test_api_key",
        api_url="https://example.wordpress.com/wp-json"
    )
    
    wp_config = PublishingConfig(
        platform=PublishingPlatform.WORDPRESS,
        target_format=ContentFormat.HTML,
        credentials=wp_credentials,
        category="Technology",
        tags=["python", "ai", "tutorial"],
        visibility="public"
    )
    
    result = publisher.publish_to_platform(sample_content, metadata, wp_config)
    print(f"✓ Status: {result.status.value}")
    print(f"  URL: {result.published_url}")
    print(f"  Platform ID: {result.platform_id}")
    
    # Test 2: Multi-platform publishing
    print("\n2. Publishing to Multiple Platforms")
    print("-" * 40)
    
    medium_config = PublishingConfig(
        platform=PublishingPlatform.MEDIUM,
        target_format=ContentFormat.MARKDOWN,
        credentials=PublishingCredentials(
            platform=PublishingPlatform.MEDIUM,
            access_token="test_token"
        ),
        tags=["python", "ai"]
    )
    
    devto_config = PublishingConfig(
        platform=PublishingPlatform.DEV_TO,
        target_format=ContentFormat.MARKDOWN,
        credentials=PublishingCredentials(
            platform=PublishingPlatform.DEV_TO,
            api_key="test_key"
        ),
        tags=["python", "ai", "beginners"]
    )
    
    multi_result = publisher.publish_to_multiple_platforms(
        sample_content,
        metadata,
        [medium_config, devto_config]
    )
    
    print(f"✓ Total platforms: {multi_result.total_platforms}")
    print(f"  Successful: {multi_result.successful_publishes}")
    print(f"  Failed: {multi_result.failed_publishes}")
    print(f"  Duration: {multi_result.duration:.2f}s")
    
    for result in multi_result.results:
        print(f"  - {result.platform.value}: {result.status.value}")
        if result.published_url:
            print(f"    {result.published_url}")
    
    # Test 3: Scheduled publishing
    print("\n3. Scheduling Publication")
    print("-" * 40)
    
    scheduled_time = datetime.now() + timedelta(hours=2)
    
    schedule = publisher.schedule_publish(
        sample_content,
        metadata,
        [wp_config, medium_config],
        scheduled_time=scheduled_time,
        frequency=ScheduleFrequency.ONCE
    )
    
    print(f"✓ Schedule ID: {schedule.schedule_id}")
    print(f"  Scheduled for: {schedule.scheduled_time}")
    print(f"  Platforms: {', '.join([p.value for p in schedule.platforms])}")
    print(f"  Status: {schedule.status.value}")
    
    # Test 4: Format conversion
    print("\n4. Format Conversion")
    print("-" * 40)
    
    html_content = publisher.convert_format(
        sample_content,
        ContentFormat.MARKDOWN,
        ContentFormat.HTML,
        metadata
    )
    
    print(f"✓ Converted to HTML")
    print(f"  Length: {len(html_content)} characters")
    print(f"  Preview: {html_content[:100]}...")
    
    plain_text = publisher.convert_format(
        sample_content,
        ContentFormat.MARKDOWN,
        ContentFormat.PLAIN_TEXT
    )
    
    print(f"\n✓ Converted to Plain Text")
    print(f"  Length: {len(plain_text)} characters")
    print(f"  Word count: {len(plain_text.split())} words")
    
    # Test 5: Publishing history
    print("\n5. Publishing History")
    print("-" * 40)
    
    history = publisher.get_publishing_history(limit=5)
    print(f"✓ Total publishes: {len(history)}")
    
    for result in history[:3]:
        status_icon = "✓" if result.status == PublishStatus.PUBLISHED else "✗"
        print(f"  {status_icon} {result.platform.value}: {result.published_url or 'N/A'}")
    
    print("\n" + "=" * 60)
    print("Publishing integration demonstration complete!")


if __name__ == "__main__":
    demo_publishing_integration()
