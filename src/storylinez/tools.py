import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from .base_client import BaseClient

class ToolsClient(BaseClient):
    """
    Client for interacting with Storylinez Tools API.
    Provides methods for creating and managing AI-powered creative tools.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the ToolsClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.tools_url = f"{self.base_url}/tools"
    
    def get_tool_types(self) -> Dict:
        """
        Get a list of available tool types.
        
        Returns:
            Dictionary with available tool types and their names
        """
        return self._make_request("GET", f"{self.tools_url}/types")
    
    # Creative Brief Tool
    
    def create_creative_brief(self, name: str, user_input: str, org_id: str = None, 
                           company_details: str = None, auto_company_details: bool = True,
                           company_details_id: str = None, documents: List[Dict] = None, 
                           temperature: float = 0.7, deepthink: bool = False, 
                           overdrive: bool = False, web_search: bool = False, 
                           eco: bool = False) -> Dict:
        """
        Create a creative brief using AI.
        
        Args:
            name: Name for the creative brief
            user_input: Main user instructions or requirements
            org_id: Organization ID (uses default if not provided)
            company_details: Company details as text (ignored if auto_company_details=True)
            auto_company_details: Whether to automatically fetch company details
            company_details_id: Specific company details ID to use (if auto_company_details=True)
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        data = {
            "tool_type": "creative_brief",
            "org_id": org_id,
            "name": name,
            "user_input": user_input,
            "company_details": company_details,
            "auto_company_details": auto_company_details,
            "company_details_id": company_details_id,
            "documents": documents,
            "temperature": temperature,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search, 
            "eco": eco
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Audience Research Tool
    
    def create_audience_research(self, name: str, user_input: str, org_id: str = None,
                              company_details: str = None, auto_company_details: bool = True,
                              company_details_id: str = None, additional_context: str = None,
                              documents: List[Dict] = None, temperature: float = 0.7,
                              deepthink: bool = True, overdrive: bool = True, eco: bool = False) -> Dict:
        """
        Create audience research using AI.
        
        Args:
            name: Name for the audience research
            user_input: Main user instructions or audience to research
            org_id: Organization ID (uses default if not provided)
            company_details: Company details as text (ignored if auto_company_details=True)
            auto_company_details: Whether to automatically fetch company details
            company_details_id: Specific company details ID to use (if auto_company_details=True)
            additional_context: Extra context about the target audience
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics (defaults to True)
            overdrive: Enable maximum quality and detail (defaults to True)
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        data = {
            "tool_type": "audience_research",
            "org_id": org_id,
            "name": name,
            "user_input": user_input,
            "company_details": company_details,
            "auto_company_details": auto_company_details,
            "company_details_id": company_details_id,
            "additional_context": additional_context,
            "documents": documents,
            "temperature": temperature,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "eco": eco
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Video Plan Tool
    
    def create_video_plan(self, name: str, user_input: str, org_id: str = None,
                       company_details: str = None, auto_company_details: bool = True,
                       company_details_id: str = None, additional_context: str = None,
                       documents: List[Dict] = None, temperature: float = 0.7,
                       deepthink: bool = True, overdrive: bool = True, eco: bool = False) -> Dict:
        """
        Create a video plan using AI.
        
        Args:
            name: Name for the video plan
            user_input: Main user instructions for video planning
            org_id: Organization ID (uses default if not provided)
            company_details: Company details as text (ignored if auto_company_details=True)
            auto_company_details: Whether to automatically fetch company details
            company_details_id: Specific company details ID to use (if auto_company_details=True)
            additional_context: Extra context about the video requirements
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics (defaults to True)
            overdrive: Enable maximum quality and detail (defaults to True)
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        data = {
            "tool_type": "video_plan",
            "org_id": org_id,
            "name": name,
            "user_input": user_input,
            "company_details": company_details,
            "auto_company_details": auto_company_details,
            "company_details_id": company_details_id,
            "additional_context": additional_context,
            "documents": documents,
            "temperature": temperature,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "eco": eco
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Shotlist Tool
    
    def create_shotlist(self, name: str, user_input: str, org_id: str = None,
                     scene_details: str = None, visual_style: str = None,
                     documents: List[Dict] = None, temperature: float = 0.7,
                     deepthink: bool = False, overdrive: bool = False,
                     web_search: bool = False, eco: bool = False) -> Dict:
        """
        Create a shotlist using AI.
        
        Args:
            name: Name for the shotlist
            user_input: Main user instructions for shotlist creation
            org_id: Organization ID (uses default if not provided)
            scene_details: Details about the scenes to be shot
            visual_style: Description of the visual style
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        data = {
            "tool_type": "shotlist",
            "org_id": org_id,
            "name": name,
            "user_input": user_input,
            "scene_details": scene_details,
            "visual_style": visual_style,
            "documents": documents,
            "temperature": temperature,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Ad Concept Tool
    
    def create_ad_concept(self, name: str, user_input: str, org_id: str = None,
                       brand_details: str = None, auto_company_details: bool = True,
                       company_details_id: str = None, campaign_goals: str = None,
                       target_audience: str = None, documents: List[Dict] = None,
                       temperature: float = 0.7, deepthink: bool = True,
                       overdrive: bool = True, eco: bool = False) -> Dict:
        """
        Create an ad concept using AI.
        
        Args:
            name: Name for the ad concept
            user_input: Main user instructions for ad concept
            org_id: Organization ID (uses default if not provided)
            brand_details: Brand details as text (ignored if auto_company_details=True)
            auto_company_details: Whether to automatically fetch company details as brand details
            company_details_id: Specific company details ID to use (if auto_company_details=True)
            campaign_goals: Goals of the advertising campaign
            target_audience: Description of the target audience
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics (defaults to True)
            overdrive: Enable maximum quality and detail (defaults to True)
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        data = {
            "tool_type": "ad_concept",
            "org_id": org_id,
            "name": name,
            "user_input": user_input,
            "brand_details": brand_details,
            "auto_company_details": auto_company_details,
            "company_details_id": company_details_id,
            "campaign_goals": campaign_goals,
            "target_audience": target_audience,
            "documents": documents,
            "temperature": temperature,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "eco": eco
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Scene Transitions Tool
    
    def create_scene_transitions(self, name: str, scene_descriptions: List[str], 
                              org_id: str = None, project_style: str = None,
                              mood: str = None, brand_guidelines: str = None,
                              auto_company_details: bool = True, company_details_id: str = None,
                              documents: List[Dict] = None, temperature: float = 0.7,
                              deepthink: bool = True, overdrive: bool = True, 
                              eco: bool = False) -> Dict:
        """
        Create scene transitions using AI.
        
        Args:
            name: Name for the scene transitions
            scene_descriptions: List of scene descriptions to transition between
            org_id: Organization ID (uses default if not provided)
            project_style: Style of the overall project
            mood: Mood or tone of the transitions
            brand_guidelines: Brand guidelines as text (ignored if auto_company_details=True)
            auto_company_details: Whether to automatically fetch company details as brand guidelines
            company_details_id: Specific company details ID to use (if auto_company_details=True)
            documents: Optional list of document contexts to consider
            temperature: AI temperature parameter (0.0-1.0)
            deepthink: Enable advanced thinking for complex topics (defaults to True)
            overdrive: Enable maximum quality and detail (defaults to True)
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        # Validate scene descriptions
        if not isinstance(scene_descriptions, list) or len(scene_descriptions) < 2:
            raise ValueError("scene_descriptions must be a list with at least 2 scenes")
        
        data = {
            "tool_type": "scene_transitions",
            "org_id": org_id,
            "name": name,
            "scene_descriptions": scene_descriptions,
            "project_style": project_style,
            "mood": mood,
            "brand_guidelines": brand_guidelines,
            "auto_company_details": auto_company_details,
            "company_details_id": company_details_id,
            "documents": documents,
            "temperature": temperature,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "eco": eco
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Scene Splitter Tool
    
    def create_scene_splitter(self, name: str, video_path: str, bucket_name: str, 
                           org_id: str = None) -> Dict:
        """
        Split a video into scenes automatically.
        
        Args:
            name: Name for the scene splitter job
            video_path: Path to the video file in S3
            bucket_name: S3 bucket name where the video is stored
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with tool details and job information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        # Validate video_path
        if not video_path:
            raise ValueError("video_path is required")
        
        # Validate file extension
        ext = os.path.splitext(video_path)[1].lower()
        if not ext or ext[1:] not in ["mp4", "mov", "avi", "mkv", "webm"]:
            raise ValueError(f"Invalid video extension: {ext}. Supported formats: mp4, mov, avi, mkv, webm")
        
        data = {
            "tool_type": "scene_splitter",
            "org_id": org_id,
            "name": name,
            "video_path": video_path,
            "bucket_name": bucket_name
        }
        
        return self._make_request("POST", f"{self.tools_url}/create", json_data=data)
    
    # Tool Management Methods
    
    def get_tool(self, tool_id: str, include_job: bool = True) -> Dict:
        """
        Get details about a specific tool.
        
        Args:
            tool_id: ID of the tool to retrieve
            include_job: Whether to include the job result data
            
        Returns:
            Dictionary with tool details and optionally job results
        """
        if not tool_id:
            raise ValueError("tool_id is required")
            
        params = {
            "tool_id": tool_id,
            "include_job": str(include_job).lower()
        }
        
        return self._make_request("GET", f"{self.tools_url}/get", params=params)
    
    def list_tools(self, org_id: str = None, tool_type: str = None, include_results: bool = False, 
                page: int = 1, limit: int = 20) -> Dict:
        """
        List tools for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            tool_type: Optional filter by tool type
            include_results: Whether to include job results for each tool
            page: Page number for pagination
            limit: Number of items per page
            
        Returns:
            Dictionary with tools list and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
        
        params = {
            "org_id": org_id,
            "include_results": str(include_results).lower(),
            "page": page,
            "limit": limit
        }
        
        if tool_type:
            params["tool_type"] = tool_type
            
        return self._make_request("GET", f"{self.tools_url}/list", params=params)
    
    def update_tool(self, tool_id: str, name: str = None, tags: List[str] = None) -> Dict:
        """
        Update a tool's metadata.
        
        Args:
            tool_id: ID of the tool to update
            name: New name for the tool
            tags: List of tags for the tool
            
        Returns:
            Dictionary with updated tool information
        """
        if not tool_id:
            raise ValueError("tool_id is required")
            
        data = {
            "tool_id": tool_id
        }
        
        if name is not None:
            data["name"] = name
        if tags is not None:
            data["tags"] = tags
            
        if len(data) <= 1:
            raise ValueError("At least one updatable field (name or tags) must be provided")
            
        return self._make_request("PUT", f"{self.tools_url}/update", json_data=data)
    
    def delete_tool(self, tool_id: str) -> Dict:
        """
        Delete a tool.
        
        Args:
            tool_id: ID of the tool to delete
            
        Returns:
            Dictionary with deletion confirmation
        """
        if not tool_id:
            raise ValueError("tool_id is required")
            
        params = {
            "tool_id": tool_id
        }
        
        return self._make_request("DELETE", f"{self.tools_url}/delete", params=params)
    
    def redo_tool(self, tool_id: str, input_data: Dict = None, auto_company_details: bool = None,
                company_details_id: str = None, deepthink: bool = None, overdrive: bool = None,
                web_search: bool = None, eco: bool = None) -> Dict:
        """
        Restart a tool job with potentially modified parameters.
        
        Args:
            tool_id: ID of the tool to redo
            input_data: Optional dictionary of input data to override
            auto_company_details: Whether to automatically fetch company details
            company_details_id: Specific company details ID to use
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            
        Returns:
            Dictionary with job information for the restarted job
        """
        if not tool_id:
            raise ValueError("tool_id is required")
            
        data = {
            "tool_id": tool_id
        }
        
        if input_data is not None:
            data["input_data"] = input_data
            
        if auto_company_details is not None:
            data["auto_company_details"] = auto_company_details
            
        if company_details_id is not None:
            data["company_details_id"] = company_details_id
            
        if deepthink is not None:
            data["deepthink"] = deepthink
            
        if overdrive is not None:
            data["overdrive"] = overdrive
            
        if web_search is not None:
            data["web_search"] = web_search
            
        if eco is not None:
            data["eco"] = eco
            
        return self._make_request("POST", f"{self.tools_url}/redo", json_data=data)
