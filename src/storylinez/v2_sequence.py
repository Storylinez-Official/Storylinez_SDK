import time
from typing import Dict, Any, Optional, Iterable

from .base_client import BaseClient


class V2SequenceClient(BaseClient):
    """SDK helper for Storylinez V2 sequence session endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ) -> None:
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._sequence_base_url = f"{self.base_url}/v2/sequence"

    def create_session(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        message: str = "",
        temperature: float = 0.7,
        model_override: Optional[str] = None,
        eco: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Create a new V2 session and trigger the first build job."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")
        validated_temp = self._validate_temperature(temperature)

        payload: Dict[str, Any] = {
            "org_id": org,
            "project_id": project_id,
            "message": message,
            "temperature": validated_temp,
        }
        if model_override:
            payload["model_override"] = model_override
        if eco is not None:
            payload["eco"] = bool(eco)

        return self._make_request("POST", f"{self._sequence_base_url}/create", json_data=payload)

    def continue_session(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        message: str = "",
        temperature: float = 0.7,
        model_override: Optional[str] = None,
        eco: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Continue an existing session with a follow-up instruction."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")
        validated_temp = self._validate_temperature(temperature)

        payload: Dict[str, Any] = {
            "org_id": org,
            "project_id": project_id,
            "message": message,
            "temperature": validated_temp,
        }
        if model_override:
            payload["model_override"] = model_override
        if eco is not None:
            payload["eco"] = bool(eco)

        return self._make_request("POST", f"{self._sequence_base_url}/continue", json_data=payload)

    def list_sequences(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List sequences for the active session including job metadata."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
        }
        if page is not None:
            params["page"] = str(page)
        if page_size is not None:
            params["page_size"] = str(page_size)

        return self._make_request("GET", f"{self._sequence_base_url}/list", params=params)

    def list_sequences_lite(
        self,
        project_id: str,
        org_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Lightweight sequence list returning identifiers and labels only."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        params = {
            "org_id": org,
            "project_id": project_id,
        }
        return self._make_request("GET", f"{self._sequence_base_url}/list_lite", params=params)

    def get_sequence(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        sequence_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve a specific sequence or the primary sequence when sequence_id is omitted."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
        }
        if sequence_id:
            params["sequence_id"] = sequence_id

        return self._make_request("GET", f"{self._sequence_base_url}/get", params=params)

    def list_sequence_media(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        sequence_id: Optional[str] = None,
        include_analysis: bool = False,
    ) -> Dict[str, Any]:
        """Resolve media analysis for assets referenced by a sequence."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
            "include_analysis": str(include_analysis).lower(),
        }
        if sequence_id:
            params["sequence_id"] = sequence_id

        return self._make_request("GET", f"{self._sequence_base_url}/media/list", params=params)

    def update_sequence(
        self,
        project_id: str,
        sequence_id: str,
        sequence: Dict[str, Any],
        org_id: Optional[str] = None,
        *,
        session_id: Optional[str] = None,
        validate_only: bool = False,
    ) -> Dict[str, Any]:
        """Validate or persist a sequence document."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")
        if not sequence_id:
            raise ValueError("sequence_id is required")
        if not isinstance(sequence, dict):
            raise ValueError("sequence payload must be a dictionary")

        payload: Dict[str, Any] = {
            "org_id": org,
            "project_id": project_id,
            "sequence_id": sequence_id,
            "sequence": sequence,
            "validate_only": bool(validate_only),
        }
        if session_id:
            payload["session_id"] = session_id

        return self._make_request("PUT", f"{self._sequence_base_url}/update", json_data=payload)

    def list_snapshots(
        self,
        project_id: str,
        session_id: str,
        sequence_id: str,
        org_id: Optional[str] = None,
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List undo snapshots for a sequence."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")
        if not session_id:
            raise ValueError("session_id is required")
        if not sequence_id:
            raise ValueError("sequence_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
            "session_id": session_id,
            "sequence_id": sequence_id,
        }
        if page is not None:
            params["page"] = str(page)
        if page_size is not None:
            params["page_size"] = str(page_size)

        return self._make_request("GET", f"{self._sequence_base_url}/snapshots", params=params)

    def get_history(
        self,
        project_id: str,
        session_id: str,
        org_id: Optional[str] = None,
        *,
        sequence_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        bearer_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return the filtered history timeline for a session."""
        if not bearer_token:
            raise ValueError("bearer_token is required for the history endpoint")
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")
        if not session_id:
            raise ValueError("session_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
            "session_id": session_id,
        }
        if sequence_id:
            params["sequence_id"] = sequence_id
        if page is not None:
            params["page"] = str(page)
        if page_size is not None:
            params["page_size"] = str(page_size)

        headers = {
            "Authorization": f"Bearer {bearer_token}",
        }
        return self._make_request("GET", f"{self._sequence_base_url}/history", params=params, headers=headers)

    def wait_for_job_completion(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        sequence_id: Optional[str] = None,
        poll_interval: float = 5.0,
        timeout: Optional[float] = 300.0,
        terminal_statuses: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        """Poll sequence jobs until a terminal status is reached and return the latest sequence doc."""
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        normalized_terminals = {str(status).upper() for status in (terminal_statuses or (
            "COMPLETED",
            "SUCCESS",
            "FAILED",
            "ERROR",
            "CANCELLED",
            "REJECTED",
        ))}
        deadline = time.time() + timeout if timeout is not None else None

        while True:
            response = self.list_sequences(project_id=project_id, org_id=org)
            sequences = response.get("sequences") or []
            target: Optional[Dict[str, Any]] = None
            if sequence_id:
                target = next((seq for seq in sequences if str(seq.get("sequence_id")) == sequence_id), None)
            else:
                target = next((seq for seq in sequences if seq.get("is_primary")), None) or (sequences[0] if sequences else None)

            if not target:
                raise RuntimeError("No sequence found matching the provided criteria")

            status = str(target.get("job_status") or target.get("status") or "").upper()
            if not status or status in normalized_terminals:
                return target

            if deadline is not None and time.time() >= deadline:
                raise TimeoutError("Sequence job did not reach a terminal status within the allotted time")

            time.sleep(poll_interval)

    def _require_org(self, explicit_org: Optional[str]) -> str:
        org = explicit_org or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        return str(org)

    @staticmethod
    def _validate_temperature(value: float) -> float:
        try:
            temperature = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("temperature must be a number") from exc
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")
        return temperature
