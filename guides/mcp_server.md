# Storylinez MCP Server

Drive your Storylinez account from any MCP-capable agent — Claude Desktop, Cursor,
Codex, or your own client — using your Storylinez API key. The headline capability is
the **end-to-end video pipeline**: hand the agent a prompt and it can build a full
video start to finish, then track the job and fetch the result.

## Install

```bash
pip install "storylinez[mcp]"
```

This pulls in the official `mcp` package and installs the `storylinez-mcp` console script.

## Configure credentials

The server reads credentials from the environment (never passed on the command line):

| Variable | Required | Purpose |
|---|---|---|
| `STORYLINEZ_API_KEY` | ✅ | Your Storylinez API key |
| `STORYLINEZ_API_SECRET` | ✅ | Your Storylinez API secret |
| `STORYLINEZ_ORG_ID` | optional | Default organization for all calls |
| `STORYLINEZ_BASE_URL` | optional | Defaults to the production API |

If the key/secret are missing, the server starts but every call returns a clear
"not configured" error so the agent can tell you what to fix.

## Launch

```bash
storylinez-mcp          # console script (recommended)
python -m storylinez.mcp # module form
```

The server speaks MCP over stdio.

## Wire it into Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "storylinez": {
      "command": "storylinez-mcp",
      "env": {
        "STORYLINEZ_API_KEY": "your-key",
        "STORYLINEZ_API_SECRET": "your-secret",
        "STORYLINEZ_ORG_ID": "your-org-id"
      }
    }
  }
}
```

Cursor / Codex / other clients use the same `command` + `env` shape in their own MCP config.

## Available tools

**Pipeline (end-to-end video creation)**
- `pipeline_create_video_v2` — start a V2 sequence-builder video from a prompt
- `pipeline_create_video_v1` — start a V1 video from a prompt and/or reference video
- `pipeline_get_job_status` / `pipeline_get_job_result` / `pipeline_get_job` — track & collect
- `pipeline_cancel_job`, `pipeline_status`

**Projects** — `list_projects`, `get_project`, `create_project`, `search_projects`

**Media search** — `search_media`, `search_by_transcription`

**Sequences** — `list_sequences`, `get_sequence`, `list_sequence_snapshots`

**Rendering** — `create_render`, `get_render_status`, `get_render_download_links`

**Storage** — `list_folder_contents`

Extra pipeline options are passed as a JSON-object string via `config_json`.

## Typical flow

1. `create_project(name, orientation="landscape", project_type="v2")`
2. `pipeline_create_video_v2(label, sequence_prompt, ...)` → returns `job_id`
3. Poll `pipeline_get_job_status(job_id)` until done
4. `pipeline_get_job_result(job_id)` → output references
5. `create_render(project_id)` → `get_render_download_links(render_id)`
