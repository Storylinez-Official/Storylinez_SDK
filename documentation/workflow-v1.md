# V1 End-to-End Workflow

This is the practical V1 pipeline most teams run in production.

1. Create project
2. Add media (optional)
3. Create prompt
4. Generate storyboard
5. Generate voiceover (optional)
6. Build sequence
7. Render output

## Step 1 - Create Project

```python
project = client.project.create_project(
    name="Campaign Video",
    orientation="landscape",
    purpose="Promote launch campaign"
)
project_id = project["project"]["project_id"]
```

## Step 2 - Add Media

### Upload user media

```python
uploaded = client.storage.upload_file(
    file_path="./assets/hero.mp4",
    folder_path="/campaign_assets",
    context="Hero shot for launch video",
)

client.project.add_associated_file(
    project_id=project_id,
    file_id=uploaded["file"]["file_id"],
)
```

### Add stock media

```python
stock = client.stock.search(
    queries=["startup office", "product launch"],
    collections=["videos"],
    num_results_videos=3,
)

for item in stock.get("videos", []):
    client.project.add_stock_file(
        project_id=project_id,
        stock_id=item.get("stock_id") or item.get("_id"),
        media_type="videos",
    )
```

## Step 3 - Create Prompt

```python
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a modern 30-second launch teaser.",
    document_context="Keep tone confident, fast-paced, and premium.",
    total_length=30,
    temperature=0.7,
)
```

## Step 4 - Generate Storyboard

```python
client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True,
    iterations=3,
)

storyboard = client.storyboard.create_storyboard_and_wait(
    project_id=project_id,
    polling_interval=5,
    timeout=300,
)
```

## Step 5 - Voiceover

```python
voiceover = client.voiceover.create_and_wait(
    project_id=project_id,
    timeout_seconds=300,
)
```

If you already have narration, upload and attach custom audio:

```python
uploaded_audio = client.storage.upload_file(file_path="./assets/narration.wav")
client.project.add_voiceover(
    project_id=project_id,
    file_id=uploaded_audio["file"]["file_id"],
    voice_name="Studio Voiceover",
)
```

## Step 6 - Sequence

```python
sequence = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True,
    grade_type="single",
    iterations=2,
)
```

For manual + AI refinement loops:

```python
client.sequence.send_chat_prompt(
    project_id=project_id,
    prompt="Keep pacing quick and reduce slow intro shots",
    wait_for_completion=True,
)
```

## Step 7 - Render

```python
client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
    company_name="My Company",
    call_to_action="Visit our website",
)

render = client.render.create_and_wait_for_render(
    project_id=project_id,
    timeout=1800,
)
```

Generate streamable/download links:

```python
links = client.render.get_render_download_links(project_id=project_id)
print(links)
```

## Polling and Timeouts

Use `create_and_wait_*` helpers when available.

For manual polling, check statuses repeatedly with a timeout guard. Keep polling interval between 3 and 10 seconds for most jobs.

## Recommended V1 Module Order

- `project`
- `storage` and/or `stock`
- `prompt`
- `storyboard`
- `voiceover`
- `sequence`
- `render`

## Next

- Full module coverage: [Module Usage Guide](./module-usage-guide.md)
- Full signatures: [Complete Method Reference](./module-method-reference.md)
