# Getting Started

This guide helps you go from zero to first generated video with Storylinez SDK.

## 1. Installation

Install from PyPI:

```bash
pip install storylinez
```

Or install from source:

```bash
git clone https://github.com/Storylinez-Official/Storylinez_SDK.git
cd Storylinez_SDK
pip install -e .
```

## 2. Environment Variables

Create a `.env` file:

```env
STORYLINEZ_API_KEY=api_your_key_here
STORYLINEZ_API_SECRET=your_secret_here
STORYLINEZ_ORG_ID=your_org_id_here
STORYLINEZ_BASE_URL=https://api.storylinezads.com
```

## 3. Initialize the Client

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

## 4. Minimal End-to-End Example

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

# 1) Create a project
project = client.project.create_project(
    name="SDK Quickstart Demo",
    orientation="landscape",
    purpose="Create a short product intro video"
)
project_id = project["project"]["project_id"]

# 2) Create prompt
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a 30-second launch teaser for a productivity app",
    document_context="Target audience: startup founders and freelancers.",
    total_length=30,
)

# 3) Storyboard
client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True,
)
storyboard = client.storyboard.create_storyboard_and_wait(
    project_id=project_id,
    timeout=300,
)

# 4) Sequence
client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True,
)

# 5) Render
render_job = client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
)

render = client.render.create_and_wait_for_render(
    project_id=project_id,
    timeout=1800,
)

print("Render status:", render.get("status"))
```

## 5. Common Initialization Patterns

### Use one default organization for all calls

```python
client = StorylinezClient(api_key="...", api_secret="...", org_id="org_123")
```

### Override org per call

Most module methods accept `org_id` directly.

```python
client.project.get_all_projects(org_id="org_secondary")
```

### Use direct credentials in CI

```python
client = StorylinezClient(
    api_key=os.environ["STORYLINEZ_API_KEY"],
    api_secret=os.environ["STORYLINEZ_API_SECRET"],
    org_id=os.environ.get("STORYLINEZ_ORG_ID"),
)
```

## 6. Where To Go Next

- Full module-by-module usage: [Module Usage Guide](./module-usage-guide.md)
- Full signatures for all public methods: [Complete Method Reference](./module-method-reference.md)
- End-to-end production flow: [V1 End-to-End Workflow](./workflow-v1.md)
