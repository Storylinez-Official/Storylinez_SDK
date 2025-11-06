import time
from typing import Dict, Any, Optional, Iterable

from .base_client import BaseClient


class V2RenderClient(BaseClient):
    """SDK helper for Storylinez V2 render endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ) -> None:
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._render_base_url = f"{self.base_url}/v2/render"

    def start_render(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        sequence_id: Optional[str] = None,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        video_bitrate: Optional[int] = None,
        audio_bitrate: Optional[int] = None,
        video_preset: Optional[str] = None,
        watermark: Optional[bool] = None,
        codec: Optional[str] = None,
        audio_codec: Optional[str] = None,
        output_bucket: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Request a new render job for a sequence."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")
        if (target_width is None) != (target_height is None):
            raise ValueError("target_width and target_height must be provided together")

        payload: Dict[str, Any] = {
            "org_id": org,
            "project_id": project_id,
        }
        if sequence_id:
            payload["sequence_id"] = sequence_id
        if target_width is not None and target_height is not None:
            payload["target_width"] = int(target_width)
            payload["target_height"] = int(target_height)
        if video_bitrate is not None:
            payload["video_bitrate"] = int(video_bitrate)
        if audio_bitrate is not None:
            payload["audio_bitrate"] = int(audio_bitrate)
        if video_preset:
            payload["video_preset"] = video_preset
        if watermark is not None:
            payload["watermark"] = bool(watermark)
        if codec:
            payload["codec"] = codec
        if audio_codec:
            payload["audio_codec"] = audio_codec
        if output_bucket:
            payload["output_bucket"] = output_bucket

        return self._make_request("POST", f"{self._render_base_url}/start", json_data=payload)

    def get_render(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        render_id: Optional[str] = None,
        include_results: Optional[bool] = None,
        include_sequence: Optional[bool] = None,
        include_subtitles: Optional[bool] = None,
        generate_download_link: Optional[bool] = None,
        generate_streamable_link: Optional[bool] = None,
        generate_thumbnail_stream_link: Optional[bool] = None,
        stream_use_cdn: Optional[bool] = None,
        download_use_cdn: Optional[bool] = None,
        thumbnail_stream_use_cdn: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Fetch render documents or a single render by id."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
        }
        if render_id:
            params["render_id"] = render_id
        self._set_optional_bool(params, "include_results", include_results)
        self._set_optional_bool(params, "include_sequence", include_sequence)
        self._set_optional_bool(params, "include_subtitles", include_subtitles)
        self._set_optional_bool(params, "generate_download_link", generate_download_link)
        self._set_optional_bool(params, "generate_streamable_link", generate_streamable_link)
        self._set_optional_bool(params, "generate_thumbnail_stream_link", generate_thumbnail_stream_link)
        self._set_optional_bool(params, "stream_use_cdn", stream_use_cdn)
        self._set_optional_bool(params, "download_use_cdn", download_use_cdn)
        self._set_optional_bool(params, "thumbnail_stream_use_cdn", thumbnail_stream_use_cdn)
        if page is not None:
            params["page"] = str(page)
        if page_size is not None:
            params["page_size"] = str(page_size)

        return self._make_request("GET", f"{self._render_base_url}/get", params=params)

    def get_history(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        render_id: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        generate_streamable_link: Optional[bool] = None,
        generate_thumbnail_stream_link: Optional[bool] = None,
        generate_download_link: Optional[bool] = None,
        stream_use_cdn: Optional[bool] = None,
        thumbnail_stream_use_cdn: Optional[bool] = None,
        download_use_cdn: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """List archived render history with optional presigned URLs."""
        org = self._require_org(org_id)
        if not project_id:
            raise ValueError("project_id is required")

        params: Dict[str, str] = {
            "org_id": org,
            "project_id": project_id,
        }
        if render_id:
            params["render_id"] = render_id
        if page is not None:
            params["page"] = str(page)
        if limit is not None:
            params["limit"] = str(limit)
        self._set_optional_bool(params, "generate_streamable_link", generate_streamable_link)
        self._set_optional_bool(params, "generate_thumbnail_stream_link", generate_thumbnail_stream_link)
        self._set_optional_bool(params, "generate_download_link", generate_download_link)
        self._set_optional_bool(params, "stream_use_cdn", stream_use_cdn)
        self._set_optional_bool(params, "thumbnail_stream_use_cdn", thumbnail_stream_use_cdn)
        self._set_optional_bool(params, "download_use_cdn", download_use_cdn)

        return self._make_request("GET", f"{self._render_base_url}/history", params=params)

    def wait_for_render_completion(
        self,
        project_id: str,
        render_id: str,
        org_id: Optional[str] = None,
        *,
        poll_interval: float = 5.0,
        timeout: Optional[float] = 600.0,
        terminal_statuses: Optional[Iterable[str]] = None,
        **get_kwargs: Any,
    ) -> Dict[str, Any]:
        """Poll render status until it reaches a terminal state and return the render document."""
        if not render_id:
            raise ValueError("render_id is required")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")

        org = self._require_org(org_id)
        normalized_terminals = {str(status).upper() for status in (terminal_statuses or (
            "COMPLETED",
            "SUCCESS",
            "FAILED",
            "ERROR",
            "CANCELLED",
            "STOPPED",
            "REJECTED",
        ))}
        deadline = time.time() + timeout if timeout is not None else None

        while True:
            response = self.get_render(
                project_id=project_id,
                org_id=org,
                render_id=render_id,
                **get_kwargs,
            )
            render_doc = response.get("render")
            if not render_doc:
                renders = response.get("renders") or []
                render_doc = renders[0] if renders else None

            if not render_doc:
                raise RuntimeError("Render document not found while polling for completion")

            status = str(
                render_doc.get("status")
                or (render_doc.get("job") or {}).get("status")
                or ""
            ).upper()
            if not status or status in normalized_terminals:
                return render_doc

            if deadline is not None and time.time() >= deadline:
                raise TimeoutError("Render job did not reach a terminal status within the allotted time")

            time.sleep(poll_interval)

    def _require_org(self, explicit_org: Optional[str]) -> str:
        org = explicit_org or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        return str(org)

    @staticmethod
    def _set_optional_bool(params: Dict[str, str], key: str, value: Optional[bool]) -> None:
        if value is None:
            return
        params[key] = str(bool(value)).lower()
