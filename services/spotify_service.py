"""
Service for interacting with the Spotify API to retrieve artist data.
"""
import requests
import base64
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Any, Optional

from config.credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


class SpotifyService:
    """Service class for interacting with Spotify API."""
    
    BASE_URL = "https://api.spotify.com/v1"
    AUTH_URL = "https://accounts.spotify.com/api/token"
    
    def __init__(self):
        self.access_token = None
        self.token_expiry = None
    
    def _get_auth_header(self) -> Dict[str, str]:
        """Get the authorization header for API requests."""
        auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        return {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def _get_api_header(self) -> Dict[str, str]:
        """Get the API request header with bearer token."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def authenticate(self) -> bool:
        """Authenticate with Spotify API and get access token."""
        if self.access_token and self.token_expiry and self.token_expiry > datetime.now():
            return True  # Token is still valid
        
        headers = self._get_auth_header()
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(self.AUTH_URL, headers=headers, data=data)
            response.raise_for_status()
            
            response_data = response.json()
            self.access_token = response_data["access_token"]
            
            # Set token expiry (usually 3600 seconds)
            expires_in = response_data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            return False
    
    def get_artist(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Get artist information by Spotify artist ID."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/artists/{artist_id}"
        
        try:
            response = requests.get(url, headers=self._get_api_header())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting artist: {e}")
            return None
    
    def get_artist_by_name(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """Search for an artist by name and return the first result."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/search"
        params = {
            "q": artist_name,
            "type": "artist",
            "limit": 1
        }
        
        try:
            response = requests.get(url, headers=self._get_api_header(), params=params)
            response.raise_for_status()
            
            results = response.json()
            if results.get("artists", {}).get("items"):
                return results["artists"]["items"][0]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error searching for artist: {e}")
            return None
    
    def get_artist_top_tracks(self, artist_id: str, country: str = "US") -> Optional[List[Dict[str, Any]]]:
        """Get an artist's top tracks in a specific country."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/artists/{artist_id}/top-tracks"
        params = {"country": country}
        
        try:
            response = requests.get(url, headers=self._get_api_header(), params=params)
            response.raise_for_status()
            return response.json().get("tracks", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting top tracks: {e}")
            return None
    
    def get_artist_albums(self, artist_id: str, album_type: str = "album,single") -> Optional[List[Dict[str, Any]]]:
        """Get an artist's albums."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/artists/{artist_id}/albums"
        params = {
            "album_type": album_type,
            "limit": 50
        }
        
        all_albums = []
        
        try:
            while url:
                response = requests.get(url, headers=self._get_api_header(), params=params)
                response.raise_for_status()
                
                results = response.json()
                all_albums.extend(results.get("items", []))
                
                # Handle pagination
                url = results.get("next")
                params = {}  # Parameters are included in the next URL
                
                # Avoid rate limiting
                if url:
                    time.sleep(0.1)
            
            return all_albums
        except requests.exceptions.RequestException as e:
            print(f"Error getting albums: {e}")
            return None
    
    def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a track."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/tracks/{track_id}"
        
        try:
            response = requests.get(url, headers=self._get_api_header())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting track info: {e}")
            return None
    
    def get_artist_related(self, artist_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get artists related to the specified artist."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/artists/{artist_id}/related-artists"
        
        try:
            response = requests.get(url, headers=self._get_api_header())
            response.raise_for_status()
            return response.json().get("artists", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting related artists: {e}")
            return None
    
    # Note: Spotify API doesn't provide streaming stats directly.
    # This would typically require artist account access through a separate authentication flow.
    # The following method is a placeholder for what real implementation might look like.
    
    def format_artist_data(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Format artist data for the dashboard."""
        artist_info = self.get_artist(artist_id)
        if not artist_info:
            return None
            
        top_tracks = self.get_artist_top_tracks(artist_id)
        albums = self.get_artist_albums(artist_id)
        related_artists = self.get_artist_related(artist_id)
        
        return {
            "artist": {
                "name": artist_info.get("name"),
                "id": artist_info.get("id"),
                "followers": artist_info.get("followers", {}).get("total", 0),
                "popularity": artist_info.get("popularity", 0),
                "genres": artist_info.get("genres", []),
                "image_url": artist_info.get("images", [{}])[0].get("url") if artist_info.get("images") else None
            },
            "top_tracks": [
                {
                    "name": track.get("name"),
                    "id": track.get("id"),
                    "album": track.get("album", {}).get("name"),
                    "popularity": track.get("popularity", 0),
                    "duration_ms": track.get("duration_ms", 0),
                    "explicit": track.get("explicit", False),
                    "preview_url": track.get("preview_url")
                }
                for track in (top_tracks or [])
            ],
            "albums": [
                {
                    "name": album.get("name"),
                    "id": album.get("id"),
                    "type": album.get("album_type"),
                    "release_date": album.get("release_date"),
                    "total_tracks": album.get("total_tracks", 0),
                    "image_url": album.get("images", [{}])[0].get("url") if album.get("images") else None
                }
                for album in (albums or [])
            ],
            "related_artists": [
                {
                    "name": artist.get("name"),
                    "id": artist.get("id"),
                    "popularity": artist.get("popularity", 0)
                }
                for artist in (related_artists or [])[:5]  # Top 5 related artists
            ]
        }