# Storylinez SDK Documentation Hub

This folder contains practical, source-aligned documentation for Storylinez SDK.

If you are new to the SDK, start here:

1. [Getting Started](./getting-started.md)
2. [V1 End-to-End Workflow](./workflow-v1.md)
3. [Module Usage Guide](./module-usage-guide.md)
4. [Advanced V2 and Automation](./advanced-v2-automation.md)
5. [Complete Method Reference](./module-method-reference.md)
6. [Production Best Practices](./production-best-practices.md)

## What This Documentation Covers

- Authentication and client initialization
- End-to-end video generation flow (project -> prompt -> storyboard -> sequence -> render)
- How and when to use each module client
- V2 modules and automation routes
- Source-derived method signatures for all public client methods
- Production patterns for retries, polling, and resilient error handling

## Notes

- Method signatures in [Complete Method Reference](./module-method-reference.md) are generated from `src/storylinez/*.py` public methods.
- Some modules accept either `project_id` or `render_id`/`sequence_id` depending on route shape.
- `youtube_downloads` and `trending_ads` support Bearer-token style auth in addition to API key/secret initialization.

## Related Resources

- Root SDK README: `../README.md`
- Tutorial-style guides: `../guides/`
- Working examples: `../examples/`
