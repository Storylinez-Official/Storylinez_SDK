from typing import Dict, Optional

from .base_client import BaseClient


class PipelineJobsClient(BaseClient):
    """Client for /pipeline job endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._pipeline_url = f"{self.base_url}/pipeline"

    def status(self) -> Dict:
        """Get pipeline service status."""
        return self._make_request("GET", f"{self._pipeline_url}/status")

    def start_v1(
        self,
        label: str,
        org_id: Optional[str] = None,
        *,
        main_prompt: Optional[str] = None,
        reference_video_id: Optional[str] = None,
        **config,
    ) -> Dict:
        """Start a v1 pipeline job."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not label:
            raise ValueError("label is required")
        if not main_prompt and not reference_video_id:
            raise ValueError("Either main_prompt or reference_video_id is required")

        payload = {
            "org_id": org,
            "label": label,
            "main_prompt": main_prompt,
            "reference_video_id": reference_video_id,
        }
        payload.update({k: v for k, v in config.items() if v is not None})

        return self._make_request("POST", f"{self._pipeline_url}/v1", json_data=payload)

    def start_v2(
        self,
        label: str,
        sequence_prompt: str,
        org_id: Optional[str] = None,
        **config,
    ) -> Dict:
        """Start a v2 pipeline job."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not label:
            raise ValueError("label is required")
        if not sequence_prompt:
            raise ValueError("sequence_prompt is required")

        payload = {
            "org_id": org,
            "label": label,
            "sequence_prompt": sequence_prompt,
        }
        payload.update({k: v for k, v in config.items() if v is not None})

        return self._make_request("POST", f"{self._pipeline_url}/v2", json_data=payload)

    def get_job(self, job_id: str) -> Dict:
        """Get full pipeline job document."""
        if not job_id:
            raise ValueError("job_id is required")
        return self._make_request("GET", f"{self._pipeline_url}/{job_id}")

    def get_job_status(self, job_id: str) -> Dict:
        """Get lightweight pipeline job status payload."""
        if not job_id:
            raise ValueError("job_id is required")
        return self._make_request("GET", f"{self._pipeline_url}/{job_id}/status")

    def get_job_result(self, job_id: str) -> Dict:
        """Get pipeline job result payload."""
        if not job_id:
            raise ValueError("job_id is required")
        return self._make_request("GET", f"{self._pipeline_url}/{job_id}/result")

    def cancel_job(self, job_id: str) -> Dict:
        """Cancel a pipeline job."""
        if not job_id:
            raise ValueError("job_id is required")
        return self._make_request("DELETE", f"{self._pipeline_url}/{job_id}")
