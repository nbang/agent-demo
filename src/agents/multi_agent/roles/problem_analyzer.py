"""
Problem Analyzer Agent Role - Breaks down complex problems into manageable components.

This module provides a specialized agent role for analyzing complex problems,
identifying root causes, understanding dependencies, and recognizing opportunities.

Key Capabilities:
- Root cause analysis
- Problem decomposition
- Dependency mapping
- Risk identification
- Impact assessment
- Opportunity recognition

Usage:
    analyzer = create_problem_analyzer()
    analysis = analyzer.analyze_problem(
        problem_description="System performance degradation",
        context={"system": "e-commerce", "scale": "1M users"}
    )
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AnalysisMethod(Enum):
    """Methods for problem analysis."""
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    FISHBONE_DIAGRAM = "fishbone_diagram"
    FIVE_WHYS = "five_whys"
    SWOT_ANALYSIS = "swot_analysis"
    PARETO_ANALYSIS = "pareto_analysis"
    FAULT_TREE_ANALYSIS = "fault_tree_analysis"


class AnalysisDepth(Enum):
    """Depth of analysis."""
    SURFACE = "surface"
    MODERATE = "moderate"
    DEEP = "deep"
    COMPREHENSIVE = "comprehensive"


class ImpactLevel(Enum):
    """Impact level classification."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


@dataclass
class RootCause:
    """Identified root cause of a problem."""
    cause_id: str
    description: str
    category: str  # Technical, Process, People, Environment
    evidence: List[str]
    confidence: float  # 0.0 to 1.0
    impact_level: ImpactLevel
    related_causes: List[str] = field(default_factory=list)


@dataclass
class ProblemComponent:
    """Key component of the problem."""
    component_id: str
    name: str
    description: str
    role_in_problem: str
    affected_stakeholders: List[str]
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Dependency:
    """Dependency identified in the problem."""
    dependency_id: str
    from_component: str
    to_component: str
    dependency_type: str  # Technical, Business, Process
    criticality: str  # Critical, Important, Optional
    description: str


@dataclass
class RiskFactor:
    """Risk factor in the problem."""
    risk_id: str
    description: str
    probability: float  # 0.0 to 1.0
    impact: ImpactLevel
    risk_score: float
    mitigation_approaches: List[str] = field(default_factory=list)


@dataclass
class Opportunity:
    """Opportunity identified during analysis."""
    opportunity_id: str
    description: str
    potential_benefit: str
    required_action: str
    feasibility: str  # High, Medium, Low
    priority: str  # High, Medium, Low


@dataclass
class ImpactArea:
    """Area impacted by the problem."""
    area_id: str
    name: str
    description: str
    impact_level: ImpactLevel
    affected_metrics: List[str]
    stakeholders: List[str]
    estimated_cost: Optional[str] = None


@dataclass
class ProblemAnalysisCapability:
    """Capabilities of the problem analyzer."""
    analysis_methods: List[AnalysisMethod]
    max_depth: AnalysisDepth
    specialized_domains: List[str]
    supported_problem_types: List[str]
    confidence_threshold: float


@dataclass
class ComprehensiveProblemAnalysis:
    """Complete analysis result from problem analyzer."""
    analysis_id: str
    problem_id: str
    problem_title: str
    problem_description: str
    
    # Analysis findings
    root_causes: List[RootCause]
    key_components: List[ProblemComponent]
    dependencies: List[Dependency]
    risk_factors: List[RiskFactor]
    opportunities: List[Opportunity]
    impact_areas: List[ImpactArea]
    
    # Analysis metadata
    analysis_method: AnalysisMethod
    analysis_depth: AnalysisDepth
    confidence_score: float
    analysis_summary: str
    recommendations: List[str]
    
    # Analyst info
    analyzed_by: str
    analyzed_at: datetime = field(default_factory=datetime.now)
    
    def get_critical_root_causes(self) -> List[RootCause]:
        """Get root causes with critical or high impact."""
        return [rc for rc in self.root_causes 
                if rc.impact_level in [ImpactLevel.CRITICAL, ImpactLevel.HIGH]]
    
    def get_high_priority_opportunities(self) -> List[Opportunity]:
        """Get high-priority opportunities."""
        return [opp for opp in self.opportunities if opp.priority == "High"]
    
    def get_critical_dependencies(self) -> List[Dependency]:
        """Get critical dependencies."""
        return [dep for dep in self.dependencies if dep.criticality == "Critical"]


class ProblemAnalyzerRole:
    """
    Problem Analyzer agent role specializing in breaking down complex problems.
    
    This agent analyzes problems systematically to identify root causes,
    understand dependencies, assess impacts, and recognize opportunities.
    
    Core Capabilities:
    - Root cause identification using multiple methodologies
    - Problem decomposition into manageable components
    - Dependency and relationship mapping
    - Risk factor identification and assessment
    - Impact area analysis
    - Opportunity recognition
    """
    
    def __init__(
        self,
        analyzer_name: str = "Problem Analyzer",
        analysis_methods: Optional[List[AnalysisMethod]] = None,
        max_depth: AnalysisDepth = AnalysisDepth.DEEP,
        specialized_domains: Optional[List[str]] = None,
        confidence_threshold: float = 0.7
    ):
        """
        Initialize the problem analyzer role.
        
        Args:
            analyzer_name: Name of the analyzer
            analysis_methods: Preferred analysis methods
            max_depth: Maximum depth of analysis
            specialized_domains: Domains of expertise
            confidence_threshold: Minimum confidence for findings
        """
        self.analyzer_name = analyzer_name
        self.analysis_methods = analysis_methods or [
            AnalysisMethod.ROOT_CAUSE_ANALYSIS,
            AnalysisMethod.FIVE_WHYS,
            AnalysisMethod.SWOT_ANALYSIS
        ]
        self.max_depth = max_depth
        self.specialized_domains = specialized_domains or [
            "Software Systems",
            "Business Processes",
            "Technical Architecture",
            "Operational Efficiency"
        ]
        self.confidence_threshold = confidence_threshold
        
        self.capability = ProblemAnalysisCapability(
            analysis_methods=self.analysis_methods,
            max_depth=max_depth,
            specialized_domains=self.specialized_domains,
            supported_problem_types=[
                "Technical", "Business", "Process", "Strategic", "Operational"
            ],
            confidence_threshold=confidence_threshold
        )
        
        logger.info(f"Initialized {analyzer_name} with {len(self.analysis_methods)} methods")
    
    def analyze_problem(
        self,
        problem_id: str,
        problem_title: str,
        problem_description: str,
        context: Optional[Dict[str, Any]] = None,
        analysis_method: Optional[AnalysisMethod] = None,
        analysis_depth: Optional[AnalysisDepth] = None
    ) -> ComprehensiveProblemAnalysis:
        """
        Analyze a complex problem to identify root causes and key components.
        
        Args:
            problem_id: Unique problem identifier
            problem_title: Problem title
            problem_description: Detailed problem description
            context: Additional context information
            analysis_method: Specific method to use (optional)
            analysis_depth: Desired analysis depth (optional)
            
        Returns:
            ComprehensiveProblemAnalysis with detailed findings
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🔍 {self.analyzer_name}: Analyzing Problem")
        logger.info(f"{'='*60}")
        logger.info(f"Problem: {problem_title}")
        
        method = analysis_method or self.analysis_methods[0]
        depth = analysis_depth or self.max_depth
        context = context or {}
        
        logger.info(f"Method: {method.value}")
        logger.info(f"Depth: {depth.value}")
        
        # Perform root cause analysis
        logger.info("\n🎯 Step 1: Root Cause Analysis")
        root_causes = self._identify_root_causes(
            problem_description, context, method, depth
        )
        logger.info(f"   Found {len(root_causes)} root causes")
        
        # Decompose into key components
        logger.info("\n🧩 Step 2: Problem Decomposition")
        components = self._decompose_problem(
            problem_description, context, root_causes
        )
        logger.info(f"   Identified {len(components)} key components")
        
        # Map dependencies
        logger.info("\n🔗 Step 3: Dependency Mapping")
        dependencies = self._map_dependencies(components, context)
        logger.info(f"   Mapped {len(dependencies)} dependencies")
        
        # Identify risk factors
        logger.info("\n⚠️  Step 4: Risk Identification")
        risk_factors = self._identify_risks(
            problem_description, root_causes, components, context
        )
        logger.info(f"   Identified {len(risk_factors)} risk factors")
        
        # Assess impact areas
        logger.info("\n📊 Step 5: Impact Assessment")
        impact_areas = self._assess_impact(
            problem_description, components, context
        )
        logger.info(f"   Assessed {len(impact_areas)} impact areas")
        
        # Recognize opportunities
        logger.info("\n💡 Step 6: Opportunity Recognition")
        opportunities = self._recognize_opportunities(
            problem_description, root_causes, components, context
        )
        logger.info(f"   Recognized {len(opportunities)} opportunities")
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(
            root_causes, components, context
        )
        
        # Generate summary and recommendations
        summary = self._generate_summary(
            problem_title, root_causes, components, confidence
        )
        recommendations = self._generate_recommendations(
            root_causes, opportunities, risk_factors
        )
        
        analysis = ComprehensiveProblemAnalysis(
            analysis_id=f"ANALYSIS-{problem_id}",
            problem_id=problem_id,
            problem_title=problem_title,
            problem_description=problem_description,
            root_causes=root_causes,
            key_components=components,
            dependencies=dependencies,
            risk_factors=risk_factors,
            opportunities=opportunities,
            impact_areas=impact_areas,
            analysis_method=method,
            analysis_depth=depth,
            confidence_score=confidence,
            analysis_summary=summary,
            recommendations=recommendations,
            analyzed_by=self.analyzer_name
        )
        
        logger.info(f"\n✅ Analysis Complete")
        logger.info(f"   Confidence: {confidence:.0%}")
        logger.info(f"   Critical Root Causes: {len(analysis.get_critical_root_causes())}")
        logger.info(f"   High-Priority Opportunities: {len(analysis.get_high_priority_opportunities())}")
        
        return analysis
    
    def _identify_root_causes(
        self,
        problem_description: str,
        context: Dict[str, Any],
        method: AnalysisMethod,
        depth: AnalysisDepth
    ) -> List[RootCause]:
        """Identify root causes of the problem."""
        # In real implementation, this would use AI to analyze the problem
        # For now, we'll simulate analysis based on keywords
        
        root_causes = []
        
        # Simulate root cause identification
        if "performance" in problem_description.lower():
            root_causes.append(RootCause(
                cause_id="RC-001",
                description="Inefficient database query patterns leading to slow response times",
                category="Technical",
                evidence=[
                    "Query execution times exceed 5 seconds",
                    "Database CPU utilization above 90%",
                    "N+1 query problems identified in logs"
                ],
                confidence=0.90,
                impact_level=ImpactLevel.CRITICAL
            ))
            root_causes.append(RootCause(
                cause_id="RC-002",
                description="Lack of caching strategy for frequently accessed data",
                category="Technical",
                evidence=[
                    "Same queries repeated multiple times per request",
                    "No cache layer implemented",
                    "High database load during peak hours"
                ],
                confidence=0.85,
                impact_level=ImpactLevel.HIGH,
                related_causes=["RC-001"]
            ))
        
        if "scalability" in problem_description.lower() or "monolithic" in problem_description.lower():
            root_causes.append(RootCause(
                cause_id="RC-003",
                description="Monolithic architecture limiting horizontal scalability",
                category="Technical",
                evidence=[
                    "Single application instance handles all requests",
                    "Tightly coupled components",
                    "Difficult to scale specific services independently"
                ],
                confidence=0.88,
                impact_level=ImpactLevel.HIGH
            ))
        
        if "resource" in problem_description.lower() or "constraint" in problem_description.lower():
            root_causes.append(RootCause(
                cause_id="RC-004",
                description="Insufficient resource allocation and capacity planning",
                category="Process",
                evidence=[
                    "No capacity planning process in place",
                    "Resources allocated reactively",
                    "Frequent resource exhaustion incidents"
                ],
                confidence=0.75,
                impact_level=ImpactLevel.MEDIUM
            ))
        
        if "technical debt" in problem_description.lower() or "legacy" in problem_description.lower():
            root_causes.append(RootCause(
                cause_id="RC-005",
                description="Accumulated technical debt reducing maintainability",
                category="Technical",
                evidence=[
                    "Legacy code without documentation",
                    "High coupling and low cohesion",
                    "Difficulty implementing new features"
                ],
                confidence=0.80,
                impact_level=ImpactLevel.MEDIUM,
                related_causes=["RC-003"]
            ))
        
        # If no specific root causes identified, provide generic ones
        if not root_causes:
            root_causes = [
                RootCause(
                    cause_id="RC-001",
                    description="Insufficient understanding of system requirements and constraints",
                    category="Process",
                    evidence=["Unclear requirements", "Ambiguous specifications"],
                    confidence=0.70,
                    impact_level=ImpactLevel.MEDIUM
                ),
                RootCause(
                    cause_id="RC-002",
                    description="Resource constraints limiting effective problem resolution",
                    category="Environment",
                    evidence=["Budget limitations", "Time constraints"],
                    confidence=0.65,
                    impact_level=ImpactLevel.MEDIUM
                )
            ]
        
        return root_causes
    
    def _decompose_problem(
        self,
        problem_description: str,
        context: Dict[str, Any],
        root_causes: List[RootCause]
    ) -> List[ProblemComponent]:
        """Decompose problem into key components."""
        components = []
        
        # Simulate problem decomposition based on context
        if "performance" in problem_description.lower():
            components.append(ProblemComponent(
                component_id="COMP-001",
                name="Application Layer",
                description="Frontend and backend application components experiencing slow response times",
                role_in_problem="Primary bottleneck for user requests",
                affected_stakeholders=["End Users", "Development Team", "Operations Team"],
                metrics={"response_time": "5-10 seconds", "throughput": "100 req/s"}
            ))
            components.append(ProblemComponent(
                component_id="COMP-002",
                name="Database Layer",
                description="Database queries and connection management causing delays",
                role_in_problem="Data access bottleneck",
                affected_stakeholders=["Database Team", "Operations Team"],
                metrics={"query_time": "2-5 seconds", "cpu_usage": "90%"}
            ))
        
        if "infrastructure" in problem_description.lower() or "monolithic" in problem_description.lower():
            components.append(ProblemComponent(
                component_id="COMP-003",
                name="Infrastructure Architecture",
                description="Overall system architecture and deployment infrastructure",
                role_in_problem="Limits scalability and flexibility",
                affected_stakeholders=["DevOps Team", "Architecture Team", "Management"],
                metrics={"instances": "1", "scaling": "vertical only"}
            ))
        
        if "user" in problem_description.lower() or "customer" in problem_description.lower():
            components.append(ProblemComponent(
                component_id="COMP-004",
                name="User Experience",
                description="End-user interaction and satisfaction with the system",
                role_in_problem="Affected by performance and availability issues",
                affected_stakeholders=["End Users", "Product Team", "Support Team"],
                metrics={"satisfaction": "60%", "abandonment_rate": "35%"}
            ))
        
        # Add business impact component
        components.append(ProblemComponent(
            component_id="COMP-005",
            name="Business Operations",
            description="Business processes and operations impacted by the problem",
            role_in_problem="Revenue and operational efficiency affected",
            affected_stakeholders=["Management", "Sales Team", "Finance Team"],
            metrics={"revenue_impact": context.get("revenue_impact", "Unknown")}
        ))
        
        return components
    
    def _map_dependencies(
        self,
        components: List[ProblemComponent],
        context: Dict[str, Any]
    ) -> List[Dependency]:
        """Map dependencies between components."""
        dependencies = []
        
        # Create dependencies based on component relationships
        comp_dict = {c.component_id: c for c in components}
        
        if "COMP-001" in comp_dict and "COMP-002" in comp_dict:
            dependencies.append(Dependency(
                dependency_id="DEP-001",
                from_component="COMP-001",
                to_component="COMP-002",
                dependency_type="Technical",
                criticality="Critical",
                description="Application layer depends on database layer for data access"
            ))
        
        if "COMP-002" in comp_dict and "COMP-003" in comp_dict:
            dependencies.append(Dependency(
                dependency_id="DEP-002",
                from_component="COMP-002",
                to_component="COMP-003",
                dependency_type="Technical",
                criticality="Critical",
                description="Database performance depends on infrastructure capacity"
            ))
        
        if "COMP-001" in comp_dict and "COMP-004" in comp_dict:
            dependencies.append(Dependency(
                dependency_id="DEP-003",
                from_component="COMP-004",
                to_component="COMP-001",
                dependency_type="Business",
                criticality="Critical",
                description="User experience directly depends on application performance"
            ))
        
        if "COMP-004" in comp_dict and "COMP-005" in comp_dict:
            dependencies.append(Dependency(
                dependency_id="DEP-004",
                from_component="COMP-005",
                to_component="COMP-004",
                dependency_type="Business",
                criticality="Important",
                description="Business operations depend on positive user experience"
            ))
        
        return dependencies
    
    def _identify_risks(
        self,
        problem_description: str,
        root_causes: List[RootCause],
        components: List[ProblemComponent],
        context: Dict[str, Any]
    ) -> List[RiskFactor]:
        """Identify risk factors."""
        risks = []
        
        # Identify risks based on root causes and components
        if any("technical" in rc.category.lower() for rc in root_causes):
            risks.append(RiskFactor(
                risk_id="RISK-001",
                description="Implementation complexity may exceed estimates",
                probability=0.65,
                impact=ImpactLevel.HIGH,
                risk_score=0.65 * 0.8,  # probability * impact
                mitigation_approaches=[
                    "Conduct detailed technical assessment",
                    "Build proof-of-concept first",
                    "Allocate buffer time in schedule"
                ]
            ))
        
        if "resource" in problem_description.lower() or "budget" in problem_description.lower():
            risks.append(RiskFactor(
                risk_id="RISK-002",
                description="Resource availability may not meet project needs",
                probability=0.55,
                impact=ImpactLevel.MEDIUM,
                risk_score=0.55 * 0.6,
                mitigation_approaches=[
                    "Secure resource commitments early",
                    "Identify backup resources",
                    "Prioritize critical work"
                ]
            ))
        
        if len(components) > 3:
            risks.append(RiskFactor(
                risk_id="RISK-003",
                description="Integration complexity between multiple components",
                probability=0.70,
                impact=ImpactLevel.HIGH,
                risk_score=0.70 * 0.8,
                mitigation_approaches=[
                    "Define clear integration contracts",
                    "Test integrations early and often",
                    "Implement fallback mechanisms"
                ]
            ))
        
        risks.append(RiskFactor(
            risk_id="RISK-004",
            description="Timeline constraints may lead to rushed implementation",
            probability=0.50,
            impact=ImpactLevel.MEDIUM,
            risk_score=0.50 * 0.6,
            mitigation_approaches=[
                "Break work into smaller iterations",
                "Focus on MVP first",
                "Communicate timeline risks early"
            ]
        ))
        
        return risks
    
    def _assess_impact(
        self,
        problem_description: str,
        components: List[ProblemComponent],
        context: Dict[str, Any]
    ) -> List[ImpactArea]:
        """Assess impact areas."""
        impact_areas = []
        
        # Identify impact areas based on problem and components
        impact_areas.append(ImpactArea(
            area_id="IMPACT-001",
            name="End User Experience",
            description="User satisfaction and engagement with the system",
            impact_level=ImpactLevel.CRITICAL,
            affected_metrics=["Page Load Time", "Bounce Rate", "Session Duration", "Conversion Rate"],
            stakeholders=["End Users", "Product Team", "Customer Success"],
            estimated_cost=context.get("revenue_impact", "Significant")
        ))
        
        impact_areas.append(ImpactArea(
            area_id="IMPACT-002",
            name="Operational Efficiency",
            description="Team productivity and operational overhead",
            impact_level=ImpactLevel.HIGH,
            affected_metrics=["Incident Response Time", "Development Velocity", "System Uptime"],
            stakeholders=["Engineering Team", "Operations Team", "Support Team"]
        ))
        
        if "business" in context or "revenue" in problem_description.lower():
            impact_areas.append(ImpactArea(
                area_id="IMPACT-003",
                name="Business Revenue",
                description="Direct impact on company revenue and growth",
                impact_level=ImpactLevel.CRITICAL,
                affected_metrics=["Revenue", "Customer Acquisition", "Customer Retention"],
                stakeholders=["Management", "Sales Team", "Finance"],
                estimated_cost=context.get("revenue_impact", "High")
            ))
        
        impact_areas.append(ImpactArea(
            area_id="IMPACT-004",
            name="Technical Debt",
            description="Long-term maintainability and system health",
            impact_level=ImpactLevel.MEDIUM,
            affected_metrics=["Code Quality", "Test Coverage", "Deployment Frequency"],
            stakeholders=["Engineering Team", "Architecture Team"]
        ))
        
        return impact_areas
    
    def _recognize_opportunities(
        self,
        problem_description: str,
        root_causes: List[RootCause],
        components: List[ProblemComponent],
        context: Dict[str, Any]
    ) -> List[Opportunity]:
        """Recognize opportunities within the problem."""
        opportunities = []
        
        # Identify opportunities based on the problem context
        if "performance" in problem_description.lower() or "technical" in problem_description.lower():
            opportunities.append(Opportunity(
                opportunity_id="OPP-001",
                description="Modernize technology stack and architecture",
                potential_benefit="Improved performance, scalability, and developer productivity",
                required_action="Evaluate modern frameworks and migration strategies",
                feasibility="High",
                priority="High"
            ))
        
        if any("process" in rc.category.lower() for rc in root_causes):
            opportunities.append(Opportunity(
                opportunity_id="OPP-002",
                description="Establish systematic capacity planning process",
                potential_benefit="Proactive resource management and cost optimization",
                required_action="Implement monitoring and forecasting tools",
                feasibility="High",
                priority="Medium"
            ))
        
        opportunities.append(Opportunity(
            opportunity_id="OPP-003",
            description="Build team expertise through problem resolution",
            potential_benefit="Enhanced team capabilities and knowledge transfer",
            required_action="Document learnings and conduct knowledge sharing sessions",
            feasibility="High",
            priority="Medium"
        ))
        
        if len(components) > 2:
            opportunities.append(Opportunity(
                opportunity_id="OPP-004",
                description="Improve monitoring and observability",
                potential_benefit="Earlier detection of issues and faster resolution",
                required_action="Implement comprehensive monitoring and alerting system",
                feasibility="High",
                priority="High"
            ))
        
        return opportunities
    
    def _calculate_confidence(
        self,
        root_causes: List[RootCause],
        components: List[ProblemComponent],
        context: Dict[str, Any]
    ) -> float:
        """Calculate overall confidence in the analysis."""
        if not root_causes:
            return 0.5
        
        # Average confidence of root causes
        avg_confidence = sum(rc.confidence for rc in root_causes) / len(root_causes)
        
        # Adjust based on available context
        context_factor = min(1.0, len(context) / 5.0)  # More context = higher confidence
        
        # Adjust based on analysis completeness
        completeness_factor = min(1.0, (len(root_causes) + len(components)) / 10.0)
        
        # Calculate weighted confidence
        confidence = (
            avg_confidence * 0.5 +
            context_factor * 0.3 +
            completeness_factor * 0.2
        )
        
        return min(0.95, confidence)  # Cap at 95%
    
    def _generate_summary(
        self,
        problem_title: str,
        root_causes: List[RootCause],
        components: List[ProblemComponent],
        confidence: float
    ) -> str:
        """Generate analysis summary."""
        critical_causes = [rc for rc in root_causes if rc.impact_level == ImpactLevel.CRITICAL]
        
        summary = f"""
Problem '{problem_title}' has been comprehensively analyzed.

Key Findings:
- Identified {len(root_causes)} root causes ({len(critical_causes)} critical)
- Decomposed into {len(components)} key components
- Analysis confidence: {confidence:.0%}

Critical Root Causes:
{chr(10).join(f'  • {rc.description}' for rc in critical_causes[:3])}

The problem requires immediate attention to address critical root causes
and prevent further impact on stakeholders and operations.
"""
        return summary.strip()
    
    def _generate_recommendations(
        self,
        root_causes: List[RootCause],
        opportunities: List[Opportunity],
        risk_factors: List[RiskFactor]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Address critical root causes
        critical_causes = [rc for rc in root_causes if rc.impact_level == ImpactLevel.CRITICAL]
        if critical_causes:
            recommendations.append(
                f"Prioritize addressing {len(critical_causes)} critical root causes immediately"
            )
        
        # Leverage high-priority opportunities
        high_priority_opps = [opp for opp in opportunities if opp.priority == "High"]
        if high_priority_opps:
            recommendations.append(
                f"Capitalize on {len(high_priority_opps)} high-priority opportunities for improvement"
            )
        
        # Mitigate high-risk factors
        high_risks = [r for r in risk_factors if r.risk_score > 0.5]
        if high_risks:
            recommendations.append(
                f"Implement mitigation strategies for {len(high_risks)} high-risk factors"
            )
        
        # General recommendations
        recommendations.extend([
            "Establish regular monitoring and assessment to track progress",
            "Engage all affected stakeholders in solution development",
            "Consider phased approach with quick wins followed by strategic improvements",
            "Document findings and learnings for future reference"
        ])
        
        return recommendations


def create_problem_analyzer(
    analyzer_name: str = "Problem Analyzer",
    analysis_depth: AnalysisDepth = AnalysisDepth.DEEP
) -> ProblemAnalyzerRole:
    """
    Factory function to create a problem analyzer agent.
    
    Args:
        analyzer_name: Name for the analyzer
        analysis_depth: Depth of analysis to perform
        
    Returns:
        Configured ProblemAnalyzerRole instance
    """
    return ProblemAnalyzerRole(
        analyzer_name=analyzer_name,
        analysis_methods=[
            AnalysisMethod.ROOT_CAUSE_ANALYSIS,
            AnalysisMethod.FIVE_WHYS,
            AnalysisMethod.SWOT_ANALYSIS
        ],
        max_depth=analysis_depth,
        specialized_domains=[
            "Software Systems",
            "Business Processes",
            "Technical Architecture",
            "Operational Efficiency",
            "User Experience"
        ],
        confidence_threshold=0.7
    )


def demo_problem_analyzer():
    """Demonstrate problem analyzer capabilities."""
    print("\n" + "="*80)
    print("🔍 PROBLEM ANALYZER DEMONSTRATION")
    print("="*80)
    
    # Create analyzer
    analyzer = create_problem_analyzer(
        analyzer_name="Senior Problem Analyzer",
        analysis_depth=AnalysisDepth.COMPREHENSIVE
    )
    
    # Define problem
    problem_description = """
    Our e-commerce platform is experiencing significant performance degradation
    during peak hours (12-2 PM and 6-9 PM daily). Page load times have increased
    from 1-2 seconds to 5-10 seconds, resulting in a 35% cart abandonment rate
    and estimated revenue loss of $500K per month.
    
    Current system:
    - Monolithic application architecture
    - Single PostgreSQL database instance
    - No caching layer
    - No CDN for static assets
    - 1M+ daily active users
    - Growing 20% month-over-month
    
    Recent changes:
    - Added new product recommendation engine (2 weeks ago)
    - Increased marketing campaigns driving 30% more traffic
    - Expanded product catalog by 50%
    """
    
    context = {
        "system_type": "E-commerce Platform",
        "scale": "1M+ daily active users",
        "revenue_impact": "$500K/month loss",
        "growth_rate": "20% MoM",
        "recent_changes": ["New recommendation engine", "Increased marketing", "Expanded catalog"]
    }
    
    # Analyze problem
    analysis = analyzer.analyze_problem(
        problem_id="PROB-001",
        problem_title="E-commerce Performance Degradation",
        problem_description=problem_description,
        context=context,
        analysis_method=AnalysisMethod.ROOT_CAUSE_ANALYSIS,
        analysis_depth=AnalysisDepth.COMPREHENSIVE
    )
    
    # Display results
    print("\n" + "="*80)
    print("📊 ANALYSIS RESULTS")
    print("="*80)
    
    print("\n📝 SUMMARY")
    print(analysis.analysis_summary)
    
    print("\n🎯 ROOT CAUSES")
    for i, rc in enumerate(analysis.root_causes, 1):
        print(f"\n{i}. {rc.description}")
        print(f"   Category: {rc.category}")
        print(f"   Impact: {rc.impact_level.value.upper()}")
        print(f"   Confidence: {rc.confidence:.0%}")
        print(f"   Evidence:")
        for evidence in rc.evidence[:2]:
            print(f"     • {evidence}")
    
    print(f"\n🧩 KEY COMPONENTS ({len(analysis.key_components)})")
    for comp in analysis.key_components[:3]:
        print(f"  • {comp.name}: {comp.description}")
    
    print(f"\n🔗 DEPENDENCIES ({len(analysis.dependencies)})")
    for dep in analysis.dependencies[:3]:
        print(f"  • {dep.description} ({dep.criticality})")
    
    print(f"\n⚠️  RISK FACTORS ({len(analysis.risk_factors)})")
    for risk in analysis.risk_factors[:3]:
        print(f"  • {risk.description} (Score: {risk.risk_score:.2f})")
    
    print(f"\n💡 OPPORTUNITIES ({len(analysis.opportunities)})")
    for opp in analysis.get_high_priority_opportunities():
        print(f"  • {opp.description}")
        print(f"    Benefit: {opp.potential_benefit}")
    
    print(f"\n📊 IMPACT AREAS ({len(analysis.impact_areas)})")
    for area in analysis.impact_areas[:3]:
        print(f"  • {area.name}: {area.impact_level.value.upper()} impact")
    
    print("\n📋 RECOMMENDATIONS")
    for i, rec in enumerate(analysis.recommendations[:5], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "="*80)
    print("✅ ANALYSIS METRICS")
    print("="*80)
    print(f"Overall Confidence: {analysis.confidence_score:.0%}")
    print(f"Critical Root Causes: {len(analysis.get_critical_root_causes())}")
    print(f"High-Priority Opportunities: {len(analysis.get_high_priority_opportunities())}")
    print(f"Critical Dependencies: {len(analysis.get_critical_dependencies())}")
    print(f"Analysis Method: {analysis.analysis_method.value}")
    print(f"Analysis Depth: {analysis.analysis_depth.value}")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    demo_problem_analyzer()
