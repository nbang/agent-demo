"""Content Version Control System

Comprehensive version control system for content drafts with change tracking,
revision history, collaborative editing capabilities, and rollback support.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path
import difflib

from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class ChangeType(Enum):
    """Types of changes in content versions."""
    CREATION = "creation"
    EDIT = "edit"
    DELETION = "deletion"
    MERGE = "merge"
    REVERT = "revert"
    BRANCH = "branch"
    TAG = "tag"


class ContentStatus(Enum):
    """Status of content versions."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class DiffFormat(Enum):
    """Formats for displaying differences."""
    UNIFIED = "unified"
    CONTEXT = "context"
    HTML = "html"
    SIDE_BY_SIDE = "side_by_side"
    JSON = "json"


@dataclass
class ContentChange:
    """Represents a single change in content."""
    change_type: str  # added, removed, modified
    line_number: int
    old_content: Optional[str]
    new_content: Optional[str]
    section: Optional[str] = None
    change_id: str = field(default_factory=lambda: hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8])


@dataclass
class ContentVersion:
    """Represents a single version of content."""
    version_id: str
    version_number: int
    content: str
    content_hash: str
    author: str
    timestamp: datetime
    change_type: ChangeType
    commit_message: str
    parent_version_id: Optional[str] = None
    branch: str = "main"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Change tracking
    changes_summary: Dict[str, int] = field(default_factory=dict)  # lines added/removed/modified
    word_count: int = 0
    character_count: int = 0
    
    # Review information
    status: ContentStatus = ContentStatus.DRAFT
    reviewers: List[str] = field(default_factory=list)
    comments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ContentBranch:
    """Represents a content branch."""
    branch_name: str
    base_version_id: str
    created_by: str
    created_at: datetime
    description: str
    is_active: bool = True
    merged_into: Optional[str] = None
    merged_at: Optional[datetime] = None


@dataclass
class MergeConflict:
    """Represents a merge conflict."""
    conflict_id: str
    section: str
    line_number: int
    current_content: str
    incoming_content: str
    base_content: Optional[str] = None
    resolved: bool = False
    resolution: Optional[str] = None


@dataclass
class VersionDiff:
    """Represents differences between two versions."""
    from_version_id: str
    to_version_id: str
    changes: List[ContentChange]
    lines_added: int
    lines_removed: int
    lines_modified: int
    words_added: int
    words_removed: int
    similarity_score: float  # 0-1, how similar the versions are
    diff_text: str  # Human-readable diff
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class VersionHistory:
    """Complete version history for content."""
    content_id: str
    title: str
    versions: List[ContentVersion]
    branches: Dict[str, ContentBranch]
    current_version_id: str
    total_versions: int
    created_at: datetime
    last_modified: datetime
    authors: Set[str] = field(default_factory=set)
    total_commits: int = 0


class ContentVersionControl:
    """Comprehensive content version control system."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize content version control system.
        
        Args:
            storage_path: Path to store version control data
        """
        self.storage_path = storage_path or Path("./content_versions")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory version histories
        self.histories: Dict[str, VersionHistory] = {}
        
        # Current branches per content
        self.current_branches: Dict[str, str] = {}  # content_id -> branch_name
        
        logger.info(f"Content version control initialized at {self.storage_path}")
    
    def create_content(
        self,
        content_id: str,
        title: str,
        initial_content: str,
        author: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContentVersion:
        """Create new content with initial version.
        
        Args:
            content_id: Unique identifier for content
            title: Content title
            initial_content: Initial content text
            author: Author name
            metadata: Additional metadata
            
        Returns:
            ContentVersion for the initial version
        """
        logger.info(f"Creating new content: {content_id}")
        
        # Create initial version
        version = self._create_version(
            content=initial_content,
            author=author,
            change_type=ChangeType.CREATION,
            commit_message="Initial content creation",
            parent_version_id=None,
            branch="main",
            metadata=metadata or {}
        )
        
        # Create version history
        history = VersionHistory(
            content_id=content_id,
            title=title,
            versions=[version],
            branches={"main": ContentBranch(
                branch_name="main",
                base_version_id=version.version_id,
                created_by=author,
                created_at=datetime.now(),
                description="Main branch"
            )},
            current_version_id=version.version_id,
            total_versions=1,
            created_at=datetime.now(),
            last_modified=datetime.now(),
            authors={author},
            total_commits=1
        )
        
        self.histories[content_id] = history
        self.current_branches[content_id] = "main"
        
        # Persist to storage
        self._save_history(content_id)
        
        logger.info(f"Content created: {content_id} (version {version.version_id})")
        return version
    
    def commit_changes(
        self,
        content_id: str,
        new_content: str,
        author: str,
        commit_message: str,
        branch: Optional[str] = None
    ) -> ContentVersion:
        """Commit changes to content, creating a new version.
        
        Args:
            content_id: Content identifier
            new_content: Updated content
            author: Author of changes
            commit_message: Description of changes
            branch: Branch to commit to (default: current branch)
            
        Returns:
            New ContentVersion
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        branch = branch or self.current_branches.get(content_id, "main")
        
        # Get parent version (latest on this branch)
        parent_version = self._get_latest_version(content_id, branch)
        
        logger.info(f"Committing changes to {content_id} on branch '{branch}'")
        
        # Create new version
        version = self._create_version(
            content=new_content,
            author=author,
            change_type=ChangeType.EDIT,
            commit_message=commit_message,
            parent_version_id=parent_version.version_id,
            branch=branch,
            metadata={}
        )
        
        # Calculate changes
        changes = self._calculate_changes(parent_version.content, new_content)
        version.changes_summary = {
            "added": sum(1 for c in changes if c.change_type == "added"),
            "removed": sum(1 for c in changes if c.change_type == "removed"),
            "modified": sum(1 for c in changes if c.change_type == "modified")
        }
        
        # Update history
        history.versions.append(version)
        history.current_version_id = version.version_id
        history.last_modified = datetime.now()
        history.authors.add(author)
        history.total_commits += 1
        history.total_versions = len(history.versions)
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Changes committed: {version.version_id} ({version.changes_summary})")
        return version
    
    def create_branch(
        self,
        content_id: str,
        branch_name: str,
        author: str,
        description: str,
        base_version_id: Optional[str] = None
    ) -> ContentBranch:
        """Create a new branch for content.
        
        Args:
            content_id: Content identifier
            branch_name: Name for new branch
            author: Author creating the branch
            description: Branch description
            base_version_id: Version to branch from (default: current version)
            
        Returns:
            ContentBranch
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        
        if branch_name in history.branches:
            raise ValueError(f"Branch already exists: {branch_name}")
        
        # Get base version
        base_version_id = base_version_id or history.current_version_id
        base_version = self._get_version(content_id, base_version_id)
        
        logger.info(f"Creating branch '{branch_name}' for {content_id}")
        
        # Create branch
        branch = ContentBranch(
            branch_name=branch_name,
            base_version_id=base_version_id,
            created_by=author,
            created_at=datetime.now(),
            description=description
        )
        
        history.branches[branch_name] = branch
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Branch created: {branch_name}")
        return branch
    
    def switch_branch(self, content_id: str, branch_name: str) -> ContentVersion:
        """Switch to a different branch.
        
        Args:
            content_id: Content identifier
            branch_name: Branch to switch to
            
        Returns:
            Latest version on the branch
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        
        if branch_name not in history.branches:
            raise ValueError(f"Branch not found: {branch_name}")
        
        logger.info(f"Switching to branch '{branch_name}' for {content_id}")
        
        self.current_branches[content_id] = branch_name
        latest_version = self._get_latest_version(content_id, branch_name)
        
        return latest_version
    
    def merge_branches(
        self,
        content_id: str,
        source_branch: str,
        target_branch: str,
        author: str,
        merge_message: str,
        auto_resolve: bool = False
    ) -> Tuple[ContentVersion, List[MergeConflict]]:
        """Merge changes from source branch into target branch.
        
        Args:
            content_id: Content identifier
            source_branch: Branch to merge from
            target_branch: Branch to merge into
            author: Author performing merge
            merge_message: Merge commit message
            auto_resolve: Automatically resolve simple conflicts
            
        Returns:
            Tuple of (merged version, list of conflicts)
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        
        if source_branch not in history.branches:
            raise ValueError(f"Source branch not found: {source_branch}")
        if target_branch not in history.branches:
            raise ValueError(f"Target branch not found: {target_branch}")
        
        logger.info(f"Merging {source_branch} into {target_branch} for {content_id}")
        
        # Get latest versions from both branches
        source_version = self._get_latest_version(content_id, source_branch)
        target_version = self._get_latest_version(content_id, target_branch)
        
        # Detect conflicts
        conflicts = self._detect_merge_conflicts(
            target_version.content,
            source_version.content
        )
        
        if conflicts and not auto_resolve:
            logger.warning(f"Merge conflicts detected: {len(conflicts)} conflicts")
            return target_version, conflicts
        
        # Perform merge (simple approach - can be enhanced)
        merged_content = self._merge_content(
            target_version.content,
            source_version.content,
            conflicts,
            auto_resolve
        )
        
        # Create merge version
        merge_version = self._create_version(
            content=merged_content,
            author=author,
            change_type=ChangeType.MERGE,
            commit_message=f"{merge_message} (merged {source_branch} into {target_branch})",
            parent_version_id=target_version.version_id,
            branch=target_branch,
            metadata={
                "source_branch": source_branch,
                "source_version": source_version.version_id,
                "target_branch": target_branch,
                "target_version": target_version.version_id,
                "auto_resolved": auto_resolve
            }
        )
        
        # Update history
        history.versions.append(merge_version)
        history.current_version_id = merge_version.version_id
        history.last_modified = datetime.now()
        history.total_commits += 1
        history.total_versions = len(history.versions)
        
        # Mark source branch as merged
        history.branches[source_branch].is_active = False
        history.branches[source_branch].merged_into = target_branch
        history.branches[source_branch].merged_at = datetime.now()
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Merge completed: {merge_version.version_id}")
        return merge_version, conflicts
    
    def revert_to_version(
        self,
        content_id: str,
        version_id: str,
        author: str,
        revert_message: str
    ) -> ContentVersion:
        """Revert content to a previous version.
        
        Args:
            content_id: Content identifier
            version_id: Version to revert to
            author: Author performing revert
            revert_message: Revert commit message
            
        Returns:
            New version with reverted content
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        # Get target version
        target_version = self._get_version(content_id, version_id)
        current_version = self._get_version(content_id, self.histories[content_id].current_version_id)
        
        logger.info(f"Reverting {content_id} to version {version_id}")
        
        # Create revert version
        revert_version = self._create_version(
            content=target_version.content,
            author=author,
            change_type=ChangeType.REVERT,
            commit_message=f"{revert_message} (reverted to {version_id})",
            parent_version_id=current_version.version_id,
            branch=current_version.branch,
            metadata={"reverted_to": version_id}
        )
        
        history = self.histories[content_id]
        history.versions.append(revert_version)
        history.current_version_id = revert_version.version_id
        history.last_modified = datetime.now()
        history.total_commits += 1
        history.total_versions = len(history.versions)
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Content reverted: {revert_version.version_id}")
        return revert_version
    
    def tag_version(
        self,
        content_id: str,
        version_id: str,
        tag_name: str,
        author: str,
        description: Optional[str] = None
    ) -> ContentVersion:
        """Add a tag to a version for easy reference.
        
        Args:
            content_id: Content identifier
            version_id: Version to tag
            tag_name: Tag name (e.g., "v1.0", "release")
            author: Author adding tag
            description: Optional tag description
            
        Returns:
            Tagged version
        """
        version = self._get_version(content_id, version_id)
        
        logger.info(f"Tagging version {version_id} with '{tag_name}'")
        
        if tag_name not in version.tags:
            version.tags.append(tag_name)
            version.metadata[f"tag_{tag_name}"] = {
                "added_by": author,
                "added_at": datetime.now().isoformat(),
                "description": description
            }
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Version tagged: {tag_name}")
        return version
    
    def get_diff(
        self,
        content_id: str,
        from_version_id: str,
        to_version_id: str,
        diff_format: DiffFormat = DiffFormat.UNIFIED
    ) -> VersionDiff:
        """Get differences between two versions.
        
        Args:
            content_id: Content identifier
            from_version_id: Starting version
            to_version_id: Ending version
            diff_format: Format for diff output
            
        Returns:
            VersionDiff with detailed changes
        """
        from_version = self._get_version(content_id, from_version_id)
        to_version = self._get_version(content_id, to_version_id)
        
        logger.info(f"Calculating diff from {from_version_id} to {to_version_id}")
        
        # Calculate changes
        changes = self._calculate_changes(from_version.content, to_version.content)
        
        # Count changes
        lines_added = sum(1 for c in changes if c.change_type == "added")
        lines_removed = sum(1 for c in changes if c.change_type == "removed")
        lines_modified = sum(1 for c in changes if c.change_type == "modified")
        
        # Word-level changes
        from_words = from_version.content.split()
        to_words = to_version.content.split()
        words_added = max(0, len(to_words) - len(from_words))
        words_removed = max(0, len(from_words) - len(to_words))
        
        # Similarity score
        similarity = self._calculate_similarity(from_version.content, to_version.content)
        
        # Generate diff text
        diff_text = self._generate_diff_text(
            from_version.content,
            to_version.content,
            diff_format
        )
        
        diff = VersionDiff(
            from_version_id=from_version_id,
            to_version_id=to_version_id,
            changes=changes,
            lines_added=lines_added,
            lines_removed=lines_removed,
            lines_modified=lines_modified,
            words_added=words_added,
            words_removed=words_removed,
            similarity_score=similarity,
            diff_text=diff_text
        )
        
        logger.info(f"Diff calculated: +{lines_added} -{lines_removed} ~{lines_modified} lines")
        return diff
    
    def get_version_history(
        self,
        content_id: str,
        branch: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[ContentVersion]:
        """Get version history for content.
        
        Args:
            content_id: Content identifier
            branch: Filter by branch (default: all branches)
            limit: Maximum number of versions to return
            
        Returns:
            List of versions in reverse chronological order
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        versions = history.versions
        
        # Filter by branch if specified
        if branch:
            versions = [v for v in versions if v.branch == branch]
        
        # Sort by timestamp (newest first)
        versions = sorted(versions, key=lambda v: v.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            versions = versions[:limit]
        
        return versions
    
    def get_version(self, content_id: str, version_id: str) -> ContentVersion:
        """Get a specific version.
        
        Args:
            content_id: Content identifier
            version_id: Version identifier
            
        Returns:
            ContentVersion
        """
        return self._get_version(content_id, version_id)
    
    def get_current_version(self, content_id: str) -> ContentVersion:
        """Get the current version of content.
        
        Args:
            content_id: Content identifier
            
        Returns:
            Current ContentVersion
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        return self._get_version(content_id, history.current_version_id)
    
    def get_branches(self, content_id: str) -> Dict[str, ContentBranch]:
        """Get all branches for content.
        
        Args:
            content_id: Content identifier
            
        Returns:
            Dictionary of branch name to ContentBranch
        """
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        return self.histories[content_id].branches
    
    def add_comment(
        self,
        content_id: str,
        version_id: str,
        author: str,
        comment: str,
        line_number: Optional[int] = None
    ) -> None:
        """Add a comment to a version.
        
        Args:
            content_id: Content identifier
            version_id: Version to comment on
            author: Comment author
            comment: Comment text
            line_number: Optional line number for inline comments
        """
        version = self._get_version(content_id, version_id)
        
        comment_data = {
            "author": author,
            "comment": comment,
            "timestamp": datetime.now().isoformat(),
            "line_number": line_number
        }
        
        version.comments.append(comment_data)
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Comment added to version {version_id} by {author}")
    
    def update_status(
        self,
        content_id: str,
        version_id: str,
        status: ContentStatus,
        author: str
    ) -> ContentVersion:
        """Update the status of a version.
        
        Args:
            content_id: Content identifier
            version_id: Version to update
            status: New status
            author: Author updating status
            
        Returns:
            Updated ContentVersion
        """
        version = self._get_version(content_id, version_id)
        
        old_status = version.status
        version.status = status
        version.metadata["status_history"] = version.metadata.get("status_history", [])
        version.metadata["status_history"].append({
            "from": old_status.value,
            "to": status.value,
            "changed_by": author,
            "changed_at": datetime.now().isoformat()
        })
        
        # Persist changes
        self._save_history(content_id)
        
        logger.info(f"Version status updated: {old_status.value} -> {status.value}")
        return version
    
    # Private helper methods
    
    def _create_version(
        self,
        content: str,
        author: str,
        change_type: ChangeType,
        commit_message: str,
        parent_version_id: Optional[str],
        branch: str,
        metadata: Dict[str, Any]
    ) -> ContentVersion:
        """Create a new content version."""
        version_id = hashlib.sha256(
            f"{content}{author}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        version_number = 1
        if parent_version_id:
            # Count versions to determine version number
            version_number = len([v for v in self.histories.get(list(self.histories.keys())[0] if self.histories else "", 
                                   VersionHistory("", "", [], {}, "", 0, datetime.now(), datetime.now())).versions]) + 1
        
        version = ContentVersion(
            version_id=version_id,
            version_number=version_number,
            content=content,
            content_hash=content_hash,
            author=author,
            timestamp=datetime.now(),
            change_type=change_type,
            commit_message=commit_message,
            parent_version_id=parent_version_id,
            branch=branch,
            metadata=metadata,
            word_count=len(content.split()),
            character_count=len(content)
        )
        
        return version
    
    def _get_version(self, content_id: str, version_id: str) -> ContentVersion:
        """Get a specific version."""
        if content_id not in self.histories:
            raise ValueError(f"Content not found: {content_id}")
        
        history = self.histories[content_id]
        
        for version in history.versions:
            if version.version_id == version_id:
                return version
        
        raise ValueError(f"Version not found: {version_id}")
    
    def _get_latest_version(self, content_id: str, branch: str) -> ContentVersion:
        """Get the latest version on a branch."""
        history = self.histories[content_id]
        
        branch_versions = [v for v in history.versions if v.branch == branch]
        
        if not branch_versions:
            raise ValueError(f"No versions found on branch: {branch}")
        
        return max(branch_versions, key=lambda v: v.timestamp)
    
    def _calculate_changes(self, old_content: str, new_content: str) -> List[ContentChange]:
        """Calculate changes between two versions."""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        differ = difflib.Differ()
        diff = list(differ.compare(old_lines, new_lines))
        
        changes = []
        line_number = 0
        
        for line in diff:
            if line.startswith('+ '):
                changes.append(ContentChange(
                    change_type="added",
                    line_number=line_number,
                    old_content=None,
                    new_content=line[2:]
                ))
                line_number += 1
            elif line.startswith('- '):
                changes.append(ContentChange(
                    change_type="removed",
                    line_number=line_number,
                    old_content=line[2:],
                    new_content=None
                ))
            elif line.startswith('? '):
                # Line with differences (ignored for now)
                pass
            else:
                # Unchanged line
                line_number += 1
        
        return changes
    
    def _detect_merge_conflicts(
        self,
        target_content: str,
        source_content: str
    ) -> List[MergeConflict]:
        """Detect merge conflicts between two versions."""
        conflicts = []
        
        target_lines = target_content.splitlines()
        source_lines = source_content.splitlines()
        
        # Simple conflict detection - lines that differ in same position
        max_lines = max(len(target_lines), len(source_lines))
        
        for i in range(max_lines):
            target_line = target_lines[i] if i < len(target_lines) else ""
            source_line = source_lines[i] if i < len(source_lines) else ""
            
            if target_line != source_line and target_line and source_line:
                conflict = MergeConflict(
                    conflict_id=f"conflict_{i}",
                    section=f"Line {i+1}",
                    line_number=i + 1,
                    current_content=target_line,
                    incoming_content=source_line
                )
                conflicts.append(conflict)
        
        return conflicts
    
    def _merge_content(
        self,
        target_content: str,
        source_content: str,
        conflicts: List[MergeConflict],
        auto_resolve: bool
    ) -> str:
        """Merge content from source into target."""
        if not conflicts or auto_resolve:
            # Simple merge - prefer source content for conflicts
            return source_content
        else:
            # Keep target content if conflicts exist and not auto-resolving
            return target_content
    
    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity score between two content versions."""
        matcher = difflib.SequenceMatcher(None, content1, content2)
        return matcher.ratio()
    
    def _generate_diff_text(
        self,
        old_content: str,
        new_content: str,
        diff_format: DiffFormat
    ) -> str:
        """Generate human-readable diff text."""
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        if diff_format == DiffFormat.UNIFIED:
            diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
            return '\n'.join(diff)
        elif diff_format == DiffFormat.CONTEXT:
            diff = difflib.context_diff(old_lines, new_lines, lineterm='')
            return '\n'.join(diff)
        elif diff_format == DiffFormat.HTML:
            differ = difflib.HtmlDiff()
            return differ.make_file(old_lines, new_lines)
        else:
            # Default to unified
            diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
            return '\n'.join(diff)
    
    def _save_history(self, content_id: str) -> None:
        """Persist version history to storage."""
        history = self.histories[content_id]
        
        # Create JSON-serializable data
        history_data = {
            "content_id": history.content_id,
            "title": history.title,
            "current_version_id": history.current_version_id,
            "total_versions": history.total_versions,
            "created_at": history.created_at.isoformat(),
            "last_modified": history.last_modified.isoformat(),
            "authors": list(history.authors),
            "total_commits": history.total_commits,
            "versions": [self._version_to_dict(v) for v in history.versions],
            "branches": {name: self._branch_to_dict(branch) for name, branch in history.branches.items()}
        }
        
        # Save to file
        file_path = self.storage_path / f"{content_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    def _version_to_dict(self, version: ContentVersion) -> Dict[str, Any]:
        """Convert ContentVersion to dictionary."""
        return {
            "version_id": version.version_id,
            "version_number": version.version_number,
            "content": version.content,
            "content_hash": version.content_hash,
            "author": version.author,
            "timestamp": version.timestamp.isoformat(),
            "change_type": version.change_type.value,
            "commit_message": version.commit_message,
            "parent_version_id": version.parent_version_id,
            "branch": version.branch,
            "tags": version.tags,
            "metadata": version.metadata,
            "changes_summary": version.changes_summary,
            "word_count": version.word_count,
            "character_count": version.character_count,
            "status": version.status.value,
            "reviewers": version.reviewers,
            "comments": version.comments
        }
    
    def _branch_to_dict(self, branch: ContentBranch) -> Dict[str, Any]:
        """Convert ContentBranch to dictionary."""
        return {
            "branch_name": branch.branch_name,
            "base_version_id": branch.base_version_id,
            "created_by": branch.created_by,
            "created_at": branch.created_at.isoformat(),
            "description": branch.description,
            "is_active": branch.is_active,
            "merged_into": branch.merged_into,
            "merged_at": branch.merged_at.isoformat() if branch.merged_at else None
        }


# Demo function
def demo_version_control():
    """Demonstrate content version control system."""
    print("Content Version Control System Demonstration")
    print("=" * 60)
    
    vcs = ContentVersionControl()
    
    # Create initial content
    print("\n1. Creating Initial Content")
    print("-" * 40)
    
    initial_content = """# My First Blog Post

Welcome to my blog! This is the introduction.

## Main Content

This is where the main content goes. I'll be writing about various topics.

## Conclusion

Thanks for reading!
"""
    
    v1 = vcs.create_content(
        content_id="blog_001",
        title="My First Blog Post",
        initial_content=initial_content,
        author="Alice"
    )
    print(f"✓ Created version {v1.version_id}")
    print(f"  Author: {v1.author}")
    print(f"  Word count: {v1.word_count}")
    
    # Make some edits
    print("\n2. Committing Changes")
    print("-" * 40)
    
    edited_content = """# My First Blog Post - Updated

Welcome to my blog! This is an improved introduction with more context.

## Main Content

This is where the main content goes. I'll be writing about Python programming,
AI development, and software engineering best practices.

## Examples

Here are some code examples to illustrate my points.

## Conclusion

Thanks for reading! Stay tuned for more posts.
"""
    
    v2 = vcs.commit_changes(
        content_id="blog_001",
        new_content=edited_content,
        author="Alice",
        commit_message="Added more detail and examples section"
    )
    print(f"✓ Committed version {v2.version_id}")
    print(f"  Changes: +{v2.changes_summary.get('added', 0)} "
          f"-{v2.changes_summary.get('removed', 0)} "
          f"~{v2.changes_summary.get('modified', 0)} lines")
    
    # Create a branch for review
    print("\n3. Creating Branch")
    print("-" * 40)
    
    branch = vcs.create_branch(
        content_id="blog_001",
        branch_name="review-draft",
        author="Bob",
        description="Review and editing branch"
    )
    print(f"✓ Created branch '{branch.branch_name}'")
    
    # Switch to branch and make changes
    print("\n4. Working on Branch")
    print("-" * 40)
    
    vcs.switch_branch("blog_001", "review-draft")
    
    reviewed_content = edited_content.replace(
        "## Conclusion",
        "## Key Takeaways\n\n- Point 1\n- Point 2\n\n## Conclusion"
    )
    
    v3 = vcs.commit_changes(
        content_id="blog_001",
        new_content=reviewed_content,
        author="Bob",
        commit_message="Added key takeaways section"
    )
    print(f"✓ Committed to review-draft: {v3.version_id}")
    
    # Get diff
    print("\n5. Viewing Differences")
    print("-" * 40)
    
    diff = vcs.get_diff("blog_001", v2.version_id, v3.version_id)
    print(f"Similarity: {diff.similarity_score:.1%}")
    print(f"Changes: +{diff.lines_added} -{diff.lines_removed} lines")
    print(f"Words: +{diff.words_added} -{diff.words_removed}")
    
    # Merge branches
    print("\n6. Merging Branches")
    print("-" * 40)
    
    merged_version, conflicts = vcs.merge_branches(
        content_id="blog_001",
        source_branch="review-draft",
        target_branch="main",
        author="Alice",
        merge_message="Merged reviewed changes",
        auto_resolve=True
    )
    print(f"✓ Merged successfully: {merged_version.version_id}")
    print(f"  Conflicts: {len(conflicts)}")
    
    # Tag version
    print("\n7. Tagging Version")
    print("-" * 40)
    
    tagged = vcs.tag_version(
        content_id="blog_001",
        version_id=merged_version.version_id,
        tag_name="v1.0",
        author="Alice",
        description="First published version"
    )
    print(f"✓ Tagged version as 'v1.0'")
    
    # Update status
    print("\n8. Updating Status")
    print("-" * 40)
    
    vcs.update_status(
        content_id="blog_001",
        version_id=merged_version.version_id,
        status=ContentStatus.PUBLISHED,
        author="Alice"
    )
    print(f"✓ Status updated to: PUBLISHED")
    
    # View history
    print("\n9. Version History")
    print("-" * 40)
    
    history = vcs.get_version_history("blog_001", limit=5)
    for version in history:
        print(f"  {version.version_id[:8]} | {version.branch:12s} | {version.author:10s} | {version.commit_message}")
    
    # Get branches
    print("\n10. Branch Overview")
    print("-" * 40)
    
    branches = vcs.get_branches("blog_001")
    for name, branch in branches.items():
        status = "merged" if not branch.is_active else "active"
        print(f"  {name:20s} | {status:8s} | created by {branch.created_by}")
    
    print("\n" + "=" * 60)
    print("Version control demonstration complete!")


if __name__ == "__main__":
    demo_version_control()
