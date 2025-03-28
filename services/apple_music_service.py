"""
Service for interacting with the Apple Music API to retrieve artist data.
"""
import requests
import jwt
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from config.credentials import APPLE_MUSIC_KEY_ID, APPLE_MUSIC_TEAM_ID, APPLE_MUSIC_PRIVATE_KEY


class AppleMusicService:
    """Service class for interacting with Apple Music API."""
    
    BASE_URL = "https://api.music.apple.com/v1"
    
    def __init__(self):
        self.developer_token = None
        self.token_expiry = None
    
    def _generate_token(self) -> str:
        """Generate a developer token for Apple Music API."""
        # Token expiry time - 15 minutes (Apple's max is 6 months)
        expiry_time = int(time.time()) + 900  # 15 minutes
        
        # Create the payload
        payload = {
            'iss': APPLE_MUSIC_TEAM_ID,
            'iat': int(time.time()),
            'exp': expiry_time,
            'sub': 'artist-dashboard'  # Can be any string
        }
        
        # Generate the token
        token = jwt.encode(
            payload,
            APPLE_MUSIC_PRIVATE_KEY,
            algorithm='ES256',
            headers={
                'kid': APPLE_MUSIC_KEY_ID,
                'alg': 'ES256'
            }
        )
        
        return token
    
    def authenticate(self) -> bool:
        """Authenticate with Apple Music API."""
        if self.developer_token and self.token_expiry and self.token_expiry > datetime.now():
            return True  # Token is still valid
        
        try:
            self.developer_token = self._generate_token()
            self.token_expiry = datetime.now() + timedelta(minutes=15)
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def _get_api_header(self) -> Dict[str, str]:
        """Get the API request header with developer token."""
        return {
            "Authorization": f"Bearer {self.developer_token}",
            "Content-Type": "application/json"
        }
    
    def search_artist(self, artist_name: str, limit: int = 1) -> Optional[List[Dict[str, Any]]]:
        """Search for an artist by name."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/catalog/us/search"
        params = {
            "term": artist_name,
            "types": "artists",
            "limit": limit
        }
        
        try:
            response = requests.get(url, headers=self._get_api_header(), params=params)
            response.raise_for_status()
            
            results = response.json()
            return results.get("results", {}).get("artists", {}).get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching for artist: {e}")
            return None
    
    def get_artist(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Get artist information by Apple Music artist ID."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/catalog/us/artists/{artist_id}"
        
        try:
            response = requests.get(url, headers=self._get_api_header())
            response.raise_for_status()
            
            results = response.json()
            data = results.get("data", [])
            return data[0] if data else None
        except requests.exceptions.RequestException as e:
            print(f"Error getting artist: {e}")
            return None
    
    def get_artist_albums(self, artist_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get albums for an artist by ID."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/catalog/us/artists/{artist_id}/albums"
        params = {"limit": 100}
        
        try:
            response = requests.get(url, headers=self._get_api_header(), params=params)
            response.raise_for_status()
            
            results = response.json()
            return results.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting artist albums: {e}")
            return None
    
    def get_album_tracks(self, album_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get tracks for an album by ID."""
        if not self.authenticate():
            return None
        
        url = f"{self.BASE_URL}/catalog/us/albums/{album_id}/tracks"
        
        try:
            response = requests.get(url, headers=self._get_api_header())
            response.raise_for_status()
            
            results = response.json()
            return results.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting album tracks: {e}")
            return None
    
    def format_artist_data(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Format artist data for the dashboard."""
        artist_info = self.get_artist(artist_id)
        if not artist_info:
            return None
        
        # Get attributes from the artist info
        attributes = artist_info.get("attributes", {})
        
        # Get albums
        albums_data = self.get_artist_albums(artist_id) or []
        
        # Process albums and get tracks for each album
        albums = []
        top_tracks = []
        
        for album in albums_data:
            album_id = album.get("id")
            album_attributes = album.get("attributes", {})
            
            # Format album data
            albums.append({
                "name": album_attributes.get("name"),
                "id": album_id,
                "type": album_attributes.get("artistName"),
                "release_date": album_attributes.get("releaseDate"),
                "track_count": album_attributes.get("trackCount", 0),
                "genre": album_attributes.get("genreNames", []),
                "image_url": album_attributes.get("artwork", {}).get("url", "").replace("{w}", "300").replace("{h}", "300")
            })
            
            # Get tracks for this album
            album_tracks = self.get_album_tracks(album_id) or []
            
            for track in album_tracks:
                track_attributes = track.get("attributes", {})
                
                # Add to top tracks list
                top_tracks.append({
                    "name": track_attributes.get("name"),
                    "id": track.get("id"),
                    "album": album_attributes.get("name"),
                    "duration_ms": track_attributes.get("durationInMillis", 0),
                    "disc_number": track_attributes.get("discNumber", 1),
                    "track_number": track_attributes.get("trackNumber", 1),
                    "preview_url": track_attributes.get("previews", [{}])[0].get("url") if track_attributes.get("previews") else None
                })
        
        # Sort top tracks by popularity (not directly available, so we'll use track number as a proxy)
        top_tracks.sort(key=lambda x: (x.get("disc_number", 1), x.get("track_number", 1)))
        top_tracks = top_tracks[:10]  # Take top 10 tracks
        
        return {
            "artist": {
                "name": attributes.get("name"),
                "id": artist_id,
                "genre": attributes.get("genreNames", []),
                "image_url": attributes.get("artwork", {}).get("url", "").replace("{w}", "300").replace("{h}", "300")
            },
            "top_tracks": top_tracks,
            "albums": albums
        }