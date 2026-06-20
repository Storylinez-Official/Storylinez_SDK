"""
Storylinez MCP server (FastMCP).

Exposes a curated, high-value slice of the Storylinez SDK over the Model Context
Protocol. The headline capability is the end-to-end *pipeline* — an agent can take a
prompt and drive a full start-to-finish video build — alongside project management,
media search, sequence inspection, and rendering.

Credentials come from the environment so the server can be launched by any MCP client
without passing secrets on the command line:

    STORYLINEZ_API_KEY      (required)
    STORYLINEZ_API_SECRET   (required)
    STORYLINEZ_ORG_ID       (optional default org for all calls)
    STORYLINEZ_BASE_URL     (optional, defaults to production)

Run:
    storylinez-mcp           # console script
    python -m storylinez.mcp # module form
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - import guard
    raise ImportError(
        "The MCP server requires the 'mcp' package. Install it with:\n"
        "    pip install \"storylinez[mcp]\"   (or)   pip install \"mcp[cli]\"\n"
    ) from exc

from ..client import StorylinezClient


# ---------------------------------------------------------------------------
# Client wiring
# ---------------------------------------------------------------------------

def _build_client() -> StorylinezClient:
    """Construct a StorylinezClient from environment credentials.

    Raises a clear error (surfaced to the MCP client) if required creds are missing.
    """
    api_key = os.getenv("STORYLINEZ_API_KEY")
    api_secret = os.getenv("STORYLINEZ_API_SECRET")
    if not api_key or not api_secret:
        raise RuntimeError(
            "Storylinez MCP server is not configured. Set STORYLINEZ_API_KEY and "
            "STORYLINEZ_API_SECRET in the environment (STORYLINEZ_ORG_ID optional)."
        )
    base_url = os.getenv("STORYLINEZ_BASE_URL", "https://api.storylinezads.com")
    org_id = os.getenv("STORYLINEZ_ORG_ID") or None
    return StorylinezClient(
        api_key=api_key,
        api_secret=api_secret,
        base_url=base_url,
        org_id=org_id,
    )


def _ok(data: Any) -> str:
    """Serialize a successful result as compact JSON text for the model."""
    return json.dumps({"success": True, "data": data}, default=str, ensure_ascii=False)


def _err(message: str, **extra: Any) -> str:
    """Serialize an error as JSON text the model can read and act on."""
    payload = {"success": False, "error": message}
    payload.update(extra)
    return json.dumps(payload, default=str, ensure_ascii=False)


def _call(fn, *args, **kwargs) -> str:
    """Invoke an SDK method, translating exceptions into structured MCP error text."""
    try:
        return _ok(fn(*args, **kwargs))
    except Exception as exc:  # noqa: BLE001 - report any SDK/HTTP failure to the agent
        return _err(str(exc), type=type(exc).__name__)


# ---------------------------------------------------------------------------
# Server definition
# ---------------------------------------------------------------------------

def build_server() -> FastMCP:
    """Create and configure the FastMCP server with the curated Storylinez toolset."""
    mcp = FastMCP("storylinez")
    client = _build_client()

    # ----- Pipeline: the headline end-to-end video creation capability -----

    @mcp.tool()
    def pipeline_create_video_v2(
        label: str,
        sequence_prompt: str,
        org_id: Optional[str] = None,
        config_json: Optional[str] = None,
    ) -> str:
        """Start an end-to-end V2 (sequence-builder) video pipeline from a prompt.

        This is the start-to-finish creation path: give it a descriptive prompt and it
        orchestrates the full build. Returns a job document including a job_id; poll
        pipeline_get_job_status / pipeline_get_job_result to track and collect output.
        Pass extra pipeline options as a JSON object string in config_json.
        """
        config: Dict[str, Any] = {}
        if config_json:
            try:
                config = json.loads(config_json)
            except json.JSONDecodeError as exc:
                return _err(f"config_json is not valid JSON: {exc}")
        return _call(
            client.pipeline_jobs.start_v2,
            label=label,
            sequence_prompt=sequence_prompt,
            org_id=org_id,
            **config,
        )

    @mcp.tool()
    def pipeline_create_video_v1(
        label: str,
        main_prompt: Optional[str] = None,
        reference_video_id: Optional[str] = None,
        org_id: Optional[str] = None,
        config_json: Optional[str] = None,
    ) -> str:
        """Start an end-to-end V1 (legacy media) video pipeline.

        Provide main_prompt and/or reference_video_id. Returns a job document with a
        job_id for tracking. Pass extra options as a JSON object string in config_json.
        """
        config: Dict[str, Any] = {}
        if config_json:
            try:
                config = json.loads(config_json)
            except json.JSONDecodeError as exc:
                return _err(f"config_json is not valid JSON: {exc}")
        return _call(
            client.pipeline_jobs.start_v1,
            label=label,
            main_prompt=main_prompt,
            reference_video_id=reference_video_id,
            org_id=org_id,
            **config,
        )

    @mcp.tool()
    def pipeline_get_job_status(job_id: str) -> str:
        """Get the lightweight status of a pipeline job (use to poll progress)."""
        return _call(client.pipeline_jobs.get_job_status, job_id)

    @mcp.tool()
    def pipeline_get_job_result(job_id: str) -> str:
        """Get the result payload of a finished pipeline job (final output references)."""
        return _call(client.pipeline_jobs.get_job_result, job_id)

    @mcp.tool()
    def pipeline_get_job(job_id: str) -> str:
        """Get the full pipeline job document (config, stage history, status, result)."""
        return _call(client.pipeline_jobs.get_job, job_id)

    @mcp.tool()
    def pipeline_cancel_job(job_id: str) -> str:
        """Cancel a running pipeline job."""
        return _call(client.pipeline_jobs.cancel_job, job_id)

    @mcp.tool()
    def pipeline_status() -> str:
        """Get the pipeline service status (availability / health)."""
        return _call(client.pipeline_jobs.status)

    # ----- Projects -----

    @mcp.tool()
    def list_projects(status: Optional[str] = None, org_id: Optional[str] = None) -> str:
        """List the caller's projects, optionally filtered by status."""
        return _call(client.project.get_all_projects, status=status, org_id=org_id)

    @mcp.tool()
    def get_project(project_id: str) -> str:
        """Get a single project by id."""
        return _call(client.project.get_project, project_id)

    @mcp.tool()
    def create_project(
        name: str,
        orientation: str,
        purpose: str = "",
        target_audience: str = "",
        project_type: str = "v2",
        org_id: Optional[str] = None,
    ) -> str:
        """Create a new project (orientation: 'landscape' or 'portrait'; type 'v1' or 'v2')."""
        return _call(
            client.project.create_project,
            name=name,
            orientation=orientation,
            purpose=purpose,
            target_audience=target_audience,
            project_type=project_type,
            org_id=org_id,
        )

    @mcp.tool()
    def search_projects(query: str = "", org_id: Optional[str] = None) -> str:
        """Search projects by free-text query."""
        return _call(client.project.search_projects, query=query, org_id=org_id)

    # ----- Media search -----

    @mcp.tool()
    def search_media(
        query: str,
        media_types: Optional[List[str]] = None,
        media_source: str = "user",
        org_id: Optional[str] = None,
    ) -> str:
        """Search across the user's media library (combined video/audio/image)."""
        kwargs: Dict[str, Any] = {"query": query, "media_source": media_source, "org_id": org_id}
        if media_types is not None:
            kwargs["media_types"] = media_types
        return _call(client.search.search_combined, **kwargs)

    @mcp.tool()
    def search_by_transcription(query: str, media_source: str = "user", org_id: Optional[str] = None) -> str:
        """Find audio/video where the given text is spoken (transcription search)."""
        return _call(
            client.search.search_audio_by_transcription,
            query=query,
            media_source=media_source,
            org_id=org_id,
        )

    # ----- V2 sequence inspection -----

    @mcp.tool()
    def list_sequences(project_id: str, org_id: Optional[str] = None) -> str:
        """List the sequences in a project."""
        return _call(client.v2_sequence.list_sequences, project_id=project_id, org_id=org_id)

    @mcp.tool()
    def get_sequence(project_id: str, org_id: Optional[str] = None) -> str:
        """Get the primary sequence (timeline structure) of a project."""
        return _call(client.v2_sequence.get_sequence, project_id=project_id, org_id=org_id)

    @mcp.tool()
    def list_sequence_snapshots(project_id: str, session_id: str, org_id: Optional[str] = None) -> str:
        """List saved timeline snapshots for a sequence session."""
        return _call(
            client.v2_sequence.list_snapshots,
            project_id=project_id,
            session_id=session_id,
            org_id=org_id,
        )

    # ----- Rendering -----

    @mcp.tool()
    def create_render(project_id: str, org_id: Optional[str] = None) -> str:
        """Create a render job for a project's current sequence."""
        return _call(client.render.create_render, project_id=project_id, org_id=org_id)

    @mcp.tool()
    def get_render_status(render_id: str, org_id: Optional[str] = None) -> str:
        """Get the status of a render job."""
        return _call(client.render.get_render_status, render_id=render_id, org_id=org_id)

    @mcp.tool()
    def get_render_download_links(render_id: str, org_id: Optional[str] = None) -> str:
        """Get download links for a finished render."""
        return _call(client.render.get_render_download_links, render_id=render_id, org_id=org_id)

    # ----- Storage browse -----

    @mcp.tool()
    def list_folder_contents(folder_id: Optional[str] = None, org_id: Optional[str] = None) -> str:
        """List files and subfolders in a storage folder (root if folder_id omitted)."""
        return _call(client.storage.get_folder_contents, folder_id=folder_id, org_id=org_id)

    return mcp


def main() -> None:
    """Console-script / module entrypoint: build the server and serve over stdio."""
    server = build_server()
    server.run()


if __name__ == "__main__":
    main()
