import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urljoin
from .base_client import BaseClient

class StorageClient(BaseClient):
    """
    Client for interacting with Storylinez Storage API.
    Provides methods for managing files, folders, and storage resources.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the StorageClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.storage_url = f"{self.base_url}/storage"
    
    # File Upload Methods
    
    def generate_upload_link(self, filename: str, file_size: int = 0, 
                           folder_path: str = "/", org_id: str = None) -> Dict:
        """
        Generate a secure upload link for a file.
        
        Args:
            filename: Name of the file to upload
            file_size: Size of the file in bytes (optional, for quota check)
            folder_path: Target folder path (defaults to root)
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with upload details including:
            - upload_link: URL to upload the file to
            - key: S3 key for the file
            - upload_id: ID to reference this upload
            - expires_in: Expiration time in seconds
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "filename": filename,
            "file_size": file_size,
            "folder_path": folder_path
        }
        
        return self._make_request("GET", f"{self.storage_url}/upload/create_link", params=params)
    
    def upload_file(self, file_path: str, folder_path: str = "/", 
                    context: str = "", tags: List[str] = None,
                    analyze_audio: bool = True,
                    auto_company_details: bool = True,
                    company_details_id: str = "",
                    org_id: str = None,
                    **kwargs) -> Dict:
        """
        Upload a file to Storylinez storage.
        This is a convenience method that handles both the link generation and upload.
        
        Args:
            file_path: Path to the file on local disk
            folder_path: Target folder path (defaults to root)
            context: Context for AI processing
            tags: Tags for categorization
            analyze_audio: Whether to analyze audio in media files
            auto_company_details: Whether to use company details for analysis
            company_details_id: ID of company details to use
            org_id: Organization ID (uses default if not provided)
            **kwargs: Additional analysis parameters:
                - deepthink: Enable deep analysis
                - overdrive: Use more computational resources
                - web_search: Enable web search for analysis
                - eco: Use eco-friendly processing
                - temperature: AI temperature (0.0-1.0)
        
        Returns:
            Dictionary with file details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Get file information
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        
        # Generate upload link
        upload_info = self.generate_upload_link(
            filename=filename,
            file_size=file_size,
            folder_path=folder_path,
            org_id=org_id
        )
        
        # Upload the file to the pre-signed URL
        upload_link = upload_info.get("upload_link")
        upload_id = upload_info.get("upload_id")
        
        # Use requests to upload the file
        with open(file_path, 'rb') as file_data:
            upload_response = requests.put(upload_link, data=file_data)
            
            if upload_response.status_code >= 400:
                raise Exception(f"File upload failed with status {upload_response.status_code}")
        
        # Prepare completion data
        completion_data = {
            "org_id": org_id,
            "upload_id": upload_id,
            "filename": filename,
            "folder_path": folder_path,
            "context": context,
            "tags": tags or [],
            "analyze_audio": analyze_audio,
            "auto_company_details": auto_company_details,
            "company_details_id": company_details_id,
        }
        
        # Add optional analysis parameters if provided
        for key in ["deepthink", "overdrive", "web_search", "eco", "temperature"]:
            if key in kwargs:
                completion_data[key] = kwargs[key]
        
        # Mark upload as complete and start processing
        return self._make_request("POST", f"{self.storage_url}/upload/complete", json_data=completion_data)
    
    def mark_upload_complete(self, upload_id: str, org_id: str = None, **kwargs) -> Dict:
        """
        Mark an upload as complete after uploading to the pre-signed URL.
        
        Args:
            upload_id: The upload ID from generate_upload_link
            org_id: Organization ID (uses default if not provided)
            **kwargs: Additional parameters (filename, folder_path, context, tags, etc.)
        
        Returns:
            Dictionary with file details and job_id
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        data = {
            "org_id": org_id,
            "upload_id": upload_id,
            **kwargs
        }
        
        return self._make_request("POST", f"{self.storage_url}/upload/complete", json_data=data)
    
    # Folder Methods

    def get_folder_contents(self, path: str = "/", recursive: bool = False, 
                          detailed: bool = False, generate_thumbnail: bool = True,
                          generate_streamable: bool = False,
                          generate_download: bool = False,
                          org_id: str = None) -> Dict:
        """
        Get the contents of a folder.
        
        Args:
            path: Folder path
            recursive: If True, include files from subfolders
            detailed: If True, include full analysis data
            generate_thumbnail: If True, generate thumbnail URLs
            generate_streamable: If True, generate streaming URLs
            generate_download: If True, generate download URLs
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with folders and files lists
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "path": path,
            "recursive": str(recursive).lower(),
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        return self._make_request("GET", f"{self.storage_url}/folder/contents", params=params)
    
    def create_folder(self, folder_name: str, parent_path: str = "/", 
                    org_id: str = None) -> Dict:
        """
        Create a new folder.
        
        Args:
            folder_name: Name of the folder to create
            parent_path: Path where the folder should be created
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with folder details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        data = {
            "org_id": org_id,
            "folder_name": folder_name,
            "parent_path": parent_path
        }
        
        return self._make_request("POST", f"{self.storage_url}/folder/create", json_data=data)
    
    def delete_folder(self, folder_id: str, delete_contents: bool = False) -> Dict:
        """
        Delete a folder.
        
        Args:
            folder_id: ID of the folder to delete
            delete_contents: If True, delete all contents recursively
        
        Returns:
            Dictionary with deletion results
        """
        params = {
            "folder_id": folder_id,
            "delete_contents": str(delete_contents).lower()
        }
        
        return self._make_request("DELETE", f"{self.storage_url}/folder/delete", params=params)
    
    def rename_folder(self, folder_id: str, new_name: str) -> Dict:
        """
        Rename a folder.
        
        Args:
            folder_id: ID of the folder to rename
            new_name: New name for the folder
        
        Returns:
            Dictionary with the updated folder details
        """
        data = {
            "folder_id": folder_id,
            "new_name": new_name
        }
        
        return self._make_request("PUT", f"{self.storage_url}/folder/rename", json_data=data)
    
    def get_folder_tree(self, path: str = "/", org_id: str = None) -> Dict:
        """
        Get a hierarchical tree of folders and files.
        
        Args:
            path: Root path for the tree
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with the tree structure
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "path": path
        }
        
        return self._make_request("GET", f"{self.storage_url}/tree", params=params)
    
    def list_folders(self, path: str = "/", recursive: bool = False, org_id: str = None) -> Dict:
        """
        List folders under a specific path.
        
        Args:
            path: Parent folder path
            recursive: If True, include all descendant folders
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with folders list
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "path": path,
            "recursive": str(recursive).lower()
        }
        
        return self._make_request("GET", f"{self.storage_url}/folder/list", params=params)
    
    def search_files_by_name(self, query: str, path: str = "/", 
                          recursive: bool = False, detailed: bool = True,
                          generate_thumbnail: bool = True,
                          org_id: str = None) -> Dict:
        """
        Search for files by filename.
        
        Args:
            query: Text to search for in filenames
            path: Folder path to search within
            recursive: If True, search in subfolders
            detailed: If True, include full analysis data
            generate_thumbnail: If True, generate thumbnail URLs
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with matching files
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "path": path,
            "query": query,
            "recursive": str(recursive).lower(),
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
        }
        
        return self._make_request("GET", f"{self.storage_url}/folder/search-by-name", params=params)
    
    def vector_search(self, queries: List[str], path: str = None, 
                    detailed: bool = True, generate_thumbnail: bool = True,
                    num_results: int = 10, similarity_threshold: float = 0.5,
                    file_types: str = "all",
                    org_id: str = None) -> Dict:
        """
        Search files semantically using vector embeddings.
        
        Args:
            queries: List of natural language queries
            path: Folder path to search within (None or empty to search all folders)
            detailed: If True, include full analysis data
            generate_thumbnail: If True, generate thumbnail URLs
            num_results: Maximum results per query
            similarity_threshold: Minimum similarity score (0.0-1.0)
            file_types: Comma-separated list of types to search ("all", "video", "audio", "image")
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with semantically matching files
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "num_results": num_results,
            "similarity_threshold": similarity_threshold,
            "file_types": file_types
        }
        
        # Only add path if explicitly provided (to search all folders if None/empty)
        if path:
            params["path"] = path
            
        data = {
            "queries": queries
        }
        
        return self._make_request("POST", f"{self.storage_url}/folder/vector-search", params=params, json_data=data)
    
    # File Methods
    
    def get_file_analysis(self, file_id: str, detailed: bool = True,
                        generate_thumbnail: bool = True,
                        generate_streamable: bool = True,
                        generate_download: bool = True) -> Dict:
        """
        Get detailed information about a file including analysis results.
        
        Args:
            file_id: File ID
            detailed: If True, include full analysis data
            generate_thumbnail: If True, generate thumbnail URL
            generate_streamable: If True, generate streaming URL
            generate_download: If True, generate download URL
        
        Returns:
            Dictionary with file details and analysis
        """
        params = {
            "file_id": file_id,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        return self._make_request("GET", f"{self.storage_url}/file/analysis", params=params)
    
    def delete_file(self, file_id: str) -> Dict:
        """
        Delete a file.
        
        Args:
            file_id: ID of the file to delete
        
        Returns:
            Dictionary with deletion results
        """
        params = {
            "file_id": file_id
        }
        
        return self._make_request("DELETE", f"{self.storage_url}/file/delete", params=params)
    
    def rename_file(self, file_id: str, new_name: str) -> Dict:
        """
        Rename a file.
        
        Args:
            file_id: ID of the file to rename
            new_name: New name for the file
        
        Returns:
            Dictionary with the updated file details
        """
        data = {
            "file_id": file_id,
            "new_name": new_name
        }
        
        return self._make_request("PUT", f"{self.storage_url}/file/rename", json_data=data)
    
    def move_file(self, file_id: str, target_folder_path: str) -> Dict:
        """
        Move a file to a different folder.
        
        Args:
            file_id: ID of the file to move
            target_folder_path: Path of the target folder
        
        Returns:
            Dictionary with the updated file details
        """
        data = {
            "file_id": file_id,
            "target_folder_path": target_folder_path
        }
        
        return self._make_request("PUT", f"{self.storage_url}/file/move", json_data=data)
    
    def get_download_link(self, file_id: str) -> Dict:
        """
        Get a download link for a file (prioritizes processed version if available).
        
        Args:
            file_id: ID of the file
        
        Returns:
            Dictionary with download URL and expiration
        """
        params = {
            "file_id": file_id
        }
        
        return self._make_request("GET", f"{self.storage_url}/file/download", params=params)
    
    def get_original_download_link(self, file_id: str) -> Dict:
        """
        Get a download link specifically for the original unprocessed file.
        
        Args:
            file_id: ID of the file
        
        Returns:
            Dictionary with download URL and expiration
        """
        params = {
            "file_id": file_id
        }
        
        return self._make_request("GET", f"{self.storage_url}/file/download/original", params=params)
    
    def reprocess_file(self, file_id: str, **analysis_params) -> Dict:
        """
        Reprocess a file with new analysis parameters.
        
        Args:
            file_id: ID of the file to reprocess
            **analysis_params: Analysis parameters to update (context, tags, deepthink, etc.)
        
        Returns:
            Dictionary with reprocessing details and new job_id
        """
        return self._make_request("POST", f"{self.storage_url}/file/reprocess?file_id={file_id}", json_data=analysis_params)
    
    def get_files_by_ids(self, file_ids: List[str], 
                       detailed: bool = False, generate_thumbnail: bool = True,
                       org_id: str = None) -> Dict:
        """
        Get details for multiple files by their IDs.
        
        Args:
            file_ids: List of file IDs to retrieve
            detailed: If True, include full analysis data
            generate_thumbnail: If True, generate thumbnail URLs
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with file details for found files
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "detailed": str(detailed).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
        }
        
        data = {
            "file_ids": file_ids
        }
        
        return self._make_request("POST", f"{self.storage_url}/files/get_by_ids", params=params, json_data=data)
    
    def get_storage_usage(self, org_id: str = None) -> Dict:
        """
        Get storage usage and limits for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with storage usage statistics
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id
        }
        
        return self._make_request("GET", f"{self.storage_url}/storage/usage", params=params)
