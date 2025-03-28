"""
Service for interacting with the YouTube Music API to retrieve artist data.
"""
import requests
from typing import Dict, List, Any, Optional

from config.credentials import YOUTUBE_API_KEY


class YouTubeService:
    """Service class for interacting with YouTube API."""
    
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
    
    def search_artists(self, artist_name: str, max_results: int = 5) -> Optional[List[Dict[str, Any]]]:
        """Search for artists by name."""
        url = f"{self.BASE_URL}/search"
        params = {
            "part": "snippet",
            "q": f"{artist_name} official artist",
            "type": "channel",
            "maxResults": max_results,
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching for artists: {e}")
            return None
    
    def get_channel_details(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get details for a YouTube channel."""
        url = f"{self.BASE_URL}/channels"
        params = {
            "part": "snippet,statistics,brandingSettings",
            "id": channel_id,
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            items = response.json().get("items", [])
            return items[0] if items else None
        except requests.exceptions.RequestException as e:
            print(f"Error getting channel details: {e}")
            return None
    
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> Optional[List[Dict[str, Any]]]:
        """Get videos from a channel."""
        # First get the uploads playlist ID
        channel_details = self.get_channel_details(channel_id)
        if not channel_details:
            return None
        
        # Get the uploads playlist ID
        content_details = channel_details.get("contentDetails", {})
        uploads_playlist_id = content_details.get("relatedPlaylists", {}).get("uploads")
        
        if not uploads_playlist_id:
            return None
        
        # Now get the videos from the uploads playlist
        url = f"{self.BASE_URL}/playlistItems"
        params = {
            "part": "snippet,contentDetails",
            "playlistId": uploads_playlist_id,
            "maxResults": max_results,
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting channel videos: {e}")
            return None
    
    def get_video_details(self, video_ids: List[str]) -> Optional[List[Dict[str, Any]]]:
        """Get detailed information about videos."""
        if not video_ids:
            return []
        
        url = f"{self.BASE_URL}/videos"
        params = {
            "part": "snippet,contentDetails,statistics",
            "id": ",".join(video_ids),
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting video details: {e}")
            return None
    
    def search_music_videos(self, artist_name: str, max_results: int = 10) -> Optional[List[Dict[str, Any]]]:
        """Search for music videos by an artist."""
        url = f"{self.BASE_URL}/search"
        params = {
            "part": "snippet",
            "q": f"{artist_name} official music video",
            "type": "video",
            "videoCategoryId": "10",  # 10 is the category ID for Music
            "maxResults": max_results,
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            items = response.json().get("items", [])
            
            # If we have items, get more details for them
            if items:
                video_ids = [item.get("id", {}).get("videoId") for item in items]
                return self.get_video_details(video_ids)
            
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error searching for music videos: {e}")
            return None
    
    def format_artist_data(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """Format artist data for the dashboard."""
        # Search for the artist channel
        channels = self.search_artists(artist_name, max_results=1)
        if not channels:
            return None
        
        channel = channels[0]
        channel_id = channel.get("id", {}).get("channelId")
        
        # Get channel details
        channel_details = self.get_channel_details(channel_id)
        if not channel_details:
            return None
        
        # Get channel statistics
        statistics = channel_details.get("statistics", {})
        
        # Get channel videos
        videos = self.get_channel_videos(channel_id, max_results=50)
        if not videos:
            videos = []
        
        # Get music videos
        music_videos = self.search_music_videos(artist_name)
        if not music_videos:
            music_videos = []
        
        return {
            "channel": {
                "id": channel_id,
                "title": channel_details.get("snippet", {}).get("title"),
                "description": channel_details.get("snippet", {}).get("description"),
                "customUrl": channel_details.get("snippet", {}).get("customUrl"),
                "publishedAt": channel_details.get("snippet", {}).get("publishedAt"),
                "thumbnail": channel_details.get("snippet", {}).get("thumbnails", {}).get("high", {}).get("url"),
                "subscriberCount": int(statistics.get("subscriberCount", 0)),
                "videoCount": int(statistics.get("videoCount", 0)),
                "viewCount": int(statistics.get("viewCount", 0)),
            },
            "videos": [
                {
                    "id": video.get("contentDetails", {}).get("videoId"),
                    "title": video.get("snippet", {}).get("title"),
                    "publishedAt": video.get("snippet", {}).get("publishedAt"),
                    "thumbnail": video.get("snippet", {}).get("thumbnails", {}).get("high", {}).get("url"),
                    "description": video.get("snippet", {}).get("description")
                }
                for video in videos
            ],
            "musicVideos": [
                {
                    "id": video.get("id"),
                    "title": video.get("snippet", {}).get("title"),
                    "publishedAt": video.get("snippet", {}).get("publishedAt"),
                    "thumbnail": video.get("snippet", {}).get("thumbnails", {}).get("high", {}).get("url"),
                    "viewCount": int(video.get("statistics", {}).get("viewCount", 0)),
                    "likeCount": int(video.get("statistics", {}).get("likeCount", 0)),
                    "commentCount": int(video.get("statistics", {}).get("commentCount", 0))
                }
                for video in music_videos
            ]
        }