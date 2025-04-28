import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from .base_client import BaseClient

class StoryboardClient(BaseClient):
    """
    Client for interacting with Storylinez Storyboard API.
    Provides methods for creating and managing storyboards, editing storyboard content, and retrieving history.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the StoryboardClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.storyboard_url = f"{self.base_url}/storyboard"
    
    # Storyboard Creation and Management
    
    def create_storyboard(self, project_id: str, deepthink: bool = False, overdrive: bool = False, 
                        web_search: bool = False, eco: bool = False, temperature: float = 0.7, 
                        iterations: int = 3, full_length: int = None, 
                        voiceover_mode: str = "generated", skip_voiceover: bool = False) -> Dict:
        """
        Create a new storyboard for a project.
        
        Args:
            project_id: ID of the project to create the storyboard for
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            full_length: Target length of the video in seconds
            voiceover_mode: Voiceover mode ('generated' or 'uploaded')
            skip_voiceover: Whether to skip generating voiceover
            
        Returns:
            Dictionary with the created storyboard details and job information
        """
        data = {
            "project_id": project_id,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
            "temperature": max(0.0, min(1.0, temperature)),  # Clamp between 0 and 1
            "iterations": iterations
        }
        
        if full_length is not None:
            data["full_length"] = full_length
            
        if voiceover_mode not in ["generated", "uploaded"]:
            raise ValueError("voiceover_mode must be either 'generated' or 'uploaded'")
            
        data["voiceover_mode"] = voiceover_mode
        data["skip_voiceover"] = skip_voiceover
        
        params = {"include_details": "false"}
        return self._make_request("POST", f"{self.storyboard_url}/create", params=params, json_data=data)
    
    def get_storyboard(self, storyboard_id: str = None, project_id: str = None, 
                     include_results: bool = False, include_details: bool = False) -> Dict:
        """
        Get a storyboard by ID or project ID.
        
        Args:
            storyboard_id: ID of the storyboard to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the storyboard for (either this or storyboard_id must be provided)
            include_results: Whether to include job results
            include_details: Whether to include media details (stock videos, audio, etc.)
            
        Returns:
            Dictionary with the storyboard details
        """
        if not storyboard_id and not project_id:
            raise ValueError("Either storyboard_id or project_id must be provided")
            
        params = {
            "include_results": str(include_results).lower(),
            "include_details": str(include_details).lower()
        }
        
        if storyboard_id:
            params["storyboard_id"] = storyboard_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.storyboard_url}/get", params=params)
    
    def update_storyboard(self, storyboard_id: str = None, project_id: str = None, 
                        update_ai_params: bool = True) -> Dict:
        """
        Update a storyboard with the latest project and prompt data.
        
        Args:
            storyboard_id: ID of the storyboard to update (either this or project_id must be provided)
            project_id: ID of the project whose storyboard to update (either this or storyboard_id must be provided)
            update_ai_params: Whether to update AI parameters from the project's prompt
            
        Returns:
            Dictionary with the updated storyboard
        """
        if not storyboard_id and not project_id:
            raise ValueError("Either storyboard_id or project_id must be provided")
            
        data = {"update_ai_params": update_ai_params}
        
        if storyboard_id:
            data["storyboard_id"] = storyboard_id
        if project_id:
            data["project_id"] = project_id
            
        return self._make_request("PUT", f"{self.storyboard_url}/selfupdate", json_data=data)
    
    def update_storyboard_values(self, storyboard_id: str = None, project_id: str = None, 
                               edited_storyboard: Dict = None, regeneration_prompt: str = None,
                               deepthink: bool = None, overdrive: bool = None, 
                               web_search: bool = None, eco: bool = None,
                               temperature: float = None, iterations: int = None, 
                               full_length: int = None, skip_voiceover: bool = None,
                               voiceover_mode: str = None) -> Dict:
        """
        Update specific values in a storyboard.
        
        Args:
            storyboard_id: ID of the storyboard to update (either this or project_id must be provided)
            project_id: ID of the project whose storyboard to update (either this or storyboard_id must be provided)
            edited_storyboard: Updated storyboard data structure
            regeneration_prompt: Prompt to guide regeneration
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            full_length: Target length of the video in seconds
            skip_voiceover: Whether to skip generating voiceover
            voiceover_mode: Voiceover mode ('generated' or 'uploaded')
            
        Returns:
            Dictionary with the updated storyboard
        """
        if not storyboard_id and not project_id:
            raise ValueError("Either storyboard_id or project_id must be provided")
            
        data = {}
        
        if storyboard_id:
            data["storyboard_id"] = storyboard_id
        if project_id:
            data["project_id"] = project_id
            
        if edited_storyboard is not None:
            data["edited_storyboard"] = edited_storyboard
        if regeneration_prompt is not None:
            data["regeneration_prompt"] = regeneration_prompt
        if deepthink is not None:
            data["deepthink"] = deepthink
        if overdrive is not None:
            data["overdrive"] = overdrive
        if web_search is not None:
            data["web_search"] = web_search
        if eco is not None:
            data["eco"] = eco
        if temperature is not None:
            data["temperature"] = temperature
        if iterations is not None:
            data["iterations"] = iterations
        if full_length is not None:
            data["full_length"] = full_length
        if skip_voiceover is not None:
            data["skip_voiceover"] = skip_voiceover
        if voiceover_mode is not None:
            if voiceover_mode not in ["generated", "uploaded"]:
                raise ValueError("voiceover_mode must be either 'generated' or 'uploaded'")
            data["voiceover_mode"] = voiceover_mode
            
        return self._make_request("PUT", f"{self.storyboard_url}/update", json_data=data)
    
    def redo_storyboard(self, storyboard_id: str = None, project_id: str = None, 
                      include_history: bool = False) -> Dict:
        """
        Redo a storyboard generation job.
        
        Args:
            storyboard_id: ID of the storyboard to redo (either this or project_id must be provided)
            project_id: ID of the project whose storyboard to redo (either this or storyboard_id must be provided)
            include_history: Whether to include history as context for regeneration
            
        Returns:
            Dictionary with job information
        """
        if not storyboard_id and not project_id:
            raise ValueError("Either storyboard_id or project_id must be provided")
            
        data = {"include_history": include_history}
        
        if storyboard_id:
            data["storyboard_id"] = storyboard_id
        if project_id:
            data["project_id"] = project_id
            
        return self._make_request("POST", f"{self.storyboard_url}/redo", json_data=data)
    
    # Storyboard Content Editing
    
    def reorder_storyboard_items(self, storyboard_id: str, array_type: str, 
                              new_order: List[int]) -> Dict:
        """
        Reorder items in a storyboard array.
        
        Args:
            storyboard_id: ID of the storyboard to update
            array_type: Type of array to reorder ('videos' or 'background_music')
            new_order: List of indices in the new order
            
        Returns:
            Dictionary with operation result
        """
        if array_type not in ['videos', 'background_music']:
            raise ValueError("array_type must be either 'videos' or 'background_music'")
            
        if not isinstance(new_order, list) or not all(isinstance(i, int) for i in new_order):
            raise ValueError("new_order must be a list of integers")
            
        data = {
            "storyboard_id": storyboard_id,
            "array_type": array_type,
            "new_order": new_order
        }
        
        return self._make_request("PUT", f"{self.storyboard_url}/reorder", json_data=data)
    
    def edit_storyboard_item(self, storyboard_id: str, item_type: str, 
                          item_index: int = None, updated_item: Dict = None) -> Dict:
        """
        Edit an item in a storyboard.
        
        Args:
            storyboard_id: ID of the storyboard to update
            item_type: Type of item to edit ('videos', 'background_music', or 'voiceover')
            item_index: Index of the item to update (required for videos and background_music)
            updated_item: Updated item data
            
        Returns:
            Dictionary with operation result
        """
        if item_type not in ['videos', 'background_music', 'voiceover']:
            raise ValueError("item_type must be one of: 'videos', 'background_music', 'voiceover'")
            
        if item_type != 'voiceover' and item_index is None:
            raise ValueError(f"item_index is required for item_type '{item_type}'")
            
        if not updated_item:
            raise ValueError("updated_item is required")
            
        data = {
            "storyboard_id": storyboard_id,
            "item_type": item_type,
            "updated_item": updated_item
        }
        
        if item_index is not None:
            data["item_index"] = item_index
            
        return self._make_request("PUT", f"{self.storyboard_url}/edit/item", json_data=data)
    
    def change_storyboard_media(self, storyboard_id: str, item_type: str, item_index: int,
                             file_id: str = None, stock_id: str = None, path: str = None) -> Dict:
        """
        Change media for an item in a storyboard.
        
        Args:
            storyboard_id: ID of the storyboard to update
            item_type: Type of item to update ('videos' or 'background_music')
            item_index: Index of the item to update
            file_id: ID of the file to use (one of file_id, stock_id, or path must be provided)
            stock_id: ID of the stock media to use (one of file_id, stock_id, or path must be provided)
            path: Direct path to the media file (one of file_id, stock_id, or path must be provided)
            
        Returns:
            Dictionary with operation result
        """
        if item_type not in ['videos', 'background_music']:
            raise ValueError("item_type must be either 'videos' or 'background_music'")
            
        if not any([file_id, stock_id, path]):
            raise ValueError("One of file_id, stock_id, or path must be provided")
            
        data = {
            "storyboard_id": storyboard_id,
            "item_type": item_type,
            "item_index": item_index
        }
        
        if file_id:
            data["file_id"] = file_id
        elif stock_id:
            data["stock_id"] = stock_id
        elif path:
            data["path"] = path
            
        return self._make_request("PUT", f"{self.storyboard_url}/change_media", json_data=data)
    
    # Storyboard History and Media
    
    def get_storyboard_history(self, storyboard_id: str, page: int = 1, limit: int = 10,
                             history_type: str = None, include_current: bool = False) -> Dict:
        """
        Get history of changes for a storyboard.
        
        Args:
            storyboard_id: ID of the storyboard
            page: Page number for pagination
            limit: Number of items per page
            history_type: Filter by history type (e.g., 'update', 'generation', 'prompt')
            include_current: Whether to include the current state
            
        Returns:
            Dictionary with history entries
        """
        params = {
            "storyboard_id": storyboard_id,
            "page": page,
            "limit": limit,
            "include_current": str(include_current).lower()
        }
        
        if history_type:
            params["history_type"] = history_type
            
        return self._make_request("GET", f"{self.storyboard_url}/history", params=params)
    
    def get_storyboard_media(self, storyboard_id: str = None, project_id: str = None,
                          include_analysis: bool = False, generate_thumbnail: bool = True,
                          generate_streamable: bool = True, generate_download: bool = False) -> Dict:
        """
        Get media files used in a storyboard.
        
        Args:
            storyboard_id: ID of the storyboard (either this or project_id must be provided)
            project_id: ID of the project (either this or storyboard_id must be provided)
            include_analysis: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            
        Returns:
            Dictionary with media files grouped by type (videos, background_music, voiceover)
        """
        if not storyboard_id and not project_id:
            raise ValueError("Either storyboard_id or project_id must be provided")
            
        params = {
            "include_analysis": str(include_analysis).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if storyboard_id:
            params["storyboard_id"] = storyboard_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.storyboard_url}/media_involved", params=params)
