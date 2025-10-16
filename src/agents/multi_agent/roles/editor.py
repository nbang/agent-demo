"""Editor Agent Role

Specialized editor agent role for content editing, refinement, and enhancement
with various editing capabilities and quality improvement expertise.
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from src.agents.multi_agent.agent_roles import RoleDefinition, create_role_definition
from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class EditingType(Enum):
    """Different types of editing specializations."""
    DEVELOPMENTAL = "developmental"  # Structure, organization, content development
    LINE_EDITING = "line_editing"    # Style, clarity, flow at sentence level
    COPY_EDITING = "copy_editing"    # Grammar, punctuation, consistency
    PROOFREADING = "proofreading"    # Final check for errors
    TECHNICAL_EDITING = "technical_editing"  # Technical accuracy and clarity
    CONTENT_EDITING = "content_editing"      # Content quality and effectiveness


class EditingFocus(Enum):
    """Areas of editing focus."""
    CLARITY = "clarity"
    CONCISENESS = "conciseness"
    COHERENCE = "coherence"
    CONSISTENCY = "consistency"
    CORRECTNESS = "correctness"
    ENGAGEMENT = "engagement"
    FLOW = "flow"
    ACCURACY = "accuracy"
    STYLE = "style"
    STRUCTURE = "structure"


@dataclass
class EditingCapability:
    """Represents a specific editing capability."""
    name: str
    description: str
    proficiency_level: float  # 0.0 to 1.0
    editing_types: List[EditingType]
    focus_areas: List[EditingFocus]
    
    def is_applicable_for(self, editing_type: EditingType, focus: EditingFocus) -> bool:
        """Check if capability applies to specific editing type and focus."""
        return editing_type in self.editing_types and focus in self.focus_areas


@dataclass
class EditingChange:
    """Represents a single editing change."""
    line_number: int
    original_text: str
    edited_text: str
    change_type: str  # grammar, style, clarity, etc.
    reasoning: str
    confidence: float  # 0.0 to 1.0


@dataclass
class EditingOutput:
    """Represents editor output with changes and metadata."""
    original_content: str
    edited_content: str
    changes_made: List[EditingChange]
    editing_summary: Dict[str, Any]
    quality_improvements: Dict[str, float]
    editing_time: float
    capabilities_used: List[str]
    metadata: Dict[str, Any]


class EditorRole:
    """Specialized editor agent role for content editing and enhancement."""
    
    def __init__(
        self,
        editor_type: str = "general",
        specialization_areas: Optional[List[str]] = None,
        quality_standards: Optional[Dict[str, float]] = None,
        editing_preferences: Optional[Dict[str, Any]] = None
    ):
        """Initialize editor role.
        
        Args:
            editor_type: Type of editor (general, copy, developmental, etc.)
            specialization_areas: Specific areas of editing expertise
            quality_standards: Quality thresholds for different metrics
            editing_preferences: Preferences for editing approach
        """
        self.editor_type = editor_type
        self.specialization_areas = specialization_areas or []
        self.quality_standards = quality_standards or {
            "grammar_accuracy": 4.8,
            "clarity_improvement": 4.0,
            "style_consistency": 4.2,
            "flow_enhancement": 3.8,
            "overall_quality": 4.0
        }
        self.editing_preferences = editing_preferences or {
            "preserve_author_voice": True,
            "prioritize_clarity": True,
            "suggest_alternatives": True,
            "detailed_feedback": False
        }
        
        # Initialize capabilities based on editor type
        self.capabilities = self._initialize_capabilities()
        
        # Create role definition
        self.role_definition = self._create_role_definition()
        
        # Initialize metrics tracking
        self.editing_history = []
        self.performance_metrics = {
            "total_content_edited": 0,
            "total_changes_made": 0,
            "average_improvement_score": 0.0,
            "average_editing_time": 0.0,
            "editing_sessions": 0
        }
        
        logger.info(f"Editor role initialized: {editor_type} with {len(self.capabilities)} capabilities")
    
    def _initialize_capabilities(self) -> List[EditingCapability]:
        """Initialize editing capabilities based on editor type."""
        capabilities = []
        
        # Base capabilities for all editors
        base_capabilities = [
            EditingCapability(
                name="grammar_correction",
                description="Correct grammar, spelling, and punctuation errors",
                proficiency_level=0.9,
                editing_types=[EditingType.COPY_EDITING, EditingType.PROOFREADING],
                focus_areas=[EditingFocus.CORRECTNESS, EditingFocus.CONSISTENCY]
            ),
            EditingCapability(
                name="clarity_enhancement",
                description="Improve clarity and readability of content",
                proficiency_level=0.8,
                editing_types=[EditingType.LINE_EDITING, EditingType.CONTENT_EDITING],
                focus_areas=[EditingFocus.CLARITY, EditingFocus.COHERENCE]
            ),
            EditingCapability(
                name="style_consistency",
                description="Ensure consistent style and tone throughout content",
                proficiency_level=0.75,
                editing_types=[EditingType.COPY_EDITING, EditingType.LINE_EDITING],
                focus_areas=[EditingFocus.STYLE, EditingFocus.CONSISTENCY]
            )
        ]
        
        capabilities.extend(base_capabilities)
        
        # Add specialized capabilities based on editor type
        if self.editor_type == "developmental":
            developmental_capabilities = [
                EditingCapability(
                    name="content_structure",
                    description="Improve overall content structure and organization",
                    proficiency_level=0.85,
                    editing_types=[EditingType.DEVELOPMENTAL],
                    focus_areas=[EditingFocus.STRUCTURE, EditingFocus.COHERENCE]
                ),
                EditingCapability(
                    name="argument_development",
                    description="Strengthen arguments and logical flow",
                    proficiency_level=0.8,
                    editing_types=[EditingType.DEVELOPMENTAL, EditingType.CONTENT_EDITING],
                    focus_areas=[EditingFocus.COHERENCE, EditingFocus.CLARITY]
                ),
                EditingCapability(
                    name="content_gaps_identification",
                    description="Identify and suggest solutions for content gaps",
                    proficiency_level=0.75,
                    editing_types=[EditingType.DEVELOPMENTAL],
                    focus_areas=[EditingFocus.STRUCTURE, EditingFocus.COHERENCE]
                )
            ]
            capabilities.extend(developmental_capabilities)
        
        elif self.editor_type == "copy":
            copy_capabilities = [
                EditingCapability(
                    name="precision_editing",
                    description="Detailed correction of grammar, punctuation, and syntax",
                    proficiency_level=0.95,
                    editing_types=[EditingType.COPY_EDITING, EditingType.PROOFREADING],
                    focus_areas=[EditingFocus.CORRECTNESS, EditingFocus.CONSISTENCY]
                ),
                EditingCapability(
                    name="fact_checking",
                    description="Verify factual accuracy and consistency",
                    proficiency_level=0.8,
                    editing_types=[EditingType.COPY_EDITING],
                    focus_areas=[EditingFocus.ACCURACY, EditingFocus.CORRECTNESS]
                ),
                EditingCapability(
                    name="citation_formatting",
                    description="Ensure proper citation and reference formatting",
                    proficiency_level=0.85,
                    editing_types=[EditingType.COPY_EDITING],
                    focus_areas=[EditingFocus.CONSISTENCY, EditingFocus.CORRECTNESS]
                )
            ]
            capabilities.extend(copy_capabilities)
        
        elif self.editor_type == "line":
            line_capabilities = [
                EditingCapability(
                    name="sentence_optimization",
                    description="Optimize sentence structure and flow",
                    proficiency_level=0.85,
                    editing_types=[EditingType.LINE_EDITING],
                    focus_areas=[EditingFocus.CLARITY, EditingFocus.FLOW, EditingFocus.CONCISENESS]
                ),
                EditingCapability(
                    name="word_choice_refinement",
                    description="Improve word choice and vocabulary usage",
                    proficiency_level=0.8,
                    editing_types=[EditingType.LINE_EDITING],
                    focus_areas=[EditingFocus.CLARITY, EditingFocus.STYLE]
                ),
                EditingCapability(
                    name="transition_improvement",
                    description="Enhance transitions between sentences and paragraphs",
                    proficiency_level=0.75,
                    editing_types=[EditingType.LINE_EDITING],
                    focus_areas=[EditingFocus.FLOW, EditingFocus.COHERENCE]
                )
            ]
            capabilities.extend(line_capabilities)
        
        elif self.editor_type == "technical":
            technical_capabilities = [
                EditingCapability(
                    name="technical_accuracy",
                    description="Ensure technical information is accurate and clear",
                    proficiency_level=0.9,
                    editing_types=[EditingType.TECHNICAL_EDITING],
                    focus_areas=[EditingFocus.ACCURACY, EditingFocus.CLARITY]
                ),
                EditingCapability(
                    name="terminology_consistency",
                    description="Maintain consistent use of technical terminology",
                    proficiency_level=0.85,
                    editing_types=[EditingType.TECHNICAL_EDITING],
                    focus_areas=[EditingFocus.CONSISTENCY, EditingFocus.ACCURACY]
                ),
                EditingCapability(
                    name="technical_style_guide",
                    description="Apply technical writing style guidelines",
                    proficiency_level=0.8,
                    editing_types=[EditingType.TECHNICAL_EDITING],
                    focus_areas=[EditingFocus.STYLE, EditingFocus.CONSISTENCY]
                )
            ]
            capabilities.extend(technical_capabilities)
        
        elif self.editor_type == "content":
            content_capabilities = [
                EditingCapability(
                    name="audience_alignment",
                    description="Ensure content aligns with target audience needs",
                    proficiency_level=0.8,
                    editing_types=[EditingType.CONTENT_EDITING],
                    focus_areas=[EditingFocus.ENGAGEMENT, EditingFocus.CLARITY]
                ),
                EditingCapability(
                    name="message_optimization",
                    description="Optimize key messages and calls-to-action",
                    proficiency_level=0.75,
                    editing_types=[EditingType.CONTENT_EDITING],
                    focus_areas=[EditingFocus.ENGAGEMENT, EditingFocus.CLARITY]
                ),
                EditingCapability(
                    name="content_flow",
                    description="Improve overall content flow and narrative",
                    proficiency_level=0.8,
                    editing_types=[EditingType.CONTENT_EDITING, EditingType.DEVELOPMENTAL],
                    focus_areas=[EditingFocus.FLOW, EditingFocus.COHERENCE]
                )
            ]
            capabilities.extend(content_capabilities)
        
        # Add general enhancement capabilities for all specialized editors
        if self.editor_type != "general":
            enhancement_capabilities = [
                EditingCapability(
                    name="readability_optimization",
                    description="Optimize content for better readability",
                    proficiency_level=0.7,
                    editing_types=[EditingType.LINE_EDITING, EditingType.CONTENT_EDITING],
                    focus_areas=[EditingFocus.CLARITY, EditingFocus.ENGAGEMENT]
                ),
                EditingCapability(
                    name="conciseness_improvement",
                    description="Remove unnecessary words and improve conciseness",
                    proficiency_level=0.75,
                    editing_types=[EditingType.LINE_EDITING, EditingType.COPY_EDITING],
                    focus_areas=[EditingFocus.CONCISENESS, EditingFocus.CLARITY]
                )
            ]
            capabilities.extend(enhancement_capabilities)
        
        return capabilities
    
    def _create_role_definition(self) -> RoleDefinition:
        """Create role definition for the editor."""
        expertise_areas = [
            "content_editing",
            "grammar_correction",
            "clarity_enhancement",
            "style_consistency"
        ]
        
        # Add specialized expertise areas
        if self.editor_type == "developmental":
            expertise_areas.extend([
                "content_structure",
                "argument_development",
                "content_strategy"
            ])
        elif self.editor_type == "copy":
            expertise_areas.extend([
                "precision_editing",
                "fact_checking",
                "citation_formatting"
            ])
        elif self.editor_type == "line":
            expertise_areas.extend([
                "sentence_optimization",
                "word_choice_refinement",
                "flow_improvement"
            ])
        elif self.editor_type == "technical":
            expertise_areas.extend([
                "technical_accuracy",
                "terminology_consistency",
                "technical_documentation"
            ])
        elif self.editor_type == "content":
            expertise_areas.extend([
                "audience_alignment",
                "message_optimization",
                "content_strategy"
            ])
        
        # Add custom specialization areas
        expertise_areas.extend(self.specialization_areas)
        
        responsibilities = [
            "Review and edit content for quality and accuracy",
            "Improve clarity, flow, and readability",
            "Ensure consistency in style and tone",
            "Correct grammar, spelling, and punctuation errors",
            "Provide constructive feedback and suggestions",
            "Maintain author voice while enhancing content",
            "Meet quality standards and editorial guidelines"
        ]
        
        interaction_patterns = [
            "collaborates_with_writers",
            "provides_feedback_to_content_team",
            "works_with_reviewers",
            "coordinates_with_content_strategists",
            "supports_quality_assurance"
        ]
        
        return create_role_definition(
            name=f"{self.editor_type.title()} Editor",
            description=f"Specialized editor focused on {self.editor_type} editing with expertise in content enhancement and quality improvement",
            expertise_areas=expertise_areas,
            responsibilities=responsibilities,
            interaction_patterns=interaction_patterns
        )
    
    def edit_content(
        self,
        content: str,
        editing_requirements: Dict[str, Any],
        style_guide: Optional[Dict[str, Any]] = None,
        feedback_level: str = "standard"
    ) -> EditingOutput:
        """Edit content based on requirements and guidelines.
        
        Args:
            content: Original content to edit
            editing_requirements: Editing requirements and preferences
            style_guide: Style guide to follow
            feedback_level: Level of feedback detail (minimal, standard, detailed)
            
        Returns:
            EditingOutput with edited content and change details
        """
        logger.info(f"Starting content editing - {len(content.split())} words")
        
        start_time = time.time()
        
        try:
            # Parse editing requirements
            editing_type = EditingType(editing_requirements.get("type", "content_editing"))
            focus_areas = [EditingFocus(f) for f in editing_requirements.get("focus", ["clarity", "correctness"])]
            target_audience = editing_requirements.get("audience", "general")
            preserve_voice = editing_requirements.get("preserve_voice", self.editing_preferences["preserve_author_voice"])
            
            # Select applicable capabilities
            applicable_capabilities = [
                cap for cap in self.capabilities 
                if any(cap.is_applicable_for(editing_type, focus) for focus in focus_areas)
            ]
            
            logger.info(f"Using {len(applicable_capabilities)} applicable capabilities for {editing_type.value}")
            
            # Perform editing passes
            edited_content = content
            all_changes = []
            
            # Pass 1: Structural and developmental editing
            if editing_type in [EditingType.DEVELOPMENTAL, EditingType.CONTENT_EDITING]:
                edited_content, structural_changes = self._perform_structural_editing(
                    edited_content, editing_requirements, focus_areas
                )
                all_changes.extend(structural_changes)
            
            # Pass 2: Line editing and style
            if editing_type in [EditingType.LINE_EDITING, EditingType.CONTENT_EDITING]:
                edited_content, line_changes = self._perform_line_editing(
                    edited_content, editing_requirements, focus_areas, style_guide
                )
                all_changes.extend(line_changes)
            
            # Pass 3: Copy editing and corrections
            if editing_type in [EditingType.COPY_EDITING, EditingType.PROOFREADING]:
                edited_content, copy_changes = self._perform_copy_editing(
                    edited_content, editing_requirements, style_guide
                )
                all_changes.extend(copy_changes)
            
            # Pass 4: Technical editing (if applicable)
            if editing_type == EditingType.TECHNICAL_EDITING:
                edited_content, technical_changes = self._perform_technical_editing(
                    edited_content, editing_requirements
                )
                all_changes.extend(technical_changes)
            
            # Pass 5: Final proofreading
            if editing_type == EditingType.PROOFREADING or editing_requirements.get("final_proofread", True):
                edited_content, proof_changes = self._perform_proofreading(edited_content)
                all_changes.extend(proof_changes)
            
            # Calculate editing metrics
            editing_time = time.time() - start_time
            
            # Generate editing summary
            editing_summary = self._generate_editing_summary(content, edited_content, all_changes)
            
            # Calculate quality improvements
            quality_improvements = self._calculate_quality_improvements(content, edited_content)
            
            # Create output
            output = EditingOutput(
                original_content=content,
                edited_content=edited_content,
                changes_made=all_changes,
                editing_summary=editing_summary,
                quality_improvements=quality_improvements,
                editing_time=editing_time,
                capabilities_used=[cap.name for cap in applicable_capabilities],
                metadata={
                    "editing_type": editing_type.value,
                    "focus_areas": [f.value for f in focus_areas],
                    "target_audience": target_audience,
                    "preserve_voice": preserve_voice,
                    "editor_type": self.editor_type,
                    "feedback_level": feedback_level,
                    "style_guide_used": style_guide is not None,
                    "edited_at": datetime.now().isoformat()
                }
            )
            
            # Update performance tracking
            self._update_performance_metrics(output)
            
            logger.info(f"Content editing completed in {editing_time:.2f}s")
            logger.info(f"Changes made: {len(all_changes)}")
            
            return output
            
        except Exception as e:
            logger.error(f"Content editing failed: {str(e)}")
            raise
    
    def _perform_structural_editing(
        self, content: str, requirements: Dict[str, Any], focus_areas: List[EditingFocus]
    ) -> Tuple[str, List[EditingChange]]:
        """Perform structural and developmental editing."""
        changes = []
        edited_content = content
        lines = content.split("\\n")
        
        # Check for proper structure
        has_title = any(line.startswith("#") for line in lines)
        has_sections = any(line.startswith("##") for line in lines)
        
        # Add structure if missing
        if not has_title and EditingFocus.STRUCTURE in focus_areas:
            # Add a title based on content analysis
            first_paragraph = next((line for line in lines if line.strip()), "")
            if first_paragraph:
                title = self._generate_title_from_content(first_paragraph)
                edited_content = f"# {title}\\n\\n{edited_content}"
                changes.append(EditingChange(
                    line_number=0,
                    original_text="",
                    edited_text=f"# {title}",
                    change_type="structure",
                    reasoning="Added title for better content structure",
                    confidence=0.8
                ))
        
        # Improve paragraph structure
        if EditingFocus.COHERENCE in focus_areas:
            # Add paragraph breaks where needed
            improved_lines = []
            for i, line in enumerate(lines):
                improved_lines.append(line)
                # Add break after long paragraphs
                if len(line) > 200 and not line.startswith("#") and i < len(lines) - 1:
                    next_line = lines[i + 1] if i + 1 < len(lines) else ""
                    if next_line.strip() and not next_line.startswith("#"):
                        improved_lines.append("")
                        changes.append(EditingChange(
                            line_number=i + 1,
                            original_text=line + next_line,
                            edited_text=line + "\\n\\n" + next_line,
                            change_type="structure",
                            reasoning="Added paragraph break for better readability",
                            confidence=0.7
                        ))
            
            edited_content = "\\n".join(improved_lines)
        
        return edited_content, changes
    
    def _perform_line_editing(
        self, content: str, requirements: Dict[str, Any], focus_areas: List[EditingFocus], style_guide: Optional[Dict[str, Any]]
    ) -> Tuple[str, List[EditingChange]]:
        """Perform line editing for style, clarity, and flow."""
        changes = []
        edited_content = content
        
        # Improve sentence structure and clarity
        if EditingFocus.CLARITY in focus_areas:
            # Replace passive voice with active where appropriate
            passive_patterns = [
                ("is being", "actively"),
                ("was being", "actively"),
                ("has been", "have"),
                ("had been", "had")
            ]
            
            for old_pattern, new_pattern in passive_patterns:
                if old_pattern in edited_content:
                    original_sentence = self._find_sentence_containing(edited_content, old_pattern)
                    if original_sentence:
                        improved_sentence = original_sentence.replace(old_pattern, new_pattern)
                        edited_content = edited_content.replace(original_sentence, improved_sentence)
                        changes.append(EditingChange(
                            line_number=self._find_line_number(content, original_sentence),
                            original_text=original_sentence,
                            edited_text=improved_sentence,
                            change_type="clarity",
                            reasoning="Converted passive voice to active for clarity",
                            confidence=0.75
                        ))
        
        # Improve conciseness
        if EditingFocus.CONCISENESS in focus_areas:
            wordy_phrases = {
                "in order to": "to",
                "due to the fact that": "because",
                "at this point in time": "now",
                "for the purpose of": "for",
                "in the event that": "if",
                "make a decision": "decide",
                "come to a conclusion": "conclude"
            }
            
            for wordy, concise in wordy_phrases.items():
                if wordy in edited_content:
                    original_sentence = self._find_sentence_containing(edited_content, wordy)
                    if original_sentence:
                        improved_sentence = original_sentence.replace(wordy, concise)
                        edited_content = edited_content.replace(original_sentence, improved_sentence)
                        changes.append(EditingChange(
                            line_number=self._find_line_number(content, original_sentence),
                            original_text=original_sentence,
                            edited_text=improved_sentence,
                            change_type="conciseness",
                            reasoning=f"Replaced wordy phrase '{wordy}' with '{concise}'",
                            confidence=0.9
                        ))
        
        return edited_content, changes
    
    def _perform_copy_editing(
        self, content: str, requirements: Dict[str, Any], style_guide: Optional[Dict[str, Any]]
    ) -> Tuple[str, List[EditingChange]]:
        """Perform copy editing for grammar, punctuation, and style."""
        changes = []
        edited_content = content
        
        # Common grammar corrections
        grammar_fixes = {
            " it's ": " its ",  # Possessive its vs. contraction it's (context-dependent)
            " your ": " you're ",  # Context-dependent
            " their ": " there ",  # Context-dependent - simplified for demo
            "alot": "a lot",
            "occured": "occurred",
            "seperate": "separate",
            "recieve": "receive",
            "definately": "definitely"
        }
        
        # Apply grammar fixes (simplified - real implementation would be more sophisticated)
        for incorrect, correct in grammar_fixes.items():
            if incorrect in edited_content:
                # Only apply if it makes sense in context (simplified check)
                edited_content = edited_content.replace(incorrect, correct)
                changes.append(EditingChange(
                    line_number=self._find_line_number(content, incorrect),
                    original_text=incorrect.strip(),
                    edited_text=correct.strip(),
                    change_type="grammar",
                    reasoning=f"Corrected spelling/grammar: '{incorrect.strip()}' to '{correct.strip()}'",
                    confidence=0.95
                ))
        
        # Punctuation improvements
        # Add comma before "and" in lists (Oxford comma)
        import re
        oxford_comma_pattern = r'(\\w+), (\\w+) and (\\w+)'
        matches = re.finditer(oxford_comma_pattern, edited_content)
        for match in matches:
            original = match.group(0)
            corrected = original.replace(" and ", ", and ")
            edited_content = edited_content.replace(original, corrected)
            changes.append(EditingChange(
                line_number=self._find_line_number(content, original),
                original_text=original,
                edited_text=corrected,
                change_type="punctuation",
                reasoning="Added Oxford comma for clarity",
                confidence=0.8
            ))
        
        return edited_content, changes
    
    def _perform_technical_editing(
        self, content: str, requirements: Dict[str, Any]
    ) -> Tuple[str, List[EditingChange]]:
        """Perform technical editing for accuracy and consistency."""
        changes = []
        edited_content = content
        
        # Ensure consistent terminology
        technical_terms = {
            "API": "API",  # Ensure consistent capitalization
            "database": "database",  # Ensure consistent spelling
            "JavaScript": "JavaScript",  # Consistent capitalization
            "GitHub": "GitHub",  # Consistent capitalization
        }
        
        # Check for inconsistent technical terms (simplified)
        for correct_term in technical_terms.values():
            variations = [
                correct_term.lower(),
                correct_term.upper(),
                correct_term.title()
            ]
            
            for variation in variations:
                if variation != correct_term and variation in edited_content:
                    edited_content = edited_content.replace(variation, correct_term)
                    changes.append(EditingChange(
                        line_number=self._find_line_number(content, variation),
                        original_text=variation,
                        edited_text=correct_term,
                        change_type="technical",
                        reasoning=f"Standardized technical term: '{variation}' to '{correct_term}'",
                        confidence=0.9
                    ))
        
        return edited_content, changes
    
    def _perform_proofreading(self, content: str) -> Tuple[str, List[EditingChange]]:
        """Perform final proofreading for remaining errors."""
        changes = []
        edited_content = content
        
        # Check for double spaces
        if "  " in edited_content:
            edited_content = edited_content.replace("  ", " ")
            changes.append(EditingChange(
                line_number=0,
                original_text="  ",
                edited_text=" ",
                change_type="formatting",
                reasoning="Removed double spaces",
                confidence=1.0
            ))
        
        # Check for missing periods at end of sentences
        lines = edited_content.split("\\n")
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().endswith((".", "!", "?", ":")):
                if not line.startswith("#") and len(line.strip()) > 10:  # Likely a sentence
                    corrected_line = line.strip() + "."
                    edited_content = edited_content.replace(line, corrected_line)
                    changes.append(EditingChange(
                        line_number=i,
                        original_text=line.strip(),
                        edited_text=corrected_line,
                        change_type="punctuation",
                        reasoning="Added missing period at end of sentence",
                        confidence=0.8
                    ))
        
        return edited_content, changes
    
    def _generate_title_from_content(self, first_paragraph: str) -> str:
        """Generate a title from the first paragraph."""
        # Simplified title generation
        words = first_paragraph.split()[:8]  # First 8 words
        title = " ".join(words)
        
        # Clean up the title
        title = title.replace(".", "").replace(",", "")
        if len(title) > 60:
            title = title[:60] + "..."
        
        return title or "Content Title"
    
    def _find_sentence_containing(self, content: str, phrase: str) -> Optional[str]:
        """Find the sentence containing a specific phrase."""
        sentences = content.split(".")
        for sentence in sentences:
            if phrase in sentence:
                return sentence.strip() + "."
        return None
    
    def _find_line_number(self, content: str, text: str) -> int:
        """Find the line number containing specific text."""
        lines = content.split("\\n")
        for i, line in enumerate(lines):
            if text in line:
                return i
        return 0
    
    def _generate_editing_summary(
        self, original: str, edited: str, changes: List[EditingChange]
    ) -> Dict[str, Any]:
        """Generate summary of editing work performed."""
        original_word_count = len(original.split())
        edited_word_count = len(edited.split())
        
        change_types = {}
        for change in changes:
            change_types[change.change_type] = change_types.get(change.change_type, 0) + 1
        
        return {
            "original_word_count": original_word_count,
            "edited_word_count": edited_word_count,
            "word_count_change": edited_word_count - original_word_count,
            "total_changes": len(changes),
            "changes_by_type": change_types,
            "most_common_change_type": max(change_types.items(), key=lambda x: x[1])[0] if change_types else None,
            "average_confidence": sum(c.confidence for c in changes) / len(changes) if changes else 0.0
        }
    
    def _calculate_quality_improvements(self, original: str, edited: str) -> Dict[str, float]:
        """Calculate quality improvement metrics."""
        original_words = len(original.split())
        edited_words = len(edited.split())
        
        # Readability improvement (simplified)
        original_avg_sentence_length = original_words / max(1, original.count("."))
        edited_avg_sentence_length = edited_words / max(1, edited.count("."))
        
        readability_improvement = max(0, min(1, (original_avg_sentence_length - edited_avg_sentence_length) / 10))
        
        # Structure improvement
        original_headings = original.count("#")
        edited_headings = edited.count("#")
        structure_improvement = min(1, max(0, (edited_headings - original_headings) / 5))
        
        # Content length optimization
        word_count_ratio = edited_words / max(1, original_words)
        length_optimization = 1.0 - abs(1.0 - word_count_ratio)
        
        # Overall quality improvement
        overall_improvement = (readability_improvement + structure_improvement + length_optimization) / 3
        
        return {
            "readability_improvement": readability_improvement,
            "structure_improvement": structure_improvement, 
            "length_optimization": length_optimization,
            "overall_improvement": overall_improvement,
            "grammar_corrections": min(1, len([c for c in self.editing_history[-1].changes_made if c.change_type == "grammar"]) / 10) if self.editing_history else 0,
            "clarity_enhancements": min(1, len([c for c in self.editing_history[-1].changes_made if c.change_type == "clarity"]) / 5) if self.editing_history else 0
        }
    
    def _update_performance_metrics(self, output: EditingOutput):
        """Update performance tracking metrics."""
        self.editing_history.append(output)
        
        # Update aggregate metrics
        self.performance_metrics["total_content_edited"] += len(output.original_content.split())
        self.performance_metrics["total_changes_made"] += len(output.changes_made)
        self.performance_metrics["editing_sessions"] += 1
        
        # Calculate averages
        total_sessions = self.performance_metrics["editing_sessions"]
        
        total_improvement = sum(
            edit.quality_improvements.get("overall_improvement", 0) 
            for edit in self.editing_history
        )
        self.performance_metrics["average_improvement_score"] = total_improvement / total_sessions
        
        total_time = sum(edit.editing_time for edit in self.editing_history)
        self.performance_metrics["average_editing_time"] = total_time / total_sessions
    
    def get_capability_summary(self) -> Dict[str, Any]:
        """Get summary of editor capabilities."""
        return {
            "editor_type": self.editor_type,
            "total_capabilities": len(self.capabilities),
            "specialization_areas": self.specialization_areas,
            "quality_standards": self.quality_standards,
            "editing_preferences": self.editing_preferences,
            "capabilities_by_type": self._group_capabilities_by_type(),
            "capabilities_by_focus": self._group_capabilities_by_focus(),
            "performance_metrics": self.performance_metrics
        }
    
    def _group_capabilities_by_type(self) -> Dict[str, List[str]]:
        """Group capabilities by editing type."""
        type_mapping = {}
        
        for editing_type in EditingType:
            applicable_caps = [
                cap.name for cap in self.capabilities 
                if editing_type in cap.editing_types
            ]
            type_mapping[editing_type.value] = applicable_caps
        
        return type_mapping
    
    def _group_capabilities_by_focus(self) -> Dict[str, List[str]]:
        """Group capabilities by focus area."""
        focus_mapping = {}
        
        for focus in EditingFocus:
            applicable_caps = [
                cap.name for cap in self.capabilities 
                if focus in cap.focus_areas
            ]
            focus_mapping[focus.value] = applicable_caps
        
        return focus_mapping


# Factory functions for different editor types

def create_developmental_editor(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> EditorRole:
    """Create a developmental editor specialized in content structure and organization."""
    return EditorRole(
        editor_type="developmental",
        specialization_areas=specialization_areas or ["content_strategy", "structural_analysis"],
        quality_standards=quality_standards or {
            "structure_improvement": 4.5,
            "content_coherence": 4.3,
            "argument_strength": 4.0,
            "overall_quality": 4.2
        }
    )


def create_copy_editor(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> EditorRole:
    """Create a copy editor specialized in grammar, punctuation, and accuracy."""
    return EditorRole(
        editor_type="copy",
        specialization_areas=specialization_areas or ["precision_editing", "fact_verification"],
        quality_standards=quality_standards or {
            "grammar_accuracy": 4.9,
            "punctuation_accuracy": 4.8,
            "fact_accuracy": 4.7,
            "consistency": 4.6
        }
    )


def create_line_editor(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> EditorRole:
    """Create a line editor specialized in sentence-level improvements."""
    return EditorRole(
        editor_type="line",
        specialization_areas=specialization_areas or ["sentence_optimization", "flow_enhancement"],
        quality_standards=quality_standards or {
            "sentence_quality": 4.4,
            "flow_improvement": 4.2,
            "word_choice": 4.0,
            "readability": 4.3
        }
    )


def create_technical_editor(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> EditorRole:
    """Create a technical editor specialized in technical content accuracy."""
    return EditorRole(
        editor_type="technical",
        specialization_areas=specialization_areas or ["technical_accuracy", "documentation_standards"],
        quality_standards=quality_standards or {
            "technical_accuracy": 4.8,
            "terminology_consistency": 4.6,
            "clarity": 4.4,
            "completeness": 4.5
        }
    )


def create_content_editor(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> EditorRole:
    """Create a content editor specialized in audience alignment and message optimization."""
    return EditorRole(
        editor_type="content",
        specialization_areas=specialization_areas or ["audience_alignment", "message_optimization"],
        quality_standards=quality_standards or {
            "audience_alignment": 4.3,
            "message_clarity": 4.2,
            "engagement": 4.0,
            "effectiveness": 4.1
        }
    )


def create_general_editor(
    specialization_areas: Optional[List[str]] = None,
    quality_standards: Optional[Dict[str, float]] = None
) -> EditorRole:
    """Create a general editor with broad editing capabilities."""
    return EditorRole(
        editor_type="general",
        specialization_areas=specialization_areas or ["versatile_editing", "quality_improvement"],
        quality_standards=quality_standards or {
            "grammar_accuracy": 4.2,
            "clarity_improvement": 4.0,
            "style_consistency": 3.8,
            "overall_quality": 4.0
        }
    )


# Demo function
def demo_editor_roles():
    """Demonstrate different editor roles and capabilities."""
    print("Editor Role Demonstration")
    print("=" * 50)
    
    # Test different editor types
    editors = {
        "Developmental": create_developmental_editor(),
        "Copy": create_copy_editor(),
        "Line": create_line_editor(),
        "Technical": create_technical_editor(),
        "Content": create_content_editor()
    }
    
    # Sample content to edit
    sample_content = """
    Artificial intelligence in healthcare is really important. It can help doctors make better decisions and it can also help patients get better care. There are many different ways that AI is being used in healthcare today. Some examples include diagnostic imaging, drug discovery, and personalized treatment recommendations.
    
    One of the main benefits of AI in healthcare is that it can process large amounts of data very quickly. This allows doctors to make more informed decisions about patient care. However their are also some challenges with using AI in healthcare. For example, there are concerns about data privacy and the accuracy of AI algorithms.
    
    In conclusion, AI has the potential to revolutionize healthcare, but there are still many challenges that need to be addressed.
    """
    
    for editor_name, editor in editors.items():
        print(f"\\n{editor_name} Editor:")
        print("-" * 30)
        
        # Show capabilities
        summary = editor.get_capability_summary()
        print(f"Capabilities: {summary['total_capabilities']}")
        print(f"Specializations: {', '.join(summary['specialization_areas'])}")
        
        # Test editing
        requirements = {
            "type": editor.editor_type,
            "focus": ["clarity", "correctness", "style"],
            "audience": "healthcare professionals",
            "preserve_voice": True
        }
        
        output = editor.edit_content(sample_content, requirements)
        
        print(f"\\nEditing results:")
        print(f"Changes made: {len(output.changes_made)}")
        print(f"Editing time: {output.editing_time:.2f}s")
        print(f"Quality improvement: {output.quality_improvements['overall_improvement']:.2f}")
        
        # Show some changes
        if output.changes_made:
            print(f"\\nSample changes:")
            for change in output.changes_made[:3]:  # Show first 3 changes
                print(f"  • {change.change_type}: '{change.original_text}' → '{change.edited_text}'")
                print(f"    Reason: {change.reasoning}")


if __name__ == "__main__":
    demo_editor_roles()