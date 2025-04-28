# Storylinez SDK

[![PyPI version](https://badge.fury.io/py/storylinez.svg)](https://badge.fury.io/py/storylinez)
[![Python Versions](https://img.shields.io/pypi/pyversions/storylinez.svg)](https://pypi.org/project/storylinez/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Storylinez SDK is a comprehensive Python library for interacting with the Storylinez API platform. It provides a modular approach to narrative generation, video creation, and content management, enabling developers to build sophisticated AI-driven content creation workflows.

The SDK offers access to all Storylinez services through a unified client interface, with specialized modules for storyboards, video sequences, rendering, media management, and more.

## Features

- **Comprehensive API coverage**: Access all Storylinez platform services
- **Modular architecture**: Use only what you need
- **Robust error handling**: Clear validation and helpful error messages
- **Convenient utilities**: Helper methods for common workflows
- **Type annotations**: Full type hinting for better IDE support
- **Advanced media processing**: Generate, edit, and search media content
- **AI-powered tools**: Create storyboards, sequences, and render videos using AI

## Installation

Install the SDK using pip:

```bash
pip install storylinez
```

For development installations:

```bash
git clone https://github.com/Kawai-Senpai/Storylinez-SDK.git
cd Storylinez-SDK
pip install -e .
```

## Authentication

Create a `.env` file with your API credentials or set environment variables:

```
STORYLINEZ_API_KEY=api_your_key_here
STORYLINEZ_API_SECRET=your_secret_here
STORYLINEZ_ORG_ID=your_org_id_here
```

Then use these credentials to initialize the client:

```python
from storylinez import StorylinezClient
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Initialize the client
client = StorylinezClient(
    api_key=os.environ.get("STORYLINEZ_API_KEY"),
    api_secret=os.environ.get("STORYLINEZ_API_SECRET"),
    org_id=os.environ.get("STORYLINEZ_ORG_ID")
)
```

## Quick Start

### Creating a Project

```python
# Create a project folder
folder = client.project.create_folder(
    name="Marketing Videos",
    description="Campaign videos for Q3"
)

# Create a project
project = client.project.create_project(
    name="Product Launch Video",
    orientation="landscape",
    purpose="Showcase new product features",
    folder_id=folder.get("folder_id")
)

project_id = project.get("project").get("project_id")
```

### Creating a Storyboard

```python
# Create a prompt for the project
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a promotional video for our eco-friendly product line",
    document_context="The product reduces carbon footprint by 30%.",
    temperature=0.7
)

# Generate a storyboard
storyboard = client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True,
    temperature=0.7,
    iterations=3
)

storyboard_id = storyboard.get("storyboard", {}).get("storyboard_id")
```

### Creating a Sequence and Rendering

```python
# Create a sequence from the storyboard
sequence = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True,
    deepthink=True
)

# Render the sequence as a video
render = client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
    subtitle_color="#FFFFFF"
)

# Get render status and download link when complete
status = client.render.get_render_status(render_id=render.get("render", {}).get("render_id"))
if status.get("status") == "COMPLETED":
    links = client.render.get_render_download_links(render_id=render.get("render", {}).get("render_id"))
    download_url = links.get("download_url")
```

## Module Overview

The SDK consists of these specialized client modules:

| Module | Description |
|--------|-------------|
| `project` | Create and manage projects and folders |
| `prompt` | Generate and manage AI prompts for content |
| `storyboard` | Create and edit storyboard scenes |
| `sequence` | Arrange media into video sequences |
| `render` | Generate final videos from sequences |
| `storage` | Upload, manage and analyze media files |
| `stock` | Search and retrieve stock media assets |
| `search` | Advanced semantic search across content |
| `brand` | Create and manage brand styling presets |
| `company_details` | Manage company profile information |
| `settings` | User preferences and settings |
| `tools` | AI-powered tools like briefs, shotlists, etc. |
| `utils` | Utility functions and helpers |
| `user` | User profile and subscription management |
| `voiceover` | Generate and manage voiceover audio |

## Detailed Usage Examples

### Media Upload and Analysis

```python
# Upload a media file
upload_result = client.storage.upload_file(
    file_path="path/to/video.mp4",
    folder_path="/project_assets",
    context="Product demo footage",
    tags=["product", "demo"],
    analyze_audio=True,
    deepthink=True
)

# Get analysis results
file_id = upload_result.get("file", {}).get("file_id")
analysis = client.storage.get_file_analysis(
    file_id=file_id,
    detailed=True,
    generate_thumbnail=True
)

# Search for similar content
search_results = client.search.search_video_scenes(
    query="person demonstrating product features",
    generate_thumbnail=True
)
```

### Stock Media Search

```python
# Search for stock videos
videos = client.stock.search_videos(
    query="aerial view of mountains",
    num_results=5,
    orientation="landscape",
    generate_thumbnail=True
)

# Search for stock audio
audio = client.stock.search_audio(
    query="upbeat corporate background music",
    num_results=3,
    generate_thumbnail=True
)
```

### Company Branding

```python
# Create company details
company = client.company_details.create(
    company_name="Acme Corporation",
    tag_line="Building the Future, Today",
    description="Acme is a technology leader focused on innovation.",
    is_default=True
)

# Create a brand preset
brand = client.brand.create(
    name="Modern Blue",
    outro_bg_color="#0066CC",
    main_text_color="#FFFFFF",
    company_font="Montserrat-Bold",
    subtitle_font="Montserrat-Regular"
)
```

## Error Handling

The SDK provides helpful error messages with validation checks:

```python
try:
    client.storyboard.create_storyboard(
        project_id=project_id,
        temperature=2.0  # Invalid temperature
    )
except ValueError as e:
    print(f"Validation error: {str(e)}")  # "temperature must be between 0.0 and 1.0"
except Exception as e:
    print(f"API error: {str(e)}")
```

## Advanced Usage

### Workflow Methods

The SDK provides convenience methods for common workflows:

```python
# Create and wait for a storyboard to complete
completed_storyboard = client.storyboard.create_and_wait(
    project_id=project_id,
    deepthink=True,
    timeout_seconds=300
)

# Create a project with files in one step
project_with_files = client.project.create_project_with_files(
    name="Quick Project",
    orientation="landscape",
    files=["file_id1", "file_id2"],
    folder_name="Quick Projects"
)

# Update settings and redo render in one step
updated_render = client.render.update_settings_and_redo(
    render_id=render_id,
    subtitle_color="#FFFF00",
    color_balance_fix=True
)
```

## Environment Variable Reference

| Variable | Description |
|----------|-------------|
| `STORYLINEZ_API_KEY` | Your API key (starts with `api_`) |
| `STORYLINEZ_API_SECRET` | Your API secret |
| `STORYLINEZ_ORG_ID` | Your organization ID (starts with `org_`) |
| `STORYLINEZ_BASE_URL` | Optional custom API URL (defaults to `https://api.storylinezads.com`) |

## Documentation

For detailed documentation on all available methods and parameters, see the [official Storylinez API documentation](https://docs.storylinezads.com).

Example scripts demonstrating each module can be found in the `examples/` directory:

- `brand_company_examples.py` - Brand and company management
- `project_examples.py` - Project and folder operations
- `prompt_examples.py` - AI prompt creation and management
- `storyboard_examples.py` - Storyboard creation and editing
- `sequence_examples.py` - Video sequence management
- `render_examples.py` - Video rendering operations
- `storage_examples.py` - File storage and management
- `stock_examples.py` - Stock media operations
- `search_examples.py` - Content search capabilities
- `settings_examples.py` - User settings management
- `tools_examples.py` - AI-powered creative tools
- `user_examples.py` - User profile and subscription
- `utils_examples.py` - Utilities and helpers
- `voiceover_examples.py` - Voice generation and management

## Requirements

- Python 3.6+
- `requests` library for API communication
- `dotenv` (optional) for environment variable loading

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@storylinezads.com or visit [Storylinez Docs](https://storylinezads.com).