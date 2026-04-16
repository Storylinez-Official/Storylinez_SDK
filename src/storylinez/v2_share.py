from typing import Dict, Optional

from .base_client import BaseClient


class V2ShareClient(BaseClient):
    """Client for /v2/share endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._share_url = f"{self.base_url}/v2/share"

    def create_share(
        self,
        project_id: str,
        render_id: str,
        org_id: Optional[str] = None,
        *,
        sequence_id: Optional[str] = None,
        render_s3_key: Optional[str] = None,
    ) -> Dict:
        """Create a public share link for a rendered V2 sequence."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not render_id:
            raise ValueError("render_id is required")

        payload = {
            "org_id": org,
            "project_id": project_id,
            "render_id": render_id,
        }
        if sequence_id is not None:
            payload["sequence_id"] = sequence_id
        if render_s3_key is not None:
            payload["render_s3_key"] = render_s3_key

        return self._make_request("POST", f"{self._share_url}/create", json_data=payload)

    def get_public_share(
        self,
        share_id: str,
        *,
        generate_streamable_link: bool = True,
        stream_use_cdn: bool = False,
    ) -> Dict:
        """Fetch public share payload without requiring auth context."""
        if not share_id:
            raise ValueError("share_id is required")

        params = {
            "generate_streamable_link": str(bool(generate_streamable_link)).lower(),
            "stream_use_cdn": str(bool(stream_use_cdn)).lower(),
        }
        return self._make_request("GET", f"{self._share_url}/public/{share_id}", params=params)

    def list_shares(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> Dict:
        """List share links for a project."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1:
            raise ValueError("limit must be >= 1")

        params = {
            "org_id": org,
            "project_id": project_id,
            "page": page,
            "limit": limit,
        }
        return self._make_request("GET", f"{self._share_url}/list", params=params)

    def revoke_share(self, share_id: str, org_id: Optional[str] = None) -> Dict:
        """Revoke an existing share link."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not share_id:
            raise ValueError("share_id is required")

        payload = {
            "org_id": org,
            "share_id": share_id,
        }
        return self._make_request("POST", f"{self._share_url}/revoke", json_data=payload)
