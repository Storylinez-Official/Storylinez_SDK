import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from .base_client import BaseClient

class StockClient(BaseClient):
    """
    Client for interacting with Storylinez Stock Media API.
    Provides methods for searching and fetching stock videos, audios, and images.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the StockClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.stock_url = f"{self.base_url}/stock"
    
    def search(self, queries: List[str], collections: List[str] = None, 
              detailed: bool = False, generate_thumbnail: bool = False,
              generate_streamable: bool = False, generate_download: bool = False,
              num_results: int = None, num_results_videos: int = 1, 
              num_results_audios: int = 1, num_results_images: int = 1,
              similarity_threshold: float = 0.5, orientation: str = None) -> Dict:
        """
        Search for stock media items across videos, audios, and/or images collections using semantic search.
        
        Args:
            queries: List of natural language search queries
            collections: List of collections to search ('videos', 'audios', 'images'). Defaults to all.
            detailed: Whether to include full analysis data in results
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable media URLs
            generate_download: Whether to generate download URLs
            num_results: Override for max results per collection (overrides individual settings)
            num_results_videos: Maximum number of video results per query
            num_results_audios: Maximum number of audio results per query
            num_results_images: Maximum number of image results per query
            similarity_threshold: Minimum similarity score (0.0-1.0)
            orientation: Filter videos by orientation ('landscape' or 'portrait')
            
        Returns:
            Dictionary containing search results grouped by media type
        """
        # Build query parameters
        params = {
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower(),
            "similarity_threshold": similarity_threshold,
        }
        
        # Add optional parameters
        if collections:
            for collection in collections:
                params["collections"] = collection
                
        if num_results is not None:
            params["num_results"] = num_results
        else:
            params["num_results_videos"] = num_results_videos
            params["num_results_audios"] = num_results_audios
            params["num_results_images"] = num_results_images
            
        if orientation:
            if orientation not in ['landscape', 'portrait']:
                raise ValueError("Orientation must be either 'landscape' or 'portrait'")
            params["orientation"] = orientation
        
        # Send search request
        data = {
            "queries": queries
        }
        
        return self._make_request("POST", f"{self.stock_url}/search", params=params, json_data=data)
    
    def get_by_id(self, stock_id: str, media_type: str, detailed: bool = True,
                 generate_thumbnail: bool = True, generate_streamable: bool = False,
                 generate_download: bool = False) -> Dict:
        """
        Get a specific stock media item by ID.
        
        Args:
            stock_id: ID of the stock item to retrieve
            media_type: Type of media ('videos', 'audios', or 'images')
            detailed: Whether to include full analysis data
            generate_thumbnail: Whether to generate thumbnail URL
            generate_streamable: Whether to generate streamable media URL
            generate_download: Whether to generate download URL
            
        Returns:
            Dictionary containing the stock item details
        """
        # Validate media_type
        if media_type not in ['videos', 'audios', 'images']:
            raise ValueError("media_type must be one of: 'videos', 'audios', 'images'")
            
        params = {
            "id": stock_id,
            "media_type": media_type,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        return self._make_request("GET", f"{self.stock_url}/get_by_id", params=params)
    
    def list_media(self, media_type: str, page: int = 1, limit: int = 20, 
                 sort_by: str = "processed_at", sort_order: str = "desc",
                 detailed: bool = False, generate_thumbnail: bool = False,
                 generate_streamable: bool = False, generate_download: bool = False,
                 orientation: str = None, search: str = None) -> Dict:
        """
        List stock media items with pagination.
        
        Args:
            media_type: Type of media to list ('videos', 'audios', or 'images')
            page: Page number for pagination (starting from 1)
            limit: Maximum number of items per page (max 100)
            sort_by: Field to sort by (e.g., 'processed_at')
            sort_order: Sort direction ('asc' or 'desc')
            detailed: Whether to include full analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable media URLs
            generate_download: Whether to generate download URLs
            orientation: Filter videos by orientation ('landscape' or 'portrait')
            search: Optional text search within title/metadata
            
        Returns:
            Dictionary containing paginated media items and pagination info
        """
        # Validate media_type
        if media_type not in ['videos', 'audios', 'images']:
            raise ValueError("media_type must be one of: 'videos', 'audios', 'images'")
            
        # Validate sort_order
        if sort_order not in ['asc', 'desc']:
            raise ValueError("sort_order must be either 'asc' or 'desc'")
            
        # Validate orientation if provided
        if orientation and orientation not in ['landscape', 'portrait']:
            raise ValueError("orientation must be either 'landscape' or 'portrait'")
        
        params = {
            "media_type": media_type,
            "page": page,
            "limit": min(limit, 100),  # Cap at 100 as per API limits
            "sort_by": sort_by,
            "sort_order": sort_order,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        # Add optional parameters
        if orientation:
            params["orientation"] = orientation
            
        if search:
            params["search"] = search
        
        return self._make_request("GET", f"{self.stock_url}/list", params=params)
    
    def get_by_ids(self, ids: List[str], media_types: List[str], 
                  detailed: bool = True, generate_thumbnail: bool = True,
                  generate_streamable: bool = False, generate_download: bool = False) -> Dict:
        """
        Get multiple stock media items by their IDs.
        
        Args:
            ids: List of stock item IDs
            media_types: Corresponding media types for each ID ('videos', 'audios', 'images')
            detailed: Whether to include full analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable media URLs
            generate_download: Whether to generate download URLs
            
        Returns:
            Dictionary containing the requested stock items
        """
        # Validate input
        if len(ids) != len(media_types):
            raise ValueError("The ids and media_types lists must be the same length")
            
        if len(ids) > 100:
            raise ValueError("Cannot request more than 100 items at once")
            
        # Validate media types
        for media_type in media_types:
            if media_type not in ['videos', 'audios', 'images']:
                raise ValueError(f"Invalid media_type: {media_type}. Must be one of: 'videos', 'audios', 'images'")
        
        params = {
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        data = {
            "ids": ids,
            "media_types": media_types
        }
        
        return self._make_request("POST", f"{self.stock_url}/get_by_ids", params=params, json_data=data)
