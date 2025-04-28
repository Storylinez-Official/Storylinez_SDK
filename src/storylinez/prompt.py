import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from .base_client import BaseClient

class PromptClient(BaseClient):
    """
    Client for interacting with Storylinez Prompt API.
    Provides methods for managing prompts, reference videos, and content search operations.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the PromptClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.prompts_url = f"{self.base_url}/prompts"
    
    # Prompt Operations
    
    def create_text_prompt(self, project_id: str, main_prompt: str, document_context: str = "",
                         temperature: float = 0.7, total_length: int = 20, iterations: int = 1,
                         deepthink: bool = False, overdrive: bool = False, web_search: bool = False,
                         eco: bool = False, skip_voiceover: bool = False,
                         voiceover_mode: str = "generated") -> Dict:
        """
        Create a new text-based prompt for a project.
        
        Args:
            project_id: ID of the project to create the prompt for
            main_prompt: The actual prompt text
            document_context: Optional document context to support the prompt
            temperature: AI temperature parameter (0.0-1.0)
            total_length: Target length of the video in seconds (10-60)
            iterations: Number of refinement iterations (1-10)
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            skip_voiceover: Whether to skip generating voiceover
            voiceover_mode: Voiceover mode ('generated' or 'uploaded')
            
        Returns:
            Dictionary with the created prompt details
        """
        data = {
            "project_id": project_id,
            "main_prompt": main_prompt,
            "document_context": document_context,
            "temperature": max(0.0, min(1.0, temperature)),  # Clamp between 0 and 1
            "total_length": max(10, min(60, total_length)),  # Clamp between 10 and 60
            "iterations": max(1, min(10, iterations)),  # Clamp between 1 and 10
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
            "skip_voiceover": skip_voiceover,
            "voiceover_mode": voiceover_mode
        }
        
        if voiceover_mode not in ["generated", "uploaded"]:
            raise ValueError("voiceover_mode must be either 'generated' or 'uploaded'")
        
        return self._make_request("POST", f"{self.prompts_url}/create", json_data=data)
    
    def create_video_prompt(self, project_id: str, reference_video_id: str,
                          temperature: float = 0.7, total_length: int = 20, iterations: int = 1,
                          deepthink: bool = False, overdrive: bool = False, web_search: bool = False,
                          eco: bool = False, skip_voiceover: bool = False,
                          voiceover_mode: str = "generated", include_detailed_analysis: bool = False) -> Dict:
        """
        Create a new video-based prompt for a project.
        
        Args:
            project_id: ID of the project to create the prompt for
            reference_video_id: ID of the reference video to use
            temperature: AI temperature parameter (0.0-1.0)
            total_length: Target length of the video in seconds (10-60)
            iterations: Number of refinement iterations (1-10)
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            skip_voiceover: Whether to skip generating voiceover
            voiceover_mode: Voiceover mode ('generated' or 'uploaded')
            include_detailed_analysis: Whether to include detailed video analysis in the prompt
            
        Returns:
            Dictionary with the created prompt details
        """
        data = {
            "project_id": project_id,
            "reference_video_id": reference_video_id,
            "temperature": max(0.0, min(1.0, temperature)),  # Clamp between 0 and 1
            "total_length": max(10, min(60, total_length)),  # Clamp between 10 and 60
            "iterations": max(1, min(10, iterations)),  # Clamp between 1 and 10
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
            "skip_voiceover": skip_voiceover,
            "voiceover_mode": voiceover_mode,
            "include_detailed_analysis": include_detailed_analysis
        }
        
        if voiceover_mode not in ["generated", "uploaded"]:
            raise ValueError("voiceover_mode must be either 'generated' or 'uploaded'")
        
        return self._make_request("POST", f"{self.prompts_url}/create", json_data=data)
    
    def get_prompt(self, prompt_id: str = None, project_id: str = None) -> Dict:
        """
        Get a prompt by ID or project ID.
        
        Args:
            prompt_id: ID of the prompt to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the prompt for (either this or prompt_id must be provided)
            
        Returns:
            Dictionary with the prompt details
        """
        if not prompt_id and not project_id:
            raise ValueError("Either prompt_id or project_id must be provided")
            
        params = {}
        if prompt_id:
            params["prompt_id"] = prompt_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.prompts_url}/get", params=params)
    
    def get_prompt_by_project(self, project_id: str) -> Dict:
        """
        Get a prompt for a specific project.
        
        Args:
            project_id: ID of the project to retrieve the prompt for
            
        Returns:
            Dictionary with the prompt details
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        params = {"project_id": project_id}
        return self._make_request("GET", f"{self.prompts_url}/get_by_project", params=params)
    
    def update_prompt(self, prompt_id: str = None, project_id: str = None, **kwargs) -> Dict:
        """
        Update an existing prompt.
        
        Args:
            prompt_id: ID of the prompt to update (either this or project_id must be provided)
            project_id: ID of the project whose prompt to update (either this or prompt_id must be provided)
            **kwargs: Fields to update (temperature, total_length, iterations, deepthink, overdrive,
                    web_search, eco, main_prompt, document_context, skip_voiceover, voiceover_mode)
            
        Returns:
            Dictionary with update confirmation
        """
        if not prompt_id and not project_id:
            raise ValueError("Either prompt_id or project_id must be provided")
            
        params = {}
        if prompt_id:
            params["prompt_id"] = prompt_id
        if project_id:
            params["project_id"] = project_id
            
        allowed_fields = [
            'temperature', 'total_length', 'iterations',
            'deepthink', 'overdrive', 'web_search', 'eco',
            'main_prompt', 'document_context', 
            'skip_voiceover', 'voiceover_mode',
            'reference_video_id'
        ]
        
        # Filter kwargs to only include allowed fields
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_data:
            raise ValueError("At least one field to update must be provided")
            
        # Validate values
        if 'temperature' in update_data and (update_data['temperature'] < 0 or update_data['temperature'] > 1):
            raise ValueError("temperature must be between 0 and 1")
            
        if 'total_length' in update_data and (update_data['total_length'] < 10 or update_data['total_length'] > 60):
            raise ValueError("total_length must be between 10 and 60 seconds")
            
        if 'iterations' in update_data and (update_data['iterations'] < 1 or update_data['iterations'] > 10):
            raise ValueError("iterations must be between 1 and 10")
            
        if 'voiceover_mode' in update_data and update_data['voiceover_mode'] not in ['generated', 'uploaded']:
            raise ValueError("voiceover_mode must be either 'generated' or 'uploaded'")
            
        return self._make_request("PUT", f"{self.prompts_url}/update", params=params, json_data=update_data)
    
    def switch_prompt_type(self, prompt_id: str, **kwargs) -> Dict:
        """
        Switch between text and video prompt types.
        
        Args:
            prompt_id: ID of the prompt to switch
            **kwargs: For switching to text prompt: main_prompt and document_context (optional)
                     For switching to video prompt: reference_video_id and include_detailed_analysis (optional)
            
        Returns:
            Dictionary with the updated prompt details
        """
        if not prompt_id:
            raise ValueError("prompt_id is required")
            
        params = {"prompt_id": prompt_id}
        
        # Determine new prompt type based on provided fields
        if "main_prompt" in kwargs:
            # Switching to text prompt
            data = {
                "main_prompt": kwargs.get("main_prompt"),
                "document_context": kwargs.get("document_context", "")
            }
        elif "reference_video_id" in kwargs:
            # Switching to video prompt
            data = {
                "reference_video_id": kwargs.get("reference_video_id"),
                "include_detailed_analysis": kwargs.get("include_detailed_analysis", False)
            }
        else:
            raise ValueError("Either main_prompt or reference_video_id must be provided")
            
        return self._make_request("PUT", f"{self.prompts_url}/switch_type", params=params, json_data=data)
    
    # Reference Video Operations
    
    def get_reference_video_upload_link(self, filename: str, org_id: str = None, file_size: int = 0) -> Dict:
        """
        Generate an upload link for a reference video.
        
        Args:
            filename: Name of the video file to upload
            org_id: Organization ID (uses default if not provided)
            file_size: Size of the file in bytes (for storage quota check)
            
        Returns:
            Dictionary with upload URL and details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "filename": filename,
            "file_size": file_size
        }
        
        return self._make_request("GET", f"{self.prompts_url}/upload/create_link", params=params)
    
    def complete_reference_video_upload(self, upload_id: str = None, key: str = None, 
                                      org_id: str = None, filename: str = None,
                                      context: str = "", tags: List[str] = None,
                                      analyze_audio: bool = True) -> Dict:
        """
        Complete a reference video upload.
        
        Args:
            upload_id: ID of the upload (either this or key must be provided)
            key: S3 key of the uploaded file (either this or upload_id must be provided)
            org_id: Organization ID (uses default if not provided)
            filename: Name to use for the file (defaults to the uploaded filename)
            context: Context description for the video
            tags: List of tags for the video
            analyze_audio: Whether to analyze audio in the video
            
        Returns:
            Dictionary with the registered video details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        if not upload_id and not key:
            raise ValueError("Either upload_id or key must be provided")
            
        data = {
            "org_id": org_id,
            "context": context,
            "analyze_audio": analyze_audio
        }
        
        if upload_id:
            data["upload_id"] = upload_id
        if key:
            data["key"] = key
        if filename:
            data["filename"] = filename
        if tags:
            data["tags"] = tags
            
        return self._make_request("POST", f"{self.prompts_url}/upload/complete", json_data=data)
    
    def list_reference_videos(self, org_id: str = None, detailed: bool = False, 
                            generate_thumbnail: bool = True, generate_streamable: bool = False,
                            generate_download: bool = False, include_usage: bool = False,
                            max_prompts_per_video: int = 5, page: int = 1, limit: int = 10) -> Dict:
        """
        List all reference videos for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            detailed: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            include_usage: Whether to include usage information
            max_prompts_per_video: Maximum number of prompts to return per video if include_usage is True
            page: Page number for pagination (starting from 1)
            limit: Number of items per page (max 50)
            
        Returns:
            Dictionary with list of reference videos and pagination metadata
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Validate pagination parameters
        page = max(1, page)  # Ensure page is at least 1
        limit = max(1, min(50, limit))  # Ensure limit is between 1 and 50
        
        params = {
            "org_id": org_id,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower(),
            "include_usage": str(include_usage).lower(),
            "max_prompts_per_video": max_prompts_per_video,
            "page": page,
            "limit": limit
        }
        
        return self._make_request("GET", f"{self.prompts_url}/reference-videos/list", params=params)
    
    def get_reference_video_details(self, file_id: str, detailed: bool = True,
                                 generate_thumbnail: bool = True, generate_streamable: bool = True,
                                 generate_download: bool = True, include_usage: bool = True) -> Dict:
        """
        Get details of a specific reference video.
        
        Args:
            file_id: ID of the reference video
            detailed: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URL
            generate_streamable: Whether to generate streamable URL
            generate_download: Whether to generate download URL
            include_usage: Whether to include usage information
            
        Returns:
            Dictionary with reference video details
        """
        if not file_id:
            raise ValueError("file_id is required")
            
        params = {
            "file_id": file_id,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower(),
            "include_usage": str(include_usage).lower()
        }
        
        return self._make_request("GET", f"{self.prompts_url}/reference-videos/details", params=params)
    
    def search_reference_videos(self, query: str, org_id: str = None, page: int = 1,
                             limit: int = 10, detailed: bool = False, 
                             generate_thumbnail: bool = True, generate_streamable: bool = False,
                             generate_download: bool = False, include_usage: bool = False,
                             max_prompts_per_video: int = 5) -> Dict:
        """
        Search for reference videos by filename.
        
        Args:
            query: Search term
            org_id: Organization ID (uses default if not provided)
            page: Page number for pagination
            limit: Number of items per page
            detailed: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            include_usage: Whether to include usage information
            max_prompts_per_video: Maximum number of prompts to return per video if include_usage is True
            
        Returns:
            Dictionary with search results
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "query": query,
            "page": page,
            "limit": limit,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower(),
            "include_usage": str(include_usage).lower(),
            "max_prompts_per_video": max_prompts_per_video
        }
        
        return self._make_request("GET", f"{self.prompts_url}/reference-videos/search", params=params)
    
    def delete_reference_video(self, file_id: str) -> Dict:
        """
        Delete a reference video.
        
        Args:
            file_id: ID of the reference video to delete
            
        Returns:
            Dictionary with deletion confirmation
        """
        if not file_id:
            raise ValueError("file_id is required")
            
        params = {"file_id": file_id}
        return self._make_request("DELETE", f"{self.prompts_url}/reference-videos/delete", params=params)
    
    def get_reference_videos_by_ids(self, file_ids: List[str], org_id: str = None,
                                   detailed: bool = False, generate_thumbnail: bool = True,
                                   generate_streamable: bool = False, generate_download: bool = False,
                                   include_usage: bool = False) -> Dict:
        """
        Get multiple reference videos by their IDs.
        
        Args:
            file_ids: List of reference video IDs
            org_id: Organization ID (uses default if not provided)
            detailed: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            include_usage: Whether to include usage information
            
        Returns:
            Dictionary with requested reference videos
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        if not file_ids:
            raise ValueError("file_ids list cannot be empty")
            
        if len(file_ids) > 50:
            raise ValueError("Cannot request more than 50 reference videos at once")
            
        params = {
            "org_id": org_id,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower(),
            "include_usage": str(include_usage).lower()
        }
        
        data = {"file_ids": file_ids}
        
        return self._make_request("POST", f"{self.prompts_url}/reference-videos/get_by_ids", params=params, json_data=data)
    
    def upload_reference_video(self, file_path: str, org_id: str = None, context: str = "", 
                              tags: List[str] = None, analyze_audio: bool = True) -> Dict:
        """
        Upload a reference video file.
        This is a convenience method that handles both the link generation, upload, and registration.
        
        Args:
            file_path: Path to the video file on local disk
            org_id: Organization ID (uses default if not provided)
            context: Context description for the video
            tags: List of tags for the video
            analyze_audio: Whether to analyze audio in the video
            
        Returns:
            Dictionary with the registered video details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Get file information
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Generate upload link
        upload_info = self.get_reference_video_upload_link(
            filename=filename,
            org_id=org_id,
            file_size=file_size
        )
        
        # Upload the file to the pre-signed URL
        upload_link = upload_info.get("upload_link")
        upload_id = upload_info.get("upload_id")
        
        # Use requests to upload the file
        with open(file_path, 'rb') as file_data:
            upload_response = requests.put(upload_link, data=file_data)
            
            if upload_response.status_code >= 400:
                raise Exception(f"Reference video upload failed with status {upload_response.status_code}")
        
        # Complete the upload and register the video
        return self.complete_reference_video_upload(
            upload_id=upload_id,
            org_id=org_id,
            filename=filename,
            context=context,
            tags=tags,
            analyze_audio=analyze_audio
        )
    
    # Content Search Operations
    
    def generate_search(self, prompt_id: str = None, project_id: str = None, 
                       num_videos: int = 5, num_audio: int = 1, num_images: int = 0,
                       company_details: str = "", documents: List[str] = None,
                       temperature: float = None) -> Dict:
        """
        Start a search job to find content matching a prompt.
        
        Args:
            prompt_id: ID of the prompt to use for search (either this or project_id must be provided)
            project_id: ID of the project whose prompt to use (either this or prompt_id must be provided)
            num_videos: Number of video results to request
            num_audio: Number of audio results to request
            num_images: Number of image results to request
            company_details: Company details to use for search context
            documents: List of document texts to use as additional context
            temperature: Custom temperature for the search query
            
        Returns:
            Dictionary with job information
        """
        if not prompt_id and not project_id:
            raise ValueError("Either prompt_id or project_id must be provided")
            
        data = {
            "num_videos": max(0, min(50, num_videos)),
            "num_audio": max(0, min(50, num_audio)),
            "num_images": max(0, min(50, num_images))
        }
        
        if prompt_id:
            data["prompt_id"] = prompt_id
        if project_id:
            data["project_id"] = project_id
        if company_details:
            data["company_details"] = company_details
        if documents:
            data["documents"] = documents
        if temperature is not None:
            data["temperature"] = max(0.0, min(1.0, temperature))
            
        return self._make_request("POST", f"{self.prompts_url}/query/generate", json_data=data)
    
    def get_search_results(self, prompt_id: str = None, project_id: str = None) -> Dict:
        """
        Get results from a previously started search job.
        
        Args:
            prompt_id: ID of the prompt used for the search (either this or project_id must be provided)
            project_id: ID of the project whose prompt was used (either this or prompt_id must be provided)
            
        Returns:
            Dictionary with search results or status
        """
        if not prompt_id and not project_id:
            raise ValueError("Either prompt_id or project_id must be provided")
            
        params = {}
        if prompt_id:
            params["prompt_id"] = prompt_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.prompts_url}/query/results", params=params)
    
    def get_storage_usage(self, org_id: str = None) -> Dict:
        """
        Get storage usage information for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with storage usage information
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {"org_id": org_id}
        return self._make_request("GET", f"{self.prompts_url}/storage/usage", params=params)
