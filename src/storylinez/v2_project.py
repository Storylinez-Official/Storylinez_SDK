from typing import Dict, List, Optional, Union

from .base_client import BaseClient


class V2ProjectClient(BaseClient):
    """
    Client for Storylinez V2 project media endpoints.
    Manage the analysed asset catalogue exposed under /v2/projects/media.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: str = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._projects_media_url = f"{self.base_url}/v2/projects/media"
        self._projects_settings_url = f"{self.base_url}/v2/projects/settings"

    def get_generation_settings(
        self,
        project_id: str,
        org_id: Optional[str] = None,
    ) -> Dict:
        """
        Get stored generation settings for a V2 project.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")

        params = {
            "org_id": org,
            "project_id": project_id,
        }
        return self._make_request("GET", f"{self._projects_settings_url}/generation", params=params)

    def add_media(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        file_id: Optional[str] = None,
        stock_id: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> Dict:
        """
        Attach a single analysed media source to a V2 project.

        Provide either file_id (user upload) OR stock_id+media_type ("videos"|"audios"|"images").
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")

        if not file_id and not stock_id:
            raise ValueError("Either file_id or stock_id must be provided")
        if stock_id and media_type is None:
            raise ValueError("media_type is required when attaching stock_id (videos|audios|images)")
        if media_type and media_type not in ["videos", "audios", "images"]:
            raise ValueError("media_type must be one of: videos, audios, images")

        payload: Dict[str, Union[str, Dict]] = {
            "org_id": org,
            "project_id": project_id,
        }
        if file_id:
            payload["file_id"] = file_id
        if stock_id:
            payload["stock_id"] = stock_id
            payload["media_type"] = media_type

        return self._make_request("POST", f"{self._projects_media_url}/add", json_data=payload)

    def add_media_bulk(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        file_ids: Optional[List[str]] = None,
        items: Optional[List[Dict]] = None,
    ) -> Dict:
        """
        Attach multiple media sources to a V2 project in one call.

        - file_ids: list of user file IDs
        - items: list of objects like {"file_id": "..."} or {"stock_id": "stk_...", "media_type": "videos"}
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")

        if not file_ids and not items:
            raise ValueError("At least one of file_ids or items must be provided")

        # Minimal sanity checks for items
        if items:
            if not isinstance(items, list):
                raise ValueError("items must be a list")
            for i, it in enumerate(items):
                if not isinstance(it, dict):
                    raise ValueError(f"items[{i}] must be a dict")
                if ("stock_id" in it) and ("media_type" not in it):
                    raise ValueError(f"items[{i}] requires media_type when stock_id is provided")

        payload: Dict[str, Union[str, List, Dict]] = {
            "org_id": org,
            "project_id": project_id,
        }
        if file_ids:
            payload["file_ids"] = file_ids
        if items:
            payload["items"] = items

        return self._make_request("POST", f"{self._projects_media_url}/add_bulk", json_data=payload)

    def list_media(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        include_analysis: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict:
        """
        List media items for a V2 project.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1 or page_size > 100:
            raise ValueError("page_size must be within 1..100")

        params = {
            "org_id": org,
            "project_id": project_id,
            "include_analysis": str(include_analysis).lower(),
            "page": page,
            "page_size": page_size,
        }
        return self._make_request("GET", f"{self._projects_media_url}/list", params=params)
