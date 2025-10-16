"""Content Templates System

Comprehensive content template system for different content types with customizable
structure, guidelines, and best practices for consistent content creation.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class TemplateType(Enum):
    """Different types of content templates."""
    BLOG_POST = "blog_post"
    ARTICLE = "article"
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    API_DOCUMENTATION = "api_documentation"
    TUTORIAL = "tutorial"
    HOW_TO_GUIDE = "how_to_guide"
    CASE_STUDY = "case_study"
    WHITE_PAPER = "white_paper"
    MARKETING_COPY = "marketing_copy"
    LANDING_PAGE = "landing_page"
    EMAIL_CAMPAIGN = "email_campaign"
    SOCIAL_MEDIA_POST = "social_media_post"
    PRESS_RELEASE = "press_release"
    PRODUCT_DESCRIPTION = "product_description"
    FAQ = "faq"
    README = "readme"


class SectionType(Enum):
    """Types of content sections."""
    TITLE = "title"
    SUBTITLE = "subtitle"
    INTRODUCTION = "introduction"
    OVERVIEW = "overview"
    BACKGROUND = "background"
    PROBLEM_STATEMENT = "problem_statement"
    SOLUTION = "solution"
    MAIN_CONTENT = "main_content"
    STEPS = "steps"
    EXAMPLES = "examples"
    CODE_BLOCKS = "code_blocks"
    BENEFITS = "benefits"
    FEATURES = "features"
    USE_CASES = "use_cases"
    BEST_PRACTICES = "best_practices"
    TROUBLESHOOTING = "troubleshooting"
    FAQ_SECTION = "faq_section"
    CONCLUSION = "conclusion"
    CALL_TO_ACTION = "call_to_action"
    NEXT_STEPS = "next_steps"
    REFERENCES = "references"
    RELATED_RESOURCES = "related_resources"


@dataclass
class TemplateSection:
    """Represents a section in a content template."""
    section_type: SectionType
    title: str
    description: str
    is_required: bool
    order: int
    guidelines: List[str]
    examples: List[str] = field(default_factory=list)
    word_count_range: Optional[Tuple[int, int]] = None
    formatting_rules: Optional[Dict[str, Any]] = None
    placeholder_content: Optional[str] = None


@dataclass
class TemplateGuidelines:
    """Guidelines for using a content template."""
    tone: List[str]  # e.g., ["professional", "friendly", "authoritative"]
    style: List[str]  # e.g., ["concise", "detailed", "conversational"]
    target_audience: List[str]
    content_goals: List[str]
    seo_requirements: Optional[Dict[str, Any]] = None
    formatting_requirements: Optional[Dict[str, Any]] = None
    brand_requirements: Optional[Dict[str, Any]] = None
    accessibility_requirements: Optional[Dict[str, Any]] = None


@dataclass
class ContentTemplate:
    """Complete content template with structure and guidelines."""
    template_id: str
    template_type: TemplateType
    name: str
    description: str
    sections: List[TemplateSection]
    guidelines: TemplateGuidelines
    word_count_range: Tuple[int, int]
    estimated_time_hours: float
    difficulty_level: str  # beginner, intermediate, advanced
    tags: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0"


class ContentTemplateSystem:
    """System for managing and using content templates."""
    
    def __init__(self):
        """Initialize content template system."""
        self.templates = {}
        self._initialize_default_templates()
        logger.info("Content template system initialized with default templates")
    
    def _initialize_default_templates(self):
        """Initialize default content templates."""
        # Blog Post Template
        self.templates["blog_post"] = self._create_blog_post_template()
        
        # Technical Documentation Template
        self.templates["technical_documentation"] = self._create_technical_documentation_template()
        
        # Tutorial Template
        self.templates["tutorial"] = self._create_tutorial_template()
        
        # How-To Guide Template
        self.templates["how_to_guide"] = self._create_how_to_guide_template()
        
        # Marketing Copy Template
        self.templates["marketing_copy"] = self._create_marketing_copy_template()
        
        # Article Template
        self.templates["article"] = self._create_article_template()
        
        # API Documentation Template
        self.templates["api_documentation"] = self._create_api_documentation_template()
        
        # Case Study Template
        self.templates["case_study"] = self._create_case_study_template()
        
        # White Paper Template
        self.templates["white_paper"] = self._create_white_paper_template()
        
        # Landing Page Template
        self.templates["landing_page"] = self._create_landing_page_template()
        
        # README Template
        self.templates["readme"] = self._create_readme_template()
        
        # Product Description Template
        self.templates["product_description"] = self._create_product_description_template()
    
    def _create_blog_post_template(self) -> ContentTemplate:
        """Create blog post template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Blog Post Title",
                description="Compelling, SEO-optimized title that captures attention",
                is_required=True,
                order=1,
                guidelines=[
                    "Keep title between 50-60 characters for SEO",
                    "Include primary keyword near the beginning",
                    "Make it compelling and click-worthy",
                    "Use numbers or power words when appropriate"
                ],
                examples=[
                    "10 Proven Strategies to Boost Your Productivity in 2024",
                    "The Complete Guide to Getting Started with AI Agents"
                ],
                word_count_range=(8, 15),
                placeholder_content="# [Your Compelling Blog Post Title Here]"
            ),
            TemplateSection(
                section_type=SectionType.INTRODUCTION,
                title="Introduction",
                description="Hook readers and introduce the topic",
                is_required=True,
                order=2,
                guidelines=[
                    "Start with a hook (question, statistic, or compelling statement)",
                    "Explain why the topic matters to the reader",
                    "Preview what the post will cover",
                    "Keep it concise (2-3 paragraphs)"
                ],
                examples=[
                    "Did you know that 80% of professionals struggle with...?",
                    "In today's fast-paced digital world..."
                ],
                word_count_range=(100, 200),
                placeholder_content="Introduction paragraph that hooks the reader..."
            ),
            TemplateSection(
                section_type=SectionType.MAIN_CONTENT,
                title="Main Content",
                description="Core content with subheadings and detailed information",
                is_required=True,
                order=3,
                guidelines=[
                    "Use H2 and H3 subheadings for structure",
                    "Break content into digestible sections",
                    "Include examples, data, or anecdotes",
                    "Use bullet points and lists for clarity",
                    "Add images or visuals to support points"
                ],
                examples=[
                    "## Key Point 1\nDetailed explanation...",
                    "### Subpoint\nSupporting details..."
                ],
                word_count_range=(500, 1500),
                placeholder_content="## Main Section\n\nDetailed content here..."
            ),
            TemplateSection(
                section_type=SectionType.EXAMPLES,
                title="Examples or Case Studies",
                description="Real-world examples to illustrate concepts",
                is_required=False,
                order=4,
                guidelines=[
                    "Provide concrete, relatable examples",
                    "Use real data or case studies when possible",
                    "Show before/after or comparison scenarios"
                ],
                word_count_range=(100, 300)
            ),
            TemplateSection(
                section_type=SectionType.CONCLUSION,
                title="Conclusion",
                description="Summarize key takeaways and wrap up",
                is_required=True,
                order=5,
                guidelines=[
                    "Recap main points briefly",
                    "Reinforce the value for the reader",
                    "Lead naturally into the CTA"
                ],
                word_count_range=(100, 150),
                placeholder_content="In conclusion, we've covered..."
            ),
            TemplateSection(
                section_type=SectionType.CALL_TO_ACTION,
                title="Call to Action",
                description="Encourage reader to take next step",
                is_required=True,
                order=6,
                guidelines=[
                    "Be clear and specific about the action",
                    "Create urgency or emphasize value",
                    "Make it easy to take action"
                ],
                examples=[
                    "Ready to get started? Download our free guide today!",
                    "What's your experience with this? Share in the comments below!"
                ],
                word_count_range=(20, 50)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["conversational", "friendly", "authoritative"],
            style=["engaging", "accessible", "scannable"],
            target_audience=["general readers", "blog subscribers", "industry professionals"],
            content_goals=[
                "Educate and inform readers",
                "Drive engagement and comments",
                "Improve SEO rankings",
                "Establish thought leadership"
            ],
            seo_requirements={
                "primary_keyword": "Include in title, first paragraph, and H2 headings",
                "meta_description": "150-160 characters with primary keyword",
                "internal_links": "3-5 relevant internal links",
                "external_links": "2-3 authoritative external sources",
                "image_alt_text": "Descriptive alt text with keywords"
            },
            formatting_requirements={
                "paragraph_length": "3-5 sentences maximum",
                "heading_structure": "H1 (title), H2 (main sections), H3 (subsections)",
                "lists": "Use bulleted or numbered lists for readability",
                "whitespace": "Plenty of whitespace between sections"
            }
        )
        
        return ContentTemplate(
            template_id="blog_post_v1",
            template_type=TemplateType.BLOG_POST,
            name="Standard Blog Post",
            description="Comprehensive template for creating engaging, SEO-optimized blog posts",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(800, 2000),
            estimated_time_hours=3.0,
            difficulty_level="beginner",
            tags=["blog", "content_marketing", "seo", "engagement"]
        )
    
    def _create_technical_documentation_template(self) -> ContentTemplate:
        """Create technical documentation template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Documentation Title",
                description="Clear, descriptive title indicating the topic",
                is_required=True,
                order=1,
                guidelines=[
                    "Be specific and descriptive",
                    "Use consistent naming conventions",
                    "Include version number if applicable"
                ],
                examples=["User Authentication Guide v2.0", "API Integration Documentation"],
                placeholder_content="# [Feature/Component Name] Documentation"
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Overview",
                description="High-level description of the feature or component",
                is_required=True,
                order=2,
                guidelines=[
                    "Explain what it is and its purpose",
                    "Describe key capabilities",
                    "Mention prerequisites if any",
                    "Keep it concise (1-2 paragraphs)"
                ],
                word_count_range=(100, 200),
                placeholder_content="## Overview\n\nThis document describes..."
            ),
            TemplateSection(
                section_type=SectionType.STEPS,
                title="Getting Started / Installation",
                description="Step-by-step instructions for setup",
                is_required=True,
                order=3,
                guidelines=[
                    "Number each step clearly",
                    "Include all necessary commands",
                    "Specify system requirements",
                    "Mention common issues and solutions"
                ],
                examples=[
                    "1. Install the package: `npm install package-name`",
                    "2. Configure your environment..."
                ],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.CODE_BLOCKS,
                title="Code Examples",
                description="Practical code examples demonstrating usage",
                is_required=True,
                order=4,
                guidelines=[
                    "Provide complete, runnable examples",
                    "Include comments explaining key parts",
                    "Show common use cases",
                    "Use proper syntax highlighting"
                ],
                examples=[
                    "```python\n# Example usage\nfrom module import function\nresult = function(param)\n```"
                ],
                word_count_range=(100, 300)
            ),
            TemplateSection(
                section_type=SectionType.BEST_PRACTICES,
                title="Best Practices",
                description="Recommended approaches and patterns",
                is_required=False,
                order=5,
                guidelines=[
                    "List do's and don'ts",
                    "Explain why certain approaches are better",
                    "Include security considerations"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.TROUBLESHOOTING,
                title="Troubleshooting",
                description="Common issues and solutions",
                is_required=False,
                order=6,
                guidelines=[
                    "List common error messages",
                    "Provide clear solutions for each",
                    "Include debugging tips"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.REFERENCES,
                title="Additional Resources",
                description="Links to related documentation and resources",
                is_required=False,
                order=7,
                guidelines=[
                    "Link to related documentation",
                    "Include API references",
                    "Add external resources"
                ],
                word_count_range=(50, 100)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["technical", "precise", "instructional"],
            style=["clear", "concise", "structured"],
            target_audience=["developers", "technical users", "system administrators"],
            content_goals=[
                "Enable users to implement the feature",
                "Reduce support requests",
                "Provide comprehensive reference",
                "Ensure technical accuracy"
            ],
            formatting_requirements={
                "code_blocks": "Use proper syntax highlighting",
                "inline_code": "Use backticks for inline code",
                "section_numbering": "Optional but recommended for complex docs",
                "table_of_contents": "Include for documents over 1000 words"
            }
        )
        
        return ContentTemplate(
            template_id="technical_documentation_v1",
            template_type=TemplateType.TECHNICAL_DOCUMENTATION,
            name="Technical Documentation",
            description="Comprehensive template for technical documentation and guides",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(1000, 3000),
            estimated_time_hours=5.0,
            difficulty_level="intermediate",
            tags=["technical", "documentation", "developer", "guide"]
        )
    
    def _create_tutorial_template(self) -> ContentTemplate:
        """Create tutorial template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Tutorial Title",
                description="Action-oriented title describing what users will learn",
                is_required=True,
                order=1,
                guidelines=[
                    "Start with 'How to' or describe the outcome",
                    "Be specific about what will be achieved",
                    "Keep it clear and actionable"
                ],
                examples=[
                    "How to Build a REST API with Python in 30 Minutes",
                    "Creating Your First Machine Learning Model"
                ],
                placeholder_content="# How to [Achieve Specific Goal]"
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="What You'll Learn",
                description="Clear outline of learning objectives",
                is_required=True,
                order=2,
                guidelines=[
                    "List specific skills or knowledge to be gained",
                    "Set clear expectations",
                    "Mention the time required",
                    "Specify prerequisite knowledge"
                ],
                word_count_range=(100, 200),
                placeholder_content="## What You'll Learn\n\nBy the end of this tutorial, you will be able to..."
            ),
            TemplateSection(
                section_type=SectionType.STEPS,
                title="Prerequisites",
                description="Required tools, knowledge, and setup",
                is_required=True,
                order=3,
                guidelines=[
                    "List all required software/tools",
                    "Specify knowledge prerequisites",
                    "Include setup instructions",
                    "Provide download links"
                ],
                word_count_range=(100, 300)
            ),
            TemplateSection(
                section_type=SectionType.STEPS,
                title="Step-by-Step Instructions",
                description="Detailed, numbered steps to follow",
                is_required=True,
                order=4,
                guidelines=[
                    "Break down into clear, actionable steps",
                    "Include screenshots or visuals",
                    "Explain what each step accomplishes",
                    "Show expected results after each step",
                    "Use consistent formatting"
                ],
                examples=[
                    "## Step 1: Set Up Your Environment\n\nFirst, we'll...",
                    "## Step 2: Create the Basic Structure\n\nNext, you'll..."
                ],
                word_count_range=(600, 1500)
            ),
            TemplateSection(
                section_type=SectionType.CODE_BLOCKS,
                title="Complete Code Example",
                description="Full working code for reference",
                is_required=True,
                order=5,
                guidelines=[
                    "Provide complete, tested code",
                    "Add comments for clarity",
                    "Include error handling",
                    "Make it copy-paste ready"
                ],
                word_count_range=(100, 500)
            ),
            TemplateSection(
                section_type=SectionType.NEXT_STEPS,
                title="Next Steps & Further Learning",
                description="Suggestions for continued learning",
                is_required=False,
                order=6,
                guidelines=[
                    "Suggest related tutorials",
                    "Recommend advanced topics",
                    "Provide additional resources"
                ],
                word_count_range=(100, 200)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["instructional", "encouraging", "supportive"],
            style=["step-by-step", "detailed", "beginner-friendly"],
            target_audience=["learners", "beginners", "developers"],
            content_goals=[
                "Enable hands-on learning",
                "Build practical skills",
                "Provide clear, actionable steps",
                "Boost learner confidence"
            ],
            formatting_requirements={
                "step_numbering": "Use clear numbering for steps",
                "visual_aids": "Include screenshots or diagrams",
                "code_formatting": "Use syntax highlighting",
                "progress_indicators": "Show what step user is on"
            }
        )
        
        return ContentTemplate(
            template_id="tutorial_v1",
            template_type=TemplateType.TUTORIAL,
            name="Step-by-Step Tutorial",
            description="Comprehensive template for creating educational tutorials",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(1000, 2500),
            estimated_time_hours=4.0,
            difficulty_level="intermediate",
            tags=["tutorial", "education", "hands-on", "learning"]
        )
    
    def _create_how_to_guide_template(self) -> ContentTemplate:
        """Create how-to guide template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="How-To Title",
                description="Clear title starting with 'How to'",
                is_required=True,
                order=1,
                guidelines=[
                    "Start with 'How to'",
                    "Describe the specific task",
                    "Keep it under 70 characters"
                ],
                examples=["How to Reset Your Password", "How to Configure SSL Certificates"],
                placeholder_content="# How to [Specific Task]"
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Introduction",
                description="Brief explanation of the task and when you'd need it",
                is_required=True,
                order=2,
                guidelines=[
                    "Explain what the guide covers",
                    "Mention why it's useful",
                    "Estimate time required"
                ],
                word_count_range=(50, 150)
            ),
            TemplateSection(
                section_type=SectionType.STEPS,
                title="Instructions",
                description="Clear, numbered steps to complete the task",
                is_required=True,
                order=3,
                guidelines=[
                    "Use numbered list format",
                    "One action per step",
                    "Be specific and concise",
                    "Include warnings or tips where needed"
                ],
                word_count_range=(200, 600)
            ),
            TemplateSection(
                section_type=SectionType.TROUBLESHOOTING,
                title="Troubleshooting",
                description="Common issues and solutions",
                is_required=False,
                order=4,
                guidelines=[
                    "List potential problems",
                    "Provide quick solutions",
                    "Link to detailed support if needed"
                ],
                word_count_range=(100, 300)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["direct", "helpful", "clear"],
            style=["concise", "actionable", "practical"],
            target_audience=["end users", "customers", "general audience"],
            content_goals=[
                "Help users complete a specific task",
                "Minimize confusion",
                "Reduce support tickets",
                "Provide quick solutions"
            ]
        )
        
        return ContentTemplate(
            template_id="how_to_guide_v1",
            template_type=TemplateType.HOW_TO_GUIDE,
            name="How-To Guide",
            description="Quick, practical guide for completing specific tasks",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(300, 1000),
            estimated_time_hours=2.0,
            difficulty_level="beginner",
            tags=["how-to", "guide", "practical", "task-based"]
        )
    
    def _create_marketing_copy_template(self) -> ContentTemplate:
        """Create marketing copy template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Headline",
                description="Attention-grabbing headline that highlights main benefit",
                is_required=True,
                order=1,
                guidelines=[
                    "Focus on the main benefit or transformation",
                    "Use power words and emotional triggers",
                    "Keep it punchy and memorable",
                    "Test multiple versions"
                ],
                examples=[
                    "Transform Your Business with AI in Just 30 Days",
                    "The Simple Solution to Complex Data Problems"
                ],
                word_count_range=(5, 15)
            ),
            TemplateSection(
                section_type=SectionType.SUBTITLE,
                title="Subheadline",
                description="Supporting headline that expands on the main benefit",
                is_required=False,
                order=2,
                guidelines=[
                    "Elaborate on the main headline",
                    "Add credibility or specifics",
                    "Address target audience directly"
                ],
                word_count_range=(10, 25)
            ),
            TemplateSection(
                section_type=SectionType.PROBLEM_STATEMENT,
                title="Problem/Pain Point",
                description="Identify and articulate the customer's problem",
                is_required=True,
                order=3,
                guidelines=[
                    "Show empathy and understanding",
                    "Use customer language",
                    "Make it relatable and specific",
                    "Amplify the pain (ethically)"
                ],
                word_count_range=(100, 200)
            ),
            TemplateSection(
                section_type=SectionType.SOLUTION,
                title="Solution",
                description="Present your product/service as the solution",
                is_required=True,
                order=4,
                guidelines=[
                    "Connect directly to the stated problem",
                    "Highlight unique value proposition",
                    "Use benefit-focused language",
                    "Show transformation clearly"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.BENEFITS,
                title="Benefits & Features",
                description="Key benefits and supporting features",
                is_required=True,
                order=5,
                guidelines=[
                    "Lead with benefits, support with features",
                    "Use bullet points for scannability",
                    "Quantify benefits when possible",
                    "Focus on outcomes, not just features"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.EXAMPLES,
                title="Social Proof",
                description="Testimonials, case studies, or statistics",
                is_required=False,
                order=6,
                guidelines=[
                    "Use real customer testimonials",
                    "Include specific results/numbers",
                    "Add credibility indicators (logos, certifications)",
                    "Show diverse success stories"
                ],
                word_count_range=(100, 250)
            ),
            TemplateSection(
                section_type=SectionType.CALL_TO_ACTION,
                title="Call to Action",
                description="Clear, compelling CTA that drives conversion",
                is_required=True,
                order=7,
                guidelines=[
                    "Use action verbs",
                    "Create urgency or scarcity",
                    "Make it specific and clear",
                    "Reduce friction (e.g., 'No credit card required')",
                    "Test different CTAs"
                ],
                examples=[
                    "Start Your Free Trial Today - No Credit Card Required",
                    "Join 10,000+ Happy Customers - Get Started Now"
                ],
                word_count_range=(10, 30)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["persuasive", "benefits-focused", "compelling"],
            style=["concise", "scannable", "conversion-focused"],
            target_audience=["prospects", "potential customers", "decision makers"],
            content_goals=[
                "Drive conversions",
                "Communicate value clearly",
                "Overcome objections",
                "Build trust and credibility"
            ],
            formatting_requirements={
                "headline_formatting": "Large, bold, attention-grabbing",
                "bullet_points": "Use for benefits and features",
                "cta_placement": "Multiple CTAs throughout page",
                "visual_hierarchy": "Clear visual flow guiding to CTA"
            }
        )
        
        return ContentTemplate(
            template_id="marketing_copy_v1",
            template_type=TemplateType.MARKETING_COPY,
            name="Marketing Copy",
            description="Persuasive marketing copy template for landing pages and campaigns",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(400, 1000),
            estimated_time_hours=3.0,
            difficulty_level="intermediate",
            tags=["marketing", "copywriting", "conversion", "sales"]
        )
    
    def _create_article_template(self) -> ContentTemplate:
        """Create long-form article template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Article Title",
                description="Engaging, informative title",
                is_required=True,
                order=1,
                guidelines=[
                    "Be specific and descriptive",
                    "Consider SEO keywords",
                    "Make it compelling"
                ],
                word_count_range=(8, 15)
            ),
            TemplateSection(
                section_type=SectionType.INTRODUCTION,
                title="Introduction",
                description="Engaging introduction that sets context",
                is_required=True,
                order=2,
                guidelines=[
                    "Hook the reader with compelling opening",
                    "Provide context and background",
                    "State the article's purpose",
                    "Preview main points"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.BACKGROUND,
                title="Background/Context",
                description="Necessary background information",
                is_required=False,
                order=3,
                guidelines=[
                    "Provide historical context if relevant",
                    "Explain key concepts",
                    "Set the stage for main content"
                ],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.MAIN_CONTENT,
                title="Main Content Sections",
                description="Core content organized in logical sections",
                is_required=True,
                order=4,
                guidelines=[
                    "Use clear H2 headings for main sections",
                    "Support arguments with evidence",
                    "Include data, research, or expert quotes",
                    "Maintain logical flow between sections"
                ],
                word_count_range=(1000, 2500)
            ),
            TemplateSection(
                section_type=SectionType.EXAMPLES,
                title="Case Studies or Examples",
                description="Real-world examples or case studies",
                is_required=False,
                order=5,
                guidelines=[
                    "Use specific, relevant examples",
                    "Include data or results",
                    "Make it relatable to audience"
                ],
                word_count_range=(200, 500)
            ),
            TemplateSection(
                section_type=SectionType.CONCLUSION,
                title="Conclusion",
                description="Summary and final thoughts",
                is_required=True,
                order=6,
                guidelines=[
                    "Recap key points",
                    "Provide final insights",
                    "Look forward or suggest implications",
                    "End with thought-provoking statement"
                ],
                word_count_range=(150, 300)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["authoritative", "informative", "engaging"],
            style=["in-depth", "well-researched", "thoughtful"],
            target_audience=["informed readers", "professionals", "enthusiasts"],
            content_goals=[
                "Educate and inform deeply",
                "Establish authority",
                "Provide comprehensive coverage",
                "Spark discussion"
            ]
        )
        
        return ContentTemplate(
            template_id="article_v1",
            template_type=TemplateType.ARTICLE,
            name="Long-Form Article",
            description="Comprehensive template for in-depth articles",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(1500, 3500),
            estimated_time_hours=6.0,
            difficulty_level="advanced",
            tags=["article", "long-form", "in-depth", "editorial"]
        )
    
    def _create_api_documentation_template(self) -> ContentTemplate:
        """Create API documentation template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="API Name",
                description="Clear API endpoint or feature name",
                is_required=True,
                order=1,
                guidelines=["Use consistent naming", "Include version if applicable"],
                placeholder_content="# API Endpoint: /api/v1/resource"
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Description",
                description="What the API endpoint does",
                is_required=True,
                order=2,
                guidelines=["Explain purpose clearly", "Mention use cases"],
                word_count_range=(50, 150)
            ),
            TemplateSection(
                section_type=SectionType.CODE_BLOCKS,
                title="Request Format",
                description="Request structure and parameters",
                is_required=True,
                order=3,
                guidelines=[
                    "Show HTTP method",
                    "List all parameters with types",
                    "Mark required vs optional",
                    "Include example request"
                ],
                word_count_range=(100, 300)
            ),
            TemplateSection(
                section_type=SectionType.CODE_BLOCKS,
                title="Response Format",
                description="Response structure and examples",
                is_required=True,
                order=4,
                guidelines=[
                    "Show response schema",
                    "Include status codes",
                    "Provide example responses",
                    "Document error responses"
                ],
                word_count_range=(100, 300)
            ),
            TemplateSection(
                section_type=SectionType.EXAMPLES,
                title="Code Examples",
                description="Implementation examples in various languages",
                is_required=True,
                order=5,
                guidelines=[
                    "Provide examples in popular languages",
                    "Include complete, working code",
                    "Show authentication if needed"
                ],
                word_count_range=(150, 400)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["technical", "precise", "comprehensive"],
            style=["structured", "reference", "detailed"],
            target_audience=["developers", "API users", "integration engineers"],
            content_goals=["Enable API integration", "Reduce integration errors", "Provide complete reference"]
        )
        
        return ContentTemplate(
            template_id="api_documentation_v1",
            template_type=TemplateType.API_DOCUMENTATION,
            name="API Documentation",
            description="Template for documenting API endpoints",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(500, 1500),
            estimated_time_hours=3.0,
            difficulty_level="advanced",
            tags=["api", "documentation", "technical", "reference"]
        )
    
    def _create_case_study_template(self) -> ContentTemplate:
        """Create case study template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Case Study Title",
                description="Client name or compelling outcome",
                is_required=True,
                order=1,
                guidelines=["Highlight the result", "Use specific numbers if possible"],
                examples=["How Company X Increased Revenue by 300%"],
                word_count_range=(8, 15)
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Executive Summary",
                description="Quick overview of the case",
                is_required=True,
                order=2,
                guidelines=["Summarize key results", "Mention client", "State timeframe"],
                word_count_range=(100, 200)
            ),
            TemplateSection(
                section_type=SectionType.BACKGROUND,
                title="Client Background",
                description="Information about the client",
                is_required=True,
                order=3,
                guidelines=["Describe client's industry", "Mention size/scale", "Provide context"],
                word_count_range=(100, 200)
            ),
            TemplateSection(
                section_type=SectionType.PROBLEM_STATEMENT,
                title="Challenge/Problem",
                description="What problem the client faced",
                is_required=True,
                order=4,
                guidelines=[
                    "Describe the specific challenge",
                    "Explain impact on business",
                    "Include quantitative data if possible"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.SOLUTION,
                title="Solution",
                description="How you addressed the problem",
                is_required=True,
                order=5,
                guidelines=[
                    "Describe your approach",
                    "Explain implementation process",
                    "Highlight unique aspects"
                ],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.USE_CASES,
                title="Results",
                description="Quantifiable outcomes and impact",
                is_required=True,
                order=6,
                guidelines=[
                    "Use specific numbers and metrics",
                    "Show before/after comparison",
                    "Include client testimonial if possible",
                    "Highlight multiple success metrics"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.CONCLUSION,
                title="Conclusion",
                description="Key takeaways and next steps",
                is_required=True,
                order=7,
                guidelines=["Summarize success", "Mention ongoing partnership", "Include CTA"],
                word_count_range=(100, 200)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["professional", "results-focused", "credible"],
            style=["story-driven", "data-backed", "persuasive"],
            target_audience=["prospects", "decision makers", "stakeholders"],
            content_goals=[
                "Demonstrate value and results",
                "Build credibility and trust",
                "Inspire prospects to take action",
                "Showcase expertise"
            ]
        )
        
        return ContentTemplate(
            template_id="case_study_v1",
            template_type=TemplateType.CASE_STUDY,
            name="Case Study",
            description="Template for client success stories and case studies",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(800, 1500),
            estimated_time_hours=4.0,
            difficulty_level="intermediate",
            tags=["case-study", "success-story", "social-proof", "results"]
        )
    
    def _create_white_paper_template(self) -> ContentTemplate:
        """Create white paper template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="White Paper Title",
                description="Authoritative, specific title",
                is_required=True,
                order=1,
                guidelines=["Be descriptive and authoritative", "Include key topic/solution"],
                word_count_range=(8, 15)
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Executive Summary",
                description="High-level overview for decision makers",
                is_required=True,
                order=2,
                guidelines=[
                    "Summarize key findings",
                    "Highlight main recommendations",
                    "Keep it standalone (some only read this)"
                ],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.INTRODUCTION,
                title="Introduction",
                description="Context and purpose of the white paper",
                is_required=True,
                order=3,
                guidelines=[
                    "Explain the problem or opportunity",
                    "State objectives",
                    "Outline structure"
                ],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.BACKGROUND,
                title="Background/Context",
                description="Industry context and relevant background",
                is_required=True,
                order=4,
                guidelines=[
                    "Provide market context",
                    "Include relevant trends",
                    "Cite authoritative sources"
                ],
                word_count_range=(300, 600)
            ),
            TemplateSection(
                section_type=SectionType.MAIN_CONTENT,
                title="Analysis & Findings",
                description="Detailed analysis and research findings",
                is_required=True,
                order=5,
                guidelines=[
                    "Present data and research",
                    "Include charts/graphs",
                    "Maintain objectivity",
                    "Support all claims with evidence"
                ],
                word_count_range=(1000, 2000)
            ),
            TemplateSection(
                section_type=SectionType.SOLUTION,
                title="Recommendations/Solution",
                description="Recommended approach or solution",
                is_required=True,
                order=6,
                guidelines=[
                    "Present clear recommendations",
                    "Explain implementation considerations",
                    "Address potential objections"
                ],
                word_count_range=(400, 800)
            ),
            TemplateSection(
                section_type=SectionType.CONCLUSION,
                title="Conclusion",
                description="Summary and final thoughts",
                is_required=True,
                order=7,
                guidelines=["Recap key points", "Reinforce recommendations", "Include next steps"],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.REFERENCES,
                title="References",
                description="Citations and sources",
                is_required=True,
                order=8,
                guidelines=["List all sources", "Use consistent citation format", "Include authoritative sources"],
                word_count_range=(100, 300)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["authoritative", "objective", "research-based"],
            style=["formal", "comprehensive", "data-driven"],
            target_audience=["decision makers", "executives", "industry professionals"],
            content_goals=[
                "Establish thought leadership",
                "Educate on complex topics",
                "Influence decision making",
                "Generate qualified leads"
            ]
        )
        
        return ContentTemplate(
            template_id="white_paper_v1",
            template_type=TemplateType.WHITE_PAPER,
            name="White Paper",
            description="Authoritative white paper template for thought leadership",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(2500, 5000),
            estimated_time_hours=10.0,
            difficulty_level="advanced",
            tags=["white-paper", "thought-leadership", "research", "b2b"]
        )
    
    def _create_landing_page_template(self) -> ContentTemplate:
        """Create landing page template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Hero Headline",
                description="Main value proposition",
                is_required=True,
                order=1,
                guidelines=[
                    "Focus on main benefit",
                    "Be clear and specific",
                    "Create immediate interest"
                ],
                word_count_range=(5, 12)
            ),
            TemplateSection(
                section_type=SectionType.SUBTITLE,
                title="Hero Subheadline",
                description="Supporting benefit statement",
                is_required=True,
                order=2,
                guidelines=["Expand on headline", "Add credibility", "Address audience directly"],
                word_count_range=(10, 20)
            ),
            TemplateSection(
                section_type=SectionType.CALL_TO_ACTION,
                title="Primary CTA",
                description="Main call to action",
                is_required=True,
                order=3,
                guidelines=["Use action verb", "Create urgency", "Make benefit clear"],
                word_count_range=(3, 8)
            ),
            TemplateSection(
                section_type=SectionType.BENEFITS,
                title="Key Benefits",
                description="3-5 main benefits with icons",
                is_required=True,
                order=4,
                guidelines=["Focus on outcomes", "Use short, scannable text", "Include visual icons"],
                word_count_range=(100, 200)
            ),
            TemplateSection(
                section_type=SectionType.FEATURES,
                title="Features Section",
                description="Product/service features",
                is_required=True,
                order=5,
                guidelines=["Lead with benefit", "Support with feature", "Use visuals"],
                word_count_range=(200, 400)
            ),
            TemplateSection(
                section_type=SectionType.EXAMPLES,
                title="Social Proof",
                description="Testimonials and trust indicators",
                is_required=True,
                order=6,
                guidelines=[
                    "Include specific results",
                    "Use real names and photos",
                    "Show variety of customers"
                ],
                word_count_range=(150, 300)
            ),
            TemplateSection(
                section_type=SectionType.CALL_TO_ACTION,
                title="Secondary CTA",
                description="Closing call to action",
                is_required=True,
                order=7,
                guidelines=["Reinforce main CTA", "Remove final objections", "Create urgency"],
                word_count_range=(50, 150)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["persuasive", "benefit-focused", "urgent"],
            style=["scannable", "visual", "conversion-optimized"],
            target_audience=["prospects", "visitors", "leads"],
            content_goals=["Drive conversions", "Capture leads", "Communicate value quickly", "Remove objections"]
        )
        
        return ContentTemplate(
            template_id="landing_page_v1",
            template_type=TemplateType.LANDING_PAGE,
            name="Landing Page",
            description="Conversion-optimized landing page template",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(500, 1200),
            estimated_time_hours=4.0,
            difficulty_level="intermediate",
            tags=["landing-page", "conversion", "marketing", "lead-generation"]
        )
    
    def _create_readme_template(self) -> ContentTemplate:
        """Create README template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Project Title",
                description="Project name with optional badge/logo",
                is_required=True,
                order=1,
                guidelines=["Use H1 heading", "Add badges if applicable", "Include logo/icon"],
                placeholder_content="# Project Name"
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Description",
                description="Brief project description",
                is_required=True,
                order=2,
                guidelines=["Explain what it does", "Mention key features", "State purpose"],
                word_count_range=(50, 150)
            ),
            TemplateSection(
                section_type=SectionType.FEATURES,
                title="Features",
                description="Key features list",
                is_required=False,
                order=3,
                guidelines=["Use bullet points", "Highlight unique features", "Be concise"],
                word_count_range=(50, 200)
            ),
            TemplateSection(
                section_type=SectionType.STEPS,
                title="Installation",
                description="How to install",
                is_required=True,
                order=4,
                guidelines=["Provide step-by-step", "Include commands", "Mention prerequisites"],
                word_count_range=(100, 300)
            ),
            TemplateSection(
                section_type=SectionType.CODE_BLOCKS,
                title="Usage",
                description="Basic usage examples",
                is_required=True,
                order=5,
                guidelines=["Show common use cases", "Include code examples", "Keep it simple"],
                word_count_range=(100, 400)
            ),
            TemplateSection(
                section_type=SectionType.RELATED_RESOURCES,
                title="Documentation",
                description="Link to additional docs",
                is_required=False,
                order=6,
                guidelines=["Link to full documentation", "Mention API reference", "Include wiki if available"],
                word_count_range=(50, 100)
            ),
            TemplateSection(
                section_type=SectionType.RELATED_RESOURCES,
                title="Contributing",
                description="How to contribute",
                is_required=False,
                order=7,
                guidelines=["Welcome contributors", "Link to guidelines", "Explain process"],
                word_count_range=(50, 150)
            ),
            TemplateSection(
                section_type=SectionType.RELATED_RESOURCES,
                title="License",
                description="License information",
                is_required=True,
                order=8,
                guidelines=["State license type", "Link to LICENSE file"],
                word_count_range=(20, 50)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["informative", "welcoming", "direct"],
            style=["structured", "scannable", "developer-friendly"],
            target_audience=["developers", "contributors", "users"],
            content_goals=["Help users get started", "Encourage contribution", "Provide quick reference"]
        )
        
        return ContentTemplate(
            template_id="readme_v1",
            template_type=TemplateType.README,
            name="README",
            description="Project README template for GitHub/GitLab",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(400, 1500),
            estimated_time_hours=2.0,
            difficulty_level="beginner",
            tags=["readme", "documentation", "github", "open-source"]
        )
    
    def _create_product_description_template(self) -> ContentTemplate:
        """Create product description template."""
        sections = [
            TemplateSection(
                section_type=SectionType.TITLE,
                title="Product Name",
                description="Clear product name",
                is_required=True,
                order=1,
                guidelines=["Use official product name", "Keep it clear"],
                word_count_range=(2, 8)
            ),
            TemplateSection(
                section_type=SectionType.OVERVIEW,
                title="Short Description",
                description="Brief, compelling overview",
                is_required=True,
                order=2,
                guidelines=[
                    "Lead with main benefit",
                    "Include key features",
                    "Keep under 160 characters for SEO"
                ],
                word_count_range=(20, 40)
            ),
            TemplateSection(
                section_type=SectionType.FEATURES,
                title="Key Features",
                description="Bulleted list of features",
                is_required=True,
                order=3,
                guidelines=["Use bullet points", "Start with benefit", "Be specific"],
                word_count_range=(50, 150)
            ),
            TemplateSection(
                section_type=SectionType.BENEFITS,
                title="Benefits",
                description="How it improves customer's life",
                is_required=True,
                order=4,
                guidelines=["Focus on outcomes", "Use emotional appeals", "Address pain points"],
                word_count_range=(100, 200)
            ),
            TemplateSection(
                section_type=SectionType.USE_CASES,
                title="Use Cases",
                description="How customers can use it",
                is_required=False,
                order=5,
                guidelines=["Give specific examples", "Make it relatable", "Show versatility"],
                word_count_range=(50, 150)
            ),
            TemplateSection(
                section_type=SectionType.CALL_TO_ACTION,
                title="Call to Action",
                description="Purchase or learn more CTA",
                is_required=True,
                order=6,
                guidelines=["Create urgency", "Remove friction", "Be clear about next step"],
                word_count_range=(10, 30)
            )
        ]
        
        guidelines = TemplateGuidelines(
            tone=["persuasive", "enthusiastic", "customer-focused"],
            style=["scannable", "benefit-driven", "concise"],
            target_audience=["shoppers", "buyers", "researchers"],
            content_goals=["Drive purchases", "Communicate value", "Improve SEO", "Reduce returns"]
        )
        
        return ContentTemplate(
            template_id="product_description_v1",
            template_type=TemplateType.PRODUCT_DESCRIPTION,
            name="Product Description",
            description="E-commerce product description template",
            sections=sections,
            guidelines=guidelines,
            word_count_range=(250, 600),
            estimated_time_hours=1.5,
            difficulty_level="beginner",
            tags=["ecommerce", "product", "sales", "seo"]
        )
    
    def get_template(self, template_key: str) -> Optional[ContentTemplate]:
        """Get a specific template by key."""
        return self.templates.get(template_key)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates."""
        return [
            {
                "key": key,
                "name": template.name,
                "type": template.template_type.value,
                "description": template.description,
                "word_count": template.word_count_range,
                "difficulty": template.difficulty_level,
                "tags": template.tags
            }
            for key, template in self.templates.items()
        ]
    
    def get_templates_by_type(self, template_type: TemplateType) -> List[ContentTemplate]:
        """Get all templates of a specific type."""
        return [
            template for template in self.templates.values()
            if template.template_type == template_type
        ]
    
    def get_templates_by_difficulty(self, difficulty: str) -> List[ContentTemplate]:
        """Get templates by difficulty level."""
        return [
            template for template in self.templates.values()
            if template.difficulty_level == difficulty
        ]
    
    def generate_content_outline(self, template_key: str) -> str:
        """Generate a content outline from a template."""
        template = self.get_template(template_key)
        if not template:
            return ""
        
        outline = f"# {template.name} Outline\n\n"
        outline += f"**Estimated Word Count**: {template.word_count_range[0]}-{template.word_count_range[1]} words\n"
        outline += f"**Estimated Time**: {template.estimated_time_hours} hours\n\n"
        
        outline += "## Content Structure:\n\n"
        
        for section in template.sections:
            required = " (Required)" if section.is_required else " (Optional)"
            outline += f"### {section.order}. {section.title}{required}\n"
            outline += f"*{section.description}*\n\n"
            
            if section.word_count_range:
                outline += f"Word Count: {section.word_count_range[0]}-{section.word_count_range[1]} words\n\n"
            
            if section.guidelines:
                outline += "**Guidelines:**\n"
                for guideline in section.guidelines:
                    outline += f"- {guideline}\n"
                outline += "\n"
            
            if section.placeholder_content:
                outline += f"```\n{section.placeholder_content}\n```\n\n"
        
        return outline
    
    def get_template_guidelines_summary(self, template_key: str) -> Dict[str, Any]:
        """Get summary of template guidelines."""
        template = self.get_template(template_key)
        if not template:
            return {}
        
        return {
            "template_name": template.name,
            "tone": template.guidelines.tone,
            "style": template.guidelines.style,
            "target_audience": template.guidelines.target_audience,
            "content_goals": template.guidelines.content_goals,
            "seo_requirements": template.guidelines.seo_requirements,
            "formatting_requirements": template.guidelines.formatting_requirements
        }


# Demo function
def demo_template_system():
    """Demonstrate template system capabilities."""
    print("Content Template System Demonstration")
    print("=" * 60)
    
    system = ContentTemplateSystem()
    
    # List all templates
    print("\nAvailable Templates:")
    print("-" * 40)
    templates = system.list_templates()
    for template in templates:
        print(f"\n• {template['name']}")
        print(f"  Type: {template['type']}")
        print(f"  Words: {template['word_count'][0]}-{template['word_count'][1]}")
        print(f"  Difficulty: {template['difficulty']}")
        print(f"  Tags: {', '.join(template['tags'][:3])}")
    
    # Show detailed outline for blog post
    print("\n\n" + "=" * 60)
    print("Blog Post Template Outline:")
    print("=" * 60)
    outline = system.generate_content_outline("blog_post")
    print(outline)
    
    # Show guidelines for technical documentation
    print("\n" + "=" * 60)
    print("Technical Documentation Guidelines:")
    print("=" * 60)
    guidelines = system.get_template_guidelines_summary("technical_documentation")
    print(f"\nTone: {', '.join(guidelines['tone'])}")
    print(f"Style: {', '.join(guidelines['style'])}")
    print(f"Target Audience: {', '.join(guidelines['target_audience'])}")
    print(f"\nContent Goals:")
    for goal in guidelines['content_goals']:
        print(f"  • {goal}")


if __name__ == "__main__":
    demo_template_system()
