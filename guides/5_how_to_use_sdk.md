# How to Use the SDK and Take Advantage of It Fully - Complete Guide

## Overview

This comprehensive guide will help you master the Storylinez SDK, from basic setup to advanced usage patterns. The SDK provides a powerful Python interface to the Storylinez platform, enabling you to build sophisticated video generation workflows with minimal code.

## What is the Storylinez SDK?

The Storylinez SDK is a Python library that provides:
- **Complete API Coverage**: Access to all Storylinez platform capabilities
- **Simplified Integration**: Easy-to-use Python interface
- **Intelligent Workflows**: Built-in helpers for common tasks
- **Robust Error Handling**: Clear error messages and validation
- **Type Safety**: Full type hints for better development experience

## Installation and Setup

### Installation

```bash
# Standard installation
pip install storylinez

# With development dependencies
pip install storylinez[dev]

# Upgrade to latest version
pip install --upgrade storylinez
```

### Environment Setup

Create a `.env` file in your project root:

```env
STORYLINEZ_API_KEY=api_your_key_here
STORYLINEZ_API_SECRET=your_secret_here
STORYLINEZ_ORG_ID=your_org_id_here
STORYLINEZ_BASE_URL=https://api.storylinezads.com  # Optional, defaults to production
```

### Basic Initialization

```python
from storylinez import StorylinezClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the client
client = StorylinezClient(
    api_key=os.environ.get("STORYLINEZ_API_KEY"),
    api_secret=os.environ.get("STORYLINEZ_API_SECRET"),
    org_id=os.environ.get("STORYLINEZ_ORG_ID")
)

# Test the connection
try:
    status = client.status.get_status()
    print(f"✅ Connected successfully! Status: {status}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## SDK Architecture and Modules

### Core Modules

#### 1. Status Module
```python
# Check system status
status = client.status.get_status()
print(f"System status: {status['status']}")
print(f"API version: {status['version']}")
```

#### 2. User Module
```python
# Get user information
user_info = client.user.get_user_info()
print(f"User: {user_info['name']}")
print(f"Email: {user_info['email']}")

# Update user profile
client.user.update_profile(
    display_name="New Display Name",
    bio="Updated bio information"
)
```

#### 3. Project Module
```python
# Create a new project
project = client.project.create_project(
    name="My SDK Project",
    orientation="landscape",
    purpose="SDK demonstration",
    target_audience="Developers"
)
project_id = project["project"]["project_id"]

# List projects
projects = client.project.list_projects()
for proj in projects["projects"]:
    print(f"Project: {proj['name']} - {proj['project_id']}")

# Get project details
project_details = client.project.get_project(project_id)
print(f"Project status: {project_details['status']}")
```

#### 4. Storage Module
```python
# Upload a file
upload_result = client.storage.upload_file(
    file_path="path/to/your/file.mp4",
    folder_path="/my-uploads",
    context="SDK upload example"
)
file_id = upload_result["file"]["file_id"]

# List files
files = client.storage.list_files(folder_path="/my-uploads")
for file in files["files"]:
    print(f"File: {file['filename']} - {file['file_id']}")

# Download a file
client.storage.download_file(
    file_id=file_id,
    local_path="./downloaded_file.mp4"
)
```

### Content Creation Modules

#### 1. Prompt Module
```python
# Create a text prompt
prompt_result = client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a 30-second video about sustainable technology",
    document_context="Focus on renewable energy and environmental impact",
    temperature=0.7,
    total_length=30
)

# Create a document prompt
doc_result = client.prompt.create_document_prompt(
    project_id=project_id,
    file_id=file_id,
    additional_context="Extract key points for video creation"
)
```

#### 2. Storyboard Module
```python
# Create a storyboard
storyboard_job = client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True
)
print(f"Storyboard job started: {storyboard_job['job_id']}")

# Wait for completion with built-in polling
storyboard = client.storyboard.wait_for_storyboard(
    project_id=project_id,
    timeout_seconds=300,
    polling_interval=10
)
print(f"Storyboard completed with {len(storyboard['scenes'])} scenes")

# Get storyboard details
storyboard_details = client.storyboard.get_storyboard(project_id)
for i, scene in enumerate(storyboard_details['scenes']):
    print(f"Scene {i+1}: {scene['description']}")
```

#### 3. Stock Module
```python
# Search for stock media
stock_results = client.stock.search(
    queries=["technology", "innovation"],
    collections=["videos", "images"],
    num_results_videos=10,
    num_results_images=5
)

# Filter by orientation
landscape_videos = client.stock.search(
    queries=["business meeting"],
    collections=["videos"],
    orientation="landscape",
    num_results_videos=5
)

# Get stock media details
for video in stock_results["videos"]:
    print(f"Video: {video['title']} - Duration: {video['duration']}s")
```

#### 4. Sequence Module
```python
# Create a sequence
sequence_job = client.sequence.create_sequence(
    project_id=project_id,
    use_ai_media=True,
    deepthink=True
)
print(f"Sequence job started: {sequence_job['job_id']}")

# Wait for sequence completion
sequence = client.sequence.wait_for_sequence(
    project_id=project_id,
    timeout_seconds=600,
    polling_interval=15
)
print(f"Sequence completed with {len(sequence['clips'])} clips")

# Get sequence details
sequence_details = client.sequence.get_sequence(project_id)
for i, clip in enumerate(sequence_details['clips']):
    print(f"Clip {i+1}: {clip['start_time']}s - {clip['end_time']}s")
```

#### 5. Voiceover Module
```python
# Create voiceover
voiceover_job = client.voiceover.create_voiceover(
    project_id=project_id,
    voice_id="default",
    speed=1.0,
    pitch=1.0
)
print(f"Voiceover job started: {voiceover_job['job_id']}")

# Wait for voiceover completion
voiceover = client.voiceover.wait_for_voiceover(
    project_id=project_id,
    timeout_seconds=300,
    polling_interval=10
)
print(f"Voiceover completed: {voiceover['duration']}s")

# List available voices
voices = client.voiceover.list_voices()
for voice in voices["voices"]:
    print(f"Voice: {voice['name']} - Language: {voice['language']}")
```

#### 6. Render Module
```python
# Start rendering
render_job = client.render.start_render(
    project_id=project_id,
    quality="high",
    format="mp4",
    resolution="1920x1080"
)
print(f"Render job started: {render_job['job_id']}")

# Wait for render completion
render_result = client.render.wait_for_render(
    project_id=project_id,
    timeout_seconds=900,
    polling_interval=30
)
print(f"Render completed! Download URL: {render_result['download_url']}")

# Get render status
render_status = client.render.get_render_status(project_id)
print(f"Render progress: {render_status['progress']}%")
```

### Management Modules

#### 1. Brand Module
```python
# Create a brand
brand = client.brand.create_brand(
    name="My Brand",
    primary_color="#FF0000",
    secondary_color="#00FF00",
    font_family="Arial",
    logo_url="https://example.com/logo.png"
)
brand_id = brand["brand"]["brand_id"]

# Apply brand to project
client.brand.apply_brand_to_project(
    project_id=project_id,
    brand_id=brand_id
)

# List brands
brands = client.brand.list_brands()
for brand in brands["brands"]:
    print(f"Brand: {brand['name']} - {brand['brand_id']}")
```

#### 2. Search Module
```python
# Search projects
project_results = client.search.search_projects(
    query="marketing video",
    limit=10
)

# Search files
file_results = client.search.search_files(
    query="product demo",
    file_types=["video", "image"],
    limit=5
)

# Advanced search with filters
advanced_results = client.search.advanced_search(
    query="technology",
    content_types=["projects", "files"],
    date_range={"start": "2024-01-01", "end": "2024-12-31"},
    sort_by="relevance"
)
```

## Advanced Usage Patterns

### 1. Complete Video Creation Workflow

```python
def create_complete_video(prompt_text, project_name="Auto-Generated Video"):
    """Complete workflow from prompt to final video"""
    try:
        # Step 1: Create project
        print("📁 Creating project...")
        project = client.project.create_project(
            name=project_name,
            orientation="landscape",
            purpose="Automated video creation"
        )
        project_id = project["project"]["project_id"]
        print(f"✅ Project created: {project_id}")
        
        # Step 2: Create text prompt
        print("✍️ Creating text prompt...")
        client.prompt.create_text_prompt(
            project_id=project_id,
            main_prompt=prompt_text,
            temperature=0.8,
            total_length=60
        )
        print("✅ Text prompt created")
        
        # Step 3: Generate storyboard
        print("🎬 Generating storyboard...")
        storyboard_job = client.storyboard.create_storyboard(
            project_id=project_id,
            deepthink=True,
            web_search=True
        )
        
        storyboard = client.storyboard.wait_for_storyboard(
            project_id=project_id,
            timeout_seconds=300,
            polling_interval=10
        )
        print(f"✅ Storyboard completed with {len(storyboard['scenes'])} scenes")
        
        # Step 4: Create sequence
        print("🎞️ Creating sequence...")
        sequence_job = client.sequence.create_sequence(
            project_id=project_id,
            use_ai_media=True,
            deepthink=True
        )
        
        sequence = client.sequence.wait_for_sequence(
            project_id=project_id,
            timeout_seconds=600,
            polling_interval=15
        )
        print(f"✅ Sequence completed with {len(sequence['clips'])} clips")
        
        # Step 5: Generate voiceover
        print("🎙️ Generating voiceover...")
        voiceover_job = client.voiceover.create_voiceover(
            project_id=project_id,
            voice_id="default",
            speed=1.0
        )
        
        voiceover = client.voiceover.wait_for_voiceover(
            project_id=project_id,
            timeout_seconds=300,
            polling_interval=10
        )
        print(f"✅ Voiceover completed: {voiceover['duration']}s")
        
        # Step 6: Render final video
        print("🎥 Rendering final video...")
        render_job = client.render.start_render(
            project_id=project_id,
            quality="high",
            format="mp4"
        )
        
        render_result = client.render.wait_for_render(
            project_id=project_id,
            timeout_seconds=900,
            polling_interval=30
        )
        print(f"✅ Video rendered! Download URL: {render_result['download_url']}")
        
        return {
            "project_id": project_id,
            "download_url": render_result["download_url"],
            "duration": voiceover["duration"]
        }
        
    except Exception as e:
        print(f"❌ Error in video creation: {e}")
        return None

# Usage
video_result = create_complete_video(
    "Create a video about the future of artificial intelligence and its impact on society"
)
```

### 2. Batch Processing

```python
def process_multiple_videos(prompts):
    """Process multiple videos in parallel"""
    import concurrent.futures
    import time
    
    def create_single_video(prompt_data):
        return create_complete_video(
            prompt_data["prompt"],
            prompt_data["name"]
        )
    
    results = []
    
    # Process in batches to avoid rate limits
    batch_size = 3
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            batch_results = list(executor.map(create_single_video, batch))
            results.extend(batch_results)
        
        # Wait between batches to respect rate limits
        if i + batch_size < len(prompts):
            time.sleep(30)
    
    return results

# Usage
video_prompts = [
    {"prompt": "Create a video about renewable energy", "name": "Renewable Energy Video"},
    {"prompt": "Create a video about space exploration", "name": "Space Exploration Video"},
    {"prompt": "Create a video about artificial intelligence", "name": "AI Technology Video"}
]

batch_results = process_multiple_videos(video_prompts)
```

### 3. Custom Media Integration

```python
def create_video_with_custom_media(prompt_text, media_files):
    """Create video using custom uploaded media"""
    try:
        # Create project
        project = client.project.create_project(
            name="Custom Media Video",
            orientation="landscape"
        )
        project_id = project["project"]["project_id"]
        
        # Upload custom media files
        uploaded_files = []
        for media_file in media_files:
            upload_result = client.storage.upload_file(
                file_path=media_file["path"],
                folder_path="/custom-media",
                context=media_file.get("context", "Custom media for video")
            )
            uploaded_files.append(upload_result["file"]["file_id"])
            
            # Add file to project
            client.project.add_associated_file(
                project_id=project_id,
                file_id=upload_result["file"]["file_id"]
            )
        
        # Create prompt
        client.prompt.create_text_prompt(
            project_id=project_id,
            main_prompt=prompt_text,
            temperature=0.7,
            total_length=45
        )
        
        # Create storyboard
        storyboard_job = client.storyboard.create_storyboard(
            project_id=project_id,
            deepthink=True,
            web_search=False  # Use custom media instead
        )
        
        storyboard = client.storyboard.wait_for_storyboard(
            project_id=project_id,
            timeout_seconds=300
        )
        
        # Create sequence with custom media preference
        sequence_job = client.sequence.create_sequence(
            project_id=project_id,
            use_ai_media=False,  # Prefer custom media
            deepthink=True
        )
        
        sequence = client.sequence.wait_for_sequence(
            project_id=project_id,
            timeout_seconds=600
        )
        
        # Generate voiceover and render
        voiceover_job = client.voiceover.create_voiceover(
            project_id=project_id,
            voice_id="default"
        )
        
        voiceover = client.voiceover.wait_for_voiceover(
            project_id=project_id,
            timeout_seconds=300
        )
        
        render_job = client.render.start_render(
            project_id=project_id,
            quality="high"
        )
        
        render_result = client.render.wait_for_render(
            project_id=project_id,
            timeout_seconds=900
        )
        
        return {
            "project_id": project_id,
            "download_url": render_result["download_url"],
            "custom_files": uploaded_files
        }
        
    except Exception as e:
        print(f"Error creating video with custom media: {e}")
        return None

# Usage
custom_media = [
    {"path": "path/to/product_demo.mp4", "context": "Product demonstration"},
    {"path": "path/to/company_logo.png", "context": "Company branding"},
    {"path": "path/to/background_music.mp3", "context": "Background audio"}
]

custom_video = create_video_with_custom_media(
    "Create a product showcase video highlighting key features",
    custom_media
)
```

### 4. Brand-Consistent Video Creation

```python
def create_branded_video(prompt_text, brand_config):
    """Create video with consistent brand styling"""
    try:
        # Create or get brand
        brand = client.brand.create_brand(
            name=brand_config["name"],
            primary_color=brand_config["primary_color"],
            secondary_color=brand_config["secondary_color"],
            font_family=brand_config["font_family"],
            logo_url=brand_config.get("logo_url")
        )
        brand_id = brand["brand"]["brand_id"]
        
        # Create project
        project = client.project.create_project(
            name=f"Branded Video - {brand_config['name']}",
            orientation="landscape"
        )
        project_id = project["project"]["project_id"]
        
        # Apply brand to project
        client.brand.apply_brand_to_project(
            project_id=project_id,
            brand_id=brand_id
        )
        
        # Create prompt with brand context
        brand_context = f"Brand: {brand_config['name']}. Colors: {brand_config['primary_color']}, {brand_config['secondary_color']}. Style: {brand_config.get('style', 'professional')}"
        
        client.prompt.create_text_prompt(
            project_id=project_id,
            main_prompt=prompt_text,
            document_context=brand_context,
            temperature=0.7,
            total_length=45
        )
        
        # Continue with storyboard, sequence, voiceover, and render
        # ... (similar to previous examples)
        
        return {"project_id": project_id, "brand_id": brand_id}
        
    except Exception as e:
        print(f"Error creating branded video: {e}")
        return None

# Usage
brand_config = {
    "name": "TechCorp",
    "primary_color": "#1E3A8A",
    "secondary_color": "#3B82F6",
    "font_family": "Roboto",
    "logo_url": "https://example.com/logo.png",
    "style": "modern"
}

branded_video = create_branded_video(
    "Create a video about our new product launch",
    brand_config
)
```

## Error Handling and Best Practices

### 1. Comprehensive Error Handling

```python
from storylinez.exceptions import StorylinezAPIError, AuthenticationError, RateLimitError

def robust_video_creation(prompt_text):
    """Video creation with robust error handling"""
    try:
        # Your video creation logic here
        return create_complete_video(prompt_text)
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Check your API key and secret")
        return None
        
    except RateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        print("Wait before making more requests")
        return None
        
    except StorylinezAPIError as e:
        print(f"❌ API error: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Error details: {e.error_details}")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
```

### 2. Retry Logic with Exponential Backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limit hit. Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(base_delay * (attempt + 1))

# Usage
def create_storyboard_with_retry(project_id):
    return retry_with_backoff(
        lambda: client.storyboard.create_storyboard(
            project_id=project_id,
            deepthink=True
        )
    )
```

### 3. Progress Monitoring

```python
def monitor_long_running_task(task_func, check_func, timeout=900, interval=30):
    """Monitor long-running tasks with progress updates"""
    import time
    
    start_time = time.time()
    
    # Start the task
    task_result = task_func()
    print(f"Task started: {task_result.get('job_id', 'N/A')}")
    
    # Monitor progress
    while time.time() - start_time < timeout:
        try:
            status = check_func()
            if status.get('status') == 'completed':
                print("✅ Task completed successfully!")
                return status
            elif status.get('status') == 'failed':
                print("❌ Task failed!")
                return None
            else:
                progress = status.get('progress', 0)
                print(f"⏳ Progress: {progress}%")
                time.sleep(interval)
        except Exception as e:
            print(f"Error checking status: {e}")
            time.sleep(interval)
    
    print("⏰ Task timed out!")
    return None

# Usage
render_result = monitor_long_running_task(
    task_func=lambda: client.render.start_render(project_id, quality="high"),
    check_func=lambda: client.render.get_render_status(project_id),
    timeout=900,
    interval=30
)
```

## Performance Optimization

### 1. Connection Pooling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure session with connection pooling
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=20, pool_maxsize=20)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Use custom session with SDK
client = StorylinezClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    org_id="your_org_id",
    session=session
)
```

### 2. Caching Strategies

```python
import functools
import time

def cache_with_ttl(ttl_seconds=300):
    """Cache function results with time-to-live"""
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        return wrapper
    return decorator

# Cache expensive operations
@cache_with_ttl(ttl_seconds=600)
def get_stock_media(query):
    return client.stock.search(queries=[query], collections=["videos"])

@cache_with_ttl(ttl_seconds=300)
def get_user_brands():
    return client.brand.list_brands()
```

### 3. Batch Operations

```python
def batch_file_operations(file_operations, batch_size=5):
    """Process file operations in batches"""
    results = []
    
    for i in range(0, len(file_operations), batch_size):
        batch = file_operations[i:i+batch_size]
        batch_results = []
        
        for operation in batch:
            try:
                if operation["type"] == "upload":
                    result = client.storage.upload_file(
                        file_path=operation["file_path"],
                        folder_path=operation["folder_path"]
                    )
                elif operation["type"] == "download":
                    result = client.storage.download_file(
                        file_id=operation["file_id"],
                        local_path=operation["local_path"]
                    )
                
                batch_results.append({"success": True, "result": result})
                
            except Exception as e:
                batch_results.append({"success": False, "error": str(e)})
        
        results.extend(batch_results)
        
        # Small delay between batches
        time.sleep(1)
    
    return results
```

## Advanced Features

### 1. Webhook Integration

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle Storylinez webhooks"""
    # Verify webhook signature
    signature = request.headers.get('X-Storylinez-Signature')
    payload = request.get_data()
    
    if not verify_webhook_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401
    
    data = request.json
    event_type = data.get('event_type')
    
    if event_type == 'render.completed':
        handle_render_completed(data)
    elif event_type == 'storyboard.completed':
        handle_storyboard_completed(data)
    
    return jsonify({"status": "success"}), 200

def verify_webhook_signature(payload, signature):
    """Verify webhook signature"""
    webhook_secret = os.environ.get('STORYLINEZ_WEBHOOK_SECRET')
    expected_signature = hmac.new(
        webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

def handle_render_completed(data):
    """Handle render completion event"""
    project_id = data['project_id']
    download_url = data['download_url']
    
    # Process completed render
    print(f"Render completed for project {project_id}")
    # Add your custom logic here
```

### 2. Custom Extensions

```python
class StorylinezExtended(StorylinezClient):
    """Extended client with custom functionality"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_cache = {}
    
    def create_video_from_template(self, template_id, variables):
        """Create video from a predefined template"""
        # Get template
        template = self.get_template(template_id)
        
        # Replace variables in template
        prompt = template['prompt'].format(**variables)
        
        # Create video
        return self.create_complete_video(prompt)
    
    def get_template(self, template_id):
        """Get video template"""
        # Your template logic here
        templates = {
            "product_launch": {
                "prompt": "Create a {duration}-second video about {product_name} launch featuring {key_features}",
                "orientation": "landscape"
            }
        }
        return templates.get(template_id)
    
    def analyze_video_performance(self, project_id):
        """Analyze video performance metrics"""
        # Your analytics logic here
        pass
    
    def bulk_create_videos(self, video_configs):
        """Create multiple videos with different configurations"""
        results = []
        
        for config in video_configs:
            try:
                result = self.create_video_from_template(
                    config['template_id'],
                    config['variables']
                )
                results.append({"success": True, "result": result})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return results

# Usage
extended_client = StorylinezExtended(
    api_key="your_api_key",
    api_secret="your_api_secret",
    org_id="your_org_id"
)

# Create video from template
video_result = extended_client.create_video_from_template(
    "product_launch",
    {
        "duration": 30,
        "product_name": "EcoWidget",
        "key_features": "sustainable materials and energy efficiency"
    }
)
```

## Testing and Debugging

### 1. Unit Testing

```python
import unittest
from unittest.mock import Mock, patch
from storylinez import StorylinezClient

class TestStorylinezIntegration(unittest.TestCase):
    
    def setUp(self):
        self.client = StorylinezClient(
            api_key="test_key",
            api_secret="test_secret",
            org_id="test_org"
        )
    
    @patch('storylinez.client.requests.post')
    def test_create_project(self, mock_post):
        # Mock response
        mock_post.return_value.json.return_value = {
            "project": {"project_id": "test_project_id"}
        }
        mock_post.return_value.status_code = 201
        
        # Test
        result = self.client.project.create_project(
            name="Test Project",
            orientation="landscape"
        )
        
        # Assertions
        self.assertEqual(result["project"]["project_id"], "test_project_id")
        mock_post.assert_called_once()
    
    def test_validation_errors(self):
        # Test validation
        with self.assertRaises(ValueError):
            self.client.project.create_project(
                name="",  # Empty name should raise error
                orientation="landscape"
            )

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Testing

```python
import pytest
from storylinez import StorylinezClient

@pytest.fixture
def client():
    return StorylinezClient(
        api_key=os.environ.get("TEST_API_KEY"),
        api_secret=os.environ.get("TEST_API_SECRET"),
        org_id=os.environ.get("TEST_ORG_ID")
    )

def test_full_workflow(client):
    """Test complete video creation workflow"""
    # Create project
    project = client.project.create_project(
        name="Integration Test Project",
        orientation="landscape"
    )
    project_id = project["project"]["project_id"]
    
    # Create prompt
    client.prompt.create_text_prompt(
        project_id=project_id,
        main_prompt="Test video creation",
        total_length=10
    )
    
    # Create storyboard
    storyboard_job = client.storyboard.create_storyboard(
        project_id=project_id,
        deepthink=False
    )
    
    # Wait for completion
    storyboard = client.storyboard.wait_for_storyboard(
        project_id=project_id,
        timeout_seconds=120
    )
    
    # Verify results
    assert storyboard is not None
    assert len(storyboard["scenes"]) > 0
    
    # Cleanup
    client.project.delete_project(project_id)
```

### 3. Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Initialize client with debug mode
client = StorylinezClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    org_id="your_org_id",
    debug=True
)

# All API calls will now log detailed information
```

## Best Practices Summary

### 1. Code Organization
- Use environment variables for credentials
- Implement proper error handling
- Create reusable wrapper functions
- Use type hints for better code quality

### 2. Performance
- Implement caching for expensive operations
- Use batch processing for multiple operations
- Monitor API rate limits
- Optimize polling intervals

### 3. Security
- Never hardcode API credentials
- Use HTTPS for all connections
- Implement proper authentication validation
- Regularly rotate API keys

### 4. Monitoring
- Log all API interactions
- Monitor error rates and response times
- Set up alerts for failures
- Track usage patterns

### 5. Testing
- Write unit tests for your integration
- Use integration tests for workflows
- Test error scenarios
- Validate data formats

## Resources and Next Steps

### Documentation
- [SDK Documentation](https://docs.storylinezads.com/sdk)
- [API Reference](https://docs.storylinezads.com/api)
- [Knowledge Base](https://docs.storylinezads.com)

### Community
- [LinkedIn](https://www.linkedin.com/company/storylinez)
- [Help Center](https://app.storylinezads.com/help)
- [Knowledge Base](https://docs.storylinezads.com)

### Support
- [Documentation](https://docs.storylinezads.com)
- [Email Support](mailto:support@storylinezads.com)
- [Help Center](https://app.storylinezads.com/help)

---

*Last updated: January 2025*
