import os
import json
import requests
from typing import Dict, List, Optional, Union, Any, Literal
from .base_client import BaseClient

class SettingsClient(BaseClient):
    """
    Client for interacting with Storylinez Settings API.
    Provides methods for managing user settings and temporary job storage.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the SettingsClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.settings_url = f"{self.base_url}/settings"
    
    # User Settings Management
    
    def get_settings(self) -> Dict:
        """
        Get all settings for the current user.
        
        Returns:
            Dictionary containing user settings (AI parameters, link preferences, UI preferences)
        """
        return self._make_request("GET", f"{self.settings_url}/get")
    
    def save_settings(self, ai_params: Dict = None, link_preferences: Dict = None, 
                    ui_preferences: Dict = None) -> Dict:
        """
        Save all settings for the current user.
        
        Args:
            ai_params: AI parameters for content generation 
                       (e.g., temperature, iterations, deepthink, web_search)
            link_preferences: File and media link preferences 
                              (e.g., generate_thumbnail, generate_streamable)
            ui_preferences: User interface preferences 
                            (e.g., dark_mode, default_view, language)
            
        Returns:
            Dictionary containing confirmation message and saved settings
        """
        data = {}
        
        if ai_params is not None:
            data["ai_params"] = ai_params
        
        if link_preferences is not None:
            data["link_preferences"] = link_preferences
            
        if ui_preferences is not None:
            data["ui_preferences"] = ui_preferences
            
        if not data:
            raise ValueError("At least one settings category (ai_params, link_preferences, or ui_preferences) must be provided")
            
        return self._make_request("POST", f"{self.settings_url}/save", json_data=data)
    
    def update_settings(self, ai_params: Dict = None, link_preferences: Dict = None, 
                      ui_preferences: Dict = None) -> Dict:
        """
        Update specific settings for the current user.
        Unlike save_settings, this method only updates the specified fields without replacing entire categories.
        
        Args:
            ai_params: AI parameters to update (e.g., temperature, iterations)
            link_preferences: Link preferences to update (e.g., generate_thumbnail)
            ui_preferences: UI preferences to update (e.g., dark_mode)
            
        Returns:
            Dictionary containing confirmation message and updated fields
        """
        data = {}
        
        if ai_params is not None:
            data["ai_params"] = ai_params
            
        if link_preferences is not None:
            data["link_preferences"] = link_preferences
            
        if ui_preferences is not None:
            data["ui_preferences"] = ui_preferences
            
        if not data:
            raise ValueError("At least one settings category (ai_params, link_preferences, or ui_preferences) must be provided")
            
        return self._make_request("PUT", f"{self.settings_url}/update", json_data=data)
    
    def reset_settings(self, category: str = "all") -> Dict:
        """
        Reset all or specific settings categories to default values.
        
        Args:
            category: Settings category to reset. One of: "all", "ai_params", "link_preferences", "ui_preferences"
            
        Returns:
            Dictionary containing confirmation message and reset settings
        """
        # Validate category
        valid_categories = ['all', 'ai_params', 'link_preferences', 'ui_preferences']
        if category not in valid_categories:
            raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
            
        return self._make_request("POST", f"{self.settings_url}/reset", json_data={"category": category})
    
    # Specialized Settings Updates
    
    def update_theme(self, dark_mode: bool) -> Dict:
        """
        Update UI theme preference (light/dark mode).
        
        Args:
            dark_mode: Whether to enable dark mode
            
        Returns:
            Dictionary containing confirmation message
        """
        return self._make_request("PUT", f"{self.settings_url}/theme", json_data={"dark_mode": dark_mode})
    
    def update_ai_defaults(self, temperature: float = None, iterations: int = None,
                         deepthink: bool = None, overdrive: bool = None,
                         web_search: bool = None, eco: bool = None) -> Dict:
        """
        Update default AI parameters for content generation.
        
        Args:
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary containing confirmation message and updated AI parameters
        """
        data = {}
        
        if temperature is not None:
            if not 0 <= temperature <= 1:
                raise ValueError("Temperature must be between 0 and 1")
            data["temperature"] = temperature
            
        if iterations is not None:
            if not isinstance(iterations, int) or iterations < 1:
                raise ValueError("Iterations must be a positive integer")
            data["iterations"] = iterations
            
        if deepthink is not None:
            data["deepthink"] = deepthink
            
        if overdrive is not None:
            data["overdrive"] = overdrive
            
        if web_search is not None:
            data["web_search"] = web_search
            
        if eco is not None:
            data["eco"] = eco
            
        if not data:
            raise ValueError("At least one AI parameter must be provided")
            
        return self._make_request("PUT", f"{self.settings_url}/ai-defaults", json_data=data)
    
    # Temporary Job Management
    
    def add_job(self, job_id: str, org_id: str = None, job_type: str = "query_generation",
              project_id: str = None, metadata: Dict = None) -> Dict:
        """
        Add a temporary job to user storage.
        
        Args:
            job_id: The ID of the job to store
            org_id: Organization ID (uses default if not provided)
            job_type: Type of job ("query_generation" or "search_recommendations")
            project_id: Optional project ID associated with the job
            metadata: Optional additional metadata about the job
            
        Returns:
            Dictionary containing confirmation message
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        if job_type not in ["query_generation", "search_recommendations"]:
            raise ValueError("job_type must be either 'query_generation' or 'search_recommendations'")
            
        data = {
            "job_id": job_id,
            "org_id": org_id,
            "job_type": job_type
        }
        
        if project_id:
            data["project_id"] = project_id
            
        if metadata:
            data["metadata"] = metadata
            
        return self._make_request("POST", f"{self.settings_url}/jobs/add", json_data=data)
    
    def list_jobs(self, org_id: str = None, project_id: str = None, job_type: str = None,
                page: int = 1, limit: int = 10, 
                sort_by: str = "created_at", sort_order: str = "desc") -> Dict:
        """
        List temporary jobs stored for the user.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            project_id: Optional filter by project ID
            job_type: Optional filter by job type
            page: Page number for pagination
            limit: Number of items per page
            sort_by: Field to sort by (default: created_at)
            sort_order: Sort direction ("asc" or "desc")
            
        Returns:
            Dictionary with jobs list and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Validate job_type if provided
        if job_type and job_type not in ["query_generation", "search_recommendations"]:
            raise ValueError("job_type must be either 'query_generation' or 'search_recommendations'")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        
        if project_id:
            params["project_id"] = project_id
            
        if job_type:
            params["job_type"] = job_type
            
        return self._make_request("GET", f"{self.settings_url}/jobs/list", params=params)
    
    def delete_job(self, job_id: str, org_id: str = None) -> Dict:
        """
        Delete a temporary job from user storage.
        
        Args:
            job_id: ID of the job to delete
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary containing confirmation message
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "job_id": job_id,
            "org_id": org_id
        }
            
        return self._make_request("DELETE", f"{self.settings_url}/jobs/delete", params=params)
    
    def fetch_job_results(self, job_id: str, org_id: str = None) -> Dict:
        """
        Fetch results for a temporary job.
        
        Args:
            job_id: ID of the job to fetch results for
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary containing job metadata and results
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "job_id": job_id,
            "org_id": org_id
        }
            
        return self._make_request("GET", f"{self.settings_url}/jobs/fetch_results", params=params)
