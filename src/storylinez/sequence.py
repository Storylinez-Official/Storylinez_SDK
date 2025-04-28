import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from .base_client import BaseClient

class SequenceClient(BaseClient):
    """
    Client for interacting with Storylinez Sequence API.
    Provides methods for creating, retrieving, and managing sequences for video generation.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the SequenceClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.sequence_url = f"{self.base_url}/sequence"
    
    # Sequence Creation and Retrieval
    
    def create_sequence(self, project_id: str, apply_template: bool = False, 
                      apply_grade: bool = False, grade_type: str = "single",
                      orientation: str = None, deepthink: bool = False, 
                      overdrive: bool = False, web_search: bool = False, 
                      eco: bool = False, temperature: float = 0.7, 
                      iterations: int = 1) -> Dict:
        """
        Create a new sequence for a project.
        
        Args:
            project_id: ID of the project to create the sequence for
            apply_template: Whether to apply a template to the sequence
            apply_grade: Whether to apply color grading to the sequence
            grade_type: Type of grading to apply ("single" or "multiple")
            orientation: Video orientation (landscape or portrait) - defaults to project setting
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            
        Returns:
            Dictionary with the created sequence details and job information
        """
        data = {
            "project_id": project_id,
            "apply_template": apply_template,
            "apply_grade": apply_grade,
            "grade_type": grade_type,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
            "temperature": temperature,
            "iterations": iterations
        }
        
        if orientation:
            data["orientation"] = orientation
        
        return self._make_request("POST", f"{self.sequence_url}/create", json_data=data)
    
    def get_sequence(self, sequence_id: str = None, project_id: str = None,
                   include_results: bool = True, include_storyboard: bool = False) -> Dict:
        """
        Get details of a sequence by either sequence ID or project ID.
        
        Args:
            sequence_id: ID of the sequence to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the sequence for (either this or sequence_id must be provided)
            include_results: Whether to include job results
            include_storyboard: Whether to include the storyboard data
            
        Returns:
            Dictionary with sequence details
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        params = {
            "include_results": str(include_results).lower(),
            "include_storyboard": str(include_storyboard).lower()
        }
        
        if sequence_id:
            params["sequence_id"] = sequence_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.sequence_url}/get", params=params)
    
    def redo_sequence(self, sequence_id: str = None, project_id: str = None,
                    include_history: bool = False, regenerate_prompt: str = None) -> Dict:
        """
        Regenerate a sequence with the latest storyboard data.
        
        Args:
            sequence_id: ID of the sequence to regenerate (either this or project_id must be provided)
            project_id: ID of the project whose sequence to regenerate (either this or sequence_id must be provided)
            include_history: Whether to include sequence history as context for regeneration
            regenerate_prompt: Optional prompt to guide the regeneration
            
        Returns:
            Dictionary with the regeneration job details
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        data = {"include_history": include_history}
        
        if sequence_id:
            data["sequence_id"] = sequence_id
        if project_id:
            data["project_id"] = project_id
        if regenerate_prompt:
            data["regenerate_prompt"] = regenerate_prompt
            
        return self._make_request("POST", f"{self.sequence_url}/redo", json_data=data)
    
    def update_sequence(self, sequence_id: str = None, project_id: str = None, 
                      update_ai_params: bool = True) -> Dict:
        """
        Update a sequence with the latest storyboard and voiceover data without regenerating it.
        
        Args:
            sequence_id: ID of the sequence to update (either this or project_id must be provided)
            project_id: ID of the project whose sequence to update (either this or sequence_id must be provided)
            update_ai_params: Whether to update AI parameters from the project's storyboard
            
        Returns:
            Dictionary with update confirmation
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        data = {"update_ai_params": update_ai_params}
        
        if sequence_id:
            data["sequence_id"] = sequence_id
        if project_id:
            data["project_id"] = project_id
            
        return self._make_request("PUT", f"{self.sequence_url}/selfupdate", json_data=data)
    
    def update_sequence_settings(self, sequence_id: str = None, project_id: str = None,
                              apply_template: bool = None, apply_grade: bool = None,
                              grade_type: str = None, orientation: str = None,
                              deepthink: bool = None, overdrive: bool = None,
                              web_search: bool = None, eco: bool = None,
                              temperature: float = None, iterations: int = None,
                              regenerate_prompt: str = None, edited_sequence: Dict = None) -> Dict:
        """
        Update sequence settings without regenerating.
        
        Args:
            sequence_id: ID of the sequence to update (either this or project_id must be provided)
            project_id: ID of the project whose sequence to update (either this or sequence_id must be provided)
            apply_template: Whether to apply a template to the sequence
            apply_grade: Whether to apply color grading to the sequence
            grade_type: Type of grading to apply ("single" or "multiple")
            orientation: Video orientation (landscape or portrait)
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            regenerate_prompt: Optional prompt to guide regeneration
            edited_sequence: Complete edited sequence structure
            
        Returns:
            Dictionary with the update confirmation
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        data = {}
        
        if sequence_id:
            data["sequence_id"] = sequence_id
        if project_id:
            data["project_id"] = project_id
        if apply_template is not None:
            data["apply_template"] = apply_template
        if apply_grade is not None:
            data["apply_grade"] = apply_grade
        if grade_type:
            data["grade_type"] = grade_type
        if orientation:
            data["orientation"] = orientation
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
        if regenerate_prompt:
            data["regenerate_prompt"] = regenerate_prompt
        if edited_sequence:
            data["edited_sequence"] = edited_sequence
            
        return self._make_request("PUT", f"{self.sequence_url}/update", json_data=data)
    
    def get_sequence_history(self, sequence_id: str, page: int = 1, limit: int = 10,
                          history_type: str = None, include_current: bool = False) -> Dict:
        """
        Get history of changes for a sequence.
        
        Args:
            sequence_id: ID of the sequence
            page: Page number for pagination
            limit: Number of items per page
            history_type: Filter by history type (e.g., "update", "generation", "prompt")
            include_current: Whether to include the current state
            
        Returns:
            Dictionary with history entries
        """
        params = {
            "sequence_id": sequence_id,
            "page": page,
            "limit": limit,
            "include_current": str(include_current).lower()
        }
        
        if history_type:
            params["history_type"] = history_type
            
        return self._make_request("GET", f"{self.sequence_url}/history", params=params)
    
    def get_sequence_media(self, sequence_id: str = None, project_id: str = None,
                        include_analysis: bool = False, generate_thumbnail: bool = True,
                        generate_streamable: bool = True, generate_download: bool = False) -> Dict:
        """
        Get media files used in a sequence.
        
        Args:
            sequence_id: ID of the sequence (either this or project_id must be provided)
            project_id: ID of the project (either this or sequence_id must be provided)
            include_analysis: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            
        Returns:
            Dictionary with media files grouped by type (clips, audios, voiceover)
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        params = {
            "include_analysis": str(include_analysis).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if sequence_id:
            params["sequence_id"] = sequence_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.sequence_url}/media_involved", params=params)
    
    # Sequence Editing Operations
    
    def reorder_sequence_items(self, sequence_id: str, array_type: str, new_order: List[int]) -> Dict:
        """
        Reorder items in a sequence array.
        
        Args:
            sequence_id: ID of the sequence to modify
            array_type: Type of array to modify ("clips" or "audios")
            new_order: List of indices in the new order
            
        Returns:
            Dictionary with operation confirmation
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
            
        if array_type not in ['clips', 'audios']:
            raise ValueError("array_type must be either 'clips' or 'audios'")
            
        if not isinstance(new_order, list) or not all(isinstance(i, int) for i in new_order):
            raise ValueError("new_order must be a list of integers")
            
        data = {
            "sequence_id": sequence_id,
            "array_type": array_type,
            "new_order": new_order
        }
        
        return self._make_request("PUT", f"{self.sequence_url}/reorder", json_data=data)
    
    def edit_sequence_item(self, sequence_id: str, item_type: str, 
                         item_index: int = None, updated_item: Dict = None) -> Dict:
        """
        Edit an item in a sequence.
        
        Args:
            sequence_id: ID of the sequence to modify
            item_type: Type of item to edit ("clips", "audios", or "voiceover")
            item_index: Index of the item to update (required for clips and audios)
            updated_item: Updated item data
            
        Returns:
            Dictionary with operation confirmation
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
            
        if item_type not in ['clips', 'audios', 'voiceover']:
            raise ValueError("item_type must be one of: 'clips', 'audios', 'voiceover'")
            
        if item_type != 'voiceover' and item_index is None:
            raise ValueError(f"item_index is required for item_type '{item_type}'")
            
        if not updated_item:
            raise ValueError("updated_item is required")
            
        data = {
            "sequence_id": sequence_id,
            "item_type": item_type,
            "updated_item": updated_item
        }
        
        if item_index is not None:
            data["item_index"] = item_index
            
        return self._make_request("PUT", f"{self.sequence_url}/edit/item", json_data=data)
    
    def change_sequence_media(self, sequence_id: str, item_type: str, item_index: int = None,
                           file_id: str = None, stock_id: str = None, path: str = None) -> Dict:
        """
        Change media for an item in a sequence.
        
        Args:
            sequence_id: ID of the sequence to modify
            item_type: Type of item to modify ("clips", "audios", or "voiceover")
            item_index: Index of the item to update (required for clips and audios)
            file_id: ID of the file to use (one of file_id, stock_id, or path must be provided)
            stock_id: ID of the stock media to use (one of file_id, stock_id, or path must be provided)
            path: Direct path to the media file (one of file_id, stock_id, or path must be provided)
            
        Returns:
            Dictionary with operation confirmation
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
            
        if item_type not in ['clips', 'audios', 'voiceover']:
            raise ValueError("item_type must be one of: 'clips', 'audios', 'voiceover'")
            
        if item_type != 'voiceover' and item_index is None:
            raise ValueError(f"item_index is required for item_type '{item_type}'")
            
        if not any([file_id, stock_id, path]):
            raise ValueError("One of file_id, stock_id, or path must be provided")
            
        data = {
            "sequence_id": sequence_id,
            "item_type": item_type
        }
        
        if item_index is not None:
            data["item_index"] = item_index
            
        if file_id:
            data["file_id"] = file_id
        elif stock_id:
            data["stock_id"] = stock_id
        elif path:
            data["path"] = path
            
        return self._make_request("PUT", f"{self.sequence_url}/change_media", json_data=data)
