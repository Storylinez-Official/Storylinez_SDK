# Storylinez SDK

[![PyPI version](https://badge.fury.io/py/storylinez.svg)](https://badge.fury.io/py/storylinez)
[![Python Versions](https://img.shields.io/pypi/pyversions/storylinez.svg)](https://pypi.org/project/storylinez/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Storylinez SDK - AI-driven content creation platform](https://github.com/Kawai-Senpai/Storylinez-SDK/blob/ecc7a73631dfd1db228baabb0ea2cf0b338fdef6/assets/Storylinez%20Cover.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Authentication](#authentication)
- [Quick Start](#quick-start)
- [Module Reference](#module-reference)
- [Detailed Usage Examples](#detailed-usage-examples)
- [Workflow Patterns](#workflow-patterns)
- [Error Handling & Best Practices](#error-handling--best-practices)
- [Environment Configuration](#environment-configuration)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [API Documentation](#api-documentation)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

Storylinez SDK is a powerful Python library that provides comprehensive access to the Storylinez AI-driven content creation platform. Designed to enable developers to build sophisticated video generation workflows, the SDK integrates natural language processing, media management, and professional video production capabilities through a clean, intuitive API.

This library empowers developers to:
- Generate professional video content from text descriptions
- Create storyboards and narrative sequences with AI assistance
- Access a vast library of stock media content
- Apply brand styling and professional effects
- Render final videos with subtitles, voiceovers, and transitions
- Manage content libraries and search across multimedia assets

Whether you're building a content automation system, integrating AI-driven video generation into your application, or creating tools for content marketers, the Storylinez SDK provides the foundation for sophisticated media production workflows.

## Features

- **Complete API Coverage** - Access all Storylinez platform capabilities through a unified interface
- **Modular Architecture** - Import only the modules you need for your specific use case
- **Intelligent Content Generation** - AI-powered tools for storyboards, scripts, and content planning
- **Custom Media Processing** - Upload, analyze, search, and transform your own media assets
- **Professional Rendering** - Create polished videos with transitions, effects, and brand styling
- **Advanced Search** - Semantic search across media content, stock libraries, and generated assets
- **Brand Management** - Create and apply consistent styling to maintain brand identity
- **Workflow Tools** - Helper methods for common content creation patterns
- **Robust Validation** - Clear error messages and parameter validation to prevent issues
- **Comprehensive Type Hints** - Complete typing for improved IDE support and code completion
- **Flexible Authentication** - Simple setup with API keys or environment variables

## Installation

### Standard Installation

Install the SDK using pip:

```bash
pip install storylinez
```

### Development Installation

For the latest features or development work:

```bash
git clone https://github.com/Kawai-Senpai/Storylinez-SDK.git
cd Storylinez-SDK
pip install -e .
```

## Authentication

### Using Environment Variables

Create a `.env` file with your API credentials:

```
STORYLINEZ_API_KEY=api_your_key_here
STORYLINEZ_API_SECRET=your_secret_here
STORYLINEZ_ORG_ID=your_org_id_here
```

Then load these credentials:

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

### Direct Initialization

You can also initialize the client directly:

```python
from storylinez import StorylinezClient

# Initialize with explicit credentials
client = StorylinezClient(
    api_key="api_your_key_here",
    api_secret="your_secret_here",
    org_id="your_org_id_here"
)

# Initialize with custom API endpoint (for enterprise customers)
client = StorylinezClient(
    api_key="api_your_key_here",
    api_secret="your_secret_here",
    org_id="your_org_id_here",
    base_url="https://your-custom-endpoint.storylinez.com"
)
```

### Multiple Organizations

If you work with multiple organizations, you can:

```python
# Initialize client without default org_id
client = StorylinezClient(
    api_key="api_your_key_here",
    api_secret="your_secret_here"
)

# Specify organization per operation
project = client.project.create_project(
    name="Project Name",
    orientation="landscape",
    org_id="specific_org_id_here"
)

# Or set a new default
client.set_default_org_id("different_org_id")
```

## Quick Start

### End-to-End Video Creation

This example shows the complete process of creating a video from a text prompt:

```python
from storylinez import StorylinezClient
import os
from dotenv import load_dotenv

# Setup
load_dotenv()
client = StorylinezClient()

# 1. Create a project
project = client.project.create_project(
    name="Product Introduction",
    orientation="landscape",
    purpose="Introduce our new sustainable product line"
)
project_id = project["project"]["project_id"]

# 2. Create a text prompt
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a 30-second video introducing our eco-friendly product line that reduces plastic waste by 75%",
    document_context="Our products are made from bamboo and recycled materials. The target audience is environmentally conscious millennials.",
    temperature=0.7,
    total_length=30
)

# 3. Generate a storyboard
storyboard_job = client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True
)
print(f"Storyboard job started: {storyboard_job['job_id']}")

# 4. Wait for storyboard completion
storyboard = client.storyboard.wait_for_storyboard(
    project_id=project_id,
    timeout_seconds=300,
    polling_interval=5
)
print(f"Storyboard created with {len(storyboard['scenes'])} scenes")

# 5. Create a sequence
sequence_job = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True
)
print(f"Sequence job started: {sequence_job['job_id']}")

# 6. Wait for sequence completion
sequence = client.sequence.get_sequence(
    project_id=project_id,
    include_results=True
)
while sequence.get("status") != "COMPLETED":
    import time
    time.sleep(5)
    sequence = client.sequence.get_sequence(project_id=project_id)
print("Sequence completed")

# 7. Render the final video
render_job = client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
    company_name="Eco Solutions Inc.",
    call_to_action="Visit eco-solutions.com today"
)
print(f"Render job started: {render_job['job_id']}")

# 8. Get the download link when complete
render = client.render.wait_for_render(
    project_id=project_id,
    timeout_seconds=1800,
    polling_interval=20
)
if render["status"] == "COMPLETED":
    download_info = client.render.get_render(
        project_id=project_id,
        generate_download_link=True,
        generate_streamable_link=True
    )
    print(f"Video ready! Download URL: {download_info['download_url']}")
    print(f"Stream URL: {download_info['streamable_url']}")
else:
    print(f"Render failed with status: {render['status']}")
```

### Working with Existing Media

```python
# Upload your own media files
video_file = client.storage.upload_file(
    file_path="./product_demo.mp4",
    folder_path="/marketing/product_videos",
    analyze_video=True,
    analyze_audio=True
)

# Search for relevant stock content
stock_videos = client.stock.search_videos(
    query="sustainable eco-friendly product manufacturing",
    orientation="landscape",
    duration_max=30,
    num_results=5
)

# Create a project with your media
project = client.project.create_project_with_files(
    name="Product Demo Compilation",
    orientation="landscape", 
    files=[video_file["file_id"]] + [v["id"] for v in stock_videos["videos"]],
    purpose="Showcase product features with supporting contextual footage"
)
```

## Module Reference

The SDK is organized into logical modules for different aspects of the content creation process:

### Core Modules

| Module | Primary Focus | Key Capabilities |
|--------|--------------|------------------|
| `project` | Project & folder management | Create, organize, update, and search projects and project folders |
| `prompt` | Content prompting | Create text and video-based prompts for AI content generation |
| `storyboard` | Visual planning | Create, edit, and manage scene-by-scene storyboards |
| `sequence` | Media arrangement | Arrange media into polished video sequences with transitions |
| `render` | Video production | Generate final videos with customizable settings |

### Media & Content Modules

| Module | Primary Focus | Key Capabilities |
|--------|--------------|------------------|
| `storage` | Media management | Upload, organize, analyze, and retrieve media assets |
| `stock` | Stock content | Search and license professional stock media |
| `search` | Content discovery | Semantic search across projects and media assets |
| `voiceover` | Audio narration | Generate and manage AI or custom voiceovers |

### Branding & Styling Modules

| Module | Primary Focus | Key Capabilities |
|--------|--------------|------------------|
| `brand` | Brand identity | Create and manage brand styling presets |
| `company_details` | Company information | Manage organization profiles and metadata |

### System & Utility Modules

| Module | Primary Focus | Key Capabilities |
|--------|--------------|------------------|
| `settings` | User preferences | Manage default settings and user preferences |
| `tools` | AI tools | Access specialized AI tools like briefs and audience research |
| `utils` | Utilities | Helper functions for common tasks |
| `user` | User management | Profile and subscription operations |

## Detailed Usage Examples

### Project Management

```python
# Create project folders for organization
quarterly_folder = client.project.create_folder(
    name="Q3 Marketing Campaigns",
    description="All campaign videos for Q3 2023"
)

# Create a project in the folder
project = client.project.create_project(
    name="Summer Product Launch",
    orientation="landscape",
    purpose="Announce new summer product line with emphasis on outdoor use",
    target_audience="Active adults 25-40, outdoor enthusiasts",
    folder_id=quarterly_folder["folder_id"]
)

# List all projects in a folder
folder_projects = client.project.get_projects_by_folder(
    folder_id=quarterly_folder["folder_id"],
    generate_thumbnail_links=True
)

# Search for specific projects
search_results = client.project.search_projects(
    query="summer product",
    search_fields=["name", "purpose"],
    status="completed",
    created_after="2023-06-01",
    sort_by="created_at",
    sort_order="desc"
)
```

### Advanced Media Operations

```python
# Upload and analyze video with advanced options
video_result = client.storage.upload_file(
    file_path="./interview.mp4",
    folder_path="/raw_footage/interviews",
    context="CEO interview about new product line",
    tags=["interview", "CEO", "product launch"],
    analyze_video=True,
    analyze_audio=True,
    transcribe=True,
    generate_chapters=True,
    deepthink=True
)

# Access detailed analysis results
video_id = video_result["file"]["file_id"]
analysis = client.storage.get_file_analysis(
    file_id=video_id,
    include_transcript=True,
    include_scenes=True
)

# Find specific moments in the video
moments = client.search.search_video_moments(
    file_id=video_id,
    query="CEO explains product benefits",
    detailed=True
)

# Use a specific moment as reference for a new video
for moment in moments["moments"]:
    if moment["confidence"] > 0.8:
        clip_start = moment["start_time"]
        clip_end = moment["end_time"]
        print(f"Found relevant clip from {clip_start}s to {clip_end}s")
        
        # Create a clip from this moment
        clip = client.storage.create_clip(
            file_id=video_id,
            start_time=clip_start,
            end_time=clip_end,
            name=f"CEO explaining benefits - {clip_start}s",
            generate_thumbnail=True
        )
```

### Storyboard Creation and Editing

```python
# Create a storyboard with AI assistance
storyboard = client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True,
    overdrive=True
)

# Wait for storyboard completion
completed_storyboard = client.storyboard.wait_for_storyboard(
    project_id=project_id,
    timeout_seconds=300
)

# Regenerate a specific scene
scene_index = 2
client.storyboard.regenerate_scene(
    storyboard_id=completed_storyboard["storyboard_id"],
    scene_index=scene_index,
    guidance="Make this scene more dynamic and emphasize the product's durability"
)

# Update multiple scenes
updates = [
    {
        "scene_index": 0, 
        "visual_description": "Open with aerial shot of mountains with overlay text: 'Adventure Awaits'"
    },
    {
        "scene_index": 4,
        "scene_type": "product_closeup",
        "visual_description": "Close-up of product with water splashing off it, demonstrating waterproof feature"
    }
]
client.storyboard.update_scenes(
    storyboard_id=completed_storyboard["storyboard_id"],
    scene_updates=updates
)

# Export storyboard to PDF
pdf_result = client.storyboard.export_to_pdf(
    storyboard_id=completed_storyboard["storyboard_id"],
    include_script=True,
    include_thumbnails=True
)
pdf_url = pdf_result["download_url"]
```

### Brand Management and Styling

```python
# Upload a logo and create a brand preset
brand = client.brand.upload_logo(
    file_path="./company_logo.png",
    name="Corporate Blue",
    is_default=True,
    # Styling options
    outro_bg_color="#003366",
    main_text_color="#FFFFFF",
    sub_text_color="#E0E0E0",
    company_font="Montserrat-Bold",
    subtext_font="Montserrat-Regular",
    # Subtitle styling
    subtitle_font="OpenSans-Regular",
    subtitle_font_size=28,
    subtitle_color="#FFFFFF",
    subtitle_bg_color="#000000",
    subtitle_bg_opacity=0.7,
    subtitle_bg_rounded=True
)

# Update company details
company = client.company_details.create(
    company_name="EcoTech Solutions",
    tag_line="Innovating for a Sustainable Future",
    description="""EcoTech Solutions develops eco-friendly technologies 
                  that help businesses reduce their environmental impact 
                  while maintaining productivity.""",
    website="https://ecotechsolutions.example.com",
    industry="Environmental Technology",
    is_default=True
)

# Apply brand to project
client.project.update_project(
    project_id=project_id,
    brand_id=brand["brand_id"],
    company_details_id=company["company_details_id"]
)
```

### Advanced Sequence Operations

```python
# Create a sequence with detailed settings
sequence = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True,
    grade_type="multi",  # Enhanced color grading
    orientation="landscape",
    deepthink=True,
    overdrive=True,
    temperature=0.6,
    iterations=2
)

# Update sequence after storyboard changes
client.sequence.update_sequence(
    sequence_id=sequence["sequence_id"],
    update_ai_params=True
)

# Wait for sequence to be ready
completed_sequence = client.sequence.wait_for_sequence(
    sequence_id=sequence["sequence_id"],
    timeout_seconds=600
)

# Get media assets used in the sequence
media = client.sequence.get_sequence_media(
    sequence_id=sequence["sequence_id"],
    include_analysis=True,
    generate_thumbnail=True,
    generate_streamable=True
)

# Track history of sequence changes
history = client.sequence.get_sequence_history(
    sequence_id=sequence["sequence_id"],
    history_type="generation",
    include_current=True
)
```

### AI-Powered Tools

```python
# Generate a creative brief
brief = client.tools.create_creative_brief(
    name="Q4 Campaign Brief",
    user_input="Create a creative brief for our winter product line focusing on indoor comfort and wellness",
    company_details_id=company["company_details_id"],
    deepthink=True,
    overdrive=True,
    web_search=True
)

# Generate audience research
audience = client.tools.create_audience_research(
    name="Home Wellness Audience",
    user_input="Research the audience for premium home wellness products",
    additional_context="Focus on demographics, behaviors, and purchasing patterns of health-conscious homeowners",
    deepthink=True
)

# Create a video plan
plan = client.tools.create_video_plan(
    name="Winter Wellness Campaign",
    user_input="Create a detailed video plan for a series promoting indoor wellness products during winter",
    additional_context="Should cover product benefits, user testimonials, and lifestyle imagery",
    deepthink=True,
    overdrive=True
)

# Generate a shotlist for a specific scene
shotlist = client.tools.create_shotlist(
    name="Product Demo Sequence",
    user_input="Create a shotlist for demonstrating our air purifier's key features",
    scene_details="Modern living room setting, morning light through windows, focus on product operation and air quality indicator",
    visual_style="Clean, bright, minimalist aesthetic with soft natural lighting"
)
```

## Workflow Patterns

Storylinez SDK supports several workflow patterns to fit different use cases:

### Asynchronous Processing with Polling

For long-running operations:

```python
# Start the job
job = client.storyboard.create_storyboard(project_id=project_id)
job_id = job["job_id"]

# Poll for completion
while True:
    status = client.storyboard.get_storyboard(project_id=project_id)
    if status["status"] in ["COMPLETED", "ERROR"]:
        break
    print(f"Status: {status['status']}, progress: {status.get('progress', '?')}%")
    time.sleep(10)
```

### Helper Methods for Waiting

For convenience, many modules offer wait methods:

```python
# Create and wait in one call
storyboard = client.storyboard.create_and_wait(
    project_id=project_id,
    timeout_seconds=300,
    polling_interval=5
)

# Or use the standalone wait method
render = client.render.wait_for_render(
    render_id=render_id,
    timeout_seconds=1200
)
```

### Batch Operations

For processing multiple items:

```python
# Process a batch of videos
video_paths = ["./video1.mp4", "./video2.mp4", "./video3.mp4"]
upload_results = client.storage.batch_upload_files(
    file_paths=video_paths,
    folder_path="/batch_uploads",
    analyze_video=True
)

# Create projects from templates
project_templates = [
    {"name": "Product Demo 1", "orientation": "landscape"},
    {"name": "Product Demo 2", "orientation": "portrait"},
    {"name": "Tutorial Video", "orientation": "landscape"}
]

projects = []
for template in project_templates:
    project = client.project.create_project(**template)
    projects.append(project)
```

### Template-Based Production

For consistent video production:

```python
def create_product_video(product_name, description, features, image_url):
    """Generate a standardized product video based on template"""
    
    # Create project
    project = client.project.create_project(
        name=f"{product_name} Video",
        orientation="landscape"
    )
    project_id = project["project"]["project_id"]
    
    # Create prompt with standardized format
    prompt_text = f"""
    Create a 30-second product video for {product_name}.
    
    Product description:
    {description}
    
    Key features to highlight:
    {", ".join(features)}
    
    Use a professional, modern style with bold typography.
    Include product shots, feature demonstrations, and end with a call to action.
    """
    
    client.prompt.create_text_prompt(
        project_id=project_id,
        main_prompt=prompt_text
    )
    
    # Upload product image if provided
    if image_url:
        # Download and upload image (simplified example)
        import requests
        from io import BytesIO
        
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            client.storage.upload_file_object(
                file_object=image_data,
                filename=f"{product_name}.jpg",
                folder_path="/product_images",
                project_id=project_id
            )
    
    # Generate storyboard and wait for completion
    storyboard = client.storyboard.create_and_wait(
        project_id=project_id,
        timeout_seconds=300
    )
    
    # Apply standard brand
    default_brand = client.brand.get_default()
    client.project.update_project(
        project_id=project_id,
        brand_id=default_brand["brand_id"]
    )
    
    # Create sequence and render
    sequence = client.sequence.create_and_wait(
        project_id=project_id,
        apply_template=True,
        apply_grade=True
    )
    
    render = client.render.create_and_wait(
        project_id=project_id,
        target_width=1920,
        target_height=1080,
        subtitle_enabled=True,
        call_to_action="Visit our website to learn more"
    )
    
    # Return completed video info
    return {
        "project_id": project_id,
        "render_id": render["render_id"],
        "download_url": client.render.get_render(
            render_id=render["render_id"], 
            generate_download_link=True
        ).get("download_url")
    }

# Use the template function
new_product_video = create_product_video(
    product_name="EcoWash 3000",
    description="Revolutionary washing machine that uses 50% less water and energy",
    features=["Eco-Mode", "Smart Detection", "Ultra Capacity", "Whisper Quiet"],
    image_url="https://example.com/images/ecowash3000.jpg"
)
```

## Error Handling & Best Practices

### Validation and Error Handling

The SDK provides comprehensive validation and clear error messages:

```python
try:
    # Invalid parameter (temperature must be 0.0-1.0)
    client.storyboard.create_storyboard(
        project_id=project_id,
        temperature=2.0
    )
except ValueError as e:
    print(f"Validation error: {str(e)}")
    # Output: "Validation error: temperature must be between 0.0 and 1.0"
    
try:
    # Network or API errors
    result = client.project.get_project(project_id="invalid_id")
except requests.RequestException as e:
    print(f"Network error: {str(e)}")
except Exception as e:
    print(f"API error: {str(e)}")
```

### Handling Long-Running Jobs

For operations that may take time:

```python
def create_with_timeout(project_id, max_attempts=12, check_interval=10):
    """Create a storyboard with timeout handling"""
    try:
        # Start the storyboard creation
        job = client.storyboard.create_storyboard(project_id=project_id)
        job_id = job["job_id"]
        
        # Poll for completion with timeout
        attempts = 0
        while attempts < max_attempts:
            status = client.storyboard.get_storyboard(project_id=project_id)
            
            if status["status"] == "COMPLETED":
                return status
            
            if status["status"] == "ERROR":
                error_msg = status.get("error_message", "Unknown error")
                raise Exception(f"Storyboard creation failed: {error_msg}")
                
            print(f"Status: {status['status']}, attempt {attempts+1}/{max_attempts}")
            attempts += 1
            time.sleep(check_interval)
            
        # Timeout reached
        raise TimeoutError(f"Operation timed out after {max_attempts * check_interval} seconds")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

### Resource Management

Best practices for managing SDK resources:

```python
# Organizing content with folders
uploads_folder = client.storage.create_folder(
    folder_path="/projects/campaign_2023/uploads"
)

# Cleaning up temporary resources
tmp_files = client.storage.list_files(
    folder_path="/tmp",
    created_before=(datetime.now() - timedelta(days=7)).isoformat()
)

for file in tmp_files["files"]:
    client.storage.delete_file(file_id=file["file_id"])

# Setting sensible timeouts for operations
try:
    result = client.storyboard.create_and_wait(
        project_id=project_id,
        timeout_seconds=300  # 5 minutes max
    )
except TimeoutError:
    print("Operation is taking longer than expected. Check status later.")
```

## Environment Configuration

The SDK can be configured through environment variables or direct initialization:

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `STORYLINEZ_API_KEY` | API key for authentication | Yes | None |
| `STORYLINEZ_API_SECRET` | API secret for authentication | Yes | None |
| `STORYLINEZ_ORG_ID` | Organization ID | No | None |
| `STORYLINEZ_BASE_URL` | Custom API endpoint | No | `https://api.storylinez.com` |
| `STORYLINEZ_DEBUG` | Enable debug logging | No | `False` |
| `STORYLINEZ_TIMEOUT` | Request timeout in seconds | No | `120` |
| `STORYLINEZ_MAX_RETRIES` | Max retry attempts for failed requests | No | `3` |

### Configuration File

You can also create a config file (`~/.storylinez/config.json`):

```json
{
  "api_key": "api_your_key_here",
  "api_secret": "your_secret_here",
  "org_id": "your_org_id_here",
  "base_url": "https://api.storylinez.com",
  "debug": false,
  "timeout": 120,
  "max_retries": 3
}
```

Load this configuration with:

```python
client = StorylinezClient.from_config()
```

## Performance Considerations

### Rate Limits

The Storylinez API applies rate limits based on your subscription plan:

- Free tier: 60 requests per minute
- Pro tier: 300 requests per minute
- Enterprise: Custom limits

The SDK includes built-in rate limiting and automatic retry logic to handle rate limit errors.

### Batch Operations

For bulk processing, use batch operations when available:

```python
# Better than uploading files in a loop
results = client.storage.batch_upload_files(
    file_paths=[file1, file2, file3],
    folder_path="/batch_uploads"
)

# Better than individual requests
files = client.storage.get_files_by_ids(
    file_ids=["id1", "id2", "id3", "id4", "id5"]
)
```

### Asynchronous Processing

For high-throughput applications, consider asynchronous patterns:

```python
import asyncio
import concurrent.futures

async def process_projects(project_ids):
    # Use a thread pool for concurrent API calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                lambda id=pid: client.project.get_project(project_id=id)
            )
            for pid in project_ids
        ]
        results = await asyncio.gather(*futures)
        return results

# Use the async function
project_ids = ["id1", "id2", "id3", "id4", "id5"]
results = asyncio.run(process_projects(project_ids))
```

## Troubleshooting

### Common Issues and Solutions

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| Authentication failed | Invalid API key | Verify API key and secret are correct |
| Permission denied | Missing role/scope | Check permissions in Storylinez dashboard |
| Rate limit exceeded | Too many requests | Add backoff logic or request rate limit increase |
| Timeout errors | Operation taking too long | Increase timeout value or use asynchronous patterns |
| Resource not found | Incorrect ID or deleted resource | Verify IDs and check if resource exists |

### Debug Mode

Enable debug mode to see detailed request/response information:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('storylinez')
logger.setLevel(logging.DEBUG)

# Create client with debug enabled
client = StorylinezClient(
    api_key="your_key",
    api_secret="your_secret",
    debug=True
)
```

### Checking API Health

Check API service status:

```python
status = client.utils.service_status()
print(f"API Status: {status['status']}")
print(f"API Version: {status['version']}")
```

## API Documentation

For full details on all available methods and parameters, refer to the following resources:

- [Official Storylinez API Documentation](https://docs.storylinez.com)

The SDK examples directory contains additional code samples:

- `examples/project_examples.py` - Project creation and management
- `examples/storyboard_examples.py` - Storyboard generation
- `examples/rendering_examples.py` - Video rendering options
- `examples/branding_examples.py` - Brand styling and presets
- `examples/advanced_workflows.py` - Complex production workflows

## Requirements

- Python 3.6+
- Core dependencies:
  - `requests>=2.25.0`
  - `python-dotenv>=0.15.0`

## Contributing

Contributions to the Storylinez SDK are welcome! Here's how to get started:

1. **Fork the Repository**
   - Create a fork from our main GitHub repository

2. **Set Up Development Environment**
   ```bash
   git clone https://github.com/your-username/Storylinez-SDK.git
   cd Storylinez-SDK
   pip install -e ".[dev]"
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-amazing-feature
   ```

4. **Make Your Changes**
   - Implement your feature or bug fix
   - Add or update tests as necessary
   - Update documentation to reflect changes

5. **Run Tests**
   ```bash
   pytest
   ```

6. **Commit and Push Changes**
   ```bash
   git commit -m "Add detailed description of your changes"
   git push origin feature/your-amazing-feature
   ```

7. **Submit a Pull Request**
   - Open a PR against the main repository
   - Provide a clear description of the changes
   - Reference any related issues

### Code Style Guidelines

- Follow PEP 8 standards
- Add type hints to function signatures
- Include docstrings for all public methods
- Maintain test coverage above 80%

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support with the Storylinez SDK:

- **Documentation:** [https://docs.storylinez.com](https://docs.storylinez.com)
- **Email Support:** support@storylinezads.com

For enterprise customers, please contact your dedicated account manager for priority support.