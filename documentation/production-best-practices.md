# Production Best Practices

This checklist helps keep Storylinez SDK workflows reliable in production.

## 1. Validate Credentials Early

- Verify `STORYLINEZ_API_KEY`, `STORYLINEZ_API_SECRET`, and org scope before long jobs.
- Run a lightweight call at startup, such as `client.user.get_current_user()`.

## 2. Treat Generation as Async Jobs

Most heavy operations are async behind the scenes.

- Storyboard
- Voiceover
- Sequence
- Render
- Tool jobs
- Pipeline jobs

Use wait helpers where available.

```python
storyboard = client.storyboard.create_storyboard_and_wait(
    project_id=project_id,
    timeout=300,
)
```

## 3. Keep Timeouts Realistic

Recommended starting points:

- Storyboard: 300 to 600 seconds
- Voiceover: 180 to 300 seconds
- Sequence: 600 to 900 seconds
- Render: 1200 to 2400 seconds

## 4. Add Retry Guards Around Network Calls

`BaseClient` includes retry behavior for transient request failures.

You should still wrap critical workflow stages to support app-level recovery.

```python
def run_stage(name, fn):
    try:
        return fn()
    except Exception as exc:
        print(f"Stage failed: {name} -> {exc}")
        raise
```

## 5. Keep IDs and Statuses in Logs

Always log and persist:

- `project_id`
- `job_id`
- `sequence_id`
- `render_id`
- final status

This makes reruns and recovery deterministic.

## 6. Prefer Explicit Project Context

Even with default org configured, pass explicit IDs in background jobs and workers when possible.

- `org_id`
- `project_id`
- specific `*_id` values for assets/jobs

## 7. Separate Draft and Final Render Profiles

Maintain at least two render parameter sets:

- Draft: faster/cheaper previews
- Final: production resolution and subtitle tuning

## 8. Validate Media Inputs

Before upload:

- Confirm file exists
- Confirm extension is expected
- Track source metadata for audits

After upload:

- Wait for processing if downstream search/analysis depends on it

## 9. Version Your Workflow Config

When calling sequence/render/tool modules, keep config snapshots in your own app DB.

Store:

- prompt content
- AI flags (`deepthink`, `overdrive`, `web_search`, `eco`)
- template and grading choices
- render settings

## 10. Suggested Error Envelope

Wrap SDK exceptions into your own consistent shape:

```python
{
  "ok": False,
  "stage": "render",
  "project_id": "...",
  "job_id": "...",
  "error": "human readable message"
}
```

## 11. Build Safe Recovery Paths

- If storyboard fails: retry with lower complexity flags
- If sequence fails: regenerate with simplified prompt
- If render fails: retry with fewer advanced toggles
- If a job stalls: fetch status and restart from last successful artifact

## 12. Keep SDK and Docs in Sync

When adding or changing module methods:

1. Update source module
2. Update [Module Usage Guide](./module-usage-guide.md)
3. Regenerate [Complete Method Reference](./module-method-reference.md)
