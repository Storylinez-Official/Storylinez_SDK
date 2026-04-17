# Advanced V2 and Automation

This guide covers V2-oriented modules and production automation paths.

## 1. V2 Session Pattern

Use V2 when you need schema-aware, iterative sequence workflows.

Typical flow:

1. Add context docs and references
2. Start a sequence session
3. Continue/refine messages
4. Update sequence payload if needed
5. Start render and poll for completion
6. Create share link

```python
# 1) Attach context
client.v2_context.add_document(
    project_id=project_id,
    title="Campaign brief",
    content="Target audience, value props, constraints",
)

# 2) Start session
start = client.v2_sequence.create_session(
    project_id=project_id,
    message="Create a 30-second ad sequence with 5 scenes",
)

# 3) Continue session
client.v2_sequence.continue_session(
    project_id=project_id,
    message="Tighten pacing and strengthen CTA scene",
)

# 4) Inspect generated sequences
seqs = client.v2_sequence.list_sequences(project_id=project_id)
```

## 2. V2 Render and Share

```python
render_job = client.v2_render.start_render(project_id=project_id)
render_id = render_job.get("render", {}).get("render_id")

render_result = client.v2_render.wait_for_render_completion(
    project_id=project_id,
    render_id=render_id,
    timeout=1200,
)

share = client.v2_share.create_share(
    project_id=project_id,
    render_id=render_id,
)
```

## 3. Pipeline Jobs (One-Shot Automation)

If you want fewer manual module calls, use `pipeline_jobs`:

```python
job = client.pipeline_jobs.start_v2(
    label="Launch Automation",
    sequence_prompt="Create a high-energy product launch video",
)

status = client.pipeline_jobs.get_job_status(job["job_id"])
result = client.pipeline_jobs.get_job_result(job["job_id"])
```

Use `start_v1` if you are running V1-style pipeline orchestration.

## 4. Data Collection Workflows

Use `data_collection` for YouTube collection + extraction jobs.

```python
collect = client.data_collection.start_youtube_collection(
    query="best performing AI SaaS ads",
    max_results=20,
)

job_id = collect["job_id"]

extract = client.data_collection.start_youtube_extraction(
    job_id=job_id,
    video_indices=[0, 1, 2],
)

item_url = client.data_collection.get_youtube_item_url(
    job_id=job_id,
    item_index=0,
)
```

## 5. Voice Library and TTS

```python
voices = client.voice_library.list_voices(query="warm female", limit=5)
voice_id = voices["voices"][0]["voice_id"]

tts_job = client.voice_library.generate_tts(
    text="Welcome to the launch event.",
    voice_id=voice_id,
)

tts_result = client.voice_library.get_tts_job(tts_job["job_id"], poll=True)
```

## 6. Optional Pipeline Helper Class

If you want a single helper call for web scraping + brand extraction:

```python
from storylinez.pipeline import PipelineClient

pipeline = PipelineClient(client)
result = pipeline.run_web_scraping_and_brand_extraction(
    website_url="https://example.com",
    deepthink=True,
    polling_interval=10,
)
```

## 7. Practical Notes

- Prefer V2 modules for schema-driven editing and session-like interactions.
- Use pipeline jobs for operational simplicity when teams need fewer SDK calls.
- Keep render polling timeout generous for long videos.
- Persist `job_id`, `project_id`, and `render_id` in your app logs for replay/debug.
