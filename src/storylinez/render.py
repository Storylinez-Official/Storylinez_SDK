import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from .base_client import BaseClient

class RenderClient(BaseClient):
    """
    Client for interacting with Storylinez Render API.
    Provides methods for creating and managing video renders based on sequences.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the RenderClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.render_url = f"{self.base_url}/render"
    
    # Render Creation and Management
    
    def create_render(self, project_id: str, **kwargs) -> Dict:
        """
        Create a new render for a project. The project must have an existing sequence.
        
        Args:
            project_id: ID of the project to create the render for
            **kwargs: Optional render parameters including:
                target_width: Width of the output video (must be valid for orientation)
                target_height: Height of the output video (must be valid for orientation)
                bg_music_volume: Background music volume (0.0 to 1.0)
                video_audio_volume: Video audio track volume (0.0 to 1.0)
                voiceover_volume: Voiceover track volume (0.0 to 1.0)
                subtitle_enabled: Whether to show subtitles
                subtitle_font_size: Subtitle text size
                subtitle_color: Subtitle text color
                subtitle_bg_color: Subtitle background color
                subtitle_bg_opacity: Subtitle background opacity
                outro_duration: Duration of the outro in seconds
                company_name: Company name to display in outro
                company_subtext: Company tagline to display in outro
                main_text_color: Color for primary text
                sub_text_color: Color for secondary text
                call_to_action: CTA text
                call_to_action_subtext: CTA subtext
                enable_cta: Whether to show CTA
                cta_text_color: CTA text color
                cta_subtext_color: CTA subtext color
                cta_bg_color: CTA background color
                standardize_resolution_enabled: Whether to standardize resolution
                color_balance_fix: Apply color balance correction
                color_exposure_fix: Apply exposure correction
                color_contrast_fix: Apply contrast correction
                fps: Frames per second for render
                and many other render customization parameters...
            
        Returns:
            Dictionary with the created render details and job information
        """
        data = {"project_id": project_id}
        
        # Add any optional parameters
        for key, value in kwargs.items():
            data[key] = value
        
        return self._make_request("POST", f"{self.render_url}/create", json_data=data)
    
    def get_render(self, render_id: str = None, project_id: str = None,
                 include_results: bool = True, include_sequence: bool = False,
                 include_subtitles: bool = False, generate_download_link: bool = False,
                 generate_streamable_link: bool = False, 
                 generate_thumbnail_stream_link: bool = False) -> Dict:
        """
        Get details of a render by either render ID or project ID.
        
        Args:
            render_id: ID of the render to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the render for (either this or render_id must be provided)
            include_results: Whether to include job results
            include_sequence: Whether to include the full sequence data
            include_subtitles: Whether to include subtitles data
            generate_download_link: Whether to generate a temporary download link
            generate_streamable_link: Whether to generate a temporary streamable link
            generate_thumbnail_stream_link: Whether to generate a thumbnail streamable link
            
        Returns:
            Dictionary with render details
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")
            
        params = {
            "include_results": str(include_results).lower(),
            "include_sequence": str(include_sequence).lower(),
            "include_subtitles": str(include_subtitles).lower(),
            "generate_download_link": str(generate_download_link).lower(),
            "generate_streamable_link": str(generate_streamable_link).lower(),
            "generate_thumbnail_stream_link": str(generate_thumbnail_stream_link).lower()
        }
        
        if render_id:
            params["render_id"] = render_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.render_url}/get", params=params)
    
    def redo_render(self, render_id: str = None, project_id: str = None, **kwargs) -> Dict:
        """
        Regenerate a render with the same or updated settings.
        
        Args:
            render_id: ID of the render to regenerate (either this or project_id must be provided)
            project_id: ID of the project whose render to regenerate (either this or render_id must be provided)
            **kwargs: Optional parameters to override in the render (same parameters as create_render)
            
        Returns:
            Dictionary with the regeneration job details
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")
            
        data = {}
        
        if render_id:
            data["render_id"] = render_id
        if project_id:
            data["project_id"] = project_id
            
        # Add any override parameters
        for key, value in kwargs.items():
            if key not in ["render_id", "project_id"]:
                data[key] = value
            
        return self._make_request("POST", f"{self.render_url}/redo", json_data=data)
    
    def update_render_settings(self, render_id: str = None, project_id: str = None, **kwargs) -> Dict:
        """
        Update render settings without regenerating.
        
        Args:
            render_id: ID of the render to update (either this or project_id must be provided)
            project_id: ID of the project whose render to update (either this or render_id must be provided)
            **kwargs: Settings to update (same parameters as create_render)
            
        Returns:
            Dictionary with update confirmation
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")
            
        data = {}
        
        if render_id:
            data["render_id"] = render_id
        if project_id:
            data["project_id"] = project_id
            
        # Add settings to update
        for key, value in kwargs.items():
            if key not in ["render_id", "project_id"]:
                data[key] = value
            
        return self._make_request("PUT", f"{self.render_url}/update", json_data=data)
    
    def update_render(self, render_id: str = None, project_id: str = None, 
                    fields_to_update: List[str] = None) -> Dict:
        """
        Update a render with the latest sequence data.
        
        Args:
            render_id: ID of the render to update (either this or project_id must be provided)
            project_id: ID of the project whose render to update (either this or render_id must be provided)
            fields_to_update: Optional list of specific fields to update from the sequence
            
        Returns:
            Dictionary with update confirmation
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")
            
        data = {}
        
        if render_id:
            data["render_id"] = render_id
        if project_id:
            data["project_id"] = project_id
        if fields_to_update:
            data["fields_to_update"] = fields_to_update
            
        return self._make_request("PUT", f"{self.render_url}/selfupdate", json_data=data)
    
    # Render Output Management
    
    def get_render_status(self, render_id: str = None, project_id: str = None) -> Dict:
        """
        Get the current status of a render job.
        
        Args:
            render_id: ID of the render to check (either this or project_id must be provided)
            project_id: ID of the project whose render to check (either this or render_id must be provided)
            
        Returns:
            Dictionary with render status information
        """
        result = self.get_render(render_id, project_id, include_results=True, 
                               include_sequence=False, include_subtitles=False)
        
        # Extract status information for a cleaner response
        status = "unknown"
        job_result = result.get("job_result", {})
        
        if job_result:
            status = job_result.get("status", "UNKNOWN")
            
        return {
            "render_id": result.get("render_id"),
            "project_id": result.get("project_id"),
            "status": status,
            "created_at": result.get("created_at"),
            "updated_at": result.get("updated_at"),
            "is_stale": result.get("is_stale", False),
            "job_id": result.get("job_id")
        }
    
    def get_render_download_links(self, render_id: str = None, project_id: str = None) -> Dict:
        """
        Get download and streaming links for a completed render.
        
        Args:
            render_id: ID of the render (either this or project_id must be provided)
            project_id: ID of the project whose render to access (either this or render_id must be provided)
            
        Returns:
            Dictionary with download and streaming URLs
        """
        result = self.get_render(
            render_id, project_id, 
            include_results=True,
            generate_download_link=True, 
            generate_streamable_link=True, 
            generate_thumbnail_stream_link=True
        )
        
        # Check if render is complete
        job_result = result.get("job_result", {})
        if job_result.get("status") != "COMPLETED":
            raise Exception(f"Render is not yet complete. Current status: {job_result.get('status', 'UNKNOWN')}")
            
        # Extract and return just the links
        links = {
            "render_id": result.get("render_id"),
            "project_id": result.get("project_id"),
            "download_url": result.get("download_url"),
            "download_expires_in": result.get("download_expires_in"),
            "streamable_url": result.get("streamable_url"),
            "streamable_expires_in": result.get("streamable_expires_in"),
            "thumbnail_streamable_url": result.get("thumbnail_streamable_url"),
            "thumbnail_streamable_expires_in": result.get("thumbnail_streamable_expires_in"),
            "srt_download_url": result.get("srt_download_url"),
            "srt_download_expires_in": result.get("srt_download_expires_in")
        }
        
        return links
