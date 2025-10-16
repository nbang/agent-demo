"""Content Creation Workflow

Comprehensive content creation pipeline that orchestrates research, writing, 
editing, and review phases with proper coordination between specialized agent roles.
"""

import time
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from src.agents.multi_agent.roles.writer import WriterRole, WritingOutput, create_technical_writer, create_creative_writer
from src.agents.multi_agent.roles.editor import EditorRole, EditingOutput, create_copy_editor, create_line_editor
from src.agents.multi_agent.roles.reviewer import ContentReviewerRole, ReviewFeedback, ReviewDecision, create_technical_reviewer, create_editorial_reviewer
from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class WorkflowStage(Enum):
    """Content creation workflow stages."""
    PLANNING = "planning"
    RESEARCH = "research"
    WRITING = "writing"
    EDITING = "editing"
    REVIEW = "review"
    REVISION = "revision"
    APPROVAL = "approval"
    FINALIZATION = "finalization"
    COMPLETED = "completed"


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REQUIRES_ATTENTION = "requires_attention"


@dataclass
class ContentRequirements:
    """Requirements for content creation."""
    content_type: str  # blog_post, article, documentation, etc.
    topic: str
    target_audience: str
    content_purpose: str
    word_count_range: Tuple[int, int]
    tone: str
    style_guide: Optional[Dict[str, Any]] = None
    seo_keywords: Optional[List[str]] = None
    deadline: Optional[datetime] = None
    brand_guidelines: Optional[Dict[str, Any]] = None
    technical_requirements: Optional[Dict[str, Any]] = None
    approval_criteria: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowStageResult:
    """Result from a workflow stage."""
    stage: WorkflowStage
    status: WorkflowStatus
    output: Optional[Any] = None
    feedback: Optional[str] = None
    issues: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0
    agent_type: Optional[str] = None
    completed_at: Optional[datetime] = None


@dataclass
class ContentWorkflowResult:
    """Final result of content creation workflow."""
    workflow_id: str
    requirements: ContentRequirements
    final_content: str
    content_metadata: Dict[str, Any]
    workflow_status: WorkflowStatus
    stage_results: List[WorkflowStageResult]
    total_duration: float
    quality_score: float
    revision_count: int
    created_at: datetime
    completed_at: Optional[datetime] = None


class ContentCreationWorkflow:
    """Orchestrates the complete content creation process."""
    
    def __init__(
        self,
        workflow_config: Optional[Dict[str, Any]] = None,
        agent_assignments: Optional[Dict[str, str]] = None
    ):
        """Initialize content creation workflow.
        
        Args:
            workflow_config: Configuration for workflow behavior
            agent_assignments: Specific agent type assignments for stages
        """
        self.workflow_config = workflow_config or {
            "max_revisions": 3,
            "quality_threshold": 4.0,
            "auto_proceed": True,
            "parallel_processing": False,
            "save_intermediate": True,
            "timeout_minutes": 60
        }
        
        self.agent_assignments = agent_assignments or {
            "writer": "technical",
            "editor": "copy", 
            "reviewer": "editorial"
        }
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        # Workflow tracking
        self.active_workflows = {}
        self.workflow_history = []
        
        logger.info("Content creation workflow initialized")
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize agents based on assignments."""
        agents = {}
        
        # Initialize writers
        writer_type = self.agent_assignments.get("writer", "technical")
        if writer_type == "technical":
            agents["writer"] = create_technical_writer()
        elif writer_type == "creative":
            agents["writer"] = create_creative_writer()
        else:
            agents["writer"] = WriterRole(writer_type=writer_type)
        
        # Initialize editors
        editor_type = self.agent_assignments.get("editor", "copy")
        if editor_type == "copy":
            agents["editor"] = create_copy_editor()
        elif editor_type == "line":
            agents["editor"] = create_line_editor()
        else:
            agents["editor"] = EditorRole(editor_type=editor_type)
        
        # Initialize reviewers
        reviewer_type = self.agent_assignments.get("reviewer", "editorial")
        if reviewer_type == "technical":
            agents["reviewer"] = create_technical_reviewer()
        elif reviewer_type == "editorial":
            agents["reviewer"] = create_editorial_reviewer()
        else:
            agents["reviewer"] = ContentReviewerRole(reviewer_type=reviewer_type)
        
        return agents
    
    async def create_content(
        self,
        requirements: ContentRequirements,
        workflow_id: Optional[str] = None
    ) -> ContentWorkflowResult:
        """Execute complete content creation workflow.
        
        Args:
            requirements: Content requirements and specifications
            workflow_id: Optional workflow identifier
            
        Returns:
            ContentWorkflowResult with final content and workflow details
        """
        workflow_id = workflow_id or f"workflow_{int(time.time())}"
        start_time = time.time()
        
        logger.info(f"Starting content creation workflow: {workflow_id}")
        logger.info(f"Topic: {requirements.topic}")
        logger.info(f"Content type: {requirements.content_type}")
        
        # Initialize workflow tracking
        stage_results = []
        current_content = ""
        revision_count = 0
        workflow_status = WorkflowStatus.IN_PROGRESS
        
        try:
            # Stage 1: Planning
            planning_result = await self._execute_planning_stage(requirements)
            stage_results.append(planning_result)
            
            if planning_result.status == WorkflowStatus.FAILED:
                raise Exception("Planning stage failed")
            
            # Stage 2: Research (if needed)
            research_result = await self._execute_research_stage(requirements, planning_result)
            stage_results.append(research_result)
            
            # Stage 3: Initial Writing
            writing_result = await self._execute_writing_stage(requirements, research_result, planning_result)
            stage_results.append(writing_result)
            current_content = writing_result.output.generated_content if writing_result.output else ""
            
            if not current_content:
                raise Exception("Writing stage produced no content")
            
            # Iterative improvement loop
            max_revisions = self.workflow_config.get("max_revisions", 3)
            quality_threshold = self.workflow_config.get("quality_threshold", 4.0)
            
            for revision in range(max_revisions):
                logger.info(f"Starting revision cycle {revision + 1}/{max_revisions}")
                
                # Stage 4: Editing
                editing_result = await self._execute_editing_stage(current_content, requirements)
                stage_results.append(editing_result)
                
                if editing_result.output:
                    current_content = editing_result.output.edited_content
                
                # Stage 5: Review
                review_result = await self._execute_review_stage(current_content, requirements)
                stage_results.append(review_result)
                
                if not review_result.output:
                    continue
                
                review_feedback = review_result.output
                
                # Check if content meets quality threshold
                if review_feedback.overall_score >= quality_threshold:
                    if review_feedback.decision in [ReviewDecision.APPROVED, ReviewDecision.APPROVED_WITH_MINOR_CHANGES]:
                        logger.info(f"Content approved with score {review_feedback.overall_score:.2f}")
                        break
                
                # Stage 6: Revision (if needed)
                if review_feedback.decision == ReviewDecision.MAJOR_REVISIONS_REQUIRED:
                    revision_result = await self._execute_revision_stage(
                        current_content, requirements, review_feedback
                    )
                    stage_results.append(revision_result)
                    
                    if revision_result.output:
                        current_content = revision_result.output
                        revision_count += 1
                elif review_feedback.decision == ReviewDecision.REJECTED:
                    logger.error("Content rejected by reviewer")
                    workflow_status = WorkflowStatus.FAILED
                    break
            
            # Final stage: Approval and finalization
            if workflow_status != WorkflowStatus.FAILED:
                finalization_result = await self._execute_finalization_stage(
                    current_content, requirements, stage_results
                )
                stage_results.append(finalization_result)
                workflow_status = WorkflowStatus.COMPLETED
            
            total_duration = time.time() - start_time
            
            # Calculate final quality score
            final_quality_score = self._calculate_final_quality_score(stage_results)
            
            # Create workflow result
            result = ContentWorkflowResult(
                workflow_id=workflow_id,
                requirements=requirements,
                final_content=current_content,
                content_metadata=self._generate_content_metadata(current_content, stage_results),
                workflow_status=workflow_status,
                stage_results=stage_results,
                total_duration=total_duration,
                quality_score=final_quality_score,
                revision_count=revision_count,
                created_at=datetime.now(),
                completed_at=datetime.now() if workflow_status == WorkflowStatus.COMPLETED else None
            )
            
            # Store workflow result
            self.workflow_history.append(result)
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
            
            logger.info(f"Content creation workflow completed: {workflow_id}")
            logger.info(f"Final quality score: {final_quality_score:.2f}")
            logger.info(f"Total duration: {total_duration:.2f}s")
            logger.info(f"Revisions: {revision_count}")
            
            return result
            
        except Exception as e:
            logger.error(f"Content creation workflow failed: {str(e)}")
            
            # Create failed result
            total_duration = time.time() - start_time
            result = ContentWorkflowResult(
                workflow_id=workflow_id,
                requirements=requirements,
                final_content=current_content,
                content_metadata={},
                workflow_status=WorkflowStatus.FAILED,
                stage_results=stage_results,
                total_duration=total_duration,
                quality_score=0.0,
                revision_count=revision_count,
                created_at=datetime.now()
            )
            
            self.workflow_history.append(result)
            return result
    
    async def _execute_planning_stage(self, requirements: ContentRequirements) -> WorkflowStageResult:
        """Execute planning stage."""
        logger.info("Executing planning stage")
        start_time = time.time()
        
        try:
            # Create content plan
            plan = {
                "content_outline": self._generate_content_outline(requirements),
                "resource_requirements": self._assess_resource_requirements(requirements),
                "timeline_estimate": self._estimate_timeline(requirements),
                "quality_criteria": self._define_quality_criteria(requirements),
                "success_metrics": self._define_success_metrics(requirements)
            }
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.PLANNING,
                status=WorkflowStatus.COMPLETED,
                output=plan,
                feedback="Content plan created successfully",
                metrics={"planning_time": duration},
                duration=duration,
                agent_type="workflow_manager",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Planning stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.PLANNING,
                status=WorkflowStatus.FAILED,
                feedback=f"Planning failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="workflow_manager"
            )
    
    async def _execute_research_stage(
        self, requirements: ContentRequirements, planning_result: WorkflowStageResult
    ) -> WorkflowStageResult:
        """Execute research stage."""
        logger.info("Executing research stage")
        start_time = time.time()
        
        try:
            # Determine if research is needed
            needs_research = self._assess_research_needs(requirements)
            
            if not needs_research:
                return WorkflowStageResult(
                    stage=WorkflowStage.RESEARCH,
                    status=WorkflowStatus.COMPLETED,
                    output={"research_needed": False},
                    feedback="No additional research required",
                    duration=time.time() - start_time,
                    agent_type="workflow_manager",
                    completed_at=datetime.now()
                )
            
            # Conduct research (simplified for demo)
            research_data = {
                "topic_overview": f"Research data for {requirements.topic}",
                "key_points": [
                    "Key concept 1 related to the topic",
                    "Important consideration 2",
                    "Best practice 3"
                ],
                "sources": [
                    "Industry documentation",
                    "Best practice guides",
                    "Expert insights"
                ],
                "audience_insights": {
                    "knowledge_level": "intermediate",
                    "pain_points": ["complexity", "implementation"],
                    "preferred_format": "step-by-step guide"
                }
            }
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.RESEARCH,
                status=WorkflowStatus.COMPLETED,
                output=research_data,
                feedback="Research completed successfully",
                metrics={"sources_found": len(research_data["sources"])},
                duration=duration,
                agent_type="research_agent",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Research stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.RESEARCH,
                status=WorkflowStatus.FAILED,
                feedback=f"Research failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="research_agent"
            )
    
    async def _execute_writing_stage(
        self, requirements: ContentRequirements, 
        research_result: WorkflowStageResult,
        planning_result: WorkflowStageResult
    ) -> WorkflowStageResult:
        """Execute writing stage."""
        logger.info("Executing writing stage")
        start_time = time.time()
        
        try:
            writer = self.agents["writer"]
            
            # Prepare writing context
            writing_context = {
                "topic": requirements.topic,
                "audience": requirements.target_audience,
                "purpose": requirements.content_purpose,
                "word_count": requirements.word_count_range,
                "tone": requirements.tone,
                "content_type": requirements.content_type
            }
            
            # Add research data if available
            if research_result.output and research_result.output.get("research_needed", True):
                writing_context["research_data"] = research_result.output.get("key_points", [])
                writing_context["audience_insights"] = research_result.output.get("audience_insights", {})
            
            # Add planning data
            if planning_result.output:
                writing_context["content_outline"] = planning_result.output.get("content_outline", [])
            
            # Generate content
            writing_output = writer.generate_content(
                content_brief=f"Write a {requirements.content_type} about {requirements.topic}",
                writing_context=writing_context,
                style_preferences=requirements.style_guide or {}
            )
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.WRITING,
                status=WorkflowStatus.COMPLETED,
                output=writing_output,
                feedback=f"Content generated successfully ({len(writing_output.generated_content.split())} words)",
                metrics={
                    "word_count": len(writing_output.generated_content.split()),
                    "writing_time": duration,
                    "quality_score": writing_output.quality_metrics.get("overall_quality", 0.0)
                },
                duration=duration,
                agent_type=f"{writer.writer_type}_writer",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Writing stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.WRITING,
                status=WorkflowStatus.FAILED,
                feedback=f"Writing failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="writer"
            )
    
    async def _execute_editing_stage(
        self, content: str, requirements: ContentRequirements
    ) -> WorkflowStageResult:
        """Execute editing stage."""
        logger.info("Executing editing stage")
        start_time = time.time()
        
        try:
            editor = self.agents["editor"]
            
            # Prepare editing requirements
            editing_requirements = {
                "type": editor.editor_type,
                "focus": ["clarity", "correctness", "style"],
                "audience": requirements.target_audience,
                "preserve_voice": True
            }
            
            # Perform editing
            editing_output = editor.edit_content(
                content=content,
                editing_requirements=editing_requirements,
                style_guide=requirements.style_guide
            )
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.EDITING,
                status=WorkflowStatus.COMPLETED,
                output=editing_output,
                feedback=f"Content edited successfully ({len(editing_output.changes_made)} changes made)",
                metrics={
                    "changes_made": len(editing_output.changes_made),
                    "editing_time": duration,
                    "improvement_score": editing_output.quality_improvements.get("overall_improvement", 0.0)
                },
                duration=duration,
                agent_type=f"{editor.editor_type}_editor",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Editing stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.EDITING,
                status=WorkflowStatus.FAILED,
                feedback=f"Editing failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="editor"
            )
    
    async def _execute_review_stage(
        self, content: str, requirements: ContentRequirements
    ) -> WorkflowStageResult:
        """Execute review stage."""
        logger.info("Executing review stage")
        start_time = time.time()
        
        try:
            reviewer = self.agents["reviewer"]
            
            # Prepare content metadata
            content_metadata = {
                "id": f"content_{int(time.time())}",
                "type": requirements.content_type,
                "purpose": requirements.content_purpose,
                "audience": requirements.target_audience,
                "topic": requirements.topic
            }
            
            # Perform review
            review_feedback = reviewer.review_content(
                content=content,
                content_metadata=content_metadata
            )
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.REVIEW,
                status=WorkflowStatus.COMPLETED,
                output=review_feedback,
                feedback=f"Review completed: {review_feedback.decision.value} (score: {review_feedback.overall_score:.2f})",
                metrics={
                    "review_score": review_feedback.overall_score,
                    "issues_found": len(review_feedback.issues),
                    "review_time": duration,
                    "decision": review_feedback.decision.value
                },
                duration=duration,
                agent_type=f"{reviewer.reviewer_type}_reviewer",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Review stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.REVIEW,
                status=WorkflowStatus.FAILED,
                feedback=f"Review failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="reviewer"
            )
    
    async def _execute_revision_stage(
        self, content: str, requirements: ContentRequirements, review_feedback: ReviewFeedback
    ) -> WorkflowStageResult:
        """Execute revision stage."""
        logger.info("Executing revision stage")
        start_time = time.time()
        
        try:
            # Apply revisions based on review feedback
            revised_content = content
            
            # Apply priority fixes
            for fix in review_feedback.priority_fixes[:5]:  # Apply top 5 priority fixes
                # Simplified revision logic - in real implementation, this would be more sophisticated
                if "grammar" in fix.lower():
                    revised_content = self._apply_grammar_fixes(revised_content)
                elif "structure" in fix.lower():
                    revised_content = self._apply_structure_fixes(revised_content)
                elif "clarity" in fix.lower():
                    revised_content = self._apply_clarity_fixes(revised_content)
            
            # Apply specific issue fixes
            for issue in review_feedback.issues:
                if issue.suggested_fix and issue.severity.value in ["critical", "major"]:
                    # Apply the suggested fix (simplified)
                    revised_content = self._apply_suggested_fix(revised_content, issue)
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.REVISION,
                status=WorkflowStatus.COMPLETED,
                output=revised_content,
                feedback=f"Revisions applied based on {len(review_feedback.issues)} issues",
                metrics={
                    "issues_addressed": len([i for i in review_feedback.issues if i.severity.value in ["critical", "major"]]),
                    "revision_time": duration
                },
                duration=duration,
                agent_type="revision_agent",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Revision stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.REVISION,
                status=WorkflowStatus.FAILED,
                feedback=f"Revision failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="revision_agent"
            )
    
    async def _execute_finalization_stage(
        self, content: str, requirements: ContentRequirements, stage_results: List[WorkflowStageResult]
    ) -> WorkflowStageResult:
        """Execute finalization stage."""
        logger.info("Executing finalization stage")
        start_time = time.time()
        
        try:
            # Final content validation
            final_validation = {
                "word_count_check": self._validate_word_count(content, requirements.word_count_range),
                "format_check": self._validate_format(content, requirements.content_type),
                "completeness_check": self._validate_completeness(content, requirements),
                "final_quality_score": self._calculate_final_quality_score(stage_results)
            }
            
            # Generate final metadata
            final_metadata = {
                "created_at": datetime.now().isoformat(),
                "content_type": requirements.content_type,
                "topic": requirements.topic,
                "target_audience": requirements.target_audience,
                "word_count": len(content.split()),
                "workflow_stages": len(stage_results),
                "validation_results": final_validation
            }
            
            duration = time.time() - start_time
            
            return WorkflowStageResult(
                stage=WorkflowStage.FINALIZATION,
                status=WorkflowStatus.COMPLETED,
                output=final_metadata,
                feedback="Content finalized and ready for publication",
                metrics=final_validation,
                duration=duration,
                agent_type="workflow_manager",
                completed_at=datetime.now()
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Finalization stage failed: {str(e)}")
            
            return WorkflowStageResult(
                stage=WorkflowStage.FINALIZATION,
                status=WorkflowStatus.FAILED,
                feedback=f"Finalization failed: {str(e)}",
                issues=[str(e)],
                duration=duration,
                agent_type="workflow_manager"
            )
    
    def _generate_content_outline(self, requirements: ContentRequirements) -> List[str]:
        """Generate content outline based on requirements."""
        if requirements.content_type == "blog_post":
            return [
                "Introduction and hook",
                "Problem statement",
                "Solution overview", 
                "Detailed explanation",
                "Examples and use cases",
                "Conclusion and call-to-action"
            ]
        elif requirements.content_type == "technical_documentation":
            return [
                "Overview",
                "Prerequisites",
                "Step-by-step instructions",
                "Code examples",
                "Troubleshooting",
                "Additional resources"
            ]
        elif requirements.content_type == "article":
            return [
                "Compelling introduction",
                "Background and context",
                "Main content sections",
                "Supporting evidence",
                "Practical implications",
                "Summary and takeaways"
            ]
        else:
            return [
                "Introduction",
                "Main content",
                "Supporting details",
                "Conclusion"
            ]
    
    def _assess_resource_requirements(self, requirements: ContentRequirements) -> Dict[str, Any]:
        """Assess resource requirements for content creation."""
        return {
            "estimated_hours": self._estimate_hours(requirements),
            "required_expertise": self._determine_expertise_needs(requirements),
            "research_depth": "moderate" if requirements.content_type in ["article", "technical_documentation"] else "light",
            "review_cycles": 2 if requirements.content_type == "marketing_copy" else 1
        }
    
    def _estimate_timeline(self, requirements: ContentRequirements) -> Dict[str, float]:
        """Estimate timeline for content creation."""
        base_hours = self._estimate_hours(requirements)
        return {
            "planning_hours": base_hours * 0.1,
            "research_hours": base_hours * 0.2,
            "writing_hours": base_hours * 0.5,
            "editing_hours": base_hours * 0.15,
            "review_hours": base_hours * 0.05,
            "total_hours": base_hours
        }
    
    def _estimate_hours(self, requirements: ContentRequirements) -> float:
        """Estimate total hours needed."""
        word_count = sum(requirements.word_count_range) / 2
        base_hours = word_count / 500  # 500 words per hour baseline
        
        # Adjust based on content type
        if requirements.content_type == "technical_documentation":
            base_hours *= 1.5
        elif requirements.content_type == "marketing_copy":
            base_hours *= 1.3
        
        return max(1.0, base_hours)
    
    def _determine_expertise_needs(self, requirements: ContentRequirements) -> List[str]:
        """Determine required expertise areas."""
        expertise = ["content_creation"]
        
        if requirements.content_type == "technical_documentation":
            expertise.extend(["technical_writing", "subject_matter_expertise"])
        elif requirements.content_type == "marketing_copy":
            expertise.extend(["marketing", "copywriting", "brand_messaging"])
        elif requirements.content_type == "blog_post":
            expertise.extend(["seo", "audience_engagement"])
        
        return expertise
    
    def _define_quality_criteria(self, requirements: ContentRequirements) -> Dict[str, float]:
        """Define quality criteria thresholds."""
        base_criteria = {
            "clarity": 4.0,
            "grammar": 4.5,
            "structure": 4.0,
            "relevance": 4.2
        }
        
        if requirements.content_type == "technical_documentation":
            base_criteria.update({
                "accuracy": 4.8,
                "completeness": 4.5
            })
        elif requirements.content_type == "marketing_copy":
            base_criteria.update({
                "engagement": 4.3,
                "brand_alignment": 4.5
            })
        
        return base_criteria
    
    def _define_success_metrics(self, requirements: ContentRequirements) -> Dict[str, Any]:
        """Define success metrics for content."""
        return {
            "quality_score_target": 4.0,
            "word_count_target": requirements.word_count_range,
            "audience_alignment": "high",
            "completion_timeline": "on_schedule",
            "revision_limit": 3
        }
    
    def _assess_research_needs(self, requirements: ContentRequirements) -> bool:
        """Assess if research is needed."""
        research_intensive_types = [
            "technical_documentation",
            "article",
            "white_paper",
            "case_study"
        ]
        return requirements.content_type in research_intensive_types
    
    def _apply_grammar_fixes(self, content: str) -> str:
        """Apply basic grammar fixes."""
        # Simplified grammar fixes
        fixes = {
            "it's": "its",  # Context-dependent - simplified
            "alot": "a lot",
            "definately": "definitely",
            "seperate": "separate"
        }
        
        for incorrect, correct in fixes.items():
            content = content.replace(incorrect, correct)
        
        return content
    
    def _apply_structure_fixes(self, content: str) -> str:
        """Apply basic structure improvements."""
        lines = content.split("\n")
        
        # Add title if missing
        if not any(line.startswith("# ") for line in lines):
            content = "# Content Title\n\n" + content
        
        return content
    
    def _apply_clarity_fixes(self, content: str) -> str:
        """Apply basic clarity improvements."""
        # Replace wordy phrases
        clarity_fixes = {
            "in order to": "to",
            "due to the fact that": "because",
            "at this point in time": "now"
        }
        
        for wordy, concise in clarity_fixes.items():
            content = content.replace(wordy, concise)
        
        return content
    
    def _apply_suggested_fix(self, content: str, issue) -> str:
        """Apply a specific suggested fix."""
        # Simplified fix application
        if hasattr(issue, 'original_text') and hasattr(issue, 'suggested_fix'):
            if issue.original_text in content:
                content = content.replace(issue.original_text, issue.suggested_fix)
        
        return content
    
    def _validate_word_count(self, content: str, word_count_range: Tuple[int, int]) -> bool:
        """Validate content word count."""
        word_count = len(content.split())
        return word_count_range[0] <= word_count <= word_count_range[1]
    
    def _validate_format(self, content: str, content_type: str) -> bool:
        """Validate content format."""
        if content_type in ["blog_post", "article"]:
            return content.count("# ") > 0  # Has title
        elif content_type == "technical_documentation":
            return "## " in content  # Has sections
        return True
    
    def _validate_completeness(self, content: str, requirements: ContentRequirements) -> bool:
        """Validate content completeness."""
        word_count = len(content.split())
        min_words = requirements.word_count_range[0]
        
        return word_count >= min_words * 0.8  # At least 80% of minimum
    
    def _calculate_final_quality_score(self, stage_results: List[WorkflowStageResult]) -> float:
        """Calculate final quality score from all stages."""
        scores = []
        
        for result in stage_results:
            if result.stage == WorkflowStage.REVIEW and result.output:
                scores.append(result.output.overall_score)
            elif result.stage == WorkflowStage.WRITING and result.output:
                scores.append(result.output.quality_metrics.get("overall_quality", 0.0))
            elif result.stage == WorkflowStage.EDITING and result.output:
                improvement = result.output.quality_improvements.get("overall_improvement", 0.0)
                scores.append(4.0 + improvement)  # Base score + improvement
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_content_metadata(self, content: str, stage_results: List[WorkflowStageResult]) -> Dict[str, Any]:
        """Generate comprehensive content metadata."""
        return {
            "word_count": len(content.split()),
            "character_count": len(content),
            "estimated_reading_time": len(content.split()) / 200,  # 200 WPM
            "workflow_stages": len(stage_results),
            "total_processing_time": sum(r.duration for r in stage_results),
            "agents_involved": list(set(r.agent_type for r in stage_results if r.agent_type)),
            "revision_history": [r for r in stage_results if r.stage == WorkflowStage.REVISION],
            "final_validation": all(r.status == WorkflowStatus.COMPLETED for r in stage_results)
        }
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of an active workflow."""
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        
        # Check completed workflows
        for workflow in self.workflow_history:
            if workflow.workflow_id == workflow_id:
                return {
                    "status": workflow.workflow_status.value,
                    "completed_at": workflow.completed_at,
                    "final_score": workflow.quality_score
                }
        
        return None
    
    def get_workflow_history(self, limit: int = 10) -> List[ContentWorkflowResult]:
        """Get workflow history."""
        return self.workflow_history[-limit:]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get workflow performance metrics."""
        if not self.workflow_history:
            return {}
        
        completed_workflows = [w for w in self.workflow_history if w.workflow_status == WorkflowStatus.COMPLETED]
        
        if not completed_workflows:
            return {"total_workflows": len(self.workflow_history), "completed_workflows": 0}
        
        return {
            "total_workflows": len(self.workflow_history),
            "completed_workflows": len(completed_workflows),
            "success_rate": len(completed_workflows) / len(self.workflow_history),
            "average_duration": sum(w.total_duration for w in completed_workflows) / len(completed_workflows),
            "average_quality_score": sum(w.quality_score for w in completed_workflows) / len(completed_workflows),
            "average_revisions": sum(w.revision_count for w in completed_workflows) / len(completed_workflows)
        }


# Factory functions for different workflow configurations

def create_blog_workflow(
    writer_type: str = "creative",
    editor_type: str = "line", 
    reviewer_type: str = "editorial"
) -> ContentCreationWorkflow:
    """Create workflow optimized for blog posts."""
    config = {
        "max_revisions": 2,
        "quality_threshold": 4.0,
        "auto_proceed": True,
        "save_intermediate": True
    }
    
    agents = {
        "writer": writer_type,
        "editor": editor_type,
        "reviewer": reviewer_type
    }
    
    return ContentCreationWorkflow(config, agents)


def create_technical_workflow(
    writer_type: str = "technical",
    editor_type: str = "technical",
    reviewer_type: str = "technical"
) -> ContentCreationWorkflow:
    """Create workflow optimized for technical documentation."""
    config = {
        "max_revisions": 3,
        "quality_threshold": 4.5,
        "auto_proceed": False,
        "save_intermediate": True
    }
    
    agents = {
        "writer": writer_type,
        "editor": editor_type,
        "reviewer": reviewer_type
    }
    
    return ContentCreationWorkflow(config, agents)


def create_marketing_workflow(
    writer_type: str = "marketing",
    editor_type: str = "copy",
    reviewer_type: str = "brand"
) -> ContentCreationWorkflow:
    """Create workflow optimized for marketing content."""
    config = {
        "max_revisions": 3,
        "quality_threshold": 4.2,
        "auto_proceed": True,
        "save_intermediate": True
    }
    
    agents = {
        "writer": writer_type,
        "editor": editor_type,
        "reviewer": reviewer_type
    }
    
    return ContentCreationWorkflow(config, agents)


# Demo function
async def demo_content_workflow():
    """Demonstrate content creation workflow."""
    print("Content Creation Workflow Demonstration")
    print("=" * 60)
    
    # Create different workflow types
    workflows = {
        "Blog Post": create_blog_workflow(),
        "Technical Doc": create_technical_workflow(), 
        "Marketing Copy": create_marketing_workflow()
    }
    
    # Test each workflow
    for workflow_name, workflow in workflows.items():
        print(f"\n{workflow_name} Workflow:")
        print("-" * 40)
        
        # Create requirements
        requirements = ContentRequirements(
            content_type=workflow_name.lower().replace(" ", "_"),
            topic="Introduction to AI Agents",
            target_audience="developers",
            content_purpose="educational",
            word_count_range=(800, 1200),
            tone="professional but approachable",
            deadline=datetime.now()
        )
        
        # Execute workflow
        result = await workflow.create_content(requirements)
        
        print(f"Status: {result.workflow_status.value}")
        print(f"Quality Score: {result.quality_score:.2f}/5.0")
        print(f"Duration: {result.total_duration:.2f}s")
        print(f"Revisions: {result.revision_count}")
        print(f"Stages: {len(result.stage_results)}")
        print(f"Word Count: {len(result.final_content.split())} words")
        
        # Show workflow performance
        metrics = workflow.get_performance_metrics()
        if metrics:
            print(f"Success Rate: {metrics.get('success_rate', 0) * 100:.1f}%")


if __name__ == "__main__":
    asyncio.run(demo_content_workflow())