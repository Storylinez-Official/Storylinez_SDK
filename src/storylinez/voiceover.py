import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from .base_client import BaseClient

class VoiceoverClient(BaseClient):
    """
    Client for interacting with Storylinez Voiceover API.
    Provides methods for generating, retrieving, and managing voiceovers for projects.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the VoiceoverClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.voiceover_url = f"{self.base_url}/voiceover"
    
    # Voiceover Operations
    
    def create_voiceover(self, project_id: str, voiceover_code: str = None) -> Dict:
        """
        Create a new voiceover for a project. The project must have an existing storyboard.
        
        Args:
            project_id: ID of the project to create the voiceover for
            voiceover_code: Optional voice identifier to use (e.g., 'en-US-Neural2-F')
            
        Returns:
            Dictionary with the created voiceover details and job information
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        data = {"project_id": project_id}
        if voiceover_code:
            data["voiceover_code"] = voiceover_code
            
        return self._make_request("POST", f"{self.voiceover_url}/create", json_data=data)
    
    def get_voiceover(self, voiceover_id: str = None, project_id: str = None,
                   include_results: bool = True, include_storyboard: bool = False,
                   generate_audio_link: bool = True) -> Dict:
        """
        Get details of a voiceover by either voiceover ID or project ID.
        
        Args:
            voiceover_id: ID of the voiceover to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the voiceover for (either this or voiceover_id must be provided)
            include_results: Whether to include job results
            include_storyboard: Whether to include the storyboard data
            generate_audio_link: Whether to generate a temporary audio URL
            
        Returns:
            Dictionary with the voiceover details
        """
        if not voiceover_id and not project_id:
            raise ValueError("Either voiceover_id or project_id must be provided")
            
        params = {
            "include_results": str(include_results).lower(),
            "include_storyboard": str(include_storyboard).lower(),
            "generate_audio_link": str(generate_audio_link).lower()
        }
        
        if voiceover_id:
            params["voiceover_id"] = voiceover_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.voiceover_url}/get", params=params)
    
    def redo_voiceover(self, voiceover_id: str = None, project_id: str = None,
                     voiceover_code: str = None) -> Dict:
        """
        Regenerate a voiceover with the latest storyboard data.
        
        Args:
            voiceover_id: ID of the voiceover to regenerate (either this or project_id must be provided)
            project_id: ID of the project whose voiceover to regenerate (either this or voiceover_id must be provided)
            voiceover_code: Optional new voice identifier to use
            
        Returns:
            Dictionary with job information
        """
        if not voiceover_id and not project_id:
            raise ValueError("Either voiceover_id or project_id must be provided")
            
        data = {}
        
        if voiceover_id:
            data["voiceover_id"] = voiceover_id
        if project_id:
            data["project_id"] = project_id
        if voiceover_code:
            data["voiceover_code"] = voiceover_code
            
        return self._make_request("POST", f"{self.voiceover_url}/redo", json_data=data)
    
    def update_voiceover_data(self, voiceover_id: str = None, project_id: str = None) -> Dict:
        """
        Update a voiceover with the latest storyboard data without regenerating it.
        
        Args:
            voiceover_id: ID of the voiceover to update (either this or project_id must be provided)
            project_id: ID of the project whose voiceover to update (either this or voiceover_id must be provided)
            
        Returns:
            Dictionary with the update operation result
        """
        if not voiceover_id and not project_id:
            raise ValueError("Either voiceover_id or project_id must be provided")
            
        data = {}
        
        if voiceover_id:
            data["voiceover_id"] = voiceover_id
        if project_id:
            data["project_id"] = project_id
            
        return self._make_request("PUT", f"{self.voiceover_url}/selfupdate", json_data=data)
    
    def get_voiceover_history(self, voiceover_id: str, page: int = 1, limit: int = 10) -> Dict:
        """
        Get job history for a voiceover.
        
        Args:
            voiceover_id: ID of the voiceover
            page: Page number for pagination
            limit: Number of items per page
            
        Returns:
            Dictionary with history entries
        """
        if not voiceover_id:
            raise ValueError("voiceover_id is required")
            
        params = {
            "voiceover_id": voiceover_id,
            "page": page,
            "limit": limit
        }
        
        return self._make_request("GET", f"{self.voiceover_url}/history", params=params)
    
    def get_voice_types(self) -> Dict:
        """
        Get available voice types for voiceover generation.
        
        Returns:
            Dictionary with available voice types and their details
        """
        return self._make_request("GET", f"{self.base_url}/utility/get-voice-types")
    
    # Voice Upload Operations
    
    def upload_voiceover_file(self, project_id: str, file_path: str, voice_name: str = "Custom Voiceover") -> Dict:
        """
        Upload a custom voiceover file for a project.
        
        Args:
            project_id: ID of the project
            file_path: Path to the audio file to upload
            voice_name: Name/description for the voice
            
        Returns:
            Dictionary with the upload operation result
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not file_path or not os.path.isfile(file_path):
            raise ValueError("file_path must be a valid file")
            
        # First, create an upload link
        from .storage import StorageClient
        storage_client = StorageClient(self.api_key, self.api_secret, self.base_url, self.default_org_id)
        
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        upload_result = storage_client.generate_upload_link(
            filename=filename,
            file_size=file_size
        )
        
        # Upload the file to the provided URL
        with open(file_path, "rb") as file:
            upload_url = upload_result["upload_url"]
            requests.put(upload_url, data=file.read())
        
        # Complete the upload
        completion_result = storage_client.mark_upload_complete(
            upload_id=upload_result["upload_id"],
            context=f"Voiceover file for project {project_id}"
        )
        
        file_id = completion_result["file"]["file_id"]
        
        # Add the file as project voiceover
        return self.add_voiceover_to_project(project_id, file_id, voice_name)
    
    def add_voiceover_to_project(self, project_id: str, file_id: str, voice_name: str = "Custom Voiceover") -> Dict:
        """
        Add an uploaded audio file as a project's voiceover.
        
        Args:
            project_id: ID of the project
            file_id: ID of the uploaded audio file
            voice_name: Name/description for the voice
            
        Returns:
            Dictionary with the operation result
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not file_id:
            raise ValueError("file_id is required")
            
        data = {
            "project_id": project_id,
            "file_id": file_id,
            "voice_name": voice_name
        }
        
        # This endpoint is on the project API, not voiceover
        project_url = f"{self.base_url}/projects"
        url = f"{project_url}/voiceovers/add"
        
        request_headers = self._get_headers()
        
        response = requests.post(
            url,
            params={"project_id": project_id},
            json=data,
            headers=request_headers
        )
        
        # Check if the request was successful
        if response.status_code >= 400:
            error_message = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_message = f"{error_message}: {error_data['error']}"
            except:
                if response.text:
                    error_message = f"{error_message}: {response.text}"
            
            raise Exception(error_message)
        
        return response.json()
    
    def remove_voiceover_from_project(self, project_id: str) -> Dict:
        """
        Remove the voiceover from a project.
        
        Args:
            project_id: ID of the project
            
        Returns:
            Dictionary with the operation result
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        # This endpoint is on the project API, not voiceover
        project_url = f"{self.base_url}/projects"
        url = f"{project_url}/voiceovers/remove"
        
        request_headers = self._get_headers()
        
        response = requests.delete(
            url,
            params={"project_id": project_id},
            headers=request_headers
        )
        
        # Check if the request was successful
        if response.status_code >= 400:
            error_message = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_message = f"{error_message}: {error_data['error']}"
            except:
                if response.text:
                    error_message = f"{error_message}: {response.text}"
            
            raise Exception(error_message)
        
        return response.json()
