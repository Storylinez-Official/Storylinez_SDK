import os
import json
import requests
from typing import Dict, List, Optional, Union, Any, Tuple
from .base_client import BaseClient

class BrandClient(BaseClient):
    """
    Client for interacting with Storylinez Brand API.
    Provides methods for managing brand presets and styling.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the BrandClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.brand_url = f"{self.base_url}/brand"

    def get_logo_upload_url(self, filename: str, org_id: str = None) -> Dict:
        """
        Generate a secure upload link for a brand logo.
        
        Args:
            filename: Name of the logo file to upload
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with upload details (upload_link, key, upload_id, expires_in)
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "filename": filename
        }
        
        return self._make_request("GET", "logo-upload-url", params=params)
    
    def upload_logo(self, file_path: str, org_id: str = None, is_default: bool = False, 
                    is_public: bool = False, name: str = None, **kwargs) -> Dict:
        """
        Upload a logo file for brands.
        This is a convenience method that handles the full process: generating upload link, uploading, and creating brand.
        
        Args:
            file_path: Path to the logo file on local disk
            org_id: Organization ID (uses default if not provided)
            is_default: Whether this brand should be the default 
            is_public: Whether this brand should be publicly accessible
            name: Brand name (defaults to filename without extension if not provided)
            **kwargs: Additional brand styling parameters
        
        Returns:
            Dictionary with created brand details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        # Get file information
        filename = os.path.basename(file_path)
        
        # Generate upload link
        upload_info = self.get_logo_upload_url(filename=filename, org_id=org_id)
        
        # Upload the file to the pre-signed URL
        upload_link = upload_info.get("upload_link")
        logo_key = upload_info.get("key")
        
        # Use requests to upload the file
        with open(file_path, 'rb') as file_data:
            upload_response = requests.put(upload_link, data=file_data)
            
            if upload_response.status_code >= 400:
                raise Exception(f"Logo upload failed with status {upload_response.status_code}")
        
        # Use filename without extension as default name if not provided
        if not name:
            name = os.path.splitext(filename)[0]
            
        # Create brand with the uploaded logo
        return self.create(
            name=name,
            logo_key=logo_key,
            is_default=is_default,
            is_public=is_public,
            org_id=org_id,
            **kwargs
        )
        
    def create(self, name: str, logo_key: str = None, is_default: bool = False, 
              is_public: bool = False, org_id: str = None, **kwargs) -> Dict:
        """
        Create a new brand preset with styling configurations.
        
        Args:
            name: Brand name
            logo_key: S3 key of the uploaded logo (optional)
            is_default: Whether this brand should be the default
            is_public: Whether this brand should be publicly accessible
            org_id: Organization ID (uses default if not provided)
            **kwargs: Additional brand styling parameters:
                - outro_bg_color: RGB tuple/list for outro background color
                - outro_logo_size: Size tuple/list for outro logo (width, height)
                - company_font: Font for company name
                - company_font_size: Font size for company name
                - many other styling parameters - see API documentation for full list
        
        Returns:
            Dictionary with created brand details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        data = {
            "org_id": org_id,
            "name": name,
            "logo_key": logo_key,
            "is_default": is_default,
            "is_public": is_public
        }
        
        # Add any additional styling parameters
        data.update(kwargs)
        
        return self._make_request("POST", "create", json_data=data)
    
    def get_all(self, page: int = 1, limit: int = 10, 
               include_urls: bool = True, org_id: str = None) -> Dict:
        """
        Get all brand presets for an organization with pagination.
        
        Args:
            page: Page number to retrieve
            limit: Number of items per page
            include_urls: Whether to include pre-signed URLs for logos
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with brand list and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "include_urls": str(include_urls).lower()
        }
        
        return self._make_request("GET", "get_all", params=params)
    
    def get(self, brand_id: str = None, org_id: str = None) -> Dict:
        """
        Get a specific brand preset or the default for an organization.
        
        Args:
            brand_id: ID of the brand (if None, gets default)
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with the brand details including styling
        """
        org_id = org_id or self.default_org_id
        if not org_id and not brand_id:
            raise ValueError("Either brand_id or org_id is required.")
            
        params = {}
        if brand_id:
            params["brand_id"] = brand_id
        if org_id:
            params["org_id"] = org_id
        
        return self._make_request("GET", "get", params=params)
    
    def get_default(self, org_id: str = None) -> Dict:
        """
        Get the default brand preset for an organization using the dedicated endpoint.
        
        Args:
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with the default brand details including styling
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {"org_id": org_id}
        return self._make_request("GET", "get_default", params=params)
    
    def update(self, brand_id: str, **kwargs) -> Dict:
        """
        Update a brand preset's properties.
        
        Args:
            brand_id: ID of the brand to update
            **kwargs: Brand properties to update:
                - name: Brand name
                - is_default: Whether this brand should be default
                - is_public: Whether this brand is public
                - plus various styling parameters - see API documentation
            
        Returns:
            Dictionary with the updated brand details
        """
        if not brand_id:
            raise ValueError("brand_id is required.")
            
        params = {"brand_id": brand_id}
        return self._make_request("PUT", "update", params=params, json_data=kwargs)
    
    def delete(self, brand_id: str) -> Dict:
        """
        Delete a brand preset.
        
        Args:
            brand_id: ID of the brand to delete
            
        Returns:
            Dictionary with deletion confirmation
        """
        if not brand_id:
            raise ValueError("brand_id is required.")
            
        params = {"brand_id": brand_id}
        return self._make_request("DELETE", "delete", params=params)
    
    def set_default(self, brand_id: str) -> Dict:
        """
        Set a brand preset as the default.
        
        Args:
            brand_id: ID of the brand to set as default
            
        Returns:
            Dictionary with confirmation message
        """
        if not brand_id:
            raise ValueError("brand_id is required.")
            
        params = {"brand_id": brand_id}
        return self._make_request("PUT", "set_default", params=params)
    
    def add_logo(self, brand_id: str, logo_key: str = None, upload_id: str = None) -> Dict:
        """
        Add or update a logo for a brand.
        
        Args:
            brand_id: ID of the brand to update
            logo_key: S3 key of the uploaded logo
            upload_id: Upload ID from a logo upload process
            
        Returns:
            Dictionary with the updated brand details including logo URL
        """
        if not brand_id:
            raise ValueError("brand_id is required.")
        if not logo_key and not upload_id:
            raise ValueError("Either logo_key or upload_id is required.")
            
        data = {"file_id": brand_id}
        if logo_key:
            data["logo_key"] = logo_key
        if upload_id:
            data["upload_id"] = upload_id
        
        params = {"brand_id": brand_id}
        return self._make_request("PUT", "add_logo", params=params, json_data=data)
    
    def duplicate(self, brand_id: str, name: str = None, org_id: str = None) -> Dict:
        """
        Duplicate a brand preset.
        
        Args:
            brand_id: ID of the brand to duplicate
            name: Name for the duplicated brand (optional)
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with the duplicated brand
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        if not brand_id:
            raise ValueError("brand_id is required.")
            
        data = {
            "brand_id": brand_id,
            "org_id": org_id
        }
        
        if name:
            data["name"] = name
        
        return self._make_request("POST", "duplicate", json_data=data)
    
    def get_fonts(self) -> Dict:
        """
        Get a list of available fonts for brand styling.
        
        Returns:
            Dictionary with available fonts
        """
        return self._make_request("GET", f"{self.brand_url}/fonts")
    
    def get_public_brands(self, exclude_org_id: str = None, page: int = 1, 
                      limit: int = 20, include_logos: bool = False) -> Dict:
        """
        Get publicly available brand presets.
        
        Args:
            exclude_org_id: Organization ID to exclude from results
            page: Page number to retrieve
            limit: Number of items per page
            include_logos: Whether to include logo URLs
            
        Returns:
            Dictionary with public brands and pagination info
        """
        params = {
            "page": page,
            "limit": limit,
            "include_logos": str(include_logos).lower()
        }
        
        if exclude_org_id:
            params["exclude_org_id"] = exclude_org_id
        
        return self._make_request("GET", f"{self.brand_url}/public", params=params)
    
    def search(self, query: str = "", include_public: bool = True, 
              page: int = 1, limit: int = 20,
              include_logos: bool = False, org_id: str = None) -> Dict:
        """
        Search for brand presets.
        
        Args:
            query: Search term
            include_public: Whether to include public brands
            page: Page number to retrieve
            limit: Number of items per page
            include_logos: Whether to include logo URLs
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        params = {
            "q": query,
            "include_public": str(include_public).lower(),
            "page": page,
            "limit": limit,
            "include_logos": str(include_logos).lower()
        }
        
        if org_id:
            params["org_id"] = org_id
        
        return self._make_request("GET", f"{self.brand_url}/search", params=params)
