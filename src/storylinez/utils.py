import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from .base_client import BaseClient

class UtilsClient(BaseClient):
    """
    Client for interacting with Storylinez Utility API.
    Provides methods for accessing common utilities and AI-powered helpers.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the UtilsClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.utils_url = f"{self.base_url}/utils"
    
    # Voice and Media Types
    
    def get_voice_types(self) -> Dict:
        """
        Get available voice types for voiceover generation.
        
        Returns:
            Dictionary with available voice types and their details
        """
        return self._make_request("GET", f"{self.utils_url}/voice-types")
    
    def get_transition_types(self) -> Dict:
        """
        Get available transition types for video editing.
        
        Returns:
            Dictionary with available transition types and their details
        """
        return self._make_request("GET", f"{self.utils_url}/transition-types")
    
    def get_template_types(self) -> Dict:
        """
        Get available template types for video styling.
        
        Returns:
            Dictionary with available template types and their details
        """
        return self._make_request("GET", f"{self.utils_url}/template-types")
    
    def get_color_grades(self) -> Dict:
        """
        Get available color grading options for video styling.
        
        Returns:
            Dictionary with available color grades and their details
        """
        return self._make_request("GET", f"{self.utils_url}/color-grades")
    
    # AI Assistant Functions
    
    def alter_prompt(self, old_prompt: str, org_id: str = None, job_name: str = None,
                   edited_json: Dict = None, company_details: str = None,
                   alter_type: str = "enhance", prompt_type: str = "prompt") -> Dict:
        """
        Enhance or randomize an existing prompt.
        
        Args:
            old_prompt: The original prompt text to be altered
            org_id: Organization ID (uses default if not provided)
            job_name: Optional name for the alteration job
            edited_json: Optional previous generation/edited content
            company_details: Optional company context to consider
            alter_type: Type of alteration to perform: "enhance" or "randomize"
            prompt_type: Type of prompt: "prompt", "storyboard", or "sequence"
            
        Returns:
            Dictionary with job ID and status
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Validate alter_type and prompt_type
        if alter_type not in ["enhance", "randomize"]:
            raise ValueError("alter_type must be either 'enhance' or 'randomize'")
            
        if prompt_type not in ["prompt", "storyboard", "sequence"]:
            raise ValueError("prompt_type must be either 'prompt', 'storyboard', or 'sequence'")
            
        # Prepare request data
        data = {
            "old_prompt": old_prompt,
            "org_id": org_id
        }
        
        if job_name:
            data["job_name"] = job_name
            
        if edited_json:
            data["edited_json"] = edited_json
            
        if company_details:
            data["company_details"] = company_details
        
        # Query parameters
        params = {
            "alter_type": alter_type,
            "prompt_type": prompt_type
        }
        
        return self._make_request("POST", f"{self.utils_url}/alter-prompt", params=params, json_data=data)
    
    def search_recommendations(self, user_query: str, org_id: str = None, job_name: str = None,
                             documents: List[Dict] = None, temperature: float = 0.7,
                             deepthink: bool = False, overdrive: bool = False,
                             web_search: bool = False, eco: bool = False) -> Dict:
        """
        Get search term recommendations based on a user query.
        
        Args:
            user_query: The search query to get recommendations for
            org_id: Organization ID (uses default if not provided)
            job_name: Optional name for the job
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with job ID and status
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        # Prepare request data
        data = {
            "user_query": user_query,
            "org_id": org_id,
            "temperature": temperature
        }
        
        if job_name:
            data["job_name"] = job_name
            
        if documents:
            data["documents"] = documents
        
        # Query parameters
        params = {
            "deepthink": str(deepthink).lower(),
            "overdrive": str(overdrive).lower(),
            "web_search": str(web_search).lower(),
            "eco": str(eco).lower()
        }
        
        return self._make_request("POST", f"{self.utils_url}/search-recommendations", params=params, json_data=data)
    
    def get_organization_info(self, website_url: str, org_id: str = None, job_name: str = None,
                            scraped_content: str = None, documents: List[Dict] = None,
                            chat_history: List[Dict] = None, temperature: float = 0.7,
                            deepthink: bool = True, overdrive: bool = False,
                            web_search: bool = False, eco: bool = False) -> Dict:
        """
        Extract organization information from a website URL.
        
        Args:
            website_url: The URL of the organization's website
            org_id: Organization ID (uses default if not provided)
            job_name: Optional name for the job
            scraped_content: Optional pre-scraped website content
            documents: Optional list of document contexts to consider
            chat_history: Optional list of previous interactions
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics (defaults to True)
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with job ID and status
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        # Validate website URL
        if not website_url.startswith(("http://", "https://")):
            raise ValueError("website_url must be a valid URL starting with http:// or https://")
        
        # Prepare request data
        data = {
            "website_url": website_url,
            "org_id": org_id,
            "temperature": temperature
        }
        
        if job_name:
            data["job_name"] = job_name
            
        if scraped_content is not None:
            data["scraped_content"] = scraped_content
            
        if documents is not None:
            data["documents"] = documents
            
        if chat_history is not None:
            data["chat_history"] = chat_history
        
        # Query parameters
        params = {
            "deepthink": str(deepthink).lower(),
            "overdrive": str(overdrive).lower(),
            "web_search": str(web_search).lower(),
            "eco": str(eco).lower()
        }
        
        return self._make_request("POST", f"{self.utils_url}/organization-info", params=params, json_data=data)
    
    # Job Management
    
    def get_job_result(self, job_id: str) -> Dict:
        """
        Get the result of a utility job.
        
        Args:
            job_id: The ID of the job to retrieve
            
        Returns:
            Dictionary with job details and results
        """
        if not job_id:
            raise ValueError("job_id is required")
            
        params = {"job_id": job_id}
        return self._make_request("GET", f"{self.utils_url}/get-result", params=params)
    
    def list_jobs(self, org_id: str = None, job_type: str = None, page: int = 1, limit: int = 20) -> Dict:
        """
        List utility jobs for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            job_type: Optional filter by job type: "alter_prompt", "search_recommendations", or "organization_info"
            page: Page number for pagination
            limit: Number of items per page
            
        Returns:
            Dictionary with job list and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        # Validate job_type if provided
        if job_type and job_type not in ["alter_prompt", "search_recommendations", "organization_info"]:
            raise ValueError("job_type must be one of: 'alter_prompt', 'search_recommendations', 'organization_info'")
        
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit
        }
        
        if job_type:
            params["job_type"] = job_type
            
        return self._make_request("GET", f"{self.utils_url}/list-jobs", params=params)
