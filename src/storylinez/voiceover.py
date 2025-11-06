import os
import json
import requests
import time
import re
from typing import Dict, List, Optional, Union, Any, BinaryIO, Tuple
from datetime import datetime
from .base_client import BaseClient
from .shared.validation import validate_media_extension

class VoiceoverClient(BaseClient):
    """
    Client for interacting with Storylinez Voiceover API.
    Provides methods for generating, retrieving, and managing voiceovers for projects.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinezads.com", default_org_id: str = None):
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
        self._voice_types_cache = None
        self._voice_types_timestamp = None
        self._cache_duration = 3600  # 1 hour cache duration
        # Cache for resolving project types to avoid extra lookups
        self._project_type_cache = {}
    
    # Enhanced Voiceover Operations
    
    @staticmethod
    def _normalize_project_type_hint(project_type: Optional[str]) -> Optional[str]:
        """Normalize an optional project_type hint provided by callers.

        Returns 'v1' or 'v2' when the hint is explicit; otherwise returns None.
        """
        if project_type is None:
            return None
        if not isinstance(project_type, str):
            return None
        candidate = project_type.strip().lower()
        if candidate in ("v1", "v2"):
            return candidate
        return None

    def _get_project_type(self, project_id: str) -> str:
        """Fetch and cache project type information for voiceover guard rails."""
        cached = self._project_type_cache.get(project_id)
        if cached:
            return cached

        response = self._make_request(
            "GET",
            f"{self.base_url}/projects/get_one",
            params={"project_id": project_id}
        )
        project_type = (response.get("type") or "v1").lower()
        self._project_type_cache[project_id] = project_type
        return project_type

    def _ensure_legacy_voiceover_supported(self, project_id: str, project_type_hint: Optional[str]) -> str:
        """Raise when attempting to use legacy voiceover APIs for v2 projects.

        project_type_hint can be provided by the caller to avoid an extra project lookup.
        """
        normalized_hint = self._normalize_project_type_hint(project_type_hint)
        resolved_type = normalized_hint or self._get_project_type(project_id)
        if resolved_type == "v2":
            raise ValueError(
                "Voiceovers are disabled for v2 sequence builder projects via legacy endpoints. Use the /v2/audio workflows instead."
            )
        return resolved_type

    def _resolve_project_id_from_voiceover(self, voiceover_id: str) -> str:
        """Resolve the project_id for a given voiceover to enforce legacy guards."""
        params = {
            "voiceover_id": voiceover_id,
            "include_results": "false",
            "include_storyboard": "false",
            "generate_audio_link": "false"
        }
        response = self._make_request("GET", f"{self.voiceover_url}/get", params=params)
        if isinstance(response, dict):
            project_id = response.get("project_id")
            if project_id:
                return project_id
            voiceover_payload = response.get("voiceover")
            if isinstance(voiceover_payload, dict):
                project_id = voiceover_payload.get("project_id")
                if project_id:
                    return project_id
        raise ValueError("Could not determine project_id for the provided voiceover_id")
    
    def create_voiceover(self, 
                       project_id: str, 
                       voiceover_code: Optional[str] = None,
                       **kwargs) -> Dict:
        """
        Create a new voiceover for a project. The project must have an existing storyboard.
        
        Args:
            project_id: ID of the project to create the voiceover for
            voiceover_code: Optional voice identifier to use.
            **kwargs: Additional parameters to pass to the API (for compatibility)
            
        Returns:
            Dictionary with the created voiceover details and job information
        
        Raises:
            ValueError: If project_id is missing or if voiceover_code is invalid
        """
        # Validate project_id
        if not project_id:
            raise ValueError("project_id is required for creating a voiceover")
        # Ensure legacy (v1) endpoints are not used for v2 projects.
        # Allow callers to pass an optional project_type hint via kwargs to avoid an extra lookup.
        project_type_hint = kwargs.get('project_type')
        self._ensure_legacy_voiceover_supported(project_id, project_type_hint)
        
        if not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
            
        # Validate voiceover_code if provided
        if voiceover_code:
            voiceover_code = self._normalize_voice_code(voiceover_code)
            
        data = {"project_id": project_id}
        if voiceover_code:
            data["voiceover_code"] = voiceover_code
            
        return self._make_request("POST", f"{self.voiceover_url}/create", json_data=data)
    
    def get_voiceover(self, 
                   voiceover_id: Optional[str] = None, 
                   project_id: Optional[str] = None,
                   include_results: bool = True, 
                   include_storyboard: bool = False,
                   generate_audio_link: bool = True,
                   **kwargs) -> Dict:
        """
        Get details of a voiceover by either voiceover ID or project ID.
        
        Args:
            voiceover_id: ID of the voiceover to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the voiceover for (either this or voiceover_id must be provided)
            include_results: Whether to include job results
            include_storyboard: Whether to include the storyboard data
            generate_audio_link: Whether to generate a temporary audio URL
            **kwargs: Additional parameters to pass to the API (for compatibility)
            
        Returns:
            Dictionary with the voiceover details
            
        Raises:
            ValueError: If neither voiceover_id nor project_id is provided
        """
        # Validate that either voiceover_id or project_id is provided
        if not voiceover_id and not project_id:
            raise ValueError("Either voiceover_id or project_id must be provided")
        
        # Type validation and conversion
        if voiceover_id and not isinstance(voiceover_id, str):
            voiceover_id = str(voiceover_id)
            print(f"Warning: voiceover_id was converted to string: {voiceover_id}")
            
        if project_id and not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
            
        # Ensure boolean parameters are actually booleans
        include_results = self._ensure_bool(include_results, "include_results")
        include_storyboard = self._ensure_bool(include_storyboard, "include_storyboard")
        generate_audio_link = self._ensure_bool(generate_audio_link, "generate_audio_link")
            
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
    
    def redo_voiceover(self, 
                     voiceover_id: Optional[str] = None, 
                     project_id: Optional[str] = None,
                     voiceover_code: Optional[str] = None, 
                     **kwargs) -> Dict:
        """
        Regenerate a voiceover with the latest storyboard data.
        
        Args:
            voiceover_id: ID of the voiceover to regenerate (either this or project_id must be provided)
            project_id: ID of the project whose voiceover to regenerate (either this or voiceover_id must be provided)
            voiceover_code: Optional new voice identifier to use
            **kwargs: Additional parameters to pass to the API (for compatibility)
            
        Returns:
            Dictionary with job information
            
        Raises:
            ValueError: If neither voiceover_id nor project_id is provided or if voiceover_code is invalid
        """
        # Validate that either voiceover_id or project_id is provided
        if not voiceover_id and not project_id:
            raise ValueError("Either voiceover_id or project_id must be provided")
            
        # Type validation and conversion
        if voiceover_id and not isinstance(voiceover_id, str):
            voiceover_id = str(voiceover_id)
            print(f"Warning: voiceover_id was converted to string: {voiceover_id}")
            
        if project_id and not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
        
        # Validate voiceover_code if provided
        if voiceover_code:
            voiceover_code = self._normalize_voice_code(voiceover_code)
            
        project_type_hint = kwargs.get('project_type')
        resolved_project_id = project_id
        if project_id:
            self._ensure_legacy_voiceover_supported(project_id, project_type_hint)
        else:
            resolved_project_id = self._resolve_project_id_from_voiceover(voiceover_id)
            self._ensure_legacy_voiceover_supported(resolved_project_id, project_type_hint)
            project_id = resolved_project_id

        data = {}
        
        if voiceover_id:
            data["voiceover_id"] = voiceover_id
        if project_id:
            data["project_id"] = project_id
        if voiceover_code:
            data["voiceover_code"] = voiceover_code
            
        return self._make_request("POST", f"{self.voiceover_url}/redo", json_data=data)
    
    def update_voiceover_data(self, 
                            voiceover_id: Optional[str] = None, 
                            project_id: Optional[str] = None,
                            **kwargs) -> Dict:
        """
        Update a voiceover with the latest storyboard data without regenerating it.
        
        Args:
            voiceover_id: ID of the voiceover to update (either this or project_id must be provided)
            project_id: ID of the project whose voiceover to update (either this or voiceover_id must be provided)
            **kwargs: Additional parameters to pass to the API (for compatibility)
            
        Returns:
            Dictionary with the update operation result
            
        Raises:
            ValueError: If neither voiceover_id nor project_id is provided
        """
        # Validate that either voiceover_id or project_id is provided
        if not voiceover_id and not project_id:
            raise ValueError("Either voiceover_id or project_id must be provided")
        
        # Type validation and conversion
        if voiceover_id and not isinstance(voiceover_id, str):
            voiceover_id = str(voiceover_id)
            print(f"Warning: voiceover_id was converted to string: {voiceover_id}")
            
        if project_id and not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
            
        project_type_hint = kwargs.get('project_type')
        resolved_project_id = project_id
        if project_id:
            self._ensure_legacy_voiceover_supported(project_id, project_type_hint)
        else:
            resolved_project_id = self._resolve_project_id_from_voiceover(voiceover_id)
            self._ensure_legacy_voiceover_supported(resolved_project_id, project_type_hint)
            project_id = resolved_project_id

        data = {}
        
        if voiceover_id:
            data["voiceover_id"] = voiceover_id
        if project_id:
            data["project_id"] = project_id
            
        return self._make_request("PUT", f"{self.voiceover_url}/selfupdate", json_data=data)
    
    def get_voiceover_history(self, 
                            voiceover_id: str, 
                            page: int = 1, 
                            limit: int = 10,
                            **kwargs) -> Dict:
        """
        Get job history for a voiceover.
        
        Args:
            voiceover_id: ID of the voiceover
            page: Page number for pagination
            limit: Number of items per page
            **kwargs: Additional parameters to pass to the API (for compatibility)
            
        Returns:
            Dictionary with history entries
            
        Raises:
            ValueError: If voiceover_id is missing or if page/limit are invalid
        """
        # Validate voiceover_id
        if not voiceover_id:
            raise ValueError("voiceover_id is required for fetching voiceover history")
        
        if not isinstance(voiceover_id, str):
            voiceover_id = str(voiceover_id)
            print(f"Warning: voiceover_id was converted to string: {voiceover_id}")
            
        # Validate page and limit
        if not isinstance(page, int) or page < 1:
            try:
                page = int(page)
                if page < 1:
                    page = 1
                print(f"Warning: page was adjusted to valid value: {page}")
            except (ValueError, TypeError):
                page = 1
                print(f"Warning: invalid page value was set to default: {page}")
                
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            try:
                limit = int(limit)
                if limit < 1:
                    limit = 10
                elif limit > 100:
                    limit = 100
                print(f"Warning: limit was adjusted to valid range: {limit}")
            except (ValueError, TypeError):
                limit = 10
                print(f"Warning: invalid limit value was set to default: {limit}")
            
        params = {
            "voiceover_id": voiceover_id,
            "page": page,
            "limit": limit
        }
        
        return self._make_request("GET", f"{self.voiceover_url}/history", params=params)
    
    def get_voice_types(self, refresh_cache: bool = False) -> Dict:
        """
        Get available voice types for voiceover generation.
        
        Args:
            refresh_cache: Force refresh the voice types cache
            
        Returns:
            Dictionary with available voice types and their details
        """
        # Check if we have cached data that's not expired
        current_time = time.time()
        cache_valid = (not refresh_cache and 
                      self._voice_types_cache is not None and
                      self._voice_types_timestamp is not None and
                      (current_time - self._voice_types_timestamp) < self._cache_duration)
        
        if cache_valid:
            return self._voice_types_cache
            
        # Fetch fresh data
        result = self._make_request("GET", f"{self.base_url}/utility/get-voice-types")
        
        # Cache the result
        if 'voice_types' in result:
            self._voice_types_cache = result
            self._voice_types_timestamp = current_time
            
        return result
    
    # Voice Upload Operations
    
    def upload_voiceover_file(self, 
                            project_id: str, 
                            file_path: str, 
                            voice_name: str = "Custom Voiceover") -> Dict:
        """
        Upload a custom voiceover file for a project.
        
        Args:
            project_id: ID of the project
            file_path: Path to the audio file to upload
            voice_name: Name/description for the voice
            
        Returns:
            Dictionary with the upload operation result
            
        Raises:
            ValueError: If project_id is missing or if file_path is invalid
            FileNotFoundError: If the file doesn't exist
        """
        # Validate project_id
        if not project_id:
            raise ValueError("project_id is required for uploading a voiceover file")
            
        if not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
            
        # Validate file_path
        if not file_path:
            raise ValueError("file_path is required")
        
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Validate voice_name
        if not voice_name or not isinstance(voice_name, str):
            voice_name = "Custom Voiceover"
            print(f"Warning: voice_name was reset to default: {voice_name}")
            
        filename = os.path.basename(file_path)
        try:
            validate_media_extension(filename, media_type='AUDIO')
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

        # First, create an upload link
        from .storage import StorageClient
        storage_client = StorageClient(self.api_key, self.api_secret, self.base_url, self.default_org_id)
        
        file_size = os.path.getsize(file_path)
        
        print(f"Preparing to upload {filename} ({self._format_size(file_size)})...")
        
        upload_result = storage_client.generate_upload_link(
            filename=filename,
            file_size=file_size
        )
        
        # Upload the file to the provided URL
        print(f"Uploading file to Storylinez servers...")
        with open(file_path, "rb") as file:
            upload_url = upload_result["upload_url"]
            response = requests.put(upload_url, data=file.read())
            
            if response.status_code >= 400:
                raise Exception(f"File upload failed with status {response.status_code}: {response.text}")
        
        # Complete the upload
        print(f"Finalizing upload...")
        completion_result = storage_client.mark_upload_complete(
            upload_id=upload_result["upload_id"],
            context=f"Voiceover file for project {project_id}"
        )
        
        file_id = completion_result["file"]["file_id"]
        
        # Add the file as project voiceover
        print(f"Associating voiceover file with project...")
        result = self.add_voiceover_to_project(project_id, file_id, voice_name)
        
        print(f"Voiceover file uploaded successfully!")
        return result
    
    def add_voiceover_to_project(self, 
                               project_id: str, 
                               file_id: str, 
                               voice_name: str = "Custom Voiceover") -> Dict:
        """
        Add an uploaded audio file as a project's voiceover.
        
        Args:
            project_id: ID of the project
            file_id: ID of the uploaded audio file
            voice_name: Name/description for the voice
            
        Returns:
            Dictionary with the operation result
            
        Raises:
            ValueError: If project_id or file_id is missing
        """
        # Validate project_id
        if not project_id:
            raise ValueError("project_id is required")
            
        if not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
            
        # Validate file_id
        if not file_id:
            raise ValueError("file_id is required")
            
        if not isinstance(file_id, str):
            file_id = str(file_id)
            print(f"Warning: file_id was converted to string: {file_id}")
            
        # Validate voice_name
        if not voice_name or not isinstance(voice_name, str):
            voice_name = "Custom Voiceover"
            print(f"Warning: voice_name was reset to default: {voice_name}")
            
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
            
        Raises:
            ValueError: If project_id is missing
        """
        # Validate project_id
        if not project_id:
            raise ValueError("project_id is required")
            
        if not isinstance(project_id, str):
            project_id = str(project_id)
            print(f"Warning: project_id was converted to string: {project_id}")
            
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
    
    # Enhanced utility methods
    
    def download_voiceover(self, 
                         voiceover_id: Optional[str] = None, 
                         project_id: Optional[str] = None, 
                         output_path: Optional[str] = None) -> str:
        """
        Download a voiceover audio file to local storage.
        
        Args:
            voiceover_id: ID of the voiceover (either this or project_id must be provided)
            project_id: ID of the project (either this or voiceover_id must be provided)
            output_path: Local path where the audio file should be saved. 
                        If not provided, will create a file in the current directory.
            
        Returns:
            Path to the downloaded file
            
        Raises:
            ValueError: If neither voiceover_id nor project_id is provided
            Exception: If the voiceover is not ready or download fails
        """
        # Get the voiceover with audio URL
        voiceover = self.get_voiceover(
            voiceover_id=voiceover_id,
            project_id=project_id,
            include_results=True,
            generate_audio_link=True
        )
        
        # Check if voiceover has a streamable audio URL
        if 'audio_url' not in voiceover:
            job_status = voiceover.get('job_result', {}).get('status', 'Unknown')
            if job_status != 'COMPLETED':
                raise Exception(f"Voiceover is not ready for download. Current status: {job_status}")
            else:
                raise Exception("Voiceover audio URL is not available")
                
        audio_url = voiceover['audio_url']
        
        # Determine output filename if not specified
        if not output_path:
            vo_id = voiceover.get('voiceover_id', 'voiceover')
            output_path = f"{vo_id}_audio.wav"
            
        # Download the file
        response = requests.get(audio_url, stream=True)
        
        if response.status_code >= 400:
            raise Exception(f"Failed to download voiceover audio: HTTP {response.status_code}")
            
        # Save to file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Voiceover audio downloaded to: {output_path}")
        return output_path
    
    def wait_for_completion(self, 
                          voiceover_id: Optional[str] = None, 
                          project_id: Optional[str] = None,
                          timeout_seconds: int = 300,
                          poll_interval: int = 5) -> Dict:
        """
        Wait for a voiceover to complete generation.
        
        Args:
            voiceover_id: ID of the voiceover (either this or project_id must be provided)
            project_id: ID of the project (either this or voiceover_id must be provided)
            timeout_seconds: Maximum time to wait in seconds
            poll_interval: How often to check status in seconds
            
        Returns:
            The completed voiceover data
            
        Raises:
            ValueError: If neither voiceover_id nor project_id is provided
            TimeoutError: If the voiceover doesn't complete within the timeout period
            Exception: If the voiceover generation fails
        """
        start_time = time.time()
        
        while True:
            # Check if we've exceeded the timeout
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError(f"Voiceover generation did not complete within {timeout_seconds} seconds")
                
            # Get current status
            voiceover = self.get_voiceover(
                voiceover_id=voiceover_id,
                project_id=project_id,
                include_results=True
            )
            
            # Check job status
            job_result = voiceover.get('job_result', {})
            status = job_result.get('status')
            
            if status == 'COMPLETED':
                print(f"Voiceover generation completed successfully!")
                return voiceover
            elif status in ['FAILED', 'ERROR']:
                error_message = job_result.get('error', 'Unknown error')
                raise Exception(f"Voiceover generation failed: {error_message}")
            
            # If still processing, wait and try again
            print(f"Voiceover generation in progress. Status: {status}. Waiting {poll_interval} seconds...")
            time.sleep(poll_interval)
    
    def create_and_wait(self, 
                      project_id: str, 
                      voiceover_code: Optional[str] = None,
                      timeout_seconds: int = 300,
                      poll_interval: int = 5) -> Dict:
        """
        Create a voiceover and wait for it to complete in one operation.
        
        Args:
            project_id: ID of the project to create the voiceover for
            voiceover_code: Optional voice identifier to use
            timeout_seconds: Maximum time to wait for completion
            poll_interval: How often to check status in seconds
            
        Returns:
            The completed voiceover data
            
        Raises:
            ValueError: If project_id is missing
            TimeoutError: If the voiceover doesn't complete within the timeout period
            Exception: If creation or generation fails
        """
        # Create the voiceover
        result = self.create_voiceover(
            project_id=project_id,
            voiceover_code=voiceover_code
        )
        
        voiceover_id = result.get('voiceover', {}).get('voiceover_id')
        
        if not voiceover_id:
            raise Exception("Failed to get voiceover_id from creation response")
            
        print(f"Voiceover creation initiated. Waiting for completion...")
        
        # Wait for completion
        return self.wait_for_completion(
            voiceover_id=voiceover_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval
        )
    
    def get_or_create_voiceover(self, 
                              project_id: str, 
                              voiceover_code: Optional[str] = None,
                              wait_for_completion: bool = False,
                              timeout_seconds: int = 300) -> Dict:
        """
        Check if a voiceover exists for a project, and create one if it doesn't.
        
        Args:
            project_id: ID of the project
            voiceover_code: Optional voice identifier to use if creating
            wait_for_completion: Whether to wait for completion if creating a new voiceover
            timeout_seconds: Maximum time to wait if waiting for completion
            
        Returns:
            The voiceover data (either existing or newly created)
            
        Raises:
            ValueError: If project_id is missing
            Exception: If creation fails or waiting times out
        """
        # Check if voiceover exists
        try:
            existing = self.get_voiceover(project_id=project_id)
            print(f"Found existing voiceover for project {project_id}")
            return existing
        except Exception as e:
            if '404' not in str(e):
                # If it's not a 404 error, re-raise it
                raise
                
        # No existing voiceover found, create a new one
        print(f"No existing voiceover found for project {project_id}. Creating...")
        result = self.create_voiceover(
            project_id=project_id,
            voiceover_code=voiceover_code
        )
        
        if wait_for_completion:
            voiceover_id = result.get('voiceover', {}).get('voiceover_id')
            if not voiceover_id:
                raise Exception("Failed to get voiceover_id from creation response")
                
            print(f"Waiting for voiceover generation to complete...")
            return self.wait_for_completion(
                voiceover_id=voiceover_id,
                timeout_seconds=timeout_seconds
            )
        
        return result['voiceover']
    
    # Helper methods
    
    def _normalize_voice_code(self, voiceover_code: str) -> str:
        """Validate and normalize a voiceover code to the canonical provider ID."""
        if voiceover_code is None:
            raise ValueError("voiceover_code cannot be None")

        if not isinstance(voiceover_code, str):
            raise ValueError("voiceover_code must be a string")

        raw_code = voiceover_code.strip()
        if not raw_code:
            raise ValueError("voiceover_code must be a non-empty string")

        voice_types: Dict[str, Any] = {}
        fetch_error: Optional[Exception] = None

        try:
            response = self.get_voice_types()
            if isinstance(response, dict):
                voice_types = response.get('voice_types', {}) or {}
        except Exception as exc:  # pragma: no cover - network failures
            fetch_error = exc

        if voice_types:
            normalized_lower = raw_code.lower()

            # Direct match on documented voice name keys
            if raw_code in voice_types:
                voice_entry = voice_types[raw_code]
                if isinstance(voice_entry, dict):
                    return voice_entry.get('id') or voice_entry.get('voice_id') or raw_code
                return raw_code

            # Case-insensitive match on voice names
            for voice_name, voice_entry in voice_types.items():
                if isinstance(voice_name, str) and voice_name.lower() == normalized_lower:
                    if isinstance(voice_entry, dict):
                        return voice_entry.get('id') or voice_entry.get('voice_id') or voice_name
                    return voice_name

            # Check aliases, IDs, and alternate codes within metadata
            for voice_name, voice_entry in voice_types.items():
                if not isinstance(voice_entry, dict):
                    continue

                candidates: List[str] = []

                for key in ('id', 'voice_id', 'code', 'voice_code', 'voiceId', 'voiceCode'):
                    value = voice_entry.get(key)
                    if isinstance(value, str) and value:
                        candidates.append(value)

                for key in ('aliases', 'codes', 'voice_aliases', 'voice_codes', 'legacy_codes'):
                    values = voice_entry.get(key)
                    if isinstance(values, (list, tuple, set)):
                        candidates.extend([str(item) for item in values if isinstance(item, str) and item])

                for candidate in candidates:
                    if candidate == raw_code or candidate.lower() == normalized_lower:
                        return voice_entry.get('id') or voice_entry.get('voice_id') or candidate

            # Provide helpful context when voices were fetched but no match found
            examples = [name for name in voice_types.keys() if isinstance(name, str)][:5]
            hint = (
                "Invalid voiceover_code '{code}'. Call get_voice_types() for the full listing"
                f". Example voices: {examples}"
            )
            raise ValueError(hint.format(code=raw_code))

        # If we could not fetch voice types, fall back to pattern validation
        pattern = r'^[a-z]{2}-[A-Z]{2}-(Neural|Standard|Wavenet|Polyglot)\d?-[A-Z]$'
        if re.match(pattern, raw_code):
            return raw_code

        if fetch_error is not None:
            raise ValueError(
                f"Unable to validate voiceover_code '{raw_code}': {fetch_error}"
            ) from fetch_error

        raise ValueError(
            f"Invalid voiceover_code '{raw_code}'. Call get_voice_types() to inspect available voices."
        )
    
    def _ensure_bool(self, value: Any, param_name: str) -> bool:
        """Convert various inputs to boolean and warn if needed"""
        if isinstance(value, bool):
            return value
            
        if isinstance(value, str):
            if value.lower() in ('true', 'yes', '1', 'y', 't'):
                return True
            elif value.lower() in ('false', 'no', '0', 'n', 'f'):
                return False
                
        if isinstance(value, int):
            return bool(value)
            
        # Default case
        print(f"Warning: {param_name} value '{value}' is not a valid boolean. Using default.")
        return True
    
    def _format_size(self, size_bytes: int) -> str:
        """Format bytes as human-readable size"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes/(1024*1024):.1f} MB"
        else:
            return f"{size_bytes/(1024*1024*1024):.1f} GB"
