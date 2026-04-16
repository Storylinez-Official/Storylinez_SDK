from typing import Dict, List, Optional

from .base_client import BaseClient


class DataCollectionClient(BaseClient):
    """Client for /data-collection endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._data_collection_url = f"{self.base_url}/data-collection"

    def status(self) -> Dict:
        """Get data collection service status."""
        return self._make_request("GET", f"{self._data_collection_url}/status")

    def start_youtube_collection(
        self,
        org_id: Optional[str] = None,
        *,
        query: Optional[str] = None,
        prompt: Optional[str] = None,
        instructions: Optional[str] = None,
        max_results: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict:
        """Start a YouTube data collection job."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")

        payload = {
            "org_id": org,
        }
        if query is not None:
            payload["query"] = query
        if prompt is not None:
            payload["prompt"] = prompt
        if instructions is not None:
            payload["instructions"] = instructions
        if max_results is not None:
            payload["max_results"] = max_results
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        return self._make_request("POST", f"{self._data_collection_url}/youtube/start", json_data=payload)

    def get_youtube_job(self, job_id: str, org_id: Optional[str] = None) -> Dict:
        """Get one data collection job."""
        if not job_id:
            raise ValueError("job_id is required")

        params = {}
        org = org_id or self.default_org_id
        if org is not None:
            params["org_id"] = org

        return self._make_request("GET", f"{self._data_collection_url}/youtube/job/{job_id}", params=params)

    def list_youtube_jobs(
        self,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
    ) -> Dict:
        """List data collection jobs for an organization."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1:
            raise ValueError("page_size must be >= 1")

        params = {
            "org_id": org,
            "page": page,
            "page_size": page_size,
        }
        if search is not None:
            params["search"] = search
        if status is not None:
            params["status"] = status
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_direction is not None:
            params["sort_direction"] = sort_direction

        return self._make_request("GET", f"{self._data_collection_url}/youtube/jobs", params=params)

    def start_youtube_extraction(
        self,
        job_id: str,
        video_indices: List[int],
        org_id: Optional[str] = None,
    ) -> Dict:
        """Start extraction for selected item indexes from a collection job."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not job_id:
            raise ValueError("job_id is required")
        if not video_indices or not isinstance(video_indices, list):
            raise ValueError("video_indices must be a non-empty list")

        payload = {
            "org_id": org,
            "video_indices": video_indices,
        }
        return self._make_request(
            "POST",
            f"{self._data_collection_url}/youtube/job/{job_id}/extract",
            json_data=payload,
        )

    def get_youtube_extraction_status(self, job_id: str, org_id: Optional[str] = None) -> Dict:
        """Get extraction status for a collection job."""
        if not job_id:
            raise ValueError("job_id is required")

        params = {}
        org = org_id or self.default_org_id
        if org is not None:
            params["org_id"] = org

        return self._make_request(
            "GET",
            f"{self._data_collection_url}/youtube/job/{job_id}/extraction-status",
            params=params,
        )

    def get_youtube_item_url(
        self,
        job_id: str,
        item_index: int,
        org_id: Optional[str] = None,
        *,
        expiry: int = 3600,
    ) -> Dict:
        """Get stream/download URL for one extracted item."""
        if not job_id:
            raise ValueError("job_id is required")
        if item_index < 0:
            raise ValueError("item_index must be >= 0")

        params = {
            "expiry": expiry,
        }
        org = org_id or self.default_org_id
        if org is not None:
            params["org_id"] = org

        return self._make_request(
            "GET",
            f"{self._data_collection_url}/youtube/job/{job_id}/item/{item_index}/url",
            params=params,
        )
