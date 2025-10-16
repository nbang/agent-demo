"""Writer Agent Role

Specialized writer agent role for content creation with various writing capabilities
and content generation expertise.
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from src.agents.multi_agent.agent_roles import RoleDefinition, create_role_definition
from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class WritingStyle(Enum):
    """Different writing styles supported."""
    FORMAL = "formal"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    PERSUASIVE = "persuasive"
    ACADEMIC = "academic"
    JOURNALISTIC = "journalistic"
    CASUAL = "casual"


class ContentGenre(Enum):
    """Content genres for writing specialization."""
    ARTICLE = "article"
    BLOG_POST = "blog_post"
    TECHNICAL_DOCUMENT = "technical_document"
    MARKETING_COPY = "marketing_copy"
    CREATIVE_CONTENT = "creative_content"
    EDUCATIONAL_CONTENT = "educational_content"
    NEWS_CONTENT = "news_content"
    SOCIAL_MEDIA = "social_media"


@dataclass
class WritingCapability:
    """Represents a specific writing capability."""
    name: str
    description: str
    proficiency_level: float  # 0.0 to 1.0
    applicable_genres: List[ContentGenre]
    applicable_styles: List[WritingStyle]
    
    def is_applicable_for(self, genre: ContentGenre, style: WritingStyle) -> bool:
        """Check if capability applies to specific genre and style."""
        return genre in self.applicable_genres and style in self.applicable_styles


@dataclass
class WritingOutput:
    """Represents writer output with metadata."""
    content: str
    word_count: int
    writing_style: WritingStyle
    content_genre: ContentGenre
    quality_metrics: Dict[str, float]
    writing_time: float
    capabilities_used: List[str]
    metadata: Dict[str, Any]


class WriterRole:
    """Specialized writer agent role for content creation."""
    
    def __init__(
        self,
        writer_type: str = "general",
        specialization_areas: Optional[List[str]] = None,
        quality_standards: Optional[Dict[str, float]] = None
    ):
        """Initialize writer role.
        
        Args:
            writer_type: Type of writer (general, technical, creative, etc.)
            specialization_areas: Specific areas of writing expertise
            quality_standards: Quality thresholds for different metrics
        """
        self.writer_type = writer_type
        self.specialization_areas = specialization_areas or []
        self.quality_standards = quality_standards or {
            "readability": 4.0,
            "engagement": 3.5,
            "accuracy": 4.5,
            "creativity": 3.0,
            "structure": 4.0
        }
        
        # Initialize capabilities based on writer type
        self.capabilities = self._initialize_capabilities()
        
        # Create role definition
        self.role_definition = self._create_role_definition()
        
        # Initialize metrics tracking
        self.writing_history = []
        self.performance_metrics = {
            "total_words_written": 0,
            "average_quality_score": 0.0,
            "content_pieces_created": 0,
            "average_writing_time": 0.0
        }
        
        logger.info(f"Writer role initialized: {writer_type} with {len(self.capabilities)} capabilities")
    
    def _initialize_capabilities(self) -> List[WritingCapability]:
        """Initialize writing capabilities based on writer type."""
        capabilities = []
        
        # Base capabilities for all writers
        base_capabilities = [
            WritingCapability(
                name="content_structuring",
                description="Organize content with clear structure and logical flow",
                proficiency_level=0.8,
                applicable_genres=list(ContentGenre),
                applicable_styles=list(WritingStyle)
            ),
            WritingCapability(
                name="audience_adaptation",
                description="Adapt content tone and style for target audience",
                proficiency_level=0.7,
                applicable_genres=list(ContentGenre),
                applicable_styles=list(WritingStyle)
            ),
            WritingCapability(
                name="grammar_proficiency",
                description="Maintain proper grammar, spelling, and syntax",
                proficiency_level=0.9,
                applicable_genres=list(ContentGenre),
                applicable_styles=list(WritingStyle)
            )
        ]
        
        capabilities.extend(base_capabilities)
        
        # Add specialized capabilities based on writer type
        if self.writer_type == "technical":
            technical_capabilities = [
                WritingCapability(
                    name="technical_documentation",
                    description="Create clear, accurate technical documentation",
                    proficiency_level=0.9,
                    applicable_genres=[ContentGenre.TECHNICAL_DOCUMENT, ContentGenre.EDUCATIONAL_CONTENT],
                    applicable_styles=[WritingStyle.TECHNICAL, WritingStyle.FORMAL]
                ),
                WritingCapability(
                    name="complex_concept_explanation",
                    description="Explain complex technical concepts clearly",
                    proficiency_level=0.85,
                    applicable_genres=[ContentGenre.TECHNICAL_DOCUMENT, ContentGenre.ARTICLE, ContentGenre.EDUCATIONAL_CONTENT],
                    applicable_styles=[WritingStyle.TECHNICAL, WritingStyle.FORMAL, WritingStyle.CONVERSATIONAL]
                ),
                WritingCapability(
                    name="api_documentation",
                    description="Write comprehensive API and code documentation",
                    proficiency_level=0.8,
                    applicable_genres=[ContentGenre.TECHNICAL_DOCUMENT],
                    applicable_styles=[WritingStyle.TECHNICAL]
                )
            ]
            capabilities.extend(technical_capabilities)
        
        elif self.writer_type == "creative":
            creative_capabilities = [
                WritingCapability(
                    name="storytelling",
                    description="Create engaging narratives and stories",
                    proficiency_level=0.9,
                    applicable_genres=[ContentGenre.CREATIVE_CONTENT, ContentGenre.BLOG_POST, ContentGenre.MARKETING_COPY],
                    applicable_styles=[WritingStyle.CREATIVE, WritingStyle.CONVERSATIONAL]
                ),
                WritingCapability(
                    name="emotional_engagement",
                    description="Create emotionally resonant content",
                    proficiency_level=0.85,
                    applicable_genres=[ContentGenre.CREATIVE_CONTENT, ContentGenre.MARKETING_COPY, ContentGenre.BLOG_POST],
                    applicable_styles=[WritingStyle.CREATIVE, WritingStyle.PERSUASIVE, WritingStyle.CONVERSATIONAL]
                ),
                WritingCapability(
                    name="metaphor_and_imagery",
                    description="Use effective metaphors and vivid imagery",
                    proficiency_level=0.8,
                    applicable_genres=[ContentGenre.CREATIVE_CONTENT, ContentGenre.MARKETING_COPY],
                    applicable_styles=[WritingStyle.CREATIVE, WritingStyle.PERSUASIVE]
                )
            ]
            capabilities.extend(creative_capabilities)
        
        elif self.writer_type == "marketing":
            marketing_capabilities = [
                WritingCapability(
                    name="persuasive_writing",
                    description="Create compelling, persuasive content",
                    proficiency_level=0.9,
                    applicable_genres=[ContentGenre.MARKETING_COPY, ContentGenre.SOCIAL_MEDIA],
                    applicable_styles=[WritingStyle.PERSUASIVE, WritingStyle.CONVERSATIONAL]
                ),
                WritingCapability(
                    name="call_to_action",
                    description="Write effective calls-to-action",
                    proficiency_level=0.85,
                    applicable_genres=[ContentGenre.MARKETING_COPY, ContentGenre.SOCIAL_MEDIA, ContentGenre.BLOG_POST],
                    applicable_styles=[WritingStyle.PERSUASIVE, WritingStyle.CONVERSATIONAL]
                ),
                WritingCapability(
                    name="brand_voice_adaptation",
                    description="Adapt writing to match brand voice and personality",
                    proficiency_level=0.8,
                    applicable_genres=[ContentGenre.MARKETING_COPY, ContentGenre.SOCIAL_MEDIA, ContentGenre.BLOG_POST],
                    applicable_styles=[WritingStyle.PERSUASIVE, WritingStyle.CONVERSATIONAL, WritingStyle.CASUAL]
                )
            ]
            capabilities.extend(marketing_capabilities)
        
        elif self.writer_type == "academic":
            academic_capabilities = [
                WritingCapability(
                    name="research_integration",
                    description="Integrate research findings into coherent arguments",
                    proficiency_level=0.9,
                    applicable_genres=[ContentGenre.ARTICLE, ContentGenre.EDUCATIONAL_CONTENT, ContentGenre.TECHNICAL_DOCUMENT],
                    applicable_styles=[WritingStyle.ACADEMIC, WritingStyle.FORMAL]
                ),
                WritingCapability(
                    name="citation_and_referencing",
                    description="Proper citation and academic referencing",
                    proficiency_level=0.85,
                    applicable_genres=[ContentGenre.ARTICLE, ContentGenre.EDUCATIONAL_CONTENT],
                    applicable_styles=[WritingStyle.ACADEMIC, WritingStyle.FORMAL]
                ),
                WritingCapability(
                    name="analytical_writing",
                    description="Create analytical and critical content",
                    proficiency_level=0.8,
                    applicable_genres=[ContentGenre.ARTICLE, ContentGenre.EDUCATIONAL_CONTENT],
                    applicable_styles=[WritingStyle.ACADEMIC, WritingStyle.FORMAL, WritingStyle.TECHNICAL]
                )
            ]
            capabilities.extend(academic_capabilities)
        
        elif self.writer_type == "journalistic":
            journalistic_capabilities = [
                WritingCapability(
                    name="news_writing",
                    description="Write clear, factual news content",
                    proficiency_level=0.9,
                    applicable_genres=[ContentGenre.NEWS_CONTENT, ContentGenre.ARTICLE],
                    applicable_styles=[WritingStyle.JOURNALISTIC, WritingStyle.FORMAL]
                ),
                WritingCapability(
                    name="fact_verification",
                    description="Verify and present factual information accurately",
                    proficiency_level=0.85,
                    applicable_genres=[ContentGenre.NEWS_CONTENT, ContentGenre.ARTICLE],
                    applicable_styles=[WritingStyle.JOURNALISTIC, WritingStyle.FORMAL]
                ),
                WritingCapability(
                    name="interview_integration",
                    description="Integrate quotes and interviews effectively",
                    proficiency_level=0.8,
                    applicable_genres=[ContentGenre.NEWS_CONTENT, ContentGenre.ARTICLE],
                    applicable_styles=[WritingStyle.JOURNALISTIC, WritingStyle.CONVERSATIONAL]
                )
            ]
            capabilities.extend(journalistic_capabilities)
        
        # Add general capabilities for all non-general writers
        if self.writer_type != "general":
            general_capabilities = [
                WritingCapability(
                    name="seo_optimization",
                    description="Optimize content for search engines",
                    proficiency_level=0.6,
                    applicable_genres=[ContentGenre.BLOG_POST, ContentGenre.ARTICLE, ContentGenre.MARKETING_COPY],
                    applicable_styles=[WritingStyle.CONVERSATIONAL, WritingStyle.FORMAL, WritingStyle.PERSUASIVE]
                ),
                WritingCapability(
                    name="headline_creation",
                    description="Create compelling headlines and titles",
                    proficiency_level=0.7,
                    applicable_genres=list(ContentGenre),
                    applicable_styles=list(WritingStyle)
                )
            ]
            capabilities.extend(general_capabilities)
        
        return capabilities
    
    def _create_role_definition(self) -> RoleDefinition:
        """Create role definition for the writer."""
        expertise_areas = [
            "content_writing",
            "audience_engagement", 
            "content_structuring",
            "grammar_proficiency"
        ]
        
        # Add specialized expertise areas
        if self.writer_type == "technical":
            expertise_areas.extend([
                "technical_documentation",
                "complex_concept_explanation",
                "api_documentation"
            ])
        elif self.writer_type == "creative":
            expertise_areas.extend([
                "storytelling",
                "emotional_engagement",
                "creative_expression"
            ])
        elif self.writer_type == "marketing":
            expertise_areas.extend([
                "persuasive_writing",
                "call_to_action",
                "brand_voice_adaptation"
            ])
        elif self.writer_type == "academic":
            expertise_areas.extend([
                "research_integration",
                "citation_and_referencing",
                "analytical_writing"
            ])
        elif self.writer_type == "journalistic":
            expertise_areas.extend([
                "news_writing",
                "fact_verification",
                "interview_integration"
            ])
        
        # Add custom specialization areas
        expertise_areas.extend(self.specialization_areas)
        
        responsibilities = [
            "Create high-quality written content based on requirements",
            "Adapt writing style and tone to target audience",
            "Ensure proper grammar, spelling, and syntax",
            "Structure content for maximum readability and engagement",
            "Collaborate with research and editorial teams",
            "Meet quality standards and deadlines",
            "Incorporate feedback and revisions effectively"
        ]
        
        interaction_patterns = [
            "collaborates_with_researchers",
            "works_with_editors",
            "receives_feedback_from_reviewers",
            "adapts_content_based_on_requirements",
            "coordinates_with_content_team"
        ]
        
        return create_role_definition(
            name=f"{self.writer_type.title()} Writer",
            description=f"Specialized writer focused on {self.writer_type} content creation with expertise in audience engagement and quality writing",
            expertise_areas=expertise_areas,
            responsibilities=responsibilities,
            interaction_patterns=interaction_patterns
        )
    
    def write_content(
        self,
        topic: str,
        requirements: Dict[str, Any],
        research_data: Optional[Dict[str, Any]] = None,
        style_guide: Optional[Dict[str, Any]] = None
    ) -> WritingOutput:
        """Write content based on topic and requirements.
        
        Args:
            topic: Main topic for content
            requirements: Content requirements (length, style, audience, etc.)
            research_data: Research information to incorporate
            style_guide: Style guide to follow
            
        Returns:
            WritingOutput with created content and metadata
        """
        logger.info(f"Starting content writing for topic: {topic}")
        
        start_time = time.time()
        
        try:
            # Parse requirements
            word_count_target = requirements.get("word_count", 800)
            writing_style = WritingStyle(requirements.get("style", "conversational"))
            content_genre = ContentGenre(requirements.get("genre", "article"))
            target_audience = requirements.get("audience", "general")
            tone = requirements.get("tone", "neutral")
            
            # Select applicable capabilities
            applicable_capabilities = [
                cap for cap in self.capabilities 
                if cap.is_applicable_for(content_genre, writing_style)
            ]
            
            logger.info(f"Using {len(applicable_capabilities)} applicable capabilities")
            
            # Generate content
            content = self._generate_content(
                topic=topic,
                word_count_target=word_count_target,
                writing_style=writing_style,
                content_genre=content_genre,
                target_audience=target_audience,
                tone=tone,
                research_data=research_data,
                style_guide=style_guide,
                capabilities=applicable_capabilities
            )
            
            # Calculate metrics
            writing_time = time.time() - start_time
            word_count = len(content.split())
            
            # Evaluate content quality
            quality_metrics = self._evaluate_content_quality(
                content, writing_style, content_genre, requirements
            )
            
            # Create output
            output = WritingOutput(
                content=content,
                word_count=word_count,
                writing_style=writing_style,
                content_genre=content_genre,
                quality_metrics=quality_metrics,
                writing_time=writing_time,
                capabilities_used=[cap.name for cap in applicable_capabilities],
                metadata={
                    "topic": topic,
                    "target_audience": target_audience,
                    "tone": tone,
                    "writer_type": self.writer_type,
                    "requirements_met": self._check_requirements_compliance(content, requirements),
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # Update performance tracking
            self._update_performance_metrics(output)
            
            logger.info(f"Content writing completed in {writing_time:.2f}s")
            logger.info(f"Quality score: {quality_metrics.get('overall_score', 0):.2f}")
            
            return output
            
        except Exception as e:
            logger.error(f"Content writing failed: {str(e)}")
            raise
    
    def _generate_content(
        self,
        topic: str,
        word_count_target: int,
        writing_style: WritingStyle,
        content_genre: ContentGenre,
        target_audience: str,
        tone: str,
        research_data: Optional[Dict[str, Any]],
        style_guide: Optional[Dict[str, Any]],
        capabilities: List[WritingCapability]
    ) -> str:
        """Generate content based on parameters."""
        content_sections = []
        
        # Generate title/headline
        title = self._generate_title(topic, content_genre, writing_style)
        content_sections.append(f"# {title}")
        content_sections.append("")
        
        # Generate introduction
        introduction = self._generate_introduction(
            topic, target_audience, writing_style, content_genre
        )
        content_sections.extend(introduction)
        content_sections.append("")
        
        # Generate main content sections
        main_sections = self._generate_main_content(
            topic, word_count_target, writing_style, content_genre, 
            target_audience, research_data, capabilities
        )
        content_sections.extend(main_sections)
        
        # Generate conclusion
        conclusion = self._generate_conclusion(
            topic, writing_style, content_genre
        )
        content_sections.extend(conclusion)
        
        # Join all sections
        full_content = "\\n".join(content_sections)
        
        # Apply style adjustments
        styled_content = self._apply_style_adjustments(
            full_content, writing_style, tone, style_guide
        )
        
        return styled_content
    
    def _generate_title(self, topic: str, genre: ContentGenre, style: WritingStyle) -> str:
        """Generate appropriate title for content."""
        if genre == ContentGenre.BLOG_POST:
            if style == WritingStyle.CONVERSATIONAL:
                return f"Everything You Need to Know About {topic}"
            elif style == WritingStyle.CREATIVE:
                return f"The Ultimate Guide to {topic}: A Journey of Discovery"
            else:
                return f"Understanding {topic}: A Comprehensive Guide"
        
        elif genre == ContentGenre.TECHNICAL_DOCUMENT:
            return f"{topic}: Technical Overview and Implementation Guide"
        
        elif genre == ContentGenre.MARKETING_COPY:
            return f"Transform Your Business with {topic}"
        
        elif genre == ContentGenre.ARTICLE:
            if style == WritingStyle.ACADEMIC:
                return f"An Analysis of {topic}: Current Trends and Future Implications"
            else:
                return f"The Future of {topic}: Trends, Challenges, and Opportunities"
        
        else:
            return topic
    
    def _generate_introduction(
        self, topic: str, audience: str, style: WritingStyle, genre: ContentGenre
    ) -> List[str]:
        """Generate introduction section."""
        intro_lines = []
        
        if style == WritingStyle.CONVERSATIONAL:
            intro_lines.extend([
                f"Have you ever wondered about {topic}? You're not alone!",
                "",
                f"In today's rapidly evolving world, {topic} has become increasingly important",
                f"for {audience}. Whether you're just getting started or looking to deepen",
                "your understanding, this guide will provide you with the insights you need."
            ])
        
        elif style == WritingStyle.FORMAL or style == WritingStyle.ACADEMIC:
            intro_lines.extend([
                f"The significance of {topic} in contemporary discourse cannot be overstated.",
                f"This analysis examines the key aspects of {topic} and its implications",
                f"for {audience}.",
                "",
                f"Through comprehensive research and analysis, we explore the multifaceted",
                f"nature of {topic} and its potential impact on various stakeholders."
            ])
        
        elif style == WritingStyle.TECHNICAL:
            intro_lines.extend([
                "## Overview",
                "",
                f"This document provides a comprehensive technical overview of {topic},",
                f"including implementation details, best practices, and considerations",
                f"for {audience}.",
                "",
                "### Key Topics Covered",
                f"- Technical specifications and requirements for {topic}",
                "- Implementation strategies and methodologies",
                "- Performance considerations and optimization techniques"
            ])
        
        else:  # Default/Creative
            intro_lines.extend([
                f"In the landscape of modern innovation, {topic} stands as a beacon",
                f"of possibility. For {audience}, understanding this domain opens",
                "doors to new opportunities and insights.",
                "", 
                f"This exploration of {topic} will take you on a journey through",
                "its complexities, revealing the potential that lies within."
            ])
        
        return intro_lines
    
    def _generate_main_content(
        self,
        topic: str,
        word_count_target: int,
        style: WritingStyle,
        genre: ContentGenre,
        audience: str,
        research_data: Optional[Dict[str, Any]],
        capabilities: List[WritingCapability]
    ) -> List[str]:
        """Generate main content sections."""
        content_lines = []
        
        # Calculate target sections based on word count
        sections_needed = max(3, min(8, word_count_target // 200))
        
        # Generate key sections
        sections = [
            "Current State and Overview",
            "Key Benefits and Advantages", 
            "Challenges and Considerations",
            "Best Practices and Recommendations",
            "Future Outlook and Trends",
            "Implementation Strategies",
            "Case Studies and Examples",
            "Technical Considerations"
        ]
        
        # Select appropriate sections based on genre and style
        selected_sections = sections[:sections_needed]
        
        for section_title in selected_sections:
            content_lines.extend([
                f"## {section_title}",
                ""
            ])
            
            # Generate section content
            section_content = self._generate_section_content(
                section_title, topic, style, genre, audience, research_data
            )
            content_lines.extend(section_content)
            content_lines.append("")
        
        return content_lines
    
    def _generate_section_content(
        self,
        section_title: str,
        topic: str,
        style: WritingStyle,
        genre: ContentGenre,
        audience: str,
        research_data: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate content for a specific section."""
        content = []
        
        if "overview" in section_title.lower():
            if style == WritingStyle.TECHNICAL:
                content.extend([
                    f"{topic} represents a comprehensive approach to addressing modern challenges.",
                    "The technical architecture consists of several key components:",
                    "",
                    f"1. **Core Infrastructure**: The foundational elements of {topic}",
                    f"2. **Integration Layer**: Connecting {topic} with existing systems",
                    f"3. **User Interface**: Enabling {audience} to interact effectively",
                    "",
                    "Each component plays a crucial role in the overall functionality and performance."
                ])
            else:
                content.extend([
                    f"Understanding {topic} begins with recognizing its fundamental principles.",
                    f"For {audience}, this means appreciating both the opportunities and",
                    "the complexities involved.",
                    "",
                    f"The current landscape of {topic} is characterized by rapid evolution",
                    "and increasing adoption across various sectors. Key developments include",
                    "technological advances, regulatory changes, and shifting market demands."
                ])
        
        elif "benefit" in section_title.lower():
            content.extend([
                f"The advantages of {topic} are multifaceted and significant:",
                "",
                f"- **Enhanced Efficiency**: {topic} streamlines processes for {audience}",
                f"- **Improved Outcomes**: Better results through optimized approaches",
                f"- **Cost Effectiveness**: Reduced overhead and resource requirements",
                f"- **Scalable Solutions**: Adaptable to growing needs and demands",
                "",
                f"These benefits make {topic} an attractive option for {audience} seeking",
                "to improve their operations and achieve better results."
            ])
        
        elif "challenge" in section_title.lower():
            content.extend([
                f"While {topic} offers significant advantages, it also presents challenges:",
                "",
                f"**Implementation Complexity**: Integrating {topic} requires careful planning",
                f"and coordination across multiple stakeholders.",
                "",
                f"**Resource Requirements**: Success depends on adequate investment in",
                "training, infrastructure, and ongoing support.",
                "",
                f"**Change Management**: {audience} must be prepared to adapt existing",
                "processes and workflows to fully realize the benefits."
            ])
        
        elif "practice" in section_title.lower() or "recommendation" in section_title.lower():
            content.extend([
                f"Based on industry experience and research, these best practices for {topic}",
                f"are recommended for {audience}:",
                "",
                "### Planning and Preparation",
                f"- Conduct thorough assessment of current state and {topic} readiness",
                "- Develop clear objectives and success metrics",
                "- Allocate appropriate resources and timeline",
                "",
                "### Implementation Strategy",
                "- Start with pilot programs to test and refine approaches",
                "- Ensure stakeholder buy-in and support throughout the process",
                "- Maintain focus on user experience and practical outcomes"
            ])
        
        else:
            # Generic section content
            content.extend([
                f"This aspect of {topic} is particularly relevant for {audience}.",
                f"Research and practical experience demonstrate the importance of",
                "taking a comprehensive approach to implementation and management.",
                "",
                f"Key considerations include understanding the specific needs of",
                f"{audience}, evaluating available options, and developing a",
                "sustainable strategy for long-term success."
            ])
        
        return content
    
    def _generate_conclusion(
        self, topic: str, style: WritingStyle, genre: ContentGenre
    ) -> List[str]:
        """Generate conclusion section."""
        conclusion = ["## Conclusion", ""]
        
        if style == WritingStyle.CONVERSATIONAL:
            conclusion.extend([
                f"As we've explored throughout this guide, {topic} offers tremendous",
                "potential for those willing to embrace its possibilities.",
                "",
                "The key to success lies in understanding the fundamentals, preparing",
                "adequately, and taking a thoughtful approach to implementation.",
                "",
                f"Whether you're just beginning your journey with {topic} or looking",
                "to optimize existing approaches, the insights shared here provide",
                "a solid foundation for moving forward."
            ])
        
        elif style == WritingStyle.FORMAL or style == WritingStyle.ACADEMIC:
            conclusion.extend([
                f"This analysis of {topic} reveals both the opportunities and challenges",
                "inherent in this domain. The evidence suggests that success requires",
                "careful planning, adequate resources, and sustained commitment.",
                "",
                f"Future developments in {topic} will likely address current limitations",
                "while expanding capabilities and applications. Organizations that",
                "invest in understanding and implementing these concepts today will",
                "be best positioned to benefit from future advances."
            ])
        
        elif style == WritingStyle.TECHNICAL:
            conclusion.extend([
                "### Summary",
                "",
                f"This technical overview of {topic} has covered the essential",
                "components, implementation considerations, and best practices.",
                "",
                "### Next Steps",
                "- Review technical requirements and system compatibility",
                "- Develop implementation timeline and resource allocation",
                "- Begin with pilot testing and gradual rollout",
                "",
                "For additional technical documentation and support resources,",
                "consult the appendices and reference materials."
            ])
        
        else:
            conclusion.extend([
                f"The journey through {topic} reveals a landscape rich with",
                "possibility and potential. As we've seen, success requires",
                "both vision and practical execution.",
                "",
                f"The future of {topic} promises continued evolution and",
                "expanding opportunities. Those who embrace this domain with",
                "thoughtful preparation and sustained effort will find themselves",
                "at the forefront of meaningful progress."
            ])
        
        return conclusion
    
    def _apply_style_adjustments(
        self, content: str, style: WritingStyle, tone: str, style_guide: Optional[Dict[str, Any]]
    ) -> str:
        """Apply final style adjustments to content."""
        adjusted_content = content
        
        # Apply tone adjustments
        if tone == "friendly":
            adjusted_content = adjusted_content.replace("must", "should")
            adjusted_content = adjusted_content.replace("cannot", "can't")
        elif tone == "authoritative":
            adjusted_content = adjusted_content.replace("might", "will")
            adjusted_content = adjusted_content.replace("could", "should")
        
        # Apply style guide if provided
        if style_guide:
            # Apply any style-specific replacements
            replacements = style_guide.get("replacements", {})
            for old_text, new_text in replacements.items():
                adjusted_content = adjusted_content.replace(old_text, new_text)
        
        return adjusted_content
    
    def _evaluate_content_quality(
        self, content: str, style: WritingStyle, genre: ContentGenre, requirements: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate content quality across multiple dimensions."""
        word_count = len(content.split())
        target_word_count = requirements.get("word_count", 800)
        
        # Calculate quality metrics
        metrics = {}
        
        # Word count compliance
        word_count_ratio = word_count / target_word_count
        metrics["word_count_score"] = max(0.0, min(5.0, 5.0 - abs(1.0 - word_count_ratio) * 2))
        
        # Structure quality (based on headings and organization)
        heading_count = content.count("## ") + content.count("# ")
        expected_headings = max(3, word_count // 200)
        structure_ratio = heading_count / expected_headings
        metrics["structure_score"] = max(0.0, min(5.0, structure_ratio * 5.0))
        
        # Readability (simplified assessment)
        avg_sentence_length = word_count / max(1, content.count("."))
        if avg_sentence_length <= 20:
            metrics["readability_score"] = 5.0
        elif avg_sentence_length <= 30:
            metrics["readability_score"] = 4.0
        else:
            metrics["readability_score"] = 3.0
        
        # Content completeness (based on section coverage)
        essential_sections = ["introduction", "conclusion", "main content"]
        sections_present = sum(1 for section in essential_sections if any(
            keyword in content.lower() for keyword in section.split()
        ))
        metrics["completeness_score"] = (sections_present / len(essential_sections)) * 5.0
        
        # Style consistency (simulated)
        metrics["style_consistency"] = 4.2
        
        # Overall score
        metrics["overall_score"] = sum(metrics.values()) / len(metrics)
        
        return metrics
    
    def _check_requirements_compliance(self, content: str, requirements: Dict[str, Any]) -> Dict[str, bool]:
        """Check if content meets specified requirements."""
        compliance = {}
        
        # Word count requirement
        word_count = len(content.split())
        target_word_count = requirements.get("word_count", 800)
        tolerance = requirements.get("word_count_tolerance", 0.2)
        
        min_words = target_word_count * (1 - tolerance)
        max_words = target_word_count * (1 + tolerance)
        compliance["word_count"] = min_words <= word_count <= max_words
        
        # Structure requirements
        compliance["has_title"] = content.startswith("#")
        compliance["has_sections"] = "## " in content
        compliance["has_conclusion"] = "conclusion" in content.lower()
        
        # Content requirements
        topic = requirements.get("topic", "")
        if topic:
            compliance["topic_covered"] = topic.lower() in content.lower()
        
        return compliance
    
    def _update_performance_metrics(self, output: WritingOutput):
        """Update performance tracking metrics."""
        self.writing_history.append(output)
        
        # Update aggregate metrics
        self.performance_metrics["total_words_written"] += output.word_count
        self.performance_metrics["content_pieces_created"] += 1
        
        # Calculate averages
        total_pieces = self.performance_metrics["content_pieces_created"]
        
        total_quality = sum(
            writing.quality_metrics.get("overall_score", 0) 
            for writing in self.writing_history
        )
        self.performance_metrics["average_quality_score"] = total_quality / total_pieces
        
        total_time = sum(writing.writing_time for writing in self.writing_history)
        self.performance_metrics["average_writing_time"] = total_time / total_pieces
    
    def get_capability_summary(self) -> Dict[str, Any]:
        """Get summary of writer capabilities."""
        return {
            "writer_type": self.writer_type,
            "total_capabilities": len(self.capabilities),
            "specialization_areas": self.specialization_areas,
            "quality_standards": self.quality_standards,
            "capabilities_by_genre": self._group_capabilities_by_genre(),
            "capabilities_by_style": self._group_capabilities_by_style(),
            "performance_metrics": self.performance_metrics
        }
    
    def _group_capabilities_by_genre(self) -> Dict[str, List[str]]:
        """Group capabilities by applicable content genres."""
        genre_mapping = {}
        
        for genre in ContentGenre:
            applicable_caps = [
                cap.name for cap in self.capabilities 
                if genre in cap.applicable_genres
            ]
            genre_mapping[genre.value] = applicable_caps
        
        return genre_mapping
    
    def _group_capabilities_by_style(self) -> Dict[str, List[str]]:
        """Group capabilities by applicable writing styles."""
        style_mapping = {}
        
        for style in WritingStyle:
            applicable_caps = [
                cap.name for cap in self.capabilities 
                if style in cap.applicable_styles
            ]
            style_mapping[style.value] = applicable_caps
        
        return style_mapping


# Factory functions for different writer types

def create_technical_writer(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> WriterRole:
    """Create a technical writer specialized in documentation and technical content."""
    return WriterRole(
        writer_type="technical",
        specialization_areas=specialization_areas or ["api_documentation", "user_guides"],
        quality_standards=quality_standards or {
            "readability": 4.5,
            "accuracy": 5.0,
            "structure": 4.5,
            "completeness": 4.8
        }
    )


def create_creative_writer(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> WriterRole:
    """Create a creative writer specialized in engaging, narrative content."""
    return WriterRole(
        writer_type="creative",
        specialization_areas=specialization_areas or ["storytelling", "brand_narratives"],
        quality_standards=quality_standards or {
            "creativity": 4.8,
            "engagement": 4.5,
            "readability": 4.0,
            "emotional_impact": 4.3
        }
    )


def create_marketing_writer(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> WriterRole:
    """Create a marketing writer specialized in persuasive, conversion-focused content."""
    return WriterRole(
        writer_type="marketing",
        specialization_areas=specialization_areas or ["conversion_copy", "social_media"],
        quality_standards=quality_standards or {
            "persuasiveness": 4.8,
            "engagement": 4.5,
            "clarity": 4.3,
            "call_to_action_effectiveness": 4.7
        }
    )


def create_academic_writer(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> WriterRole:
    """Create an academic writer specialized in research-based, analytical content."""
    return WriterRole(
        writer_type="academic",
        specialization_areas=specialization_areas or ["research_papers", "analytical_reports"],
        quality_standards=quality_standards or {
            "accuracy": 5.0,
            "analytical_depth": 4.8,
            "citation_quality": 4.7,
            "structure": 4.5
        }
    )


def create_journalistic_writer(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> WriterRole:
    """Create a journalistic writer specialized in news and factual reporting."""
    return WriterRole(
        writer_type="journalistic",
        specialization_areas=specialization_areas or ["news_reporting", "feature_articles"],
        quality_standards=quality_standards or {
            "accuracy": 5.0,
            "objectivity": 4.8,
            "clarity": 4.5,
            "fact_verification": 4.9
        }
    )


def create_general_writer(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> WriterRole:
    """Create a general writer with broad content creation capabilities."""
    return WriterRole(
        writer_type="general",
        specialization_areas=specialization_areas or ["versatile_content", "audience_adaptation"],
        quality_standards=quality_standards or {
            "readability": 4.0,
            "engagement": 3.8,
            "accuracy": 4.2,
            "structure": 4.0
        }
    )


# Demo function
def demo_writer_roles():
    """Demonstrate different writer roles and capabilities."""
    print("Writer Role Demonstration")
    print("=" * 50)
    
    # Test different writer types
    writers = {
        "Technical": create_technical_writer(),
        "Creative": create_creative_writer(),
        "Marketing": create_marketing_writer(),
        "Academic": create_academic_writer(),
        "Journalistic": create_journalistic_writer()
    }
    
    topic = "Artificial Intelligence in Healthcare"
    
    for writer_name, writer in writers.items():
        print(f"\\n{writer_name} Writer:")
        print("-" * 30)
        
        # Show capabilities
        summary = writer.get_capability_summary()
        print(f"Capabilities: {summary['total_capabilities']}")
        print(f"Specializations: {', '.join(summary['specialization_areas'])}")
        
        # Test writing
        requirements = {
            "word_count": 500,
            "style": "formal" if writer_name == "Academic" else "conversational",
            "genre": "article",
            "audience": "healthcare professionals",
            "tone": "professional"
        }
        
        output = writer.write_content(topic, requirements)
        
        print(f"\\nContent generated:")
        print(f"Word count: {output.word_count}")
        print(f"Quality score: {output.quality_metrics['overall_score']:.2f}")
        print(f"Writing time: {output.writing_time:.2f}s")
        
        # Show content preview
        preview = output.content[:200] + "..." if len(output.content) > 200 else output.content
        print(f"\\nPreview:\\n{preview}")


if __name__ == "__main__":
    demo_writer_roles()