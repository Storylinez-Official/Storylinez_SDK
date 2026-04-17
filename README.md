# Storylinez SDK

[![PyPI version](https://badge.fury.io/py/storylinez.svg)](https://pypi.org/project/storylinez/)
[![Python Versions](https://img.shields.io/pypi/pyversions/storylinez.svg)](https://pypi.org/project/storylinez/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Storylinez SDK - AI-driven content creation platform](https://github.com/Storylinez-Official/Storylinez_SDK/blob/39634c47dcb72d833a38a5292186116bdf513d5f/assets/Storylinez%20Cover.png)

Build production-grade AI video workflows in Python.

Storylinez SDK gives you one client that covers:

- Project and media management
- Prompting and generation pipelines
- Storyboard and sequence control
- Rendering, sharing, and automation jobs
- V2 schema-aware workflow modules

## Quick Navigation

- [Install](#install)
- [Authenticate](#authenticate)
- [5-Minute Quickstart](#5-minute-quickstart)
- [Module Map](#module-map)
- [Detailed Documentation](#detailed-documentation)
- [Examples](#examples)
- [Guides](#guides)
- [Support](#support)

## Install

Install from PyPI:

```bash
pip install storylinez
```

Install from source:

```bash
git clone https://github.com/Storylinez-Official/Storylinez_SDK.git
cd Storylinez_SDK
pip install -e .
```

## Authenticate

Create a `.env` file:

```env
STORYLINEZ_API_KEY=api_your_key_here
STORYLINEZ_API_SECRET=your_secret_here
STORYLINEZ_ORG_ID=your_org_id_here
STORYLINEZ_BASE_URL=https://api.storylinezads.com
```

Initialize client:

```python
import os
from dotenv import load_dotenv
from storylinez import StorylinezClient

load_dotenv()

client = StorylinezClient(
    api_key=os.getenv("STORYLINEZ_API_KEY"),
    api_secret=os.getenv("STORYLINEZ_API_SECRET"),
    org_id=os.getenv("STORYLINEZ_ORG_ID"),
    base_url=os.getenv("STORYLINEZ_BASE_URL", "https://api.storylinezads.com"),
)
```

## 5-Minute Quickstart

```python
from storylinez import StorylinezClient
import os
from dotenv import load_dotenv

load_dotenv()

client = StorylinezClient(
    api_key=os.getenv("STORYLINEZ_API_KEY"),
    api_secret=os.getenv("STORYLINEZ_API_SECRET"),
    org_id=os.getenv("STORYLINEZ_ORG_ID"),
)

# 1) Create project
project = client.project.create_project(
    name="SDK Quickstart",
    orientation="landscape",
    purpose="Generate a short launch video"
)
project_id = project["project"]["project_id"]

# 2) Create prompt
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a 30-second launch teaser for a productivity app",
    document_context="Audience: founders and operators",
    total_length=30,
)

# 3) Generate storyboard
storyboard = client.storyboard.create_storyboard_and_wait(
    project_id=project_id,
    deepthink=True,
    timeout=300,
)

# 4) Build sequence
client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True,
)

# 5) Render final output
render = client.render.create_and_wait_for_render(
    project_id=project_id,
    timeout=1800,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
)

print("Render status:", render.get("status"))
```

## Module Map

All modules are available through `StorylinezClient`.

### Core generation

| Module | What it handles |
|---|---|
| `project` | Project and folder lifecycle |
| `prompt` | Text/video prompt creation and updates |
| `storyboard` | Story generation and scene edits |
| `voiceover` | AI/custom voiceover management |
| `sequence` | Sequence timeline generation and refinement |
| `render` | Final render creation and render history |

### Media and discovery

| Module | What it handles |
|---|---|
| `storage` | Upload, process, analyze, and manage files |
| `stock` | Stock media search and retrieval |
| `search` | Semantic and metadata search across media |

### Organization and style

| Module | What it handles |
|---|---|
| `company_details` | Company profile data |
| `brand` | Brand presets, logos, and styling |
| `settings` | User defaults and settings |
| `user` | User info, storage, and usage data |

### Utility and advanced workflows

| Module | What it handles |
|---|---|
| `tools` | AI tools (briefs, plans, trend analysis, scraper) |
| `utils` | Format metadata, utility jobs, prompt helpers |
| `v2_project` | V2 project media operations |
| `v2_context` | V2 docs and references |
| `v2_effects` | V2 effect catalog |
| `v2_schema` | V2 sequence/asset schemas |
| `v2_sequence` | V2 interactive sequence sessions |
| `v2_render` | V2 render lifecycle |
| `v2_share` | V2 share links |
| `pipeline_jobs` | Start and track V1/V2 one-shot pipelines |
| `data_collection` | YouTube collection and extraction jobs |
| `voice_library` | Voice catalog and TTS jobs |

Additional helper class:

- `PipelineClient` in `src/storylinez/pipeline.py` for combined web scraping + brand extraction helper flow.

## Detailed Documentation

New detailed docs are now available in [documentation/](./documentation/):

- [Documentation Hub](./documentation/README.md)
- [Getting Started](./documentation/getting-started.md)
- [V1 End-to-End Workflow](./documentation/workflow-v1.md)
- [Module Usage Guide](./documentation/module-usage-guide.md)
- [Advanced V2 and Automation](./documentation/advanced-v2-automation.md)
- [Complete Method Reference (all public methods)](./documentation/module-method-reference.md)
- [Production Best Practices](./documentation/production-best-practices.md)

## Examples

Working scripts are in [examples/](./examples/):

- `project_examples.py`
- `storage_examples.py`
- `prompt_examples.py`
- `storyboard_examples.py`
- `sequence_examples.py`
- `render_examples.py`
- `tools_examples.py`
- `v2_project_examples.py`

## Guides

Tutorial-style docs are in [guides/](./guides/), including:

- API key setup and usage
- End-to-end platform workflows
- Organization/team management
- Prompting and editing guidance
- Publishing and support workflows

## Platform Links

- Web app: https://app.storylinezads.com
- API docs: https://docs.storylinezads.com
- API endpoint: https://api.storylinezads.com

## Requirements

- Python 3.6+
- Dependencies from package metadata (`setup.py`)

## Support

- Documentation: https://docs.storylinezads.com
- Platform help: https://app.storylinezads.com/help
- Email: support@storylinezads.com

## License

MIT License. See [LICENSE.rst](./LICENSE.rst).
