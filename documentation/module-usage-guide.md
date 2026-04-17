# Module Usage Guide

This guide explains how to use each module exposed by `StorylinezClient` and related helpers.

Use this with [Complete Method Reference](./module-method-reference.md) for full signatures.

## Core Generation Modules

### project

Use for project/folder lifecycle and linking files, stock, and voiceovers.

Common operations:

- `create_project`
- `get_project`
- `search_projects`
- `add_associated_file`
- `add_stock_file`
- `add_voiceover`

```python
project = client.project.create_project(
    name="Launch Demo",
    orientation="landscape",
    purpose="New product launch"
)
project_id = project["project"]["project_id"]
```

### prompt

Use to define the creative instructions the generation pipeline should follow.

Common operations:

- `create_text_prompt`
- `create_video_prompt`
- `update_prompt`
- `generate_search_query`

```python
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a 30-second launch ad",
    document_context="Focus on product value and call to action",
    total_length=30,
)
```

### storyboard

Use to generate and refine scenes before sequencing.

Common operations:

- `create_storyboard`
- `create_storyboard_and_wait`
- `update_storyboard_values`
- `send_chat_prompt`
- `restore_version`

```python
storyboard = client.storyboard.create_storyboard_and_wait(
    project_id=project_id,
    deepthink=True,
    timeout=300,
)
```

### voiceover

Use for AI voice generation or custom voiceover lifecycle.

Common operations:

- `create_voiceover`
- `create_and_wait`
- `upload_voiceover_file`
- `switch_generation`

```python
voiceover = client.voiceover.create_and_wait(
    project_id=project_id,
    timeout_seconds=300,
)
```

### sequence

Use to build timeline structure from storyboard assets and prompts.

Common operations:

- `create_sequence`
- `redo_sequence`
- `update_sequence_settings`
- `send_chat_prompt`
- `restore_version`

```python
sequence = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True,
    iterations=2,
)
```

### render

Use to produce final video outputs and links.

Common operations:

- `create_render`
- `create_and_wait_for_render`
- `get_render`
- `redo_render`
- `get_render_download_links`

```python
client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
)

result = client.render.create_and_wait_for_render(project_id=project_id, timeout=1800)
```

## Media and Discovery Modules

### storage

Use for uploads, folders, reprocessing, file analysis, and retrieval links.

Common operations:

- `upload_file`
- `upload_and_process_files_bulk`
- `get_folder_contents`
- `vector_search`
- `get_file_analysis`

```python
uploaded = client.storage.upload_file(
    file_path="./assets/demo.mp4",
    folder_path="/campaign",
    context="Primary footage"
)
```

### stock

Use for external stock media discovery and retrieval.

Common operations:

- `search`
- `get_by_id`
- `search_videos`
- `search_images`

```python
stock = client.stock.search(
    queries=["modern office", "team collaboration"],
    collections=["videos"],
    num_results_videos=3,
)
```

### search

Use semantic and metadata search for user media and tags.

Common operations:

- `search_video_scenes`
- `search_audio_content`
- `search_image_by_objects`
- `search_by_tags`

```python
results = client.search.search_video_scenes(
    query="person presenting in front of a screen",
    media_source="user",
)
```

## Organization and Branding Modules

### company_details

Use for organization profile data used by prompts and branding.

Common operations:

- `create`
- `get_default`
- `update`
- `search`

```python
company = client.company_details.create(
    company_name="Acme Labs",
    tag_line="Build faster with less noise",
    is_default=True,
)
```

### brand

Use for look-and-feel presets, logos, subtitle styles, and CTA visuals.

Common operations:

- `upload_logo`
- `create`
- `update`
- `set_default`
- `search`

```python
brand = client.brand.upload_logo(
    file_path="./assets/logo.png",
    name="Acme Brand",
    is_default=True,
)
```

### settings

Use for user preference and AI default persistence.

Common operations:

- `get_settings`
- `update_settings`
- `update_ai_defaults`
- `backup_settings`

```python
client.settings.update_ai_defaults(
    temperature=0.7,
    deepthink=True,
    overdrive=False,
)
```

### user

Use for user, subscription, and usage metrics.

Common operations:

- `get_current_user`
- `get_subscription`
- `get_project_usage`
- `get_org_storage`

```python
subscription = client.user.get_subscription()
```

## AI Utility and Automation Helpers

### tools

Use specialized tool endpoints for briefs, plans, trend analysis, and web scraper jobs.

Common operations:

- `create_creative_brief`
- `create_video_plan`
- `create_trend_analysis`
- `create_web_scraper_advanced`
- `wait_for_tool_completion`

```python
brief_job = client.tools.create_creative_brief(
    name="Q3 Campaign Brief",
    user_input="Build a creative brief for a B2B SaaS launch",
    deepthink=True,
)
```

### utils

Use utility endpoints for voice/template metadata, prompt enhancement, and async job polling.

Common operations:

- `get_supported_formats`
- `get_voice_types`
- `extract_brand_settings`
- `wait_for_job_completion`

```python
job = client.utils.extract_brand_settings(
    website_url="https://example.com",
    deepthink=True,
)
result = client.utils.wait_for_job_completion(job["job_id"], timeout_seconds=120)
```

### pipeline (helper class)

`PipelineClient` is a helper in `pipeline.py`. It is not attached as `client.pipeline` by default.

Use it when you want one function to run web scraping and brand extraction together.

```python
from storylinez.pipeline import PipelineClient

pipeline = PipelineClient(client)
out = pipeline.run_web_scraping_and_brand_extraction(
    website_url="https://example.com",
    depth=1,
    deepthink=True,
)
```

## V2 Modules

### v2_project

Use for V2 project-level media operations.

Common operations:

- `get_generation_settings`
- `add_media`
- `add_media_bulk`
- `list_media`

### v2_context

Use for V2 document/reference context management.

Common operations:

- `add_document`
- `list_documents`
- `set_reference`
- `list_references`

### v2_effects

Use for V2 effect catalog discovery.

Common operations:

- `get_catalog`
- `list_effects`
- `find_effect`

### v2_schema

Use for schema-aware integrations and validation.

Common operations:

- `get_sequence_schema`
- `get_asset_schema`
- `get_all_schemas`

### v2_sequence

Use interactive V2 sequence session workflows.

Common operations:

- `create_session`
- `continue_session`
- `list_sequences`
- `update_sequence`
- `import_asset`

### v2_render

Use V2 render lifecycle and status polling.

Common operations:

- `start_render`
- `get_render`
- `get_history`
- `wait_for_render_completion`

### v2_share

Use for public share links and revocation.

Common operations:

- `create_share`
- `get_public_share`
- `list_shares`
- `revoke_share`

V2 starter flow:

```python
# Add context
client.v2_context.add_document(
    project_id=project_id,
    title="Product context",
    content="Audience, positioning, and launch goals",
)

# Start sequence session
session = client.v2_sequence.create_session(
    project_id=project_id,
    message="Create a punchy 30-second launch sequence",
)

# Render
render_job = client.v2_render.start_render(project_id=project_id)
render_done = client.v2_render.wait_for_render_completion(
    project_id=project_id,
    render_id=render_job["render"]["render_id"],
)
```

## Data and Voice Modules

### pipeline_jobs

Use for one-shot end-to-end pipeline jobs (V1 and V2).

Common operations:

- `start_v1`
- `start_v2`
- `get_job_status`
- `get_job_result`

### data_collection

Use to collect and process YouTube-sourced data jobs.

Common operations:

- `start_youtube_collection`
- `list_youtube_jobs`
- `start_youtube_extraction`
- `get_youtube_item_url`

### voice_library

Use system/user voice catalog and TTS operations.

Common operations:

- `list_voices`
- `create_user_voice`
- `generate_tts`
- `generate_tts_multi_speaker`
- `get_tts_job`

## Next

- Full signatures for every method: [Complete Method Reference](./module-method-reference.md)
- Production retry and reliability patterns: [Production Best Practices](./production-best-practices.md)
