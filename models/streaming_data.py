"""Data models for streaming information."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class StreamingMetrics:
    """Class for holding daily streaming metrics."""
    date: datetime
    streams: int
    followers: int
    saves: Optional[int] = None
    shares: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None


@dataclass
class Song:
    """Class for song information."""
    title: str
    artist: str
    album: Optional[str] = None
    release_date: Optional[datetime] = None
    genre: Optional[str] = None
    isrc: Optional[str] = None
    duration_seconds: Optional[int] = None
    
    @property
    def duration_formatted(self) -> str:
        """Format song duration as MM:SS."""
        if self.duration_seconds is None:
            return "Unknown"
        
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        return f"{minutes}:{seconds:02d}"


@dataclass
class SongPerformance:
    """Class for song performance metrics."""
    song: Song
    total_streams: int
    avg_completion_rate: float
    saves: int
    shares: int
    daily_data: List[StreamingMetrics]
    platform_distribution: Dict[str, int]
    
    @property
    def save_rate(self) -> float:
        """Calculate save rate."""
        if self.total_streams == 0:
            return 0
        return self.saves / self.total_streams
    
    @property
    def share_rate(self) -> float:
        """Calculate share rate."""
        if self.total_streams == 0:
            return 0
        return self.shares / self.total_streams
    
    def get_engagement_score(self) -> float:
        """Calculate overall engagement score."""
        # Normalize values
        norm_streams = min(self.total_streams / 10000, 1)
        norm_saves = min(self.save_rate / 0.3, 1)
        norm_shares = min(self.share_rate / 0.05, 1)
        
        # Weighted score
        weights = [0.4, 0.2, 0.2, 0.2]
        score = (
            norm_streams * weights[0] +
            norm_saves * weights[1] +
            norm_shares * weights[2] +
            self.avg_completion_rate * weights[3]
        )
        
        return score * 100


@dataclass
class ArtistProfile:
    """Class for artist profile information."""
    name: str
    total_followers: int
    total_streams: int
    song_count: int
    top_songs: List[SongPerformance]
    daily_metrics: List[StreamingMetrics]
    platform_distribution: Dict[str, int]
    geographic_distribution: Dict[str, int]
    
    def get_performance_summary(self) -> Dict:
        """Get a summary of overall performance."""
        avg_daily_streams = sum(metric.streams for metric in self.daily_metrics) / len(self.daily_metrics)
        
        return {
            "name": self.name,
            "total_followers": self.total_followers,
            "total_streams": self.total_streams,
            "song_count": self.song_count,
            "avg_daily_streams": avg_daily_streams,
            "top_song": self.top_songs[0].song.title if self.top_songs else None,
            "platforms": len(self.platform_distribution),
            "countries": len(self.geographic_distribution)
        }
    
    def get_growth_metrics(self) -> Dict:
        """Calculate growth metrics between first and last data points."""
        if len(self.daily_metrics) < 2:
            return {
                "stream_growth": 0,
                "follower_growth": 0
            }
        
        first_metrics = self.daily_metrics[0]
        last_metrics = self.daily_metrics[-1]
        
        stream_growth = (last_metrics.streams - first_metrics.streams) / first_metrics.streams if first_metrics.streams > 0 else 0
        follower_growth = (last_metrics.followers - first_metrics.followers) / first_metrics.followers if first_metrics.followers > 0 else 0
        
        return {
            "stream_growth": stream_growth,
            "follower_growth": follower_growth
        }


@dataclass
class PlatformData:
    """Class for platform-specific data."""
    platform_name: str
    streams: int
    revenue: float
    avg_stream_value: float
    
    @property
    def revenue_per_thousand(self) -> float:
        """Calculate revenue per thousand streams."""
        if self.streams == 0:
            return 0
        return (self.revenue / self.streams) * 1000


@dataclass
class RevenueData:
    """Class for revenue data."""
    total_revenue: float
    platform_breakdown: List[PlatformData]
    daily_revenue: List[Dict[str, float]]
    
    def get_platform_revenue_share(self) -> Dict[str, float]:
        """Get revenue share percentage by platform."""
        total = sum(platform.revenue for platform in self.platform_breakdown)
        
        if total == 0:
            return {platform.platform_name: 0 for platform in self.platform_breakdown}
        
        return {
            platform.platform_name: platform.revenue / total
            for platform in self.platform_breakdown
        }
    
    def get_average_daily_revenue(self) -> float:
        """Calculate average daily revenue."""
        if not self.daily_revenue:
            return 0
        
        return sum(day["revenue"] for day in self.daily_revenue) / len(self.daily_revenue)