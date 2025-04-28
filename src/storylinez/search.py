import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from .base_client import BaseClient

class SearchClient(BaseClient):
    """
    Client for interacting with Storylinez Search API.
    Provides methods for searching across different media types with various criteria.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the SearchClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.search_url = f"{self.base_url}/search"
    
    def search_video_scenes(self, query: str, media_source: str = "user", 
                          folder_path: str = None, page: int = 1, page_size: int = 20,
                          generate_thumbnail: bool = True, generate_streamable: bool = False, 
                          generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for video scenes by description.
        
        Args:
            query: Text to search for in video scene descriptions
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "query": query
        }
        
        return self._make_request("POST", f"{self.search_url}/files/video/scenes", params=params, json_data=data)
    
    def search_video_objects(self, objects: List[str], media_source: str = "user", 
                           folder_path: str = None, page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False, 
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for objects in videos.
        
        Args:
            objects: List of objects to search for
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "objects": objects
        }
        
        return self._make_request("POST", f"{self.search_url}/files/video/objects", params=params, json_data=data)
    
    def search_audio_content(self, query: str = None, genre: str = None, mood: str = None,
                           instruments: List[str] = None, media_source: str = "user",
                           folder_path: str = None, page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False,
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for audio content by text, genre, mood, or instruments.
        
        Args:
            query: Text to search for in transcriptions or summaries
            genre: Genre to filter by
            mood: Mood to filter by
            instruments: List of instruments to filter by
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        # Need at least one search parameter
        if not any([query, genre, mood, instruments]):
            raise ValueError("At least one search parameter (query, genre, mood, or instruments) is required")
        
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {}
        if query:
            data["query"] = query
        if genre:
            data["genre"] = genre
        if mood:
            data["mood"] = mood
        if instruments:
            data["instruments"] = instruments
        
        return self._make_request("POST", f"{self.search_url}/files/audio", params=params, json_data=data)
    
    def search_combined(self, query: str, media_types: List[str] = None, media_source: str = "user", 
                       folder_path: str = None, page: int = 1, page_size: int = 20,
                       generate_thumbnail: bool = True, generate_streamable: bool = False, 
                       generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Combined semantic search across different media types.
        
        Args:
            query: Text query for semantic search
            media_types: List of media types to search ['video', 'audio', 'image']
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        if not media_types:
            media_types = ['video', 'audio', 'image']
        
        for media_type in media_types:
            if media_type not in ['video', 'audio', 'image']:
                raise ValueError("media_types must only contain 'video', 'audio', or 'image'")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "query": query,
            "media_types": media_types
        }
        
        return self._make_request("POST", f"{self.search_url}/files/combined", params=params, json_data=data)
    
    def search_audio_by_genre(self, genres: List[str], min_probability: float = 0.1,
                            media_source: str = "user", folder_path: str = None,
                            page: int = 1, page_size: int = 20,
                            generate_thumbnail: bool = True, generate_streamable: bool = False, 
                            generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for audio files by genre.
        
        Args:
            genres: List of genres to search for
            min_probability: Minimum probability threshold for genre matches (0.0-1.0)
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "genres": genres,
            "min_probability": min_probability
        }
        
        return self._make_request("POST", f"{self.search_url}/files/audio/by-genre", params=params, json_data=data)
    
    def search_audio_by_mood(self, moods: List[str], media_source: str = "user", 
                           folder_path: str = None, page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False, 
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for audio files by mood.
        
        Args:
            moods: List of moods to search for
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "moods": moods
        }
        
        return self._make_request("POST", f"{self.search_url}/files/audio/by-mood", params=params, json_data=data)
    
    def search_audio_by_instrument(self, instruments: List[str], min_confidence: float = 0.5,
                                media_source: str = "user", folder_path: str = None,
                                page: int = 1, page_size: int = 20,
                                generate_thumbnail: bool = True, generate_streamable: bool = False, 
                                generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for audio files by instruments.
        
        Args:
            instruments: List of instruments to search for
            min_confidence: Minimum confidence threshold for instrument detection (0.0-1.0)
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "instruments": instruments,
            "min_confidence": min_confidence
        }
        
        return self._make_request("POST", f"{self.search_url}/files/audio/by-instrument", params=params, json_data=data)
    
    def search_audio_by_transcription(self, query: str, media_source: str = "user", 
                                    folder_path: str = None, page: int = 1, page_size: int = 20,
                                    generate_thumbnail: bool = True, generate_streamable: bool = False, 
                                    generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for audio files by transcription content.
        
        Args:
            query: Text to search for in audio transcriptions
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "query": query
        }
        
        return self._make_request("POST", f"{self.search_url}/files/audio/by-transcription", params=params, json_data=data)
    
    def search_image_by_objects(self, objects: List[str], media_source: str = "user", 
                              folder_path: str = None, page: int = 1, page_size: int = 20,
                              generate_thumbnail: bool = True, generate_streamable: bool = False, 
                              generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for images by objects in them.
        
        Args:
            objects: List of objects to search for
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "objects": objects
        }
        
        return self._make_request("POST", f"{self.search_url}/files/image/by-objects", params=params, json_data=data)
    
    def search_image_by_color(self, color_moods: List[str] = None, dominant_hues: Dict[str, int] = None,
                           media_source: str = "user", folder_path: str = None,
                           page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False, 
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for images by color characteristics.
        
        Args:
            color_moods: List of color moods to search for (e.g., "warm", "cool", "vibrant")
            dominant_hues: Dict with "min" and "max" keys for hue range (0-360 degrees)
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        if not color_moods and not dominant_hues:
            raise ValueError("Either color_moods or dominant_hues must be provided")
        
        if dominant_hues:
            if "min" not in dominant_hues or "max" not in dominant_hues:
                raise ValueError("dominant_hues must contain 'min' and 'max' keys")
            if not (0 <= dominant_hues["min"] <= 360 and 0 <= dominant_hues["max"] <= 360):
                raise ValueError("Hue values must be between 0 and 360")
        
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {}
        if color_moods:
            data["color_moods"] = color_moods
        if dominant_hues:
            data["dominant_hues"] = dominant_hues
        
        return self._make_request("POST", f"{self.search_url}/files/image/by-color", params=params, json_data=data)
    
    def search_image_by_text(self, query: str, media_source: str = "user", 
                          folder_path: str = None, page: int = 1, page_size: int = 20,
                          generate_thumbnail: bool = True, generate_streamable: bool = False, 
                          generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for images by text content (OCR).
        
        Args:
            query: Text to search for in image OCR content
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "query": query
        }
        
        return self._make_request("POST", f"{self.search_url}/files/image/by-text", params=params, json_data=data)
    
    def search_by_tags(self, tags: List[str], match_all: bool = False, 
                     media_types: List[str] = None, media_source: str = "user", 
                     folder_path: str = None, page: int = 1, page_size: int = 20,
                     generate_thumbnail: bool = True, generate_streamable: bool = False, 
                     generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for files by tags across all media types.
        
        Args:
            tags: List of tags to search for
            match_all: If True, all tags must be present; if False, any tag can match
            media_types: List of media types to search ['video', 'audio', 'image']
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        if not media_types:
            media_types = ['video', 'audio', 'image']
        
        for media_type in media_types:
            if media_type not in ['video', 'audio', 'image']:
                raise ValueError("media_types must only contain 'video', 'audio', or 'image'")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "tags": tags,
            "match_all": match_all,
            "media_types": media_types
        }
        
        return self._make_request("POST", f"{self.search_url}/files/by-tags", params=params, json_data=data)
    
    def search_video_by_tags(self, tags: List[str], match_all: bool = False, 
                           media_source: str = "user", folder_path: str = None,
                           page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False, 
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for videos by tags.
        
        Args:
            tags: List of tags to search for
            match_all: If True, all tags must be present; if False, any tag can match
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "tags": tags,
            "match_all": match_all
        }
        
        return self._make_request("POST", f"{self.search_url}/files/video/by-tags", params=params, json_data=data)
    
    def search_audio_by_tags(self, tags: List[str], match_all: bool = False, 
                           media_source: str = "user", folder_path: str = None,
                           page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False, 
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for audio files by tags.
        
        Args:
            tags: List of tags to search for
            match_all: If True, all tags must be present; if False, any tag can match
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "tags": tags,
            "match_all": match_all
        }
        
        return self._make_request("POST", f"{self.search_url}/files/audio/by-tags", params=params, json_data=data)
    
    def search_image_by_tags(self, tags: List[str], match_all: bool = False, 
                           media_source: str = "user", folder_path: str = None,
                           page: int = 1, page_size: int = 20,
                           generate_thumbnail: bool = True, generate_streamable: bool = False, 
                           generate_download: bool = False, org_id: str = None) -> Dict:
        """
        Search for images by tags.
        
        Args:
            tags: List of tags to search for
            match_all: If True, all tags must be present; if False, any tag can match
            media_source: Source of media ("user" or "stock")
            folder_path: Path to search within (for user media only)
            page: Page number for pagination
            page_size: Number of results per page
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if media_source == "user" and not org_id:
            raise ValueError("Organization ID is required for user media. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "media_source": media_source,
            "page": page,
            "page_size": page_size,
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if media_source == "user":
            params["org_id"] = org_id
        
        if folder_path:
            params["folder_path"] = folder_path
        
        data = {
            "tags": tags,
            "match_all": match_all
        }
        
        return self._make_request("POST", f"{self.search_url}/files/image/by-tags", params=params, json_data=data)
