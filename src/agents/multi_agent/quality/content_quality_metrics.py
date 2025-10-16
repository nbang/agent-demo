"""Content Quality Metrics System

Comprehensive quality assessment system for content evaluation with multiple 
dimensions including readability, accuracy, engagement, style consistency, 
and SEO optimization.
"""

import re
import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class QualityDimension(Enum):
    """Different dimensions of content quality."""
    READABILITY = "readability"
    ACCURACY = "accuracy"
    ENGAGEMENT = "engagement"
    STYLE_CONSISTENCY = "style_consistency"
    SEO_OPTIMIZATION = "seo_optimization"
    GRAMMAR = "grammar"
    STRUCTURE = "structure"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    ORIGINALITY = "originality"


class ReadabilityMetric(Enum):
    """Readability measurement methods."""
    FLESCH_READING_EASE = "flesch_reading_ease"
    FLESCH_KINCAID_GRADE = "flesch_kincaid_grade"
    GUNNING_FOG = "gunning_fog"
    SMOG_INDEX = "smog_index"
    COLEMAN_LIAU = "coleman_liau"
    AUTOMATED_READABILITY = "automated_readability"


@dataclass
class ReadabilityScore:
    """Readability assessment results."""
    flesch_reading_ease: float  # 0-100, higher is easier
    flesch_kincaid_grade: float  # US grade level
    gunning_fog_index: float  # Years of education needed
    smog_index: float  # Years of education needed
    average_sentence_length: float
    average_word_length: float
    complex_word_percentage: float
    overall_readability_score: float  # 0-10 normalized score
    readability_level: str  # very easy, easy, medium, difficult, very difficult


@dataclass
class SEOMetrics:
    """SEO optimization metrics."""
    keyword_density: Dict[str, float]
    primary_keyword_score: float
    title_optimization_score: float
    meta_description_score: float
    heading_structure_score: float
    content_length_score: float
    internal_links_count: int
    external_links_count: int
    image_alt_text_score: float
    url_optimization_score: float
    overall_seo_score: float  # 0-100


@dataclass
class EngagementMetrics:
    """Content engagement potential metrics."""
    hook_strength: float  # 0-10, opening paragraph strength
    emotional_impact_score: float  # 0-10
    storytelling_score: float  # 0-10
    call_to_action_score: float  # 0-10
    question_count: int
    personal_pronoun_usage: float  # Percentage
    power_word_count: int
    overall_engagement_score: float  # 0-10


@dataclass
class StyleConsistencyMetrics:
    """Style and tone consistency metrics."""
    tone_consistency_score: float  # 0-10
    voice_consistency_score: float  # 0-10
    terminology_consistency_score: float  # 0-10
    formatting_consistency_score: float  # 0-10
    brand_alignment_score: float  # 0-10
    style_guide_compliance_score: float  # 0-10
    overall_style_score: float  # 0-10


@dataclass
class StructureMetrics:
    """Content structure and organization metrics."""
    has_title: bool
    title_quality_score: float  # 0-10
    has_introduction: bool
    has_conclusion: bool
    heading_hierarchy_score: float  # 0-10
    paragraph_length_score: float  # 0-10
    section_balance_score: float  # 0-10
    logical_flow_score: float  # 0-10
    overall_structure_score: float  # 0-10


@dataclass
class GrammarMetrics:
    """Grammar and language mechanics metrics."""
    spelling_errors: int
    grammar_errors: int
    punctuation_errors: int
    style_issues: int
    total_issues: int
    error_density: float  # Errors per 100 words
    grammar_score: float  # 0-10, 10 is perfect


@dataclass
class ContentQualityReport:
    """Comprehensive content quality assessment report."""
    content_id: str
    content_type: str
    word_count: int
    character_count: int
    
    # Dimension scores
    readability: ReadabilityScore
    seo_metrics: SEOMetrics
    engagement: EngagementMetrics
    style_consistency: StyleConsistencyMetrics
    structure: StructureMetrics
    grammar: GrammarMetrics
    
    # Overall scores
    overall_quality_score: float  # 0-100
    dimension_scores: Dict[QualityDimension, float]
    
    # Recommendations
    strengths: List[str]
    weaknesses: List[str]
    improvement_recommendations: List[str]
    
    # Metadata
    assessed_at: datetime
    assessment_duration: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContentQualityAnalyzer:
    """Comprehensive content quality assessment system."""
    
    def __init__(
        self,
        quality_standards: Optional[Dict[str, float]] = None,
        weights: Optional[Dict[QualityDimension, float]] = None
    ):
        """Initialize content quality analyzer.
        
        Args:
            quality_standards: Minimum scores for each dimension
            weights: Importance weights for different dimensions
        """
        self.quality_standards = quality_standards or {
            "readability": 6.0,
            "seo": 70.0,
            "engagement": 6.0,
            "style_consistency": 7.0,
            "structure": 7.0,
            "grammar": 8.0
        }
        
        self.weights = weights or {
            QualityDimension.READABILITY: 1.0,
            QualityDimension.SEO_OPTIMIZATION: 0.8,
            QualityDimension.ENGAGEMENT: 0.9,
            QualityDimension.STYLE_CONSISTENCY: 0.7,
            QualityDimension.STRUCTURE: 0.9,
            QualityDimension.GRAMMAR: 1.0
        }
        
        # Common power words for engagement
        self.power_words = {
            'amazing', 'proven', 'discover', 'secret', 'essential', 'ultimate',
            'exclusive', 'guaranteed', 'powerful', 'effective', 'revolutionary',
            'incredible', 'breakthrough', 'transform', 'boost', 'skyrocket',
            'unlock', 'master', 'dominate', 'crush', 'epic', 'brilliant'
        }
        
        # Complex words (3+ syllables) for readability
        self.complex_word_indicators = [
            'tion', 'sion', 'ness', 'ment', 'ical', 'ious', 'eous'
        ]
        
        logger.info("Content quality analyzer initialized")
    
    def analyze_content(
        self,
        content: str,
        content_metadata: Optional[Dict[str, Any]] = None,
        target_keywords: Optional[List[str]] = None
    ) -> ContentQualityReport:
        """Perform comprehensive content quality analysis.
        
        Args:
            content: Content to analyze
            content_metadata: Metadata about the content
            target_keywords: Target keywords for SEO analysis
            
        Returns:
            ContentQualityReport with comprehensive quality assessment
        """
        import time
        start_time = time.time()
        
        logger.info(f"Starting content quality analysis - {len(content.split())} words")
        
        content_metadata = content_metadata or {}
        content_id = content_metadata.get("id", f"content_{int(time.time())}")
        content_type = content_metadata.get("type", "general")
        
        # Calculate basic metrics
        word_count = len(content.split())
        character_count = len(content)
        
        # Analyze each dimension
        readability = self._analyze_readability(content)
        seo_metrics = self._analyze_seo(content, target_keywords)
        engagement = self._analyze_engagement(content)
        style_consistency = self._analyze_style_consistency(content, content_metadata)
        structure = self._analyze_structure(content)
        grammar = self._analyze_grammar(content)
        
        # Calculate dimension scores (normalized to 0-10)
        dimension_scores = {
            QualityDimension.READABILITY: readability.overall_readability_score,
            QualityDimension.SEO_OPTIMIZATION: seo_metrics.overall_seo_score / 10,
            QualityDimension.ENGAGEMENT: engagement.overall_engagement_score,
            QualityDimension.STYLE_CONSISTENCY: style_consistency.overall_style_score,
            QualityDimension.STRUCTURE: structure.overall_structure_score,
            QualityDimension.GRAMMAR: grammar.grammar_score
        }
        
        # Calculate overall quality score (weighted average, scaled to 0-100)
        overall_quality_score = self._calculate_overall_score(dimension_scores)
        
        # Generate insights
        strengths = self._identify_strengths(dimension_scores, readability, seo_metrics, engagement)
        weaknesses = self._identify_weaknesses(dimension_scores, readability, seo_metrics, grammar)
        recommendations = self._generate_recommendations(
            dimension_scores, readability, seo_metrics, engagement, structure, grammar
        )
        
        assessment_duration = time.time() - start_time
        
        report = ContentQualityReport(
            content_id=content_id,
            content_type=content_type,
            word_count=word_count,
            character_count=character_count,
            readability=readability,
            seo_metrics=seo_metrics,
            engagement=engagement,
            style_consistency=style_consistency,
            structure=structure,
            grammar=grammar,
            overall_quality_score=overall_quality_score,
            dimension_scores=dimension_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_recommendations=recommendations,
            assessed_at=datetime.now(),
            assessment_duration=assessment_duration,
            metadata=content_metadata
        )
        
        logger.info(f"Content quality analysis completed in {assessment_duration:.2f}s")
        logger.info(f"Overall quality score: {overall_quality_score:.1f}/100")
        
        return report
    
    def _analyze_readability(self, content: str) -> ReadabilityScore:
        """Analyze content readability using multiple metrics."""
        sentences = self._split_sentences(content)
        words = content.split()
        
        # Basic calculations
        sentence_count = len(sentences)
        word_count = len(words)
        syllable_count = sum(self._count_syllables(word) for word in words)
        
        # Avoid division by zero
        if sentence_count == 0 or word_count == 0:
            return ReadabilityScore(
                flesch_reading_ease=0,
                flesch_kincaid_grade=0,
                gunning_fog_index=0,
                smog_index=0,
                average_sentence_length=0,
                average_word_length=0,
                complex_word_percentage=0,
                overall_readability_score=0,
                readability_level="unknown"
            )
        
        # Calculate averages
        avg_sentence_length = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count
        avg_word_length = sum(len(word) for word in words) / word_count
        
        # Flesch Reading Ease (0-100, higher is easier)
        flesch_reading_ease = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_reading_ease = max(0, min(100, flesch_reading_ease))
        
        # Flesch-Kincaid Grade Level
        flesch_kincaid_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        flesch_kincaid_grade = max(0, flesch_kincaid_grade)
        
        # Gunning Fog Index
        complex_words = sum(1 for word in words if self._is_complex_word(word))
        complex_word_percentage = (complex_words / word_count) * 100
        gunning_fog = 0.4 * (avg_sentence_length + complex_word_percentage)
        
        # SMOG Index (requires at least 30 sentences for accuracy)
        if sentence_count >= 30:
            smog_index = 1.0430 * math.sqrt(complex_words * (30 / sentence_count)) + 3.1291
        else:
            smog_index = gunning_fog  # Fallback to Gunning Fog
        
        # Calculate overall readability score (0-10 scale)
        # Convert Flesch Reading Ease to 0-10 scale
        readability_score = flesch_reading_ease / 10
        
        # Adjust based on grade level (penalize if too high)
        if flesch_kincaid_grade > 12:
            readability_score -= (flesch_kincaid_grade - 12) * 0.3
        
        readability_score = max(0, min(10, readability_score))
        
        # Determine readability level
        if flesch_reading_ease >= 90:
            level = "very easy"
        elif flesch_reading_ease >= 80:
            level = "easy"
        elif flesch_reading_ease >= 70:
            level = "fairly easy"
        elif flesch_reading_ease >= 60:
            level = "standard"
        elif flesch_reading_ease >= 50:
            level = "fairly difficult"
        elif flesch_reading_ease >= 30:
            level = "difficult"
        else:
            level = "very difficult"
        
        return ReadabilityScore(
            flesch_reading_ease=flesch_reading_ease,
            flesch_kincaid_grade=flesch_kincaid_grade,
            gunning_fog_index=gunning_fog,
            smog_index=smog_index,
            average_sentence_length=avg_sentence_length,
            average_word_length=avg_word_length,
            complex_word_percentage=complex_word_percentage,
            overall_readability_score=readability_score,
            readability_level=level
        )
    
    def _analyze_seo(self, content: str, target_keywords: Optional[List[str]] = None) -> SEOMetrics:
        """Analyze SEO optimization."""
        words = content.lower().split()
        word_count = len(words)
        
        # Keyword density analysis
        keyword_density = {}
        if target_keywords:
            for keyword in target_keywords:
                keyword_lower = keyword.lower()
                count = content.lower().count(keyword_lower)
                density = (count / word_count) * 100 if word_count > 0 else 0
                keyword_density[keyword] = density
        
        # Primary keyword score (should appear in title, first 100 words, headings)
        primary_keyword_score = 0.0
        if target_keywords:
            primary_keyword = target_keywords[0].lower()
            first_100_words = ' '.join(words[:100])
            
            if content.startswith('#') and primary_keyword in content.split('\n')[0].lower():
                primary_keyword_score += 3.0  # In title
            if primary_keyword in first_100_words:
                primary_keyword_score += 2.0  # In first 100 words
            if any(primary_keyword in line.lower() for line in content.split('\n') if line.startswith('##')):
                primary_keyword_score += 2.0  # In H2 headings
            
            # Keyword density score (ideal 1-3%)
            if keyword_density.get(primary_keyword, 0) >= 1.0 and keyword_density.get(primary_keyword, 0) <= 3.0:
                primary_keyword_score += 3.0
        
        # Title optimization (H1 present, 50-60 chars)
        title_score = 0.0
        lines = content.split('\n')
        h1_lines = [line for line in lines if line.startswith('# ')]
        if h1_lines:
            title = h1_lines[0].replace('# ', '')
            title_length = len(title)
            title_score = 5.0
            if 50 <= title_length <= 60:
                title_score = 10.0
            elif 40 <= title_length <= 70:
                title_score = 7.0
        
        # Meta description score (150-160 chars - simplified check)
        meta_description_score = 5.0  # Default moderate score
        
        # Heading structure score
        h1_count = len([line for line in lines if line.startswith('# ')])
        h2_count = len([line for line in lines if line.startswith('## ')])
        h3_count = len([line for line in lines if line.startswith('### ')])
        
        heading_score = 0.0
        if h1_count == 1:  # Exactly one H1
            heading_score += 4.0
        if h2_count >= 2:  # Multiple H2s
            heading_score += 3.0
        if h3_count > 0:  # Has H3s for detail
            heading_score += 3.0
        
        # Content length score (ideal 1500-2500 words for SEO)
        length_score = 0.0
        if 1500 <= word_count <= 2500:
            length_score = 10.0
        elif 1000 <= word_count < 1500:
            length_score = 7.0
        elif 800 <= word_count < 1000:
            length_score = 5.0
        elif word_count >= 2500:
            length_score = 8.0
        else:
            length_score = 3.0
        
        # Link analysis
        internal_links = len(re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content))
        external_links = len(re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', content))
        
        # Image alt text score (simplified)
        images = re.findall(r'!\[([^\]]*)\]', content)
        images_with_alt = len([alt for alt in images if alt.strip()])
        total_images = len(images)
        
        image_score = 0.0
        if total_images > 0:
            image_score = (images_with_alt / total_images) * 10
        else:
            image_score = 5.0  # No images is neutral
        
        # URL optimization score (simplified)
        url_score = 5.0  # Default moderate score
        
        # Calculate overall SEO score (0-100)
        seo_scores = [
            primary_keyword_score,
            title_score,
            meta_description_score,
            heading_score,
            length_score,
            image_score,
            url_score
        ]
        overall_seo = (sum(seo_scores) / len(seo_scores)) * 10
        
        return SEOMetrics(
            keyword_density=keyword_density,
            primary_keyword_score=primary_keyword_score,
            title_optimization_score=title_score,
            meta_description_score=meta_description_score,
            heading_structure_score=heading_score,
            content_length_score=length_score,
            internal_links_count=internal_links,
            external_links_count=external_links,
            image_alt_text_score=image_score,
            url_optimization_score=url_score,
            overall_seo_score=overall_seo
        )
    
    def _analyze_engagement(self, content: str) -> EngagementMetrics:
        """Analyze content engagement potential."""
        words = content.split()
        word_count = len(words)
        
        # Hook strength (analyze first paragraph)
        first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
        hook_score = self._assess_hook_strength(first_paragraph)
        
        # Emotional impact (check for emotional words)
        emotional_words = {
            'love', 'hate', 'fear', 'joy', 'angry', 'sad', 'happy', 'excited',
            'worried', 'confident', 'frustrated', 'grateful', 'proud', 'disappointed'
        }
        emotional_word_count = sum(1 for word in words if word.lower() in emotional_words)
        emotional_impact = min(10, (emotional_word_count / max(1, word_count / 100)) * 2)
        
        # Storytelling elements
        storytelling_indicators = ['when', 'then', 'after', 'before', 'first', 'next', 'finally']
        storytelling_count = sum(1 for word in words if word.lower() in storytelling_indicators)
        storytelling_score = min(10, (storytelling_count / max(1, word_count / 100)))
        
        # Call to action score
        cta_phrases = [
            'learn more', 'get started', 'sign up', 'download', 'subscribe',
            'try', 'discover', 'explore', 'contact', 'buy now', 'shop', 'register'
        ]
        content_lower = content.lower()
        cta_count = sum(1 for phrase in cta_phrases if phrase in content_lower)
        cta_score = min(10, cta_count * 3)
        
        # Question count (engaging readers)
        question_count = content.count('?')
        
        # Personal pronoun usage (you, your, we, our)
        personal_pronouns = ['you', 'your', 'we', 'our', 'us']
        pronoun_count = sum(1 for word in words if word.lower() in personal_pronouns)
        pronoun_percentage = (pronoun_count / word_count) * 100 if word_count > 0 else 0
        
        # Power words
        power_word_count = sum(1 for word in words if word.lower() in self.power_words)
        
        # Calculate overall engagement score
        engagement_scores = [
            hook_score,
            emotional_impact,
            storytelling_score,
            cta_score,
            min(10, question_count * 2),  # Questions boost engagement
            min(10, pronoun_percentage / 2)  # Personal pronouns boost engagement
        ]
        overall_engagement = sum(engagement_scores) / len(engagement_scores)
        
        return EngagementMetrics(
            hook_strength=hook_score,
            emotional_impact_score=emotional_impact,
            storytelling_score=storytelling_score,
            call_to_action_score=cta_score,
            question_count=question_count,
            personal_pronoun_usage=pronoun_percentage,
            power_word_count=power_word_count,
            overall_engagement_score=overall_engagement
        )
    
    def _analyze_style_consistency(
        self, content: str, metadata: Dict[str, Any]
    ) -> StyleConsistencyMetrics:
        """Analyze style and tone consistency."""
        # Simplified style consistency analysis
        
        # Tone consistency (check for consistent language patterns)
        tone_score = 7.0  # Default good score
        
        # Voice consistency (active vs passive)
        passive_indicators = ['is being', 'was being', 'has been', 'had been', 'will be']
        passive_count = sum(content.lower().count(phrase) for phrase in passive_indicators)
        total_sentences = len(self._split_sentences(content))
        passive_ratio = passive_count / max(1, total_sentences)
        
        # Voice is consistent if passive is either very low or intentionally high
        if passive_ratio < 0.2:
            voice_score = 9.0  # Good active voice
        elif passive_ratio > 0.5:
            voice_score = 6.0  # Consistently passive (might be intentional for technical)
        else:
            voice_score = 7.0  # Mixed
        
        # Terminology consistency (check for variations of key terms)
        terminology_score = 8.0  # Default good score
        
        # Formatting consistency (check heading levels, list formats)
        formatting_score = self._assess_formatting_consistency(content)
        
        # Brand alignment (simplified - would need brand guidelines in practice)
        brand_score = 7.0  # Default moderate score
        
        # Style guide compliance (simplified)
        style_guide_score = 7.0  # Default moderate score
        
        # Calculate overall style score
        style_scores = [
            tone_score,
            voice_score,
            terminology_score,
            formatting_score,
            brand_score,
            style_guide_score
        ]
        overall_style = sum(style_scores) / len(style_scores)
        
        return StyleConsistencyMetrics(
            tone_consistency_score=tone_score,
            voice_consistency_score=voice_score,
            terminology_consistency_score=terminology_score,
            formatting_consistency_score=formatting_score,
            brand_alignment_score=brand_score,
            style_guide_compliance_score=style_guide_score,
            overall_style_score=overall_style
        )
    
    def _analyze_structure(self, content: str) -> StructureMetrics:
        """Analyze content structure and organization."""
        lines = content.split('\n')
        
        # Check for title (H1)
        has_title = any(line.startswith('# ') for line in lines)
        title_lines = [line for line in lines if line.startswith('# ')]
        
        title_quality = 0.0
        if title_lines:
            title = title_lines[0].replace('# ', '')
            # Good title: 40-70 chars, contains keywords, clear
            title_length = len(title)
            if 40 <= title_length <= 70:
                title_quality = 10.0
            elif 30 <= title_length <= 80:
                title_quality = 7.0
            else:
                title_quality = 5.0
        
        # Check for introduction (first non-heading paragraph)
        has_introduction = False
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('#')]
        if paragraphs and len(paragraphs[0]) > 50:
            has_introduction = True
        
        # Check for conclusion (look for conclusion keywords in last sections)
        conclusion_keywords = ['conclusion', 'summary', 'in conclusion', 'to sum up', 'finally']
        last_500_chars = content[-500:].lower()
        has_conclusion = any(keyword in last_500_chars for keyword in conclusion_keywords)
        
        # Heading hierarchy score
        h1_count = len([line for line in lines if line.startswith('# ')])
        h2_count = len([line for line in lines if line.startswith('## ')])
        h3_count = len([line for line in lines if line.startswith('### ')])
        
        hierarchy_score = 0.0
        if h1_count == 1:  # Exactly one H1
            hierarchy_score += 4.0
        if h2_count >= 2:  # Multiple main sections
            hierarchy_score += 3.0
        if h3_count > 0:  # Has subsections
            hierarchy_score += 3.0
        
        # Paragraph length score (ideal 3-5 sentences, 50-150 words)
        paragraph_scores = []
        for para in paragraphs:
            word_count = len(para.split())
            if 50 <= word_count <= 150:
                paragraph_scores.append(10.0)
            elif 30 <= word_count <= 200:
                paragraph_scores.append(7.0)
            else:
                paragraph_scores.append(4.0)
        
        paragraph_length_score = sum(paragraph_scores) / len(paragraph_scores) if paragraph_scores else 5.0
        
        # Section balance (check if sections are roughly equal in length)
        section_balance_score = 7.0  # Default moderate score
        
        # Logical flow score (check for transition words)
        transition_words = [
            'however', 'therefore', 'furthermore', 'moreover', 'additionally',
            'consequently', 'meanwhile', 'nevertheless', 'similarly', 'likewise'
        ]
        transition_count = sum(1 for word in content.lower().split() if word in transition_words)
        word_count = len(content.split())
        transition_density = (transition_count / max(1, word_count / 100))
        logical_flow_score = min(10, transition_density * 3)
        
        # Calculate overall structure score
        structure_scores = [
            10.0 if has_title else 0.0,
            title_quality,
            10.0 if has_introduction else 5.0,
            10.0 if has_conclusion else 5.0,
            hierarchy_score,
            paragraph_length_score,
            section_balance_score,
            logical_flow_score
        ]
        overall_structure = sum(structure_scores) / len(structure_scores)
        
        return StructureMetrics(
            has_title=has_title,
            title_quality_score=title_quality,
            has_introduction=has_introduction,
            has_conclusion=has_conclusion,
            heading_hierarchy_score=hierarchy_score,
            paragraph_length_score=paragraph_length_score,
            section_balance_score=section_balance_score,
            logical_flow_score=logical_flow_score,
            overall_structure_score=overall_structure
        )
    
    def _analyze_grammar(self, content: str) -> GrammarMetrics:
        """Analyze grammar and language mechanics."""
        # Simplified grammar analysis (in production, use language tool or similar)
        
        words = content.split()
        word_count = len(words)
        
        # Common spelling errors (simplified detection)
        common_errors = {
            'alot': 'a lot',
            'definately': 'definitely',
            'seperate': 'separate',
            'occured': 'occurred',
            'recieve': 'receive'
        }
        
        spelling_errors = sum(1 for word in words if word.lower() in common_errors)
        
        # Grammar issues (simplified detection)
        grammar_patterns = [
            (r'\s+its\s+', r'\s+it\'s\s+'),  # its/it's confusion
            (r'\s+your\s+', r'\s+you\'re\s+'),  # your/you're confusion
            (r'\s+their\s+', r'\s+there\s+')  # their/there confusion
        ]
        
        grammar_errors = 0
        for pattern, _ in grammar_patterns:
            grammar_errors += len(re.findall(pattern, content.lower()))
        
        # Punctuation issues
        punctuation_errors = 0
        # Check for missing periods at end of sentences (simplified)
        lines = content.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) > 20 and not line.strip().startswith('#'):
                if not line.strip().endswith(('.', '!', '?', ':')):
                    punctuation_errors += 1
        
        # Double spaces
        punctuation_errors += content.count('  ')
        
        # Style issues (passive voice, wordy phrases)
        style_issues = 0
        wordy_phrases = ['in order to', 'due to the fact that', 'at this point in time']
        for phrase in wordy_phrases:
            style_issues += content.lower().count(phrase)
        
        # Calculate totals
        total_issues = spelling_errors + grammar_errors + punctuation_errors + style_issues
        error_density = (total_issues / max(1, word_count / 100))
        
        # Grammar score (0-10, penalize based on error density)
        if error_density == 0:
            grammar_score = 10.0
        elif error_density < 0.5:
            grammar_score = 9.0
        elif error_density < 1.0:
            grammar_score = 8.0
        elif error_density < 2.0:
            grammar_score = 7.0
        elif error_density < 3.0:
            grammar_score = 6.0
        elif error_density < 5.0:
            grammar_score = 5.0
        else:
            grammar_score = max(0, 5.0 - (error_density - 5.0))
        
        return GrammarMetrics(
            spelling_errors=spelling_errors,
            grammar_errors=grammar_errors,
            punctuation_errors=punctuation_errors,
            style_issues=style_issues,
            total_issues=total_issues,
            error_density=error_density,
            grammar_score=grammar_score
        )
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count for a word."""
        word = word.lower()
        syllables = 0
        vowels = 'aeiouy'
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllables += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllables -= 1
        
        # Every word has at least one syllable
        return max(1, syllables)
    
    def _is_complex_word(self, word: str) -> bool:
        """Determine if a word is complex (3+ syllables)."""
        return self._count_syllables(word) >= 3
    
    def _assess_hook_strength(self, first_paragraph: str) -> float:
        """Assess the strength of the opening hook."""
        score = 5.0  # Default moderate score
        
        # Check for engaging opening techniques
        if first_paragraph.startswith('?') or '?' in first_paragraph[:100]:
            score += 2.0  # Opens with or contains question
        
        engaging_starters = ['imagine', 'what if', 'did you know', 'picture this', 'have you ever']
        if any(first_paragraph.lower().startswith(starter) for starter in engaging_starters):
            score += 2.0
        
        # Check for statistics or numbers
        if re.search(r'\d+%|\d+ percent', first_paragraph):
            score += 1.5
        
        # Penalize if too long or generic
        if len(first_paragraph) > 300:
            score -= 1.0
        
        if first_paragraph.lower().startswith(('the', 'this', 'it is', 'there are')):
            score -= 1.0
        
        return max(0, min(10, score))
    
    def _assess_formatting_consistency(self, content: str) -> float:
        """Assess formatting consistency."""
        score = 7.0  # Default good score
        
        # Check list formatting consistency
        bullet_types = [
            len(re.findall(r'^\* ', content, re.MULTILINE)),
            len(re.findall(r'^- ', content, re.MULTILINE)),
            len(re.findall(r'^\+ ', content, re.MULTILINE))
        ]
        
        # If multiple bullet types used, reduce score
        bullet_types_used = sum(1 for count in bullet_types if count > 0)
        if bullet_types_used > 1:
            score -= 1.5
        
        # Check heading formatting (should be consistent)
        # All good if using markdown properly
        
        return score
    
    def _calculate_overall_score(self, dimension_scores: Dict[QualityDimension, float]) -> float:
        """Calculate weighted overall quality score (0-100)."""
        weighted_sum = 0
        total_weight = 0
        
        for dimension, score in dimension_scores.items():
            weight = self.weights.get(dimension, 1.0)
            weighted_sum += score * weight
            total_weight += weight
        
        overall = (weighted_sum / total_weight) * 10  # Scale to 0-100
        return round(overall, 1)
    
    def _identify_strengths(
        self,
        dimension_scores: Dict[QualityDimension, float],
        readability: ReadabilityScore,
        seo: SEOMetrics,
        engagement: EngagementMetrics
    ) -> List[str]:
        """Identify content strengths."""
        strengths = []
        
        # Check each dimension
        if dimension_scores[QualityDimension.READABILITY] >= 7.0:
            strengths.append(f"Excellent readability ({readability.readability_level})")
        
        if dimension_scores[QualityDimension.SEO_OPTIMIZATION] >= 7.0:
            strengths.append(f"Strong SEO optimization (score: {seo.overall_seo_score:.1f}/100)")
        
        if dimension_scores[QualityDimension.ENGAGEMENT] >= 7.0:
            strengths.append("Highly engaging content")
        
        if dimension_scores[QualityDimension.STRUCTURE] >= 8.0:
            strengths.append("Well-structured and organized")
        
        if dimension_scores[QualityDimension.GRAMMAR] >= 9.0:
            strengths.append("Excellent grammar and mechanics")
        
        if engagement.power_word_count >= 5:
            strengths.append(f"Effective use of power words ({engagement.power_word_count} found)")
        
        if seo.internal_links_count + seo.external_links_count >= 5:
            strengths.append("Good use of internal and external links")
        
        return strengths
    
    def _identify_weaknesses(
        self,
        dimension_scores: Dict[QualityDimension, float],
        readability: ReadabilityScore,
        seo: SEOMetrics,
        grammar: GrammarMetrics
    ) -> List[str]:
        """Identify content weaknesses."""
        weaknesses = []
        
        # Check each dimension
        if dimension_scores[QualityDimension.READABILITY] < 5.0:
            weaknesses.append(f"Poor readability - grade level {readability.flesch_kincaid_grade:.1f}")
        
        if dimension_scores[QualityDimension.SEO_OPTIMIZATION] < 5.0:
            weaknesses.append(f"Weak SEO optimization (score: {seo.overall_seo_score:.1f}/100)")
        
        if dimension_scores[QualityDimension.ENGAGEMENT] < 5.0:
            weaknesses.append("Low engagement potential")
        
        if dimension_scores[QualityDimension.STRUCTURE] < 6.0:
            weaknesses.append("Poor structure and organization")
        
        if dimension_scores[QualityDimension.GRAMMAR] < 7.0:
            weaknesses.append(f"Grammar issues found ({grammar.total_issues} total issues)")
        
        if readability.average_sentence_length > 25:
            weaknesses.append(f"Sentences too long (avg: {readability.average_sentence_length:.1f} words)")
        
        if seo.heading_structure_score < 5.0:
            weaknesses.append("Poor heading structure for SEO")
        
        return weaknesses
    
    def _generate_recommendations(
        self,
        dimension_scores: Dict[QualityDimension, float],
        readability: ReadabilityScore,
        seo: SEOMetrics,
        engagement: EngagementMetrics,
        structure: StructureMetrics,
        grammar: GrammarMetrics
    ) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Readability recommendations
        if dimension_scores[QualityDimension.READABILITY] < 6.0:
            if readability.average_sentence_length > 20:
                recommendations.append("Break long sentences into shorter ones (aim for 15-20 words)")
            if readability.complex_word_percentage > 15:
                recommendations.append("Simplify complex words where possible")
        
        # SEO recommendations
        if dimension_scores[QualityDimension.SEO_OPTIMIZATION] < 7.0:
            if seo.title_optimization_score < 7.0:
                recommendations.append("Optimize title length (50-60 characters ideal)")
            if seo.heading_structure_score < 7.0:
                recommendations.append("Improve heading hierarchy (use H2 and H3 tags)")
            if seo.internal_links_count < 3:
                recommendations.append("Add more internal links (aim for 3-5)")
        
        # Engagement recommendations
        if dimension_scores[QualityDimension.ENGAGEMENT] < 6.0:
            if engagement.hook_strength < 6.0:
                recommendations.append("Strengthen opening hook (use questions, statistics, or compelling statements)")
            if engagement.call_to_action_score < 5.0:
                recommendations.append("Add clear call-to-action")
            if engagement.question_count < 2:
                recommendations.append("Include more questions to engage readers")
        
        # Structure recommendations
        if dimension_scores[QualityDimension.STRUCTURE] < 7.0:
            if not structure.has_title:
                recommendations.append("Add a clear H1 title")
            if not structure.has_introduction:
                recommendations.append("Add a proper introduction")
            if not structure.has_conclusion:
                recommendations.append("Add a conclusion section")
        
        # Grammar recommendations
        if dimension_scores[QualityDimension.GRAMMAR] < 8.0:
            if grammar.spelling_errors > 0:
                recommendations.append(f"Fix {grammar.spelling_errors} spelling errors")
            if grammar.grammar_errors > 0:
                recommendations.append(f"Correct {grammar.grammar_errors} grammar issues")
            if grammar.punctuation_errors > 0:
                recommendations.append("Review and fix punctuation errors")
        
        return recommendations


# Demo function
def demo_quality_analyzer():
    """Demonstrate content quality analyzer."""
    print("Content Quality Metrics Demonstration")
    print("=" * 60)
    
    analyzer = ContentQualityAnalyzer()
    
    # Sample content
    sample_content = """
# How to Improve Your Writing Skills

Did you know that 80% of professionals say writing is crucial to their success? Whether you're crafting emails, reports, or blog posts, strong writing skills can set you apart.

## Why Writing Matters

In today's digital world, writing is more important than ever. Good writing helps you communicate clearly, persuade effectively, and build your professional reputation.

## 5 Tips to Enhance Your Writing

### 1. Read Regularly

The best writers are avid readers. Reading exposes you to different styles, vocabulary, and techniques that you can incorporate into your own writing.

### 2. Practice Daily

Like any skill, writing improves with practice. Set aside 15-30 minutes each day to write. It doesn't matter what you write—just write!

### 3. Get Feedback

Share your work with others and ask for honest feedback. Constructive criticism helps you identify blind spots and improve faster.

### 4. Edit Ruthlessly

First drafts are rarely perfect. Take time to review and revise your work. Cut unnecessary words, clarify confusing sentences, and polish your prose.

### 5. Study Grammar

Understanding grammar rules gives you a solid foundation. While you don't need to be a grammar expert, knowing the basics prevents common errors.

## Take Action Today

Ready to improve your writing? Start by implementing one tip from this article. Pick the one that resonates most with you and practice it this week.

What's your biggest writing challenge? Share in the comments below!
    """
    
    # Analyze content
    report = analyzer.analyze_content(
        content=sample_content,
        content_metadata={"type": "blog_post", "id": "writing_tips_001"},
        target_keywords=["writing skills", "improve writing", "writing tips"]
    )
    
    # Display results
    print(f"\n📊 Overall Quality Score: {report.overall_quality_score:.1f}/100")
    print(f"Word Count: {report.word_count}")
    print(f"Assessment Duration: {report.assessment_duration:.2f}s")
    
    print("\n📈 Dimension Scores:")
    print("-" * 40)
    for dimension, score in report.dimension_scores.items():
        bar = "█" * int(score) + "░" * (10 - int(score))
        print(f"{dimension.value:20s} [{bar}] {score:.1f}/10")
    
    print("\n📖 Readability Analysis:")
    print("-" * 40)
    print(f"Flesch Reading Ease: {report.readability.flesch_reading_ease:.1f}")
    print(f"Grade Level: {report.readability.flesch_kincaid_grade:.1f}")
    print(f"Readability Level: {report.readability.readability_level}")
    print(f"Avg Sentence Length: {report.readability.average_sentence_length:.1f} words")
    
    print("\n🔍 SEO Metrics:")
    print("-" * 40)
    print(f"Overall SEO Score: {report.seo_metrics.overall_seo_score:.1f}/100")
    print(f"Title Optimization: {report.seo_metrics.title_optimization_score:.1f}/10")
    print(f"Heading Structure: {report.seo_metrics.heading_structure_score:.1f}/10")
    print(f"Internal Links: {report.seo_metrics.internal_links_count}")
    print(f"External Links: {report.seo_metrics.external_links_count}")
    
    print("\n💪 Strengths:")
    print("-" * 40)
    for strength in report.strengths:
        print(f"✓ {strength}")
    
    print("\n⚠️  Weaknesses:")
    print("-" * 40)
    if report.weaknesses:
        for weakness in report.weaknesses:
            print(f"✗ {weakness}")
    else:
        print("None identified!")
    
    print("\n💡 Recommendations:")
    print("-" * 40)
    for i, rec in enumerate(report.improvement_recommendations, 1):
        print(f"{i}. {rec}")


if __name__ == "__main__":
    demo_quality_analyzer()
