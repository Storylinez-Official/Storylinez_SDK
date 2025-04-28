import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from .base_client import BaseClient

class ProjectClient(BaseClient):
    """
    Client for interacting with Storylinez Project API.
    Provides methods for managing projects, project folders, and project resources.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the ProjectClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.project_url = f"{self.base_url}/projects"
    
    # Project Folder Management
    
    def create_folder(self, name: str, description: str = "", org_id: str = None) -> Dict:
        """
        Create a new project folder.
        
        Args:
            name: Name of the folder
            description: Optional description of the folder
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with the created folder details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        data = {
            "name": name,
            "org_id": org_id,
            "description": description
        }
        
        return self._make_request("POST", f"{self.project_url}/folders/create", json_data=data)
        
    def get_all_folders(self, org_id: str = None) -> Dict:
        """
        Get all project folders for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with list of folders
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id
        }
        
        return self._make_request("GET", f"{self.project_url}/folders/get_all", params=params)
    
    def update_folder(self, folder_id: str, name: str = None, description: str = None) -> Dict:
        """
        Update a project folder's details.
        
        Args:
            folder_id: ID of the folder to update
            name: New name for the folder (optional)
            description: New description for the folder (optional)
            
        Returns:
            Dictionary with the updated folder details
        """
        if not folder_id:
            raise ValueError("folder_id is required")
        
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
            
        if not data:
            raise ValueError("At least one field to update (name or description) must be provided")
            
        params = {
            "folder_id": folder_id
        }
        
        return self._make_request("PUT", f"{self.project_url}/folders/update", params=params, json_data=data)
    
    def delete_folder(self, folder_id: str, move_projects: bool = False) -> Dict:
        """
        Delete a project folder.
        
        Args:
            folder_id: ID of the folder to delete
            move_projects: If True, moves any projects in the folder to root before deleting
            
        Returns:
            Dictionary with deletion results
        """
        if not folder_id:
            raise ValueError("folder_id is required")
            
        params = {
            "folder_id": folder_id,
            "move_projects": str(move_projects).lower()
        }
        
        return self._make_request("DELETE", f"{self.project_url}/folders/delete", params=params)
    
    def search_folders(self, query: str = "", search_fields: List[str] = None,
                      created_after: str = None, created_before: str = None,
                      updated_after: str = None, updated_before: str = None,
                      created_by: str = None, page: int = 1, limit: int = 10,
                      sort_by: str = "created_at", sort_order: str = "desc",
                      org_id: str = None) -> Dict:
        """
        Search for project folders with various filters.
        
        Args:
            query: Search text
            search_fields: Fields to search in (name, description)
            created_after: Filter folders created after this ISO date
            created_before: Filter folders created before this ISO date
            updated_after: Filter folders updated after this ISO date
            updated_before: Filter folders updated before this ISO date
            created_by: Filter folders created by this user ID
            page: Page number for pagination
            limit: Number of items per page
            sort_by: Field to sort by (name, created_at, updated_at)
            sort_order: Sort direction (asc or desc)
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        
        if query:
            params["q"] = query
            
        if search_fields:
            params["search_fields"] = ",".join(search_fields)
            
        if created_after:
            params["created_after"] = created_after
            
        if created_before:
            params["created_before"] = created_before
            
        if updated_after:
            params["updated_after"] = updated_after
            
        if updated_before:
            params["updated_before"] = updated_before
            
        if created_by:
            params["created_by"] = created_by
            
        return self._make_request("GET", f"{self.project_url}/search/folders", params=params)
    
    # Project Management
    
    def create_project(self, name: str, orientation: str, purpose: str = "",
                     target_audience: str = "", folder_id: str = None,
                     company_details_id: str = None, brand_id: str = None,
                     associated_files: List[str] = None, settings: Dict = None,
                     org_id: str = None) -> Dict:
        """
        Create a new project.
        
        Args:
            name: Project name
            orientation: Project orientation (landscape or portrait)
            purpose: Project purpose description
            target_audience: Target audience description
            folder_id: ID of the folder to place the project in
            company_details_id: Company details ID to use for the project
            brand_id: Brand ID to use for the project
            associated_files: List of file IDs to associate with the project
            settings: Dictionary of project settings
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with the created project details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Validate orientation
        if orientation not in ["landscape", "portrait"]:
            raise ValueError("orientation must be 'landscape' or 'portrait'")
            
        data = {
            "name": name,
            "org_id": org_id,
            "orientation": orientation,
            "purpose": purpose,
            "target_audience": target_audience
        }
        
        if folder_id:
            data["folder_id"] = folder_id
            
        if company_details_id:
            data["company_details_id"] = company_details_id
            
        if brand_id:
            data["brand_id"] = brand_id
            
        if associated_files:
            data["associated_files"] = associated_files
            
        if settings:
            data["settings"] = settings
            
        return self._make_request("POST", f"{self.project_url}/create", json_data=data)
    
    def get_all_projects(self, status: str = None, generate_thumbnail_links: bool = False,
                        page: int = 1, limit: int = 10, sort_by: str = "created_at",
                        sort_order: str = "desc", org_id: str = None) -> Dict:
        """
        Get all projects for an organization with pagination.
        
        Args:
            status: Filter projects by status (draft, ongoing, error, completed)
            generate_thumbnail_links: Whether to generate thumbnail URLs
            page: Page number for pagination
            limit: Number of items per page
            sort_by: Field to sort by (name, created_at, updated_at, status)
            sort_order: Sort direction (asc or desc)
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with projects list and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "generate_thumbnail_links": str(generate_thumbnail_links).lower()
        }
        
        if status:
            params["status"] = status
            
        return self._make_request("GET", f"{self.project_url}/get_all", params=params)
    
    def get_project(self, project_id: str, generate_thumbnail_links: bool = False) -> Dict:
        """
        Get details of a specific project.
        
        Args:
            project_id: ID of the project to retrieve
            generate_thumbnail_links: Whether to generate thumbnail URLs
            
        Returns:
            Dictionary with project details
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        params = {
            "project_id": project_id,
            "generate_thumbnail_links": str(generate_thumbnail_links).lower()
        }
        
        return self._make_request("GET", f"{self.project_url}/get_one", params=params)
    
    def update_project(self, project_id: str, name: str = None, purpose: str = None,
                      target_audience: str = None, company_details_id: str = None,
                      brand_id: str = None, settings: Dict = None) -> Dict:
        """
        Update a project's details.
        
        Args:
            project_id: ID of the project to update
            name: New name for the project
            purpose: New purpose description
            target_audience: New target audience description
            company_details_id: New company details ID
            brand_id: New brand ID
            settings: New project settings dictionary
            
        Returns:
            Dictionary with the updated project details
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        data = {}
        allowed_fields = ["name", "purpose", "target_audience", "company_details_id", "brand_id", "settings"]
        
        for field in allowed_fields:
            value = locals()[field]
            if value is not None:
                data[field] = value
                
        if not data:
            raise ValueError("At least one field to update must be provided")
            
        params = {
            "project_id": project_id
        }
        
        return self._make_request("PUT", f"{self.project_url}/update", params=params, json_data=data)
    
    def delete_project(self, project_id: str) -> Dict:
        """
        Delete a project and all associated resources.
        
        Args:
            project_id: ID of the project to delete
            
        Returns:
            Dictionary with deletion results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        params = {
            "project_id": project_id
        }
        
        return self._make_request("DELETE", f"{self.project_url}/delete", params=params)
    
    def duplicate_project(self, project_id: str, name: str = None) -> Dict:
        """
        Create a duplicate of an existing project.
        
        Args:
            project_id: ID of the project to duplicate
            name: Name for the duplicated project (defaults to original name + " (Copy)")
            
        Returns:
            Dictionary with the duplicated project details
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        data = {
            "project_id": project_id
        }
        
        if name:
            data["name"] = name
            
        return self._make_request("POST", f"{self.project_url}/duplicate", json_data=data)
    
    def move_project_to_folder(self, project_id: str, folder_id: str = None) -> Dict:
        """
        Move a project to a folder or to the root.
        
        Args:
            project_id: ID of the project to move
            folder_id: ID of the destination folder (None to move to root)
            
        Returns:
            Dictionary with the move operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        data = {
            "project_id": project_id,
            "folder_id": folder_id  # Can be None to move to root
        }
        
        return self._make_request("PUT", f"{self.project_url}/move_to_folder", json_data=data)
    
    def search_projects(self, query: str = "", search_fields: List[str] = None,
                       status: str = None, folder_id: str = None, orientation: str = None,
                       brand_id: str = None, company_details_id: str = None,
                       created_by: str = None, created_after: str = None,
                       created_before: str = None, updated_after: str = None,
                       updated_before: str = None, page: int = 1, limit: int = 10,
                       sort_by: str = "created_at", sort_order: str = "desc",
                       generate_thumbnail_links: bool = False, org_id: str = None) -> Dict:
        """
        Search for projects with various filters.
        
        Args:
            query: Search text
            search_fields: Fields to search in (name, purpose, target_audience)
            status: Filter projects by status
            folder_id: Filter projects by folder ID
            orientation: Filter projects by orientation
            brand_id: Filter projects by brand ID
            company_details_id: Filter projects by company details ID
            created_by: Filter projects created by this user ID
            created_after: Filter projects created after this ISO date
            created_before: Filter projects created before this ISO date
            updated_after: Filter projects updated after this ISO date
            updated_before: Filter projects updated before this ISO date
            page: Page number for pagination
            limit: Number of items per page
            sort_by: Field to sort by
            sort_order: Sort direction (asc or desc)
            generate_thumbnail_links: Whether to generate thumbnail URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "generate_thumbnail_links": str(generate_thumbnail_links).lower()
        }
        
        if query:
            params["q"] = query
            
        if search_fields:
            params["search_fields"] = ",".join(search_fields)
            
        if status:
            params["status"] = status
            
        if folder_id:
            if folder_id.lower() == "none":
                params["folder_id"] = "none"
            else:
                params["folder_id"] = folder_id
            
        if orientation:
            params["orientation"] = orientation
            
        if brand_id:
            params["brand_id"] = brand_id
            
        if company_details_id:
            params["company_details_id"] = company_details_id
            
        if created_by:
            params["created_by"] = created_by
            
        if created_after:
            params["created_after"] = created_after
            
        if created_before:
            params["created_before"] = created_before
            
        if updated_after:
            params["updated_after"] = updated_after
            
        if updated_before:
            params["updated_before"] = updated_before
            
        return self._make_request("GET", f"{self.project_url}/search/projects", params=params)
    
    def get_projects_by_folder(self, folder_id: str = None, page: int = 1, limit: int = 10,
                             sort_by: str = "created_at", sort_order: str = "desc",
                             generate_thumbnail_links: bool = False, org_id: str = None) -> Dict:
        """
        Get projects within a specific folder or root projects.
        
        Args:
            folder_id: ID of the folder to get projects from (None for root projects)
            page: Page number for pagination
            limit: Number of items per page
            sort_by: Field to sort by
            sort_order: Sort direction (asc or desc)
            generate_thumbnail_links: Whether to generate thumbnail URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with projects and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "generate_thumbnail_links": str(generate_thumbnail_links).lower()
        }
        
        if folder_id:
            params["folder_id"] = folder_id
            
        return self._make_request("GET", f"{self.project_url}/by_folder", params=params)
    
    def get_projects_by_status(self, status: str, folder_id: str = None, page: int = 1, 
                             limit: int = 10, sort_by: str = "created_at", 
                             sort_order: str = "desc", generate_thumbnail_links: bool = False,
                             org_id: str = None) -> Dict:
        """
        Get projects with a specific status.
        
        Args:
            status: Project status to filter by (draft, ongoing, error, completed)
            folder_id: Optional folder ID to further filter projects
            page: Page number for pagination
            limit: Number of items per page
            sort_by: Field to sort by
            sort_order: Sort direction (asc or desc)
            generate_thumbnail_links: Whether to generate thumbnail URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with projects and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        if status not in ['draft', 'ongoing', 'error', 'completed']:
            raise ValueError("status must be one of: 'draft', 'ongoing', 'error', 'completed'")
            
        params = {
            "org_id": org_id,
            "status": status,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "generate_thumbnail_links": str(generate_thumbnail_links).lower()
        }
        
        if folder_id:
            params["folder_id"] = folder_id
            
        return self._make_request("GET", f"{self.project_url}/by_status", params=params)
    
    # Project Files Management
    
    def add_associated_file(self, project_id: str, file_id: str) -> Dict:
        """
        Add a file to a project.
        
        Args:
            project_id: ID of the project
            file_id: ID of the file to add
            
        Returns:
            Dictionary with the operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not file_id:
            raise ValueError("file_id is required")
            
        data = {
            "file_id": file_id
        }
        
        params = {
            "project_id": project_id
        }
        
        return self._make_request("POST", f"{self.project_url}/files/add", params=params, json_data=data)
    
    def remove_associated_file(self, project_id: str, file_id: str) -> Dict:
        """
        Remove a file from a project.
        
        Args:
            project_id: ID of the project
            file_id: ID of the file to remove
            
        Returns:
            Dictionary with the operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not file_id:
            raise ValueError("file_id is required")
            
        params = {
            "project_id": project_id,
            "file_id": file_id
        }
        
        return self._make_request("DELETE", f"{self.project_url}/files/remove", params=params)
    
    def add_stock_file(self, project_id: str, stock_id: str, media_type: str) -> Dict:
        """
        Add a stock media file to a project.
        
        Args:
            project_id: ID of the project
            stock_id: ID of the stock media to add
            media_type: Type of media ('videos', 'audios', or 'images')
            
        Returns:
            Dictionary with the operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not stock_id:
            raise ValueError("stock_id is required")
            
        if media_type not in ['videos', 'audios', 'images']:
            raise ValueError("media_type must be one of: 'videos', 'audios', 'images'")
            
        data = {
            "stock_id": stock_id,
            "media_type": media_type
        }
        
        params = {
            "project_id": project_id
        }
        
        return self._make_request("POST", f"{self.project_url}/stock-files/add", params=params, json_data=data)
    
    def remove_stock_file(self, project_id: str, stock_id: str, media_type: str) -> Dict:
        """
        Remove a stock media file from a project.
        
        Args:
            project_id: ID of the project
            stock_id: ID of the stock media to remove
            media_type: Type of media ('videos', 'audios', or 'images')
            
        Returns:
            Dictionary with the operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not stock_id:
            raise ValueError("stock_id is required")
            
        if media_type not in ['videos', 'audios', 'images']:
            raise ValueError("media_type must be one of: 'videos', 'audios', 'images'")
            
        params = {
            "project_id": project_id,
            "stock_id": stock_id,
            "media_type": media_type
        }
        
        return self._make_request("DELETE", f"{self.project_url}/stock-files/remove", params=params)
    
    def get_project_files(self, project_id: str, include_details: bool = False) -> Dict:
        """
        Get all files associated with a project.
        
        Args:
            project_id: ID of the project
            include_details: Whether to include detailed file information
            
        Returns:
            Dictionary with associated files, stock files, and voiceover information
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        params = {
            "project_id": project_id,
            "include_details": str(include_details).lower()
        }
        
        return self._make_request("GET", f"{self.project_url}/files/get_all", params=params)
    
    # Project Voiceover Management
    
    def add_voiceover(self, project_id: str, file_id: str, voice_name: str = "Custom Voiceover") -> Dict:
        """
        Add a voiceover file to a project.
        
        Args:
            project_id: ID of the project
            file_id: ID of the audio file to use as voiceover
            voice_name: Name/description of the voice
            
        Returns:
            Dictionary with the operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        if not file_id:
            raise ValueError("file_id is required")
            
        data = {
            "file_id": file_id,
            "voice_name": voice_name
        }
        
        params = {
            "project_id": project_id
        }
        
        return self._make_request("POST", f"{self.project_url}/voiceovers/add", params=params, json_data=data)
    
    def remove_voiceover(self, project_id: str) -> Dict:
        """
        Remove the voiceover from a project.
        
        Args:
            project_id: ID of the project
            
        Returns:
            Dictionary with the operation results
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        params = {
            "project_id": project_id
        }
        
        return self._make_request("DELETE", f"{self.project_url}/voiceovers/remove", params=params)
    
    def get_voiceover(self, project_id: str, include_details: bool = False) -> Dict:
        """
        Get the voiceover information for a project.
        
        Args:
            project_id: ID of the project
            include_details: Whether to include detailed file information
            
        Returns:
            Dictionary with voiceover information
        """
        if not project_id:
            raise ValueError("project_id is required")
            
        params = {
            "project_id": project_id,
            "include_details": str(include_details).lower()
        }
        
        return self._make_request("GET", f"{self.project_url}/voiceovers/get", params=params)
