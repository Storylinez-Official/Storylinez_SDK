import os
import json
import requests
from typing import Dict, List, Optional, Union, Any
from .base_client import BaseClient

class CompanyDetailsClient(BaseClient):
    """
    Client for interacting with Storylinez Company Details API.
    Provides methods for managing company details/profiles.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the CompanyDetailsClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.company_url = f"{self.base_url}/company"
    
    def create(self, 
               company_name: str, 
               company_type: str = "", 
               tag_line: str = "", 
               vision: str = "",
               products: str = "", 
               description: str = "",
               cta_text: str = "", 
               cta_subtext: str = "",
               link: str = "", 
               is_default: bool = False,
               others: Dict = None,
               org_id: str = None) -> Dict:
        """
        Create a new company details profile.
        
        Args:
            company_name: Name of the company (required)
            company_type: Type of company (e.g., "Software", "Healthcare")
            tag_line: Company's tag line or slogan
            vision: Company's vision statement
            products: Description of company's products or services
            description: Detailed company description
            cta_text: Call to action text
            cta_subtext: Call to action subtext
            link: Company website or relevant link
            is_default: Whether to set as the default company details
            others: Additional custom fields
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with the created company details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        data = {
            "org_id": org_id,
            "company_name": company_name,
            "company_type": company_type,
            "tag_line": tag_line,
            "vision": vision,
            "products": products,
            "description": description,
            "cta_text": cta_text,
            "cta_subtext": cta_subtext,
            "link": link,
            "is_default": is_default,
        }
        
        if others:
            data["others"] = others
        
        return self._make_request("POST", f"{self.company_url}/create", json_data=data)
    
    def get_all(self, page: int = 1, limit: int = 10, sort_by: str = "created_at", 
               order: str = "desc", org_id: str = None) -> Dict:
        """
        Get all company details profiles for an organization with pagination.
        
        Args:
            page: Page number to retrieve
            limit: Number of items per page
            sort_by: Field to sort by (created_at, company_name, etc.)
            order: Sort order (asc or desc)
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with company details list and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "order": order
        }
        
        return self._make_request("GET", f"{self.company_url}/get_all", params=params)
    
    def get_one(self, company_details_id: str = None, org_id: str = None) -> Dict:
        """
        Get a specific company details profile or the default for an organization.
        
        Args:
            company_details_id: ID of the company details (if None, gets default)
            org_id: Organization ID (uses default if not provided)
        
        Returns:
            Dictionary with the company details
        """
        org_id = org_id or self.default_org_id
        if not org_id and not company_details_id:
            raise ValueError("Either company_details_id or org_id is required.")
            
        params = {}
        if company_details_id:
            params["company_details_id"] = company_details_id
        if org_id:
            params["org_id"] = org_id
        
        return self._make_request("GET", f"{self.company_url}/get_one", params=params)
    
    def update(self, company_details_id: str, 
              company_name: str = None,
              company_type: str = None, 
              tag_line: str = None,
              vision: str = None,
              products: str = None,
              description: str = None,
              cta_text: str = None,
              cta_subtext: str = None,
              link: str = None,
              is_default: bool = None,
              others: Dict = None) -> Dict:
        """
        Update a company details profile.
        
        Args:
            company_details_id: ID of the company details to update
            company_name: Name of the company
            company_type: Type of company
            tag_line: Company's tag line or slogan
            vision: Company's vision statement
            products: Description of company's products or services
            description: Detailed company description
            cta_text: Call to action text
            cta_subtext: Call to action subtext
            link: Company website or relevant link
            is_default: Whether to set as the default company details
            others: Additional custom fields
            
        Returns:
            Dictionary with the updated company details
        """
        if not company_details_id:
            raise ValueError("company_details_id is required.")
            
        data = {}
        # Only include non-None parameters in the update
        if company_name is not None:
            data["company_name"] = company_name
        if company_type is not None:
            data["company_type"] = company_type
        if tag_line is not None:
            data["tag_line"] = tag_line
        if vision is not None:
            data["vision"] = vision
        if products is not None:
            data["products"] = products
        if description is not None:
            data["description"] = description
        if cta_text is not None:
            data["cta_text"] = cta_text
        if cta_subtext is not None:
            data["cta_subtext"] = cta_subtext
        if link is not None:
            data["link"] = link
        if is_default is not None:
            data["is_default"] = is_default
        if others is not None:
            data["others"] = others
            
        if not data:
            raise ValueError("At least one field to update must be provided.")
            
        params = {"company_details_id": company_details_id}
        return self._make_request("PUT", f"{self.company_url}/update", params=params, json_data=data)
    
    def delete(self, company_details_id: str) -> Dict:
        """
        Delete a company details profile.
        
        Args:
            company_details_id: ID of the company details to delete
            
        Returns:
            Dictionary with deletion confirmation
        """
        if not company_details_id:
            raise ValueError("company_details_id is required.")
            
        params = {"company_details_id": company_details_id}
        return self._make_request("DELETE", f"{self.company_url}/delete", params=params)
    
    def set_default(self, company_details_id: str) -> Dict:
        """
        Set a company details profile as the default.
        
        Args:
            company_details_id: ID of the company details to set as default
            
        Returns:
            Dictionary with confirmation message
        """
        if not company_details_id:
            raise ValueError("company_details_id is required.")
            
        params = {"company_details_id": company_details_id}
        return self._make_request("PUT", f"{self.company_url}/set_default", params=params)
    
    def duplicate(self, company_details_id: str, company_name: str = None, org_id: str = None) -> Dict:
        """
        Duplicate a company details profile.
        
        Args:
            company_details_id: ID of the company details to duplicate
            company_name: New name for the duplicated company details (optional)
            org_id: Organization ID for the duplicated company details
            
        Returns:
            Dictionary with the duplicated company details
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        if not company_details_id:
            raise ValueError("company_details_id is required.")
            
        data = {
            "company_details_id": company_details_id,
            "org_id": org_id
        }
        
        if company_name:
            data["company_name"] = company_name
        
        return self._make_request("POST", f"{self.company_url}/duplicate", json_data=data)
    
    def search(self, query: str, field: str = "company_name", page: int = 1, 
              limit: int = 10, sort_by: str = "created_at", order: str = "desc", 
              org_id: str = None) -> Dict:
        """
        Search for company details profiles.
        
        Args:
            query: Search term
            field: Field to search in (company_name, tag_line, etc.)
            page: Page number to retrieve
            limit: Number of items per page
            sort_by: Field to sort by
            order: Sort order (asc or desc)
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with search results and pagination info
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "q": query,
            "field": field,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "order": order
        }
        
        return self._make_request("GET", f"{self.company_url}/search", params=params)
