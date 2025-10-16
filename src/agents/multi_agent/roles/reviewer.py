"""Content Reviewer Agent Role

Specialized content reviewer agent role for quality assessment, feedback generation,
approval workflows, and comprehensive content validation.
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from src.agents.multi_agent.agent_roles import RoleDefinition, create_role_definition
from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class ReviewCriteria(Enum):
    """Different content review criteria."""
    ACCURACY = "accuracy"
    CLARITY = "clarity" 
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    ENGAGEMENT = "engagement"
    GRAMMAR = "grammar"
    STYLE = "style"
    STRUCTURE = "structure"
    RELEVANCE = "relevance"
    ORIGINALITY = "originality"
    SEO_OPTIMIZATION = "seo_optimization"
    BRAND_ALIGNMENT = "brand_alignment"


class ReviewDecision(Enum):
    """Review decision outcomes."""
    APPROVED = "approved"
    APPROVED_WITH_MINOR_CHANGES = "approved_with_minor_changes"
    MAJOR_REVISIONS_REQUIRED = "major_revisions_required"
    REJECTED = "rejected"
    NEEDS_FACT_CHECK = "needs_fact_check"
    NEEDS_LEGAL_REVIEW = "needs_legal_review"


class ReviewSeverity(Enum):
    """Severity levels for review issues."""
    CRITICAL = "critical"      # Must be fixed
    MAJOR = "major"           # Should be fixed
    MINOR = "minor"           # Could be improved
    SUGGESTION = "suggestion"  # Nice to have


@dataclass
class ReviewIssue:
    """Represents a specific review issue or feedback item."""
    id: str
    line_numbers: List[int]
    criteria: ReviewCriteria
    severity: ReviewSeverity
    description: str
    suggested_fix: Optional[str]
    reasoning: str
    confidence: float  # 0.0 to 1.0
    category: str  # content, technical, style, etc.


@dataclass
class ReviewScore:
    """Represents a score for a specific review criteria."""
    criteria: ReviewCriteria
    score: float  # 0.0 to 5.0
    weight: float  # Importance weight 0.0 to 1.0
    notes: str
    supporting_evidence: List[str]


@dataclass
class ReviewFeedback:
    """Comprehensive review feedback for content."""
    content_id: str
    reviewer_type: str
    review_date: datetime
    overall_score: float  # 0.0 to 5.0
    decision: ReviewDecision
    
    # Detailed scoring
    criteria_scores: List[ReviewScore]
    
    # Issues and feedback
    issues: List[ReviewIssue]
    strengths: List[str]
    improvement_areas: List[str]
    
    # Recommendations
    recommended_actions: List[str]
    priority_fixes: List[str]
    
    # Metadata
    review_time: float
    confidence_level: float
    next_review_needed: bool
    metadata: Dict[str, Any]


@dataclass
class ReviewGuidelines:
    """Guidelines and standards for content review."""
    target_audience: str
    content_purpose: str
    brand_voice: str
    style_guide: Dict[str, Any]
    quality_thresholds: Dict[ReviewCriteria, float]
    mandatory_criteria: List[ReviewCriteria]
    review_checklist: List[str]
    approval_requirements: Dict[str, Any]


class ContentReviewerRole:
    """Specialized content reviewer agent role for comprehensive content validation."""
    
    def __init__(
        self,
        reviewer_type: str = "general",
        specialization_areas: Optional[List[str]] = None,
        review_standards: Optional[Dict[str, float]] = None,
        review_preferences: Optional[Dict[str, Any]] = None
    ):
        """Initialize content reviewer role.
        
        Args:
            reviewer_type: Type of reviewer (general, technical, editorial, brand, legal)
            specialization_areas: Specific areas of review expertise
            review_standards: Quality thresholds for different criteria
            review_preferences: Preferences for review approach and style
        """
        self.reviewer_type = reviewer_type
        self.specialization_areas = specialization_areas or []
        self.review_standards = review_standards or {
            "accuracy": 4.5,
            "clarity": 4.0,
            "completeness": 4.2,
            "consistency": 4.3,
            "engagement": 3.8,
            "grammar": 4.8,
            "style": 4.0,
            "structure": 4.1,
            "overall_quality": 4.0
        }
        self.review_preferences = review_preferences or {
            "detailed_feedback": True,
            "provide_suggestions": True,
            "highlight_strengths": True,
            "prioritize_issues": True,
            "constructive_tone": True
        }
        
        # Initialize review capabilities
        self.review_capabilities = self._initialize_review_capabilities()
        
        # Create role definition
        self.role_definition = self._create_role_definition()
        
        # Initialize performance tracking
        self.review_history = []
        self.performance_metrics = {
            "total_content_reviewed": 0,
            "total_issues_identified": 0,
            "average_review_score": 0.0,
            "average_review_time": 0.0,
            "approval_rate": 0.0,
            "review_sessions": 0
        }
        
        logger.info(f"Content reviewer role initialized: {reviewer_type} with {len(self.review_capabilities)} capabilities")
    
    def _initialize_review_capabilities(self) -> List[str]:
        """Initialize review capabilities based on reviewer type."""
        base_capabilities = [
            "content_quality_assessment",
            "grammar_and_style_review",
            "structure_evaluation",
            "consistency_checking",
            "readability_analysis"
        ]
        
        # Add specialized capabilities based on reviewer type
        if self.reviewer_type == "technical":
            base_capabilities.extend([
                "technical_accuracy_validation",
                "code_example_review",
                "technical_terminology_check",
                "documentation_standards_compliance",
                "api_reference_validation"
            ])
        elif self.reviewer_type == "editorial":
            base_capabilities.extend([
                "editorial_standards_enforcement",
                "tone_and_voice_consistency",
                "narrative_flow_assessment",
                "content_organization_review",
                "audience_alignment_check"
            ])
        elif self.reviewer_type == "brand":
            base_capabilities.extend([
                "brand_voice_alignment",
                "messaging_consistency",
                "brand_guideline_compliance",
                "competitive_positioning_review",
                "brand_safety_assessment"
            ])
        elif self.reviewer_type == "legal":
            base_capabilities.extend([
                "legal_compliance_check",
                "copyright_validation",
                "disclaimer_requirements",
                "regulatory_compliance",
                "risk_assessment"
            ])
        elif self.reviewer_type == "seo":
            base_capabilities.extend([
                "seo_optimization_review",
                "keyword_usage_analysis",
                "meta_data_validation",
                "search_intent_alignment",
                "content_structure_seo"
            ])
        
        # Add custom specialization capabilities
        base_capabilities.extend(self.specialization_areas)
        
        return base_capabilities
    
    def _create_role_definition(self) -> RoleDefinition:
        """Create role definition for the content reviewer."""
        expertise_areas = [
            "content_quality_assessment",
            "editorial_review",
            "feedback_generation",
            "approval_workflows"
        ]
        
        # Add specialized expertise areas
        if self.reviewer_type == "technical":
            expertise_areas.extend([
                "technical_accuracy",
                "documentation_standards",
                "code_review"
            ])
        elif self.reviewer_type == "editorial":
            expertise_areas.extend([
                "editorial_standards",
                "content_strategy",
                "audience_analysis"
            ])
        elif self.reviewer_type == "brand":
            expertise_areas.extend([
                "brand_management",
                "messaging_strategy",
                "brand_compliance"
            ])
        elif self.reviewer_type == "legal":
            expertise_areas.extend([
                "legal_compliance",
                "risk_management",
                "regulatory_affairs"
            ])
        elif self.reviewer_type == "seo":
            expertise_areas.extend([
                "search_optimization",
                "content_marketing",
                "digital_strategy"
            ])
        
        responsibilities = [
            "Review content for quality and compliance",
            "Provide comprehensive feedback and recommendations",
            "Ensure content meets quality standards and guidelines",
            "Identify issues and suggest improvements",
            "Make approval decisions based on review criteria",
            "Document review findings and rationale",
            "Collaborate with writers and editors for content improvement"
        ]
        
        interaction_patterns = [
            "reviews_writer_content",
            "provides_feedback_to_editors",
            "collaborates_with_content_team",
            "escalates_to_senior_reviewers",
            "coordinates_with_stakeholders"
        ]
        
        return create_role_definition(
            name=f"{self.reviewer_type.title()} Content Reviewer",
            description=f"Specialized content reviewer focused on {self.reviewer_type} review with expertise in quality assessment and approval workflows",
            expertise_areas=expertise_areas,
            responsibilities=responsibilities,
            interaction_patterns=interaction_patterns
        )
    
    def review_content(
        self,
        content: str,
        content_metadata: Dict[str, Any],
        review_guidelines: Optional[ReviewGuidelines] = None,
        previous_feedback: Optional[List[ReviewFeedback]] = None
    ) -> ReviewFeedback:
        """Perform comprehensive content review.
        
        Args:
            content: Content to review
            content_metadata: Metadata about the content (type, purpose, audience, etc.)
            review_guidelines: Specific guidelines for this review
            previous_feedback: Any previous review feedback to consider
            
        Returns:
            ReviewFeedback with comprehensive review results
        """
        logger.info(f"Starting content review - {len(content.split())} words")
        
        start_time = time.time()
        content_id = content_metadata.get("id", f"content_{int(time.time())}")
        
        try:
            # Set up review criteria based on content type and guidelines
            review_criteria = self._determine_review_criteria(content_metadata, review_guidelines)
            
            # Perform multi-dimensional content analysis
            criteria_scores = []
            all_issues = []
            
            # Analyze each review criteria
            for criteria in review_criteria:
                score, issues = self._evaluate_criteria(content, criteria, content_metadata, review_guidelines)
                criteria_scores.append(score)
                all_issues.extend(issues)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(criteria_scores)
            
            # Make review decision
            decision = self._make_review_decision(overall_score, all_issues, review_guidelines)
            
            # Identify strengths and improvement areas
            strengths = self._identify_content_strengths(content, criteria_scores)
            improvement_areas = self._identify_improvement_areas(all_issues, criteria_scores)
            
            # Generate recommendations
            recommended_actions = self._generate_recommendations(all_issues, decision, improvement_areas)
            priority_fixes = self._prioritize_fixes(all_issues)
            
            # Calculate confidence and next review needs
            confidence_level = self._calculate_confidence_level(criteria_scores, all_issues)
            next_review_needed = self._determine_next_review_needs(decision, all_issues)
            
            review_time = time.time() - start_time
            
            # Create comprehensive feedback
            feedback = ReviewFeedback(
                content_id=content_id,
                reviewer_type=self.reviewer_type,
                review_date=datetime.now(),
                overall_score=overall_score,
                decision=decision,
                criteria_scores=criteria_scores,
                issues=all_issues,
                strengths=strengths,
                improvement_areas=improvement_areas,
                recommended_actions=recommended_actions,
                priority_fixes=priority_fixes,
                review_time=review_time,
                confidence_level=confidence_level,
                next_review_needed=next_review_needed,
                metadata={
                    "content_type": content_metadata.get("type", "unknown"),
                    "content_purpose": content_metadata.get("purpose", "general"),
                    "target_audience": content_metadata.get("audience", "general"),
                    "review_focus": [c.value for c in review_criteria],
                    "reviewer_capabilities": self.review_capabilities,
                    "review_standards_applied": self.review_standards,
                    "reviewed_at": datetime.now().isoformat()
                }
            )
            
            # Update performance tracking
            self._update_performance_metrics(feedback)
            
            logger.info(f"Content review completed in {review_time:.2f}s")
            logger.info(f"Overall score: {overall_score:.2f}/5.0, Decision: {decision.value}")
            logger.info(f"Issues identified: {len(all_issues)}")
            
            return feedback
            
        except Exception as e:
            logger.error(f"Content review failed: {str(e)}")
            raise
    
    def _determine_review_criteria(
        self, content_metadata: Dict[str, Any], guidelines: Optional[ReviewGuidelines]
    ) -> List[ReviewCriteria]:
        """Determine which criteria to apply based on content and guidelines."""
        content_type = content_metadata.get("type", "general")
        
        # Base criteria for all content
        criteria = [
            ReviewCriteria.CLARITY,
            ReviewCriteria.GRAMMAR,
            ReviewCriteria.STRUCTURE,
            ReviewCriteria.CONSISTENCY
        ]
        
        # Add content-type specific criteria
        if content_type in ["blog_post", "article", "marketing_copy"]:
            criteria.extend([
                ReviewCriteria.ENGAGEMENT,
                ReviewCriteria.RELEVANCE,
                ReviewCriteria.SEO_OPTIMIZATION
            ])
        
        if content_type in ["technical_documentation", "api_docs", "tutorial"]:
            criteria.extend([
                ReviewCriteria.ACCURACY,
                ReviewCriteria.COMPLETENESS
            ])
        
        if content_type in ["marketing_copy", "brand_content", "press_release"]:
            criteria.extend([
                ReviewCriteria.BRAND_ALIGNMENT,
                ReviewCriteria.ENGAGEMENT
            ])
        
        # Add reviewer-specific criteria
        if self.reviewer_type == "technical":
            criteria.append(ReviewCriteria.ACCURACY)
        elif self.reviewer_type == "brand":
            criteria.append(ReviewCriteria.BRAND_ALIGNMENT)
        elif self.reviewer_type == "seo":
            criteria.append(ReviewCriteria.SEO_OPTIMIZATION)
        
        # Add mandatory criteria from guidelines
        if guidelines and guidelines.mandatory_criteria:
            criteria.extend(guidelines.mandatory_criteria)
        
        # Remove duplicates and return
        return list(set(criteria))
    
    def _evaluate_criteria(
        self, content: str, criteria: ReviewCriteria, 
        metadata: Dict[str, Any], guidelines: Optional[ReviewGuidelines]
    ) -> Tuple[ReviewScore, List[ReviewIssue]]:
        """Evaluate content against specific criteria."""
        issues = []
        
        if criteria == ReviewCriteria.CLARITY:
            score, clarity_issues = self._evaluate_clarity(content)
            issues.extend(clarity_issues)
        elif criteria == ReviewCriteria.GRAMMAR:
            score, grammar_issues = self._evaluate_grammar(content)
            issues.extend(grammar_issues)
        elif criteria == ReviewCriteria.STRUCTURE:
            score, structure_issues = self._evaluate_structure(content)
            issues.extend(structure_issues)
        elif criteria == ReviewCriteria.CONSISTENCY:
            score, consistency_issues = self._evaluate_consistency(content)
            issues.extend(consistency_issues)
        elif criteria == ReviewCriteria.ENGAGEMENT:
            score, engagement_issues = self._evaluate_engagement(content, metadata)
            issues.extend(engagement_issues)
        elif criteria == ReviewCriteria.ACCURACY:
            score, accuracy_issues = self._evaluate_accuracy(content, metadata)
            issues.extend(accuracy_issues)
        elif criteria == ReviewCriteria.COMPLETENESS:
            score, completeness_issues = self._evaluate_completeness(content, metadata)
            issues.extend(completeness_issues)
        elif criteria == ReviewCriteria.SEO_OPTIMIZATION:
            score, seo_issues = self._evaluate_seo(content, metadata)
            issues.extend(seo_issues)
        elif criteria == ReviewCriteria.BRAND_ALIGNMENT:
            score, brand_issues = self._evaluate_brand_alignment(content, metadata, guidelines)
            issues.extend(brand_issues)
        else:
            # Default evaluation for other criteria
            score = 4.0
            
        # Create review score object
        review_score = ReviewScore(
            criteria=criteria,
            score=score,
            weight=self._get_criteria_weight(criteria, metadata),
            notes=f"{criteria.value} evaluation completed",
            supporting_evidence=self._generate_evidence(content, criteria, score)
        )
        
        return review_score, issues
    
    def _evaluate_clarity(self, content: str) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate content clarity."""
        issues = []
        score = 4.0  # Default good score
        
        # Check for overly complex sentences
        sentences = content.split(".")
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        
        if long_sentences:
            for i, sentence in enumerate(long_sentences):
                issues.append(ReviewIssue(
                    id=f"clarity_{i}",
                    line_numbers=[self._find_line_number(content, sentence)],
                    criteria=ReviewCriteria.CLARITY,
                    severity=ReviewSeverity.MINOR,
                    description="Sentence may be too long and complex",
                    suggested_fix="Consider breaking into shorter sentences",
                    reasoning="Long sentences can reduce readability",
                    confidence=0.7,
                    category="readability"
                ))
            score -= min(1.0, len(long_sentences) * 0.2)
        
        # Check for jargon without explanation
        technical_terms = ["API", "SDK", "OAuth", "JSON", "XML", "HTTP", "HTTPS"]
        for term in technical_terms:
            if term in content and f"{term} (" not in content:
                issues.append(ReviewIssue(
                    id=f"jargon_{term}",
                    line_numbers=[self._find_line_number(content, term)],
                    criteria=ReviewCriteria.CLARITY,
                    severity=ReviewSeverity.SUGGESTION,
                    description=f"Technical term '{term}' used without explanation",
                    suggested_fix=f"Consider explaining '{term}' for clarity",
                    reasoning="Technical terms may not be clear to all readers",
                    confidence=0.6,
                    category="terminology"
                ))
        
        return max(1.0, score), issues
    
    def _evaluate_grammar(self, content: str) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate grammar and language mechanics."""
        issues = []
        score = 4.5  # Start with high score for grammar
        
        # Common grammar issues (simplified detection)
        grammar_patterns = {
            "it's": "its",  # Context-dependent
            "your": "you're",  # Context-dependent  
            "their": "there",  # Context-dependent
            "alot": "a lot",
            "definately": "definitely",
            "seperate": "separate"
        }
        
        for incorrect, correct in grammar_patterns.items():
            if incorrect in content.lower():
                issues.append(ReviewIssue(
                    id=f"grammar_{incorrect}",
                    line_numbers=[self._find_line_number(content, incorrect)],
                    criteria=ReviewCriteria.GRAMMAR,
                    severity=ReviewSeverity.MAJOR,
                    description=f"Possible spelling/grammar error: '{incorrect}'",
                    suggested_fix=f"Check if '{correct}' is intended",
                    reasoning="Correct spelling and grammar improve credibility",
                    confidence=0.8,
                    category="spelling"
                ))
                score -= 0.3
        
        # Check for missing periods
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip() and len(line.strip()) > 20:
                if not line.strip().endswith((".", "!", "?", ":")):
                    if not line.startswith("#"):  # Not a header
                        issues.append(ReviewIssue(
                            id=f"punctuation_{i}",
                            line_numbers=[i],
                            criteria=ReviewCriteria.GRAMMAR,
                            severity=ReviewSeverity.MINOR,
                            description="Line may be missing end punctuation",
                            suggested_fix="Add appropriate punctuation",
                            reasoning="Proper punctuation improves readability",
                            confidence=0.6,
                            category="punctuation"
                        ))
        
        return max(1.0, score), issues
    
    def _evaluate_structure(self, content: str) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate content structure and organization."""
        issues = []
        score = 4.0
        
        lines = content.split("\n")
        
        # Check for proper heading structure
        has_main_title = any(line.startswith("# ") for line in lines)
        has_sections = any(line.startswith("## ") for line in lines)
        
        if not has_main_title:
            issues.append(ReviewIssue(
                id="structure_title",
                line_numbers=[0],
                criteria=ReviewCriteria.STRUCTURE,
                severity=ReviewSeverity.MAJOR,
                description="Content lacks a main title",
                suggested_fix="Add a main title (# Title)",
                reasoning="Clear title helps readers understand content purpose",
                confidence=0.9,
                category="organization"
            ))
            score -= 0.5
        
        # Check for logical flow
        if len(content.split()) > 200 and not has_sections:
            issues.append(ReviewIssue(
                id="structure_sections",
                line_numbers=[0],
                criteria=ReviewCriteria.STRUCTURE,
                severity=ReviewSeverity.MINOR,
                description="Long content without section headers",
                suggested_fix="Add section headers to improve organization",
                reasoning="Section headers help readers navigate content",
                confidence=0.7,
                category="organization"
            ))
            score -= 0.3
        
        return max(1.0, score), issues
    
    def _evaluate_consistency(self, content: str) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate consistency in style and terminology."""
        issues = []
        score = 4.0
        
        # Check for consistent capitalization of proper nouns
        proper_nouns = ["GitHub", "JavaScript", "Python", "API", "JSON", "HTML", "CSS"]
        
        for noun in proper_nouns:
            variations = [noun.lower(), noun.upper(), noun.title()]
            found_variations = []
            
            for variation in variations:
                if variation in content and variation != noun:
                    found_variations.append(variation)
            
            if found_variations:
                issues.append(ReviewIssue(
                    id=f"consistency_{noun}",
                    line_numbers=[self._find_line_number(content, found_variations[0])],
                    criteria=ReviewCriteria.CONSISTENCY,
                    severity=ReviewSeverity.MINOR,
                    description=f"Inconsistent capitalization of '{noun}'",
                    suggested_fix=f"Use consistent capitalization: '{noun}'",
                    reasoning="Consistent terminology improves professionalism",
                    confidence=0.8,
                    category="terminology"
                ))
                score -= 0.2
        
        return max(1.0, score), issues
    
    def _evaluate_engagement(self, content: str, metadata: Dict[str, Any]) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate content engagement potential."""
        issues = []
        score = 3.5  # Moderate default for engagement
        
        # Check for engaging opening
        first_paragraph = content.split("\n\n")[0] if "\n\n" in content else content[:200]
        
        if first_paragraph.lower().startswith(("the", "this", "it is", "there are")):
            issues.append(ReviewIssue(
                id="engagement_opening",
                line_numbers=[0],
                criteria=ReviewCriteria.ENGAGEMENT,
                severity=ReviewSeverity.SUGGESTION,
                description="Opening could be more engaging",
                suggested_fix="Consider starting with a question, statistic, or compelling statement",
                reasoning="Engaging openings capture reader attention",
                confidence=0.6,
                category="hook"
            ))
            score -= 0.3
        
        # Check for call-to-action (if marketing content)
        content_type = metadata.get("type", "")
        if "marketing" in content_type or "blog" in content_type:
            cta_phrases = ["learn more", "get started", "contact us", "sign up", "download"]
            has_cta = any(phrase in content.lower() for phrase in cta_phrases)
            
            if not has_cta:
                issues.append(ReviewIssue(
                    id="engagement_cta",
                    line_numbers=[len(content.split("\n")) - 1],
                    criteria=ReviewCriteria.ENGAGEMENT,
                    severity=ReviewSeverity.MINOR,
                    description="Content lacks clear call-to-action",
                    suggested_fix="Add a call-to-action to guide reader next steps",
                    reasoning="CTAs improve content effectiveness",
                    confidence=0.7,
                    category="conversion"
                ))
                score -= 0.4
        
        return max(1.0, score), issues
    
    def _evaluate_accuracy(self, content: str, metadata: Dict[str, Any]) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate content accuracy (basic checks)."""
        issues = []
        score = 4.0
        
        # Check for obviously incorrect statements (very basic)
        questionable_claims = [
            "100% accurate",
            "never fails",
            "always works",
            "completely secure",
            "impossible to hack"
        ]
        
        for claim in questionable_claims:
            if claim in content.lower():
                issues.append(ReviewIssue(
                    id=f"accuracy_{claim.replace(' ', '_')}",
                    line_numbers=[self._find_line_number(content, claim)],
                    criteria=ReviewCriteria.ACCURACY,
                    severity=ReviewSeverity.MAJOR,
                    description=f"Potentially inaccurate absolute claim: '{claim}'",
                    suggested_fix="Consider qualifying the statement",
                    reasoning="Absolute claims are often inaccurate",
                    confidence=0.7,
                    category="claims"
                ))
                score -= 0.5
        
        return max(1.0, score), issues
    
    def _evaluate_completeness(self, content: str, metadata: Dict[str, Any]) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate content completeness."""
        issues = []
        score = 4.0
        
        content_type = metadata.get("type", "")
        
        # Check completeness based on content type
        if "tutorial" in content_type or "guide" in content_type:
            # Should have introduction, steps, and conclusion
            has_intro = any(word in content.lower() for word in ["introduction", "overview", "getting started"])
            has_steps = any(word in content.lower() for word in ["step", "first", "next", "finally"])
            has_conclusion = any(word in content.lower() for word in ["conclusion", "summary", "next steps"])
            
            if not has_intro:
                issues.append(ReviewIssue(
                    id="completeness_intro",
                    line_numbers=[0],
                    criteria=ReviewCriteria.COMPLETENESS,
                    severity=ReviewSeverity.MINOR,
                    description="Tutorial/guide lacks clear introduction",
                    suggested_fix="Add introduction section",
                    reasoning="Introductions help readers understand content scope",
                    confidence=0.8,
                    category="structure"
                ))
                score -= 0.3
            
            if not has_conclusion:
                issues.append(ReviewIssue(
                    id="completeness_conclusion",
                    line_numbers=[len(content.split("\n")) - 1],
                    criteria=ReviewCriteria.COMPLETENESS,
                    severity=ReviewSeverity.MINOR,
                    description="Tutorial/guide lacks conclusion or next steps",
                    suggested_fix="Add conclusion or next steps section",
                    reasoning="Conclusions help readers understand outcomes",
                    confidence=0.8,
                    category="structure"
                ))
                score -= 0.3
        
        return max(1.0, score), issues
    
    def _evaluate_seo(self, content: str, metadata: Dict[str, Any]) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate SEO optimization."""
        issues = []
        score = 3.5
        
        # Check for headings (important for SEO)
        has_h1 = content.count("# ") > 0
        has_h2 = content.count("## ") > 0
        
        if not has_h1:
            issues.append(ReviewIssue(
                id="seo_h1",
                line_numbers=[0],
                criteria=ReviewCriteria.SEO_OPTIMIZATION,
                severity=ReviewSeverity.MAJOR,
                description="Missing H1 heading for SEO",
                suggested_fix="Add main heading (# Title)",
                reasoning="H1 headings are important for search engines",
                confidence=0.9,
                category="seo"
            ))
            score -= 0.5
        
        if not has_h2 and len(content.split()) > 300:
            issues.append(ReviewIssue(
                id="seo_h2",
                line_numbers=[0],
                criteria=ReviewCriteria.SEO_OPTIMIZATION,
                severity=ReviewSeverity.MINOR,
                description="Long content without subheadings",
                suggested_fix="Add subheadings (## Section) for better SEO structure",
                reasoning="Subheadings improve content structure for SEO",
                confidence=0.7,
                category="seo"
            ))
            score -= 0.3
        
        return max(1.0, score), issues
    
    def _evaluate_brand_alignment(
        self, content: str, metadata: Dict[str, Any], guidelines: Optional[ReviewGuidelines]
    ) -> Tuple[float, List[ReviewIssue]]:
        """Evaluate brand alignment."""
        issues = []
        score = 4.0
        
        if guidelines and guidelines.brand_voice:
            brand_voice = guidelines.brand_voice.lower()
            
            # Simple brand voice checking
            if "formal" in brand_voice:
                informal_words = ["gonna", "wanna", "kinda", "sorta"]
                for word in informal_words:
                    if word in content.lower():
                        issues.append(ReviewIssue(
                            id=f"brand_informal_{word}",
                            line_numbers=[self._find_line_number(content, word)],
                            criteria=ReviewCriteria.BRAND_ALIGNMENT,
                            severity=ReviewSeverity.MINOR,
                            description=f"Informal language '{word}' doesn't match formal brand voice",
                            suggested_fix=f"Replace '{word}' with more formal alternative",
                            reasoning="Content should match brand voice guidelines",
                            confidence=0.8,
                            category="tone"
                        ))
                        score -= 0.2
        
        return max(1.0, score), issues
    
    def _find_line_number(self, content: str, text: str) -> int:
        """Find line number containing specific text."""
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if text in line:
                return i + 1
        return 1
    
    def _get_criteria_weight(self, criteria: ReviewCriteria, metadata: Dict[str, Any]) -> float:
        """Get weight for specific criteria based on content type."""
        content_type = metadata.get("type", "general")
        
        # Default weights
        weights = {
            ReviewCriteria.ACCURACY: 0.9,
            ReviewCriteria.CLARITY: 0.8,
            ReviewCriteria.GRAMMAR: 0.7,
            ReviewCriteria.STRUCTURE: 0.6,
            ReviewCriteria.CONSISTENCY: 0.5,
            ReviewCriteria.ENGAGEMENT: 0.4,
            ReviewCriteria.COMPLETENESS: 0.8,
            ReviewCriteria.SEO_OPTIMIZATION: 0.3,
            ReviewCriteria.BRAND_ALIGNMENT: 0.6
        }
        
        # Adjust weights based on content type
        if "technical" in content_type:
            weights[ReviewCriteria.ACCURACY] = 1.0
            weights[ReviewCriteria.COMPLETENESS] = 0.9
        elif "marketing" in content_type:
            weights[ReviewCriteria.ENGAGEMENT] = 0.9
            weights[ReviewCriteria.BRAND_ALIGNMENT] = 0.8
        
        return weights.get(criteria, 0.5)
    
    def _generate_evidence(self, content: str, criteria: ReviewCriteria, score: float) -> List[str]:
        """Generate supporting evidence for criteria score."""
        evidence = []
        
        if criteria == ReviewCriteria.CLARITY:
            word_count = len(content.split())
            avg_sentence_length = word_count / max(1, content.count("."))
            evidence.append(f"Average sentence length: {avg_sentence_length:.1f} words")
            
        elif criteria == ReviewCriteria.STRUCTURE:
            heading_count = content.count("#")
            evidence.append(f"Heading structure: {heading_count} headings found")
            
        elif criteria == ReviewCriteria.GRAMMAR:
            evidence.append(f"Grammar score based on common error patterns")
        
        return evidence
    
    def _calculate_overall_score(self, criteria_scores: List[ReviewScore]) -> float:
        """Calculate weighted overall score."""
        if not criteria_scores:
            return 0.0
        
        weighted_sum = sum(score.score * score.weight for score in criteria_scores)
        total_weight = sum(score.weight for score in criteria_scores)
        
        return weighted_sum / max(1, total_weight)
    
    def _make_review_decision(
        self, overall_score: float, issues: List[ReviewIssue], guidelines: Optional[ReviewGuidelines]
    ) -> ReviewDecision:
        """Make review decision based on score and issues."""
        critical_issues = [i for i in issues if i.severity == ReviewSeverity.CRITICAL]
        major_issues = [i for i in issues if i.severity == ReviewSeverity.MAJOR]
        
        if critical_issues:
            return ReviewDecision.REJECTED
        elif len(major_issues) > 3 or overall_score < 2.5:
            return ReviewDecision.MAJOR_REVISIONS_REQUIRED
        elif len(major_issues) > 0 or overall_score < 3.5:
            return ReviewDecision.APPROVED_WITH_MINOR_CHANGES
        elif any(i.criteria == ReviewCriteria.ACCURACY for i in major_issues):
            return ReviewDecision.NEEDS_FACT_CHECK
        else:
            return ReviewDecision.APPROVED
    
    def _identify_content_strengths(self, content: str, scores: List[ReviewScore]) -> List[str]:
        """Identify content strengths based on high scores."""
        strengths = []
        
        high_scoring_criteria = [s for s in scores if s.score >= 4.0]
        
        for score in high_scoring_criteria:
            if score.criteria == ReviewCriteria.CLARITY:
                strengths.append("Content is clear and easy to understand")
            elif score.criteria == ReviewCriteria.STRUCTURE:
                strengths.append("Well-organized content structure")
            elif score.criteria == ReviewCriteria.GRAMMAR:
                strengths.append("Excellent grammar and language mechanics")
            elif score.criteria == ReviewCriteria.ENGAGEMENT:
                strengths.append("Engaging and compelling content")
        
        if len(content.split()) > 500:
            strengths.append("Comprehensive coverage of the topic")
        
        return strengths
    
    def _identify_improvement_areas(self, issues: List[ReviewIssue], scores: List[ReviewScore]) -> List[str]:
        """Identify areas needing improvement."""
        improvement_areas = []
        
        # Group issues by category
        issue_categories = {}
        for issue in issues:
            category = issue.category
            if category not in issue_categories:
                issue_categories[category] = []
            issue_categories[category].append(issue)
        
        # Generate improvement suggestions
        for category, category_issues in issue_categories.items():
            if len(category_issues) > 2:
                improvement_areas.append(f"Focus on improving {category} issues")
        
        # Add areas with low scores
        low_scoring_criteria = [s for s in scores if s.score < 3.5]
        for score in low_scoring_criteria:
            improvement_areas.append(f"Enhance {score.criteria.value}")
        
        return improvement_areas
    
    def _generate_recommendations(
        self, issues: List[ReviewIssue], decision: ReviewDecision, improvement_areas: List[str]
    ) -> List[str]:
        """Generate specific recommendations for improvement."""
        recommendations = []
        
        if decision == ReviewDecision.MAJOR_REVISIONS_REQUIRED:
            recommendations.append("Address all major issues before resubmission")
            recommendations.append("Consider restructuring content for better flow")
        elif decision == ReviewDecision.APPROVED_WITH_MINOR_CHANGES:
            recommendations.append("Address minor issues for publication")
            recommendations.append("Review suggestions for enhancement opportunities")
        
        # Add specific recommendations based on issues
        grammar_issues = [i for i in issues if i.criteria == ReviewCriteria.GRAMMAR]
        if len(grammar_issues) > 3:
            recommendations.append("Consider using grammar checking tools")
        
        structure_issues = [i for i in issues if i.criteria == ReviewCriteria.STRUCTURE]
        if structure_issues:
            recommendations.append("Improve content organization and flow")
        
        return recommendations
    
    def _prioritize_fixes(self, issues: List[ReviewIssue]) -> List[str]:
        """Prioritize fixes based on issue severity."""
        priority_fixes = []
        
        # Critical issues first
        critical = [i for i in issues if i.severity == ReviewSeverity.CRITICAL]
        for issue in critical:
            priority_fixes.append(f"CRITICAL: {issue.description}")
        
        # Major issues second
        major = [i for i in issues if i.severity == ReviewSeverity.MAJOR]
        for issue in major[:3]:  # Top 3 major issues
            priority_fixes.append(f"MAJOR: {issue.description}")
        
        return priority_fixes
    
    def _calculate_confidence_level(self, scores: List[ReviewScore], issues: List[ReviewIssue]) -> float:
        """Calculate confidence level in the review."""
        if not issues:
            return 0.9
        
        avg_issue_confidence = sum(i.confidence for i in issues) / len(issues)
        score_consistency = 1.0 - (max(s.score for s in scores) - min(s.score for s in scores)) / 4.0
        
        return (avg_issue_confidence + score_consistency) / 2
    
    def _determine_next_review_needs(self, decision: ReviewDecision, issues: List[ReviewIssue]) -> bool:
        """Determine if content needs another review."""
        return decision in [
            ReviewDecision.MAJOR_REVISIONS_REQUIRED,
            ReviewDecision.NEEDS_FACT_CHECK,
            ReviewDecision.NEEDS_LEGAL_REVIEW
        ]
    
    def _update_performance_metrics(self, feedback: ReviewFeedback):
        """Update reviewer performance metrics."""
        self.review_history.append(feedback)
        
        # Update aggregate metrics
        self.performance_metrics["total_content_reviewed"] += len(feedback.original_content.split()) if hasattr(feedback, 'original_content') else 1
        self.performance_metrics["total_issues_identified"] += len(feedback.issues)
        self.performance_metrics["review_sessions"] += 1
        
        # Calculate averages
        total_sessions = self.performance_metrics["review_sessions"]
        
        total_score = sum(review.overall_score for review in self.review_history)
        self.performance_metrics["average_review_score"] = total_score / total_sessions
        
        total_time = sum(review.review_time for review in self.review_history)
        self.performance_metrics["average_review_time"] = total_time / total_sessions
        
        approved_reviews = len([r for r in self.review_history if r.decision == ReviewDecision.APPROVED])
        self.performance_metrics["approval_rate"] = approved_reviews / total_sessions
    
    def get_review_summary(self) -> Dict[str, Any]:
        """Get summary of reviewer capabilities and performance."""
        return {
            "reviewer_type": self.reviewer_type,
            "review_capabilities": self.review_capabilities,
            "specialization_areas": self.specialization_areas,
            "review_standards": self.review_standards,
            "performance_metrics": self.performance_metrics,
            "recent_reviews": len(self.review_history),
            "average_issues_per_review": (
                self.performance_metrics["total_issues_identified"] / 
                max(1, self.performance_metrics["review_sessions"])
            )
        }


# Factory functions for different reviewer types

def create_technical_reviewer(
    specialization_areas: Optional[List[str]] = None,
    review_standards: Optional[Dict[str, float]] = None
) -> ContentReviewerRole:
    """Create a technical content reviewer."""
    return ContentReviewerRole(
        reviewer_type="technical",
        specialization_areas=specialization_areas or ["api_documentation", "code_accuracy", "technical_clarity"],
        review_standards=review_standards or {
            "accuracy": 4.8,
            "completeness": 4.5,
            "clarity": 4.3,
            "consistency": 4.4,
            "grammar": 4.0
        }
    )


def create_editorial_reviewer(
    specialization_areas: Optional[List[str]] = None,
    review_standards: Optional[Dict[str, float]] = None
) -> ContentReviewerRole:
    """Create an editorial content reviewer."""
    return ContentReviewerRole(
        reviewer_type="editorial",
        specialization_areas=specialization_areas or ["content_strategy", "narrative_flow", "audience_alignment"],
        review_standards=review_standards or {
            "clarity": 4.5,
            "engagement": 4.2,
            "structure": 4.3,
            "style": 4.1,
            "grammar": 4.6
        }
    )


def create_brand_reviewer(
    specialization_areas: Optional[List[str]] = None,
    review_standards: Optional[Dict[str, float]] = None
) -> ContentReviewerRole:
    """Create a brand alignment reviewer."""
    return ContentReviewerRole(
        reviewer_type="brand",
        specialization_areas=specialization_areas or ["brand_voice", "messaging_consistency", "brand_safety"],
        review_standards=review_standards or {
            "brand_alignment": 4.7,
            "consistency": 4.5,
            "style": 4.3,
            "engagement": 4.0,
            "clarity": 4.2
        }
    )


def create_seo_reviewer(
    specialization_areas: Optional[List[str]] = None,
    review_standards: Optional[Dict[str, float]] = None
) -> ContentReviewerRole:
    """Create an SEO-focused content reviewer."""
    return ContentReviewerRole(
        reviewer_type="seo",
        specialization_areas=specialization_areas or ["keyword_optimization", "content_structure", "search_intent"],
        review_standards=review_standards or {
            "seo_optimization": 4.5,
            "structure": 4.3,
            "clarity": 4.0,
            "engagement": 4.2,
            "relevance": 4.4
        }
    )


def create_legal_reviewer(
    specialization_areas: Optional[List[str]] = None,
    review_standards: Optional[Dict[str, float]] = None
) -> ContentReviewerRole:
    """Create a legal compliance reviewer."""
    return ContentReviewerRole(
        reviewer_type="legal",
        specialization_areas=specialization_areas or ["compliance_check", "risk_assessment", "regulatory_requirements"],
        review_standards=review_standards or {
            "accuracy": 4.9,
            "completeness": 4.7,
            "consistency": 4.5,
            "clarity": 4.0,
            "grammar": 4.2
        }
    )


def create_general_reviewer(
    specialization_areas: Optional[List[str]] = None,
    review_standards: Optional[Dict[str, float]] = None
) -> ContentReviewerRole:
    """Create a general content reviewer."""
    return ContentReviewerRole(
        reviewer_type="general",
        specialization_areas=specialization_areas or ["quality_assessment", "general_improvement"],
        review_standards=review_standards or {
            "clarity": 4.0,
            "grammar": 4.2,
            "structure": 3.8,
            "consistency": 3.9,
            "overall_quality": 4.0
        }
    )


# Demo function
def demo_content_reviewer():
    """Demonstrate content reviewer capabilities."""
    print("Content Reviewer Demonstration")
    print("=" * 50)
    
    # Create different reviewer types
    reviewers = {
        "Technical": create_technical_reviewer(),
        "Editorial": create_editorial_reviewer(),
        "Brand": create_brand_reviewer(),
        "SEO": create_seo_reviewer()
    }
    
    # Sample content to review
    sample_content = """
    # Getting Started with APIs
    
    APIs are really important for modern applications. They allow different systems to talk to each other and share data.
    
    When your building an API, there are several things you need to consider. First, you need to think about the data format. Most APIs use JSON because its easy to work with.
    
    Here are the main steps:
    1. Design your endpoints
    2. Choose authentication method
    3. Implement error handling
    4. Write documentation
    
    Remember, good APIs are easy to use and well documented. Make sure you test everything before releasing to production.
    """
    
    content_metadata = {
        "id": "api_guide_001",
        "type": "technical_documentation",
        "purpose": "educational",
        "audience": "developers",
        "author": "tech_writer"
    }
    
    for reviewer_name, reviewer in reviewers.items():
        print(f"\n{reviewer_name} Reviewer Analysis:")
        print("-" * 40)
        
        # Perform review
        feedback = reviewer.review_content(sample_content, content_metadata)
        
        print(f"Overall Score: {feedback.overall_score:.2f}/5.0")
        print(f"Decision: {feedback.decision.value}")
        print(f"Issues Found: {len(feedback.issues)}")
        print(f"Review Time: {feedback.review_time:.2f}s")
        
        # Show some key issues
        if feedback.issues:
            print(f"\nKey Issues:")
            for issue in feedback.issues[:3]:
                print(f"  • {issue.severity.value.upper()}: {issue.description}")
                if issue.suggested_fix:
                    print(f"    Fix: {issue.suggested_fix}")
        
        # Show strengths
        if feedback.strengths:
            print(f"\nStrengths:")
            for strength in feedback.strengths[:2]:
                print(f"  • {strength}")
        
        # Show recommendations
        if feedback.recommended_actions:
            print(f"\nRecommendations:")
            for rec in feedback.recommended_actions[:2]:
                print(f"  • {rec}")


if __name__ == "__main__":
    demo_content_reviewer()