from typing import Dict, List, Optional

from .base_client import BaseClient


class YouTubeDownloadsClient(BaseClient):
    """Client for /youtube-downloads endpoints.

    These endpoints require Bearer token authentication. Set auth_token on the client
    or pass auth_token per method call.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
        auth_token: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._youtube_downloads_url = f"{self.base_url}/youtube-downloads"
        self.auth_token = auth_token

    def set_auth_token(self, auth_token: str) -> None:
        """Set default Bearer token used for token-authenticated calls."""
        self.auth_token = auth_token

    def _auth_headers(self, auth_token: Optional[str]) -> Dict[str, str]:
        token = auth_token or self.auth_token
        if not token:
            raise ValueError("auth_token is required for youtube_downloads endpoints")
        return {
            "Authorization": f"Bearer {token}",
        }

    def status(self, auth_token: Optional[str] = None) -> Dict:
        """Get API status and endpoint map."""
        return self._make_request(
            "GET",
            f"{self._youtube_downloads_url}/status",
            headers=self._auth_headers(auth_token),
        )

    def start(
        self,
        urls: List[str],
        org_id: Optional[str] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Start a YouTube download batch job."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not urls or not isinstance(urls, list):
            raise ValueError("urls must be a non-empty list")

        payload = {
            "org_id": org,
            "urls": urls,
        }
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        return self._make_request(
            "POST",
            f"{self._youtube_downloads_url}/start",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def get_job(
        self,
        job_id: str,
        org_id: Optional[str] = None,
        *,
        include_urls: bool = True,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Get one download job by id."""
        if not job_id:
            raise ValueError("job_id is required")

        params = {
            "include_urls": str(bool(include_urls)).lower(),
        }
        org = org_id or self.default_org_id
        if org is not None:
            params["org_id"] = org

        return self._make_request(
            "GET",
            f"{self._youtube_downloads_url}/job/{job_id}",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    def list_jobs(
        self,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        include_urls: bool = True,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """List jobs for an organization."""
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
            "include_urls": str(bool(include_urls)).lower(),
        }
        if status is not None:
            params["status"] = status

        return self._make_request(
            "GET",
            f"{self._youtube_downloads_url}/jobs",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    def get_item_url(
        self,
        job_id: str,
        item_index: int,
        org_id: Optional[str] = None,
        *,
        expiration: int = 3600,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Generate fresh streamable URL for one job item."""
        if not job_id:
            raise ValueError("job_id is required")
        if item_index < 0:
            raise ValueError("item_index must be >= 0")

        params = {
            "expiration": expiration,
        }
        org = org_id or self.default_org_id
        if org is not None:
            params["org_id"] = org

        return self._make_request(
            "GET",
            f"{self._youtube_downloads_url}/job/{job_id}/item/{item_index}/url",
            params=params,
            headers=self._auth_headers(auth_token),
        )
