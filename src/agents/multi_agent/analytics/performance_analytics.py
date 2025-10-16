"""Content Performance Analytics System

Analytics system to track content performance metrics, engagement rates,
and success indicators for continuous improvement and data-driven decisions.
"""

import json
import statistics
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

from src.config.logging_config import setup_logging

logger = setup_logging(__name__)


class MetricType(Enum):
    """Types of performance metrics."""
    VIEWS = "views"
    UNIQUE_VISITORS = "unique_visitors"
    ENGAGEMENT_RATE = "engagement_rate"
    TIME_ON_PAGE = "time_on_page"
    BOUNCE_RATE = "bounce_rate"
    SCROLL_DEPTH = "scroll_depth"
    SHARES = "shares"
    LIKES = "likes"
    COMMENTS = "comments"
    CONVERSIONS = "conversions"
    CLICK_THROUGH_RATE = "click_through_rate"
    RETURN_RATE = "return_rate"


class PerformanceStatus(Enum):
    """Performance status categories."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"
    POOR = "poor"


class TrendDirection(Enum):
    """Trend direction indicators."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


@dataclass
class ContentMetrics:
    """Performance metrics for content."""
    content_id: str
    platform: str
    
    # Traffic metrics
    views: int = 0
    unique_visitors: int = 0
    page_views: int = 0
    sessions: int = 0
    
    # Engagement metrics
    average_time_on_page: float = 0.0  # seconds
    bounce_rate: float = 0.0  # percentage
    scroll_depth_average: float = 0.0  # percentage
    engagement_rate: float = 0.0  # percentage
    
    # Social metrics
    shares: int = 0
    likes: int = 0
    comments: int = 0
    bookmarks: int = 0
    
    # Conversion metrics
    conversions: int = 0
    conversion_rate: float = 0.0  # percentage
    click_through_rate: float = 0.0  # percentage
    
    # Audience metrics
    return_visitors: int = 0
    new_visitors: int = 0
    return_rate: float = 0.0  # percentage
    
    # SEO metrics
    organic_traffic: int = 0
    search_impressions: int = 0
    average_position: float = 0.0
    click_through_rate_search: float = 0.0
    
    # Time period
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=datetime.now)
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class PerformanceScore:
    """Overall performance score and rating."""
    content_id: str
    overall_score: float  # 0-100
    status: PerformanceStatus
    
    # Component scores
    traffic_score: float
    engagement_score: float
    social_score: float
    conversion_score: float
    seo_score: float
    
    # Rankings
    percentile_rank: float  # 0-100, compared to other content
    category_rank: Optional[int] = None
    
    # Insights
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    calculated_at: datetime = field(default_factory=datetime.now)


@dataclass
class TrendAnalysis:
    """Trend analysis over time."""
    metric_name: str
    direction: TrendDirection
    change_percentage: float
    change_absolute: float
    
    # Statistical data
    values: List[float]
    timestamps: List[datetime]
    mean: float
    median: float
    std_deviation: float
    
    # Forecasting
    predicted_next_value: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    
    # Period
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=datetime.now)


@dataclass
class CompetitorComparison:
    """Comparison with competitor or benchmark content."""
    content_id: str
    competitor_id: str
    
    # Comparative metrics
    views_comparison: float  # ratio: our/their
    engagement_comparison: float
    social_comparison: float
    
    # Insights
    areas_ahead: List[str]
    areas_behind: List[str]
    gap_analysis: Dict[str, float]
    
    analyzed_at: datetime = field(default_factory=datetime.now)


@dataclass
class AudienceInsights:
    """Insights about content audience."""
    content_id: str
    
    # Demographics (simplified - would come from analytics platforms)
    top_locations: List[Tuple[str, int]]  # (location, count)
    top_devices: List[Tuple[str, int]]  # (device, count)
    top_browsers: List[Tuple[str, int]]  # (browser, count)
    
    # Behavior
    average_session_duration: float
    pages_per_session: float
    most_common_entry_page: str
    most_common_exit_page: str
    
    # Traffic sources
    traffic_sources: Dict[str, int]  # source -> count
    top_referrers: List[Tuple[str, int]]
    
    # Engagement patterns
    peak_engagement_times: List[str]  # Hour of day
    peak_engagement_days: List[str]  # Day of week
    
    analyzed_at: datetime = field(default_factory=datetime.now)


@dataclass
class ContentPerformanceReport:
    """Comprehensive performance report."""
    content_id: str
    content_title: str
    report_period: str
    
    # Core metrics
    metrics: ContentMetrics
    performance_score: PerformanceScore
    
    # Analysis
    trends: List[TrendAnalysis]
    audience_insights: AudienceInsights
    
    # Comparisons
    period_over_period_comparison: Dict[str, float]
    benchmark_comparison: Optional[CompetitorComparison] = None
    
    # ROI metrics
    estimated_revenue: Optional[float] = None
    cost_per_acquisition: Optional[float] = None
    return_on_investment: Optional[float] = None
    
    # Recommendations
    top_recommendations: List[str]
    optimization_opportunities: List[str]
    
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContentAnalytics:
    """Content performance analytics system."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize content analytics system.
        
        Args:
            storage_path: Path to store analytics data
        """
        self.storage_path = storage_path or Path("./analytics_data")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory metrics storage
        self.metrics_history: Dict[str, List[ContentMetrics]] = defaultdict(list)
        
        # Performance benchmarks
        self.benchmarks = {
            "views": {"excellent": 10000, "good": 5000, "average": 1000, "poor": 100},
            "engagement_rate": {"excellent": 8.0, "good": 5.0, "average": 3.0, "poor": 1.0},
            "bounce_rate": {"excellent": 30.0, "good": 50.0, "average": 70.0, "poor": 85.0},
            "conversion_rate": {"excellent": 5.0, "good": 3.0, "average": 1.5, "poor": 0.5},
            "average_time_on_page": {"excellent": 300, "good": 180, "average": 90, "poor": 30}
        }
        
        logger.info("Content analytics system initialized")
    
    def track_metrics(
        self,
        content_id: str,
        platform: str,
        metrics_data: Dict[str, Any]
    ) -> ContentMetrics:
        """Track performance metrics for content.
        
        Args:
            content_id: Content identifier
            platform: Publishing platform
            metrics_data: Metrics data dictionary
            
        Returns:
            ContentMetrics object
        """
        logger.info(f"Tracking metrics for {content_id} on {platform}")
        
        metrics = ContentMetrics(
            content_id=content_id,
            platform=platform,
            views=metrics_data.get("views", 0),
            unique_visitors=metrics_data.get("unique_visitors", 0),
            page_views=metrics_data.get("page_views", 0),
            sessions=metrics_data.get("sessions", 0),
            average_time_on_page=metrics_data.get("average_time_on_page", 0.0),
            bounce_rate=metrics_data.get("bounce_rate", 0.0),
            scroll_depth_average=metrics_data.get("scroll_depth_average", 0.0),
            engagement_rate=metrics_data.get("engagement_rate", 0.0),
            shares=metrics_data.get("shares", 0),
            likes=metrics_data.get("likes", 0),
            comments=metrics_data.get("comments", 0),
            bookmarks=metrics_data.get("bookmarks", 0),
            conversions=metrics_data.get("conversions", 0),
            conversion_rate=metrics_data.get("conversion_rate", 0.0),
            click_through_rate=metrics_data.get("click_through_rate", 0.0),
            return_visitors=metrics_data.get("return_visitors", 0),
            new_visitors=metrics_data.get("new_visitors", 0),
            return_rate=metrics_data.get("return_rate", 0.0),
            organic_traffic=metrics_data.get("organic_traffic", 0),
            search_impressions=metrics_data.get("search_impressions", 0),
            average_position=metrics_data.get("average_position", 0.0),
            click_through_rate_search=metrics_data.get("click_through_rate_search", 0.0),
            period_start=metrics_data.get("period_start", datetime.now()),
            period_end=metrics_data.get("period_end", datetime.now())
        )
        
        # Store in history
        self.metrics_history[content_id].append(metrics)
        
        # Persist to storage
        self._save_metrics(metrics)
        
        logger.info(f"Metrics tracked: {metrics.views} views, {metrics.engagement_rate}% engagement")
        return metrics
    
    def calculate_performance_score(
        self,
        content_id: str,
        metrics: Optional[ContentMetrics] = None
    ) -> PerformanceScore:
        """Calculate overall performance score.
        
        Args:
            content_id: Content identifier
            metrics: Optional metrics (uses latest if not provided)
            
        Returns:
            PerformanceScore with detailed scoring
        """
        if metrics is None:
            if content_id not in self.metrics_history or not self.metrics_history[content_id]:
                raise ValueError(f"No metrics found for content: {content_id}")
            metrics = self.metrics_history[content_id][-1]
        
        logger.info(f"Calculating performance score for {content_id}")
        
        # Calculate component scores (0-100)
        traffic_score = self._calculate_traffic_score(metrics)
        engagement_score = self._calculate_engagement_score(metrics)
        social_score = self._calculate_social_score(metrics)
        conversion_score = self._calculate_conversion_score(metrics)
        seo_score = self._calculate_seo_score(metrics)
        
        # Weighted overall score
        weights = {
            "traffic": 0.25,
            "engagement": 0.25,
            "social": 0.15,
            "conversion": 0.20,
            "seo": 0.15
        }
        
        overall_score = (
            traffic_score * weights["traffic"] +
            engagement_score * weights["engagement"] +
            social_score * weights["social"] +
            conversion_score * weights["conversion"] +
            seo_score * weights["seo"]
        )
        
        # Determine status
        if overall_score >= 80:
            status = PerformanceStatus.EXCELLENT
        elif overall_score >= 65:
            status = PerformanceStatus.GOOD
        elif overall_score >= 50:
            status = PerformanceStatus.AVERAGE
        elif overall_score >= 35:
            status = PerformanceStatus.BELOW_AVERAGE
        else:
            status = PerformanceStatus.POOR
        
        # Calculate percentile rank (simplified)
        all_scores = self._get_all_scores()
        if all_scores:
            percentile_rank = (sum(1 for s in all_scores if s < overall_score) / len(all_scores)) * 100
        else:
            percentile_rank = 50.0
        
        # Generate insights
        strengths = self._identify_strengths(metrics, traffic_score, engagement_score, social_score, conversion_score, seo_score)
        weaknesses = self._identify_weaknesses(metrics, traffic_score, engagement_score, social_score, conversion_score, seo_score)
        recommendations = self._generate_performance_recommendations(metrics, weaknesses)
        
        score = PerformanceScore(
            content_id=content_id,
            overall_score=overall_score,
            status=status,
            traffic_score=traffic_score,
            engagement_score=engagement_score,
            social_score=social_score,
            conversion_score=conversion_score,
            seo_score=seo_score,
            percentile_rank=percentile_rank,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
        
        logger.info(f"Performance score calculated: {overall_score:.1f}/100 ({status.value})")
        return score
    
    def analyze_trends(
        self,
        content_id: str,
        metric_name: str,
        period_days: int = 30
    ) -> TrendAnalysis:
        """Analyze trends for a specific metric.
        
        Args:
            content_id: Content identifier
            metric_name: Metric to analyze
            period_days: Number of days to analyze
            
        Returns:
            TrendAnalysis with trend data
        """
        logger.info(f"Analyzing {metric_name} trends for {content_id}")
        
        if content_id not in self.metrics_history or not self.metrics_history[content_id]:
            raise ValueError(f"No metrics history found for content: {content_id}")
        
        # Get metric values from history
        history = self.metrics_history[content_id]
        
        # Filter by period
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent_history = [m for m in history if m.last_updated >= cutoff_date]
        
        if not recent_history:
            raise ValueError(f"No recent metrics found for period: {period_days} days")
        
        # Extract values
        values = [getattr(m, metric_name, 0) for m in recent_history]
        timestamps = [m.last_updated for m in recent_history]
        
        # Calculate statistics
        mean_value = statistics.mean(values) if values else 0
        median_value = statistics.median(values) if values else 0
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        # Determine trend direction
        if len(values) >= 2:
            first_half_avg = statistics.mean(values[:len(values)//2])
            second_half_avg = statistics.mean(values[len(values)//2:])
            
            change_pct = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
            change_abs = second_half_avg - first_half_avg
            
            if abs(change_pct) < 5:
                direction = TrendDirection.STABLE
            elif change_pct > 15:
                direction = TrendDirection.INCREASING
            elif change_pct < -15:
                direction = TrendDirection.DECREASING
            elif std_dev / mean_value > 0.5 if mean_value > 0 else False:
                direction = TrendDirection.VOLATILE
            else:
                direction = TrendDirection.STABLE
        else:
            direction = TrendDirection.STABLE
            change_pct = 0
            change_abs = 0
        
        # Simple forecasting (linear extrapolation)
        if len(values) >= 3:
            recent_trend = values[-1] - values[-3]
            predicted_next = values[-1] + (recent_trend / 2)
            confidence_interval = (
                predicted_next - std_dev,
                predicted_next + std_dev
            )
        else:
            predicted_next = None
            confidence_interval = None
        
        trend = TrendAnalysis(
            metric_name=metric_name,
            direction=direction,
            change_percentage=change_pct,
            change_absolute=change_abs,
            values=values,
            timestamps=timestamps,
            mean=mean_value,
            median=median_value,
            std_deviation=std_dev,
            predicted_next_value=predicted_next,
            confidence_interval=confidence_interval,
            period_start=timestamps[0] if timestamps else datetime.now(),
            period_end=timestamps[-1] if timestamps else datetime.now()
        )
        
        logger.info(f"Trend analysis: {direction.value}, change: {change_pct:+.1f}%")
        return trend
    
    def get_audience_insights(
        self,
        content_id: str,
        analytics_data: Optional[Dict[str, Any]] = None
    ) -> AudienceInsights:
        """Get insights about content audience.
        
        Args:
            content_id: Content identifier
            analytics_data: Optional analytics data (simulated if not provided)
            
        Returns:
            AudienceInsights with audience data
        """
        logger.info(f"Generating audience insights for {content_id}")
        
        # In production, this would pull from Google Analytics, etc.
        # For demo, use simulated data
        if analytics_data is None:
            analytics_data = self._generate_sample_audience_data()
        
        insights = AudienceInsights(
            content_id=content_id,
            top_locations=analytics_data.get("top_locations", []),
            top_devices=analytics_data.get("top_devices", []),
            top_browsers=analytics_data.get("top_browsers", []),
            average_session_duration=analytics_data.get("average_session_duration", 0.0),
            pages_per_session=analytics_data.get("pages_per_session", 0.0),
            most_common_entry_page=analytics_data.get("most_common_entry_page", ""),
            most_common_exit_page=analytics_data.get("most_common_exit_page", ""),
            traffic_sources=analytics_data.get("traffic_sources", {}),
            top_referrers=analytics_data.get("top_referrers", []),
            peak_engagement_times=analytics_data.get("peak_engagement_times", []),
            peak_engagement_days=analytics_data.get("peak_engagement_days", [])
        )
        
        logger.info("Audience insights generated")
        return insights
    
    def compare_periods(
        self,
        content_id: str,
        current_period_days: int = 7,
        previous_period_days: int = 7
    ) -> Dict[str, float]:
        """Compare performance between two time periods.
        
        Args:
            content_id: Content identifier
            current_period_days: Days in current period
            previous_period_days: Days in previous period
            
        Returns:
            Dictionary of metric changes (percentage)
        """
        logger.info(f"Comparing periods for {content_id}")
        
        if content_id not in self.metrics_history or len(self.metrics_history[content_id]) < 2:
            logger.warning("Insufficient data for period comparison")
            return {}
        
        history = self.metrics_history[content_id]
        
        # Get current and previous period metrics
        now = datetime.now()
        current_cutoff = now - timedelta(days=current_period_days)
        previous_cutoff = current_cutoff - timedelta(days=previous_period_days)
        
        current_metrics = [m for m in history if m.last_updated >= current_cutoff]
        previous_metrics = [m for m in history if previous_cutoff <= m.last_updated < current_cutoff]
        
        if not current_metrics or not previous_metrics:
            logger.warning("Insufficient data in one or both periods")
            return {}
        
        # Calculate averages for key metrics
        comparison = {}
        metric_names = ["views", "engagement_rate", "conversion_rate", "bounce_rate", "average_time_on_page"]
        
        for metric_name in metric_names:
            current_avg = statistics.mean([getattr(m, metric_name, 0) for m in current_metrics])
            previous_avg = statistics.mean([getattr(m, metric_name, 0) for m in previous_metrics])
            
            if previous_avg > 0:
                change_pct = ((current_avg - previous_avg) / previous_avg) * 100
            else:
                change_pct = 100.0 if current_avg > 0 else 0.0
            
            comparison[metric_name] = change_pct
        
        logger.info(f"Period comparison completed: {len(comparison)} metrics analyzed")
        return comparison
    
    def generate_performance_report(
        self,
        content_id: str,
        content_title: str,
        period_days: int = 30
    ) -> ContentPerformanceReport:
        """Generate comprehensive performance report.
        
        Args:
            content_id: Content identifier
            content_title: Content title
            period_days: Report period in days
            
        Returns:
            ContentPerformanceReport with comprehensive analysis
        """
        logger.info(f"Generating performance report for {content_id}")
        
        # Get latest metrics
        if content_id not in self.metrics_history or not self.metrics_history[content_id]:
            raise ValueError(f"No metrics found for content: {content_id}")
        
        latest_metrics = self.metrics_history[content_id][-1]
        
        # Calculate performance score
        performance_score = self.calculate_performance_score(content_id, latest_metrics)
        
        # Analyze trends for key metrics
        trends = []
        trend_metrics = ["views", "engagement_rate", "conversion_rate"]
        for metric_name in trend_metrics:
            try:
                trend = self.analyze_trends(content_id, metric_name, period_days)
                trends.append(trend)
            except Exception as e:
                logger.warning(f"Could not analyze trend for {metric_name}: {str(e)}")
        
        # Get audience insights
        audience_insights = self.get_audience_insights(content_id)
        
        # Period over period comparison
        period_comparison = self.compare_periods(content_id, period_days // 2, period_days // 2)
        
        # Generate recommendations
        top_recommendations = performance_score.recommendations[:5]
        optimization_opportunities = self._identify_optimization_opportunities(
            latest_metrics, performance_score
        )
        
        report = ContentPerformanceReport(
            content_id=content_id,
            content_title=content_title,
            report_period=f"Last {period_days} days",
            metrics=latest_metrics,
            performance_score=performance_score,
            trends=trends,
            audience_insights=audience_insights,
            period_over_period_comparison=period_comparison,
            top_recommendations=top_recommendations,
            optimization_opportunities=optimization_opportunities
        )
        
        logger.info("Performance report generated successfully")
        return report
    
    # Private helper methods
    
    def _calculate_traffic_score(self, metrics: ContentMetrics) -> float:
        """Calculate traffic score (0-100)."""
        views_score = min(100, (metrics.views / self.benchmarks["views"]["excellent"]) * 100)
        visitors_ratio = metrics.unique_visitors / max(1, metrics.views)
        visitor_quality_score = visitors_ratio * 100
        
        return (views_score * 0.7 + visitor_quality_score * 0.3)
    
    def _calculate_engagement_score(self, metrics: ContentMetrics) -> float:
        """Calculate engagement score (0-100)."""
        # Engagement rate score
        engagement_score = min(100, (metrics.engagement_rate / self.benchmarks["engagement_rate"]["excellent"]) * 100)
        
        # Time on page score
        time_score = min(100, (metrics.average_time_on_page / self.benchmarks["average_time_on_page"]["excellent"]) * 100)
        
        # Bounce rate score (inverted - lower is better)
        bounce_score = max(0, 100 - (metrics.bounce_rate / self.benchmarks["bounce_rate"]["poor"] * 100))
        
        # Scroll depth score
        scroll_score = metrics.scroll_depth_average
        
        return (engagement_score * 0.3 + time_score * 0.3 + bounce_score * 0.2 + scroll_score * 0.2)
    
    def _calculate_social_score(self, metrics: ContentMetrics) -> float:
        """Calculate social score (0-100)."""
        total_social = metrics.shares + metrics.likes + metrics.comments
        
        if total_social == 0:
            return 0.0
        
        # Social engagement relative to views
        if metrics.views > 0:
            social_rate = (total_social / metrics.views) * 100
            score = min(100, social_rate * 20)  # 5% social rate = 100 score
        else:
            score = 0.0
        
        # Bonus for diverse engagement
        engagement_types = sum([1 for x in [metrics.shares, metrics.likes, metrics.comments] if x > 0])
        diversity_bonus = engagement_types * 5
        
        return min(100, score + diversity_bonus)
    
    def _calculate_conversion_score(self, metrics: ContentMetrics) -> float:
        """Calculate conversion score (0-100)."""
        if metrics.conversion_rate == 0:
            return 0.0
        
        conversion_score = min(100, (metrics.conversion_rate / self.benchmarks["conversion_rate"]["excellent"]) * 100)
        ctr_score = min(100, metrics.click_through_rate * 10)
        
        return (conversion_score * 0.7 + ctr_score * 0.3)
    
    def _calculate_seo_score(self, metrics: ContentMetrics) -> float:
        """Calculate SEO score (0-100)."""
        # Organic traffic score
        if metrics.views > 0:
            organic_ratio = metrics.organic_traffic / metrics.views
            organic_score = min(100, organic_ratio * 150)  # 67% organic = 100 score
        else:
            organic_score = 0.0
        
        # Search position score (lower is better)
        if metrics.average_position > 0:
            position_score = max(0, 100 - (metrics.average_position * 5))
        else:
            position_score = 50.0
        
        # Search CTR score
        ctr_search_score = min(100, metrics.click_through_rate_search * 10)
        
        return (organic_score * 0.4 + position_score * 0.4 + ctr_search_score * 0.2)
    
    def _identify_strengths(
        self, metrics: ContentMetrics,
        traffic_score: float, engagement_score: float,
        social_score: float, conversion_score: float, seo_score: float
    ) -> List[str]:
        """Identify content strengths."""
        strengths = []
        
        if traffic_score >= 75:
            strengths.append(f"Strong traffic performance ({metrics.views:,} views)")
        
        if engagement_score >= 75:
            strengths.append(f"High engagement rate ({metrics.engagement_rate:.1f}%)")
        
        if social_score >= 75:
            strengths.append(f"Excellent social sharing ({metrics.shares + metrics.likes + metrics.comments} interactions)")
        
        if conversion_score >= 75:
            strengths.append(f"Strong conversion rate ({metrics.conversion_rate:.1f}%)")
        
        if seo_score >= 75:
            strengths.append(f"Good SEO performance ({metrics.organic_traffic:,} organic visits)")
        
        if metrics.average_time_on_page >= self.benchmarks["average_time_on_page"]["good"]:
            strengths.append(f"High time on page ({metrics.average_time_on_page:.0f}s average)")
        
        if metrics.bounce_rate <= self.benchmarks["bounce_rate"]["good"]:
            strengths.append(f"Low bounce rate ({metrics.bounce_rate:.1f}%)")
        
        return strengths
    
    def _identify_weaknesses(
        self, metrics: ContentMetrics,
        traffic_score: float, engagement_score: float,
        social_score: float, conversion_score: float, seo_score: float
    ) -> List[str]:
        """Identify content weaknesses."""
        weaknesses = []
        
        if traffic_score < 40:
            weaknesses.append(f"Low traffic ({metrics.views:,} views)")
        
        if engagement_score < 40:
            weaknesses.append(f"Poor engagement rate ({metrics.engagement_rate:.1f}%)")
        
        if social_score < 40:
            weaknesses.append("Limited social sharing")
        
        if conversion_score < 40:
            weaknesses.append(f"Low conversion rate ({metrics.conversion_rate:.1f}%)")
        
        if seo_score < 40:
            weaknesses.append("Weak SEO performance")
        
        if metrics.bounce_rate >= self.benchmarks["bounce_rate"]["average"]:
            weaknesses.append(f"High bounce rate ({metrics.bounce_rate:.1f}%)")
        
        if metrics.average_time_on_page <= self.benchmarks["average_time_on_page"]["poor"]:
            weaknesses.append(f"Short time on page ({metrics.average_time_on_page:.0f}s)")
        
        return weaknesses
    
    def _generate_performance_recommendations(
        self, metrics: ContentMetrics, weaknesses: List[str]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if "Low traffic" in str(weaknesses):
            recommendations.append("Improve SEO: Optimize title, meta description, and keywords")
            recommendations.append("Promote on social media and relevant communities")
            recommendations.append("Consider paid promotion to boost initial visibility")
        
        if "Poor engagement" in str(weaknesses) or "High bounce rate" in str(weaknesses):
            recommendations.append("Improve content hook: Make first paragraph more compelling")
            recommendations.append("Add more visuals, examples, and interactive elements")
            recommendations.append("Break up long paragraphs for better readability")
        
        if "Limited social sharing" in str(weaknesses):
            recommendations.append("Add prominent social sharing buttons")
            recommendations.append("Include shareable quotes or statistics")
            recommendations.append("Create engaging visuals optimized for social platforms")
        
        if "Low conversion" in str(weaknesses):
            recommendations.append("Strengthen call-to-action placement and wording")
            recommendations.append("Reduce friction in conversion funnel")
            recommendations.append("Add urgency or scarcity elements")
        
        if "Weak SEO" in str(weaknesses):
            recommendations.append("Research and target high-value keywords")
            recommendations.append("Build quality backlinks from relevant sites")
            recommendations.append("Improve page load speed and mobile experience")
        
        if "Short time on page" in str(weaknesses):
            recommendations.append("Add more depth and valuable information")
            recommendations.append("Include related content links to encourage exploration")
            recommendations.append("Use storytelling to increase reader engagement")
        
        return recommendations
    
    def _identify_optimization_opportunities(
        self, metrics: ContentMetrics, score: PerformanceScore
    ) -> List[str]:
        """Identify specific optimization opportunities."""
        opportunities = []
        
        # Quick wins
        if metrics.shares < 10 and metrics.views > 100:
            opportunities.append("Add social share buttons (low effort, high impact)")
        
        if metrics.bounce_rate > 60 and metrics.average_time_on_page < 60:
            opportunities.append("Improve content introduction to hook readers")
        
        if metrics.conversion_rate < 2.0 and metrics.views > 500:
            opportunities.append("A/B test different call-to-action variations")
        
        if metrics.organic_traffic < metrics.views * 0.3:
            opportunities.append("Conduct SEO audit and optimize on-page factors")
        
        # Strategic opportunities
        if score.traffic_score > 70 but score.conversion_score < 40:
            opportunities.append("High traffic but low conversions - optimize conversion funnel")
        
        if score.engagement_score > 70 but score.social_score < 40:
            opportunities.append("Engaged audience not sharing - make sharing easier and more rewarding")
        
        return opportunities
    
    def _get_all_scores(self) -> List[float]:
        """Get all historical scores for percentile calculation."""
        # Simplified - in production would calculate scores for all content
        return [65.0, 72.0, 58.0, 81.0, 45.0, 90.0, 55.0, 78.0]
    
    def _generate_sample_audience_data(self) -> Dict[str, Any]:
        """Generate sample audience data for demo."""
        return {
            "top_locations": [
                ("United States", 450),
                ("United Kingdom", 120),
                ("Canada", 85),
                ("Germany", 62),
                ("Australia", 48)
            ],
            "top_devices": [
                ("Desktop", 420),
                ("Mobile", 315),
                ("Tablet", 85)
            ],
            "top_browsers": [
                ("Chrome", 510),
                ("Safari", 180),
                ("Firefox", 95),
                ("Edge", 35)
            ],
            "average_session_duration": 245.5,
            "pages_per_session": 2.8,
            "most_common_entry_page": "/home",
            "most_common_exit_page": "/about",
            "traffic_sources": {
                "organic": 380,
                "direct": 210,
                "social": 145,
                "referral": 85
            },
            "top_referrers": [
                ("google.com", 380),
                ("twitter.com", 95),
                ("reddit.com", 50)
            ],
            "peak_engagement_times": ["10:00", "14:00", "19:00"],
            "peak_engagement_days": ["Tuesday", "Wednesday", "Thursday"]
        }
    
    def _save_metrics(self, metrics: ContentMetrics) -> None:
        """Save metrics to storage."""
        file_path = self.storage_path / "metrics" / f"{metrics.content_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        metrics_data = {
            "content_id": metrics.content_id,
            "platform": metrics.platform,
            "views": metrics.views,
            "engagement_rate": metrics.engagement_rate,
            "conversion_rate": metrics.conversion_rate,
            "tracked_at": metrics.last_updated.isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(metrics_data, f, indent=2)


# Demo function
def demo_performance_analytics():
    """Demonstrate content performance analytics."""
    print("Content Performance Analytics Demonstration")
    print("=" * 60)
    
    analytics = ContentAnalytics()
    
    # Simulate tracking metrics over time
    print("\n1. Tracking Content Metrics")
    print("-" * 40)
    
    content_id = "blog_post_001"
    
    # Track metrics for 3 time periods
    metrics_data_week1 = {
        "views": 1250,
        "unique_visitors": 980,
        "engagement_rate": 6.5,
        "average_time_on_page": 185.0,
        "bounce_rate": 45.0,
        "scroll_depth_average": 72.0,
        "shares": 23,
        "likes": 47,
        "comments": 8,
        "conversions": 18,
        "conversion_rate": 1.44,
        "organic_traffic": 720,
        "return_rate": 12.5
    }
    
    m1 = analytics.track_metrics(content_id, "wordpress", metrics_data_week1)
    print(f"✓ Week 1: {m1.views:,} views, {m1.engagement_rate}% engagement")
    
    # Week 2 - improved performance
    metrics_data_week2 = metrics_data_week1.copy()
    metrics_data_week2.update({
        "views": 1850,
        "unique_visitors": 1520,
        "engagement_rate": 7.8,
        "average_time_on_page": 215.0,
        "shares": 35,
        "likes": 72,
        "comments": 15,
        "conversions": 32,
        "conversion_rate": 1.73
    })
    
    m2 = analytics.track_metrics(content_id, "wordpress", metrics_data_week2)
    print(f"✓ Week 2: {m2.views:,} views, {m2.engagement_rate}% engagement")
    
    # Week 3 - continued growth
    metrics_data_week3 = metrics_data_week2.copy()
    metrics_data_week3.update({
        "views": 2340,
        "unique_visitors": 1980,
        "engagement_rate": 8.5,
        "shares": 48,
        "likes": 95,
        "conversions": 45,
        "conversion_rate": 1.92
    })
    
    m3 = analytics.track_metrics(content_id, "wordpress", metrics_data_week3)
    print(f"✓ Week 3: {m3.views:,} views, {m3.engagement_rate}% engagement")
    
    # Calculate performance score
    print("\n2. Performance Score Analysis")
    print("-" * 40)
    
    score = analytics.calculate_performance_score(content_id)
    print(f"📊 Overall Score: {score.overall_score:.1f}/100")
    print(f"   Status: {score.status.value.upper()}")
    print(f"   Percentile Rank: {score.percentile_rank:.1f}%")
    
    print("\n   Component Scores:")
    print(f"   - Traffic:     {score.traffic_score:.1f}/100")
    print(f"   - Engagement:  {score.engagement_score:.1f}/100")
    print(f"   - Social:      {score.social_score:.1f}/100")
    print(f"   - Conversion:  {score.conversion_score:.1f}/100")
    print(f"   - SEO:         {score.seo_score:.1f}/100")
    
    # Show strengths
    print("\n3. Content Strengths")
    print("-" * 40)
    for strength in score.strengths:
        print(f"   ✓ {strength}")
    
    # Show weaknesses
    if score.weaknesses:
        print("\n4. Areas for Improvement")
        print("-" * 40)
        for weakness in score.weaknesses:
            print(f"   ! {weakness}")
    
    # Analyze trends
    print("\n5. Trend Analysis")
    print("-" * 40)
    
    trend = analytics.analyze_trends(content_id, "views", period_days=30)
    print(f"   Metric: Views")
    print(f"   Direction: {trend.direction.value.upper()}")
    print(f"   Change: {trend.change_percentage:+.1f}%")
    print(f"   Mean: {trend.mean:.0f}")
    print(f"   Predicted Next: {trend.predicted_next_value:.0f}" if trend.predicted_next_value else "")
    
    # Period comparison
    print("\n6. Period-over-Period Comparison")
    print("-" * 40)
    
    comparison = analytics.compare_periods(content_id, 7, 7)
    if comparison:
        for metric, change in comparison.items():
            arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
            print(f"   {metric:25s} {arrow} {change:+.1f}%")
    
    # Audience insights
    print("\n7. Audience Insights")
    print("-" * 40)
    
    insights = analytics.get_audience_insights(content_id)
    print(f"   Top Locations:")
    for location, count in insights.top_locations[:3]:
        print(f"      - {location}: {count:,} visitors")
    
    print(f"\n   Traffic Sources:")
    for source, count in insights.traffic_sources.items():
        pct = (count / sum(insights.traffic_sources.values())) * 100
        print(f"      - {source}: {count:,} ({pct:.1f}%)")
    
    print(f"\n   Peak Engagement:")
    print(f"      Times: {', '.join(insights.peak_engagement_times)}")
    print(f"      Days: {', '.join(insights.peak_engagement_days)}")
    
    # Recommendations
    print("\n8. Top Recommendations")
    print("-" * 40)
    
    for i, rec in enumerate(score.recommendations[:5], 1):
        print(f"   {i}. {rec}")
    
    # Generate full report
    print("\n9. Comprehensive Performance Report")
    print("-" * 40)
    
    report = analytics.generate_performance_report(
        content_id,
        "Getting Started with Python AI",
        period_days=21
    )
    
    print(f"   Report Period: {report.report_period}")
    print(f"   Overall Score: {report.performance_score.overall_score:.1f}/100")
    print(f"   Total Views: {report.metrics.views:,}")
    print(f"   Engagement Rate: {report.metrics.engagement_rate:.1f}%")
    print(f"   Conversion Rate: {report.metrics.conversion_rate:.1f}%")
    print(f"\n   Trends Analyzed: {len(report.trends)}")
    print(f"   Optimization Opportunities: {len(report.optimization_opportunities)}")
    
    print("\n" + "=" * 60)
    print("Performance analytics demonstration complete!")


if __name__ == "__main__":
    demo_performance_analytics()
