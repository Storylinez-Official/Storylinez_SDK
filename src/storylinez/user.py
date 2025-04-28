import json
import requests
from typing import Dict, Optional, Any
from .base_client import BaseClient

class UserClient(BaseClient):
    """
    Client for interacting with Storylinez User API.
    Provides methods for accessing user profiles, storage information, and subscription details.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinez.com", default_org_id: str = None):
        """
        Initialize the UserClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.user_url = f"{self.base_url}/user"
    
    # User Profile Methods
    
    def get_current_user(self) -> Dict:
        """
        Get information about the currently authenticated user.
        
        Returns:
            Dictionary with current user profile information including:
            - id: User ID
            - username: Username
            - first_name: First name
            - last_name: Last name
            - image_url: Profile image URL
            - email_addresses: List of email addresses associated with the account
            - phone_numbers: List of phone numbers associated with the account
            - public_metadata: Public metadata associated with the user
            - created_at: Account creation timestamp
            - updated_at: Last update timestamp
            - last_sign_in_at: Last sign-in timestamp
            - profile_image_url: Profile image URL
        """
        return self._make_request("GET", f"{self.user_url}/me")
    
    def get_user(self, user_id: str) -> Dict:
        """
        Get information about a specific user.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            Dictionary with public user profile information including:
            - id: User ID
            - username: Username (if set)
            - first_name: First name
            - last_name: Last name
            - image_url: Profile image URL
            - public_metadata: Public metadata
        """
        return self._make_request("GET", f"{self.user_url}/user/{user_id}")
    
    # Storage Methods
    
    def get_user_storage(self, org_id: str = None) -> Dict:
        """
        Get storage usage information for a user within an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with storage used by the user within the specified organization
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {"org_id": org_id}
        return self._make_request("GET", f"{self.user_url}/storage", params=params)
    
    def get_org_storage(self, org_id: str = None, include_breakdown: bool = False) -> Dict:
        """
        Get storage usage information for an entire organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            include_breakdown: If True, includes a user-by-user breakdown of storage usage
            
        Returns:
            Dictionary with total storage used by the organization and optional user breakdown
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {
            "org_id": org_id,
            "include_breakdown": str(include_breakdown).lower()
        }
        return self._make_request("GET", f"{self.user_url}/org/storage", params=params)
    
    # Subscription Methods
    
    def get_subscription(self, org_id: str = None) -> Dict:
        """
        Get detailed subscription information for an organization.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with subscription details including:
            - subscription_id: ID of the subscription
            - tier: Subscription tier level (numeric)
            - plan_name: Name of the subscription plan
            - period: Information about the current billing period
            - projects: Project limits and usage information
            - storage: Storage limits and usage information
            - content_processing: Content processing limits and usage information
            - reset_schedules: When various limits reset
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {"org_id": org_id}
        return self._make_request("GET", f"{self.user_url}/subscription", params=params)
    
    def get_project_usage(self, org_id: str = None) -> Dict:
        """
        Get project usage information and limits.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with project usage information including:
            - monthly_limit: Monthly project limit
            - monthly_used: Projects used in current billing period
            - monthly_remaining: Projects remaining in current billing period
            - daily_limit: Daily project limit
            - daily_used: Projects used today
            - daily_remaining: Projects remaining today
            - tier: Subscription tier level
            - plan_name: Name of the subscription plan
            - period_start: Beginning of current billing period
            - period_end: End of current billing period
            - reset_schedules: When various limits reset
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {"org_id": org_id}
        return self._make_request("GET", f"{self.user_url}/projects/usage", params=params)
    
    def get_extra_projects(self, org_id: str = None) -> Dict:
        """
        Get extra projects information and costs.
        
        Args:
            org_id: Organization ID (uses default if not provided)
            
        Returns:
            Dictionary with extra projects information including:
            - extra_projects: Number of extra projects used
            - extra_projects_cost: Cost of extra projects
            - monthly_limit: Monthly project limit
            - monthly_used: Projects used in current billing period
            - can_create_extra_projects: Whether the organization can create extra projects
            - billing_period: Current billing period start and end dates
        """
        org_id = org_id or self.default_org_id
        if not org_id:
            raise ValueError("Organization ID is required. Either provide org_id parameter or set a default_org_id when initializing the client.")
            
        params = {"org_id": org_id}
        return self._make_request("GET", f"{self.user_url}/projects/extras", params=params)
    
    # Developer Status Methods
    
    def get_developer_status(self) -> Dict:
        """
        Check if the user has developer API access.
        
        Returns:
            Dictionary with developer status information including:
            - user_id: ID of the user
            - has_developer_access: Whether the user has developer API access
            - pending_request: Whether there's a pending API access request
            - request_date: Date of the pending request (if applicable)
        """
        return self._make_request("GET", f"{self.user_url}/developer-status")
