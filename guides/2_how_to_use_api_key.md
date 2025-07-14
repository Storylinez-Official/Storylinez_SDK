# How to Use an API Key - Complete Tutorial

## Overview

This tutorial will guide you through using your Storylinez API key to access the Storylinez API and integrate it into your applications. We'll cover authentication, making API calls, and best practices for using the API effectively.

## Prerequisites

- A valid Storylinez API key and secret (see [How to Make an API Key](./1_how_to_make_api_key.md))
- Basic understanding of HTTP requests and APIs
- A programming environment (Python, JavaScript, etc.) or API testing tool

## Authentication Methods

### Method 1: Header-based Authentication

The primary method for authenticating with the Storylinez API is using headers:

```bash
curl -X GET "https://api.storylinezads.com/status" \
  -H "X-API-Key: your_api_key_here" \
  -H "X-API-Secret: your_api_secret_here"
```

### Method 2: Using the Python SDK (Recommended)

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
status = client.status.get_status()
print(f"API Status: {status}")
```

## Making Your First API Call

### 1. Test API Connection

```python
import requests

def test_api_connection():
    url = "https://api.storylinezads.com/status"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ API connection successful!")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ API connection failed: {response.status_code}")
        print(f"Error: {response.text}")

test_api_connection()
```

### 2. Get User Information

```python
def get_user_info():
    url = "https://api.storylinezads.com/user"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"Welcome, {user_data.get('name', 'User')}!")
        print(f"Email: {user_data.get('email')}")
        print(f"Organization: {user_data.get('organization', {}).get('name')}")
    else:
        print(f"Failed to get user info: {response.status_code}")

get_user_info()
```

## Common API Operations

### 1. Working with Projects

#### Create a Project

```python
def create_project():
    url = "https://api.storylinezads.com/project"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here',
        'Content-Type': 'application/json'
    }
    
    data = {
        "name": "My First Project",
        "orientation": "landscape",
        "purpose": "Testing API integration",
        "target_audience": "Developers"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        project = response.json()
        print(f"✅ Project created successfully!")
        print(f"Project ID: {project['project']['project_id']}")
        return project['project']['project_id']
    else:
        print(f"❌ Failed to create project: {response.status_code}")
        print(f"Error: {response.text}")
        return None
```

#### List Projects

```python
def list_projects():
    url = "https://api.storylinezads.com/project/list"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        projects = response.json()
        print(f"📁 Found {len(projects.get('projects', []))} projects:")
        for project in projects.get('projects', []):
            print(f"  - {project['name']} (ID: {project['project_id']})")
    else:
        print(f"❌ Failed to list projects: {response.status_code}")
```

### 2. Working with Files

#### Upload a File

```python
def upload_file(file_path):
    url = "https://api.storylinezads.com/storage/upload"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here'
    }
    
    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {
            'folder_path': '/uploads',
            'context': 'Uploaded via API'
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        file_data = response.json()
        print(f"✅ File uploaded successfully!")
        print(f"File ID: {file_data['file']['file_id']}")
        return file_data['file']['file_id']
    else:
        print(f"❌ Failed to upload file: {response.status_code}")
        print(f"Error: {response.text}")
        return None
```

### 3. Working with Prompts

#### Create a Text Prompt

```python
def create_text_prompt(project_id):
    url = "https://api.storylinezads.com/prompt/text"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here',
        'Content-Type': 'application/json'
    }
    
    data = {
        "project_id": project_id,
        "main_prompt": "Create a 30-second video about sustainable technology",
        "document_context": "Focus on renewable energy and eco-friendly solutions",
        "temperature": 0.7,
        "total_length": 30
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        prompt_data = response.json()
        print(f"✅ Text prompt created successfully!")
        print(f"Prompt ID: {prompt_data.get('prompt_id')}")
        return prompt_data.get('prompt_id')
    else:
        print(f"❌ Failed to create prompt: {response.status_code}")
        print(f"Error: {response.text}")
        return None
```

### 4. Working with Storyboards

#### Create a Storyboard

```python
def create_storyboard(project_id):
    url = "https://api.storylinezads.com/storyboard/create"
    headers = {
        'X-API-Key': 'your_api_key_here',
        'X-API-Secret': 'your_api_secret_here',
        'Content-Type': 'application/json'
    }
    
    data = {
        "project_id": project_id,
        "deepthink": True,
        "web_search": True
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        storyboard_data = response.json()
        print(f"✅ Storyboard creation started!")
        print(f"Job ID: {storyboard_data.get('job_id')}")
        return storyboard_data.get('job_id')
    else:
        print(f"❌ Failed to create storyboard: {response.status_code}")
        print(f"Error: {response.text}")
        return None
```

## Using the Python SDK

### Installation

```bash
pip install storylinez
```

### Basic Usage

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

# Example: Complete workflow
def complete_workflow():
    try:
        # 1. Create a project
        project = client.project.create_project(
            name="SDK Demo Project",
            orientation="landscape",
            purpose="Demonstrating SDK capabilities"
        )
        project_id = project["project"]["project_id"]
        print(f"✅ Project created: {project_id}")
        
        # 2. Create a text prompt
        client.prompt.create_text_prompt(
            project_id=project_id,
            main_prompt="Create a video about AI technology",
            document_context="Focus on machine learning and neural networks",
            temperature=0.8,
            total_length=45
        )
        print("✅ Text prompt created")
        
        # 3. Create a storyboard
        storyboard_job = client.storyboard.create_storyboard(
            project_id=project_id,
            deepthink=True,
            web_search=True
        )
        print(f"✅ Storyboard job started: {storyboard_job['job_id']}")
        
        # 4. Wait for storyboard completion
        storyboard = client.storyboard.wait_for_storyboard(
            project_id=project_id,
            timeout_seconds=300,
            polling_interval=10
        )
        print("✅ Storyboard completed")
        
        # 5. Get project details
        project_details = client.project.get_project(project_id)
        print(f"📊 Project has {len(project_details.get('storyboard', {}).get('scenes', []))} scenes")
        
    except Exception as e:
        print(f"❌ Error in workflow: {str(e)}")

# Run the workflow
complete_workflow()
```

## Error Handling

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Invalid API credentials
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### Error Handling Examples

```python
import requests
from requests.exceptions import RequestException

def robust_api_call(url, headers, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=30)
        
        # Check for successful response
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("❌ Authentication failed. Check your API key and secret.")
        elif response.status_code == 403:
            print("❌ Insufficient permissions. Check your API key permissions.")
        elif response.status_code == 429:
            print("❌ Rate limit exceeded. Wait before making more requests.")
        elif response.status_code == 500:
            print("❌ Server error. Try again later.")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error details: {response.text}")
        
        return None
        
    except RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return None
```

## Rate Limiting

### Understanding Rate Limits

- Each API key has default rate limits
- Rate limits are enforced per minute
- Different endpoints may have different limits
- You can check your current usage in the dashboard

### Handling Rate Limits

```python
import time
import requests

def make_rate_limited_request(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Rate limit exceeded, wait and retry
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Request failed: {response.status_code}")
            break
    
    return None
```

## Best Practices

### 1. Security
- Store API credentials securely (environment variables)
- Never expose credentials in client-side code
- Use HTTPS for all API calls
- Rotate API keys regularly

### 2. Performance
- Implement proper error handling
- Use exponential backoff for retries
- Cache responses when appropriate
- Monitor your API usage

### 3. Code Organization
- Create wrapper functions for common operations
- Use consistent error handling patterns
- Log API calls for debugging
- Document your API integration

### 4. Example Wrapper Class

```python
class StorylinezAPIWrapper:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.storylinezads.com"
        self.headers = {
            'X-API-Key': self.api_key,
            'X-API-Secret': self.api_secret,
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None
    
    def get_user_info(self):
        return self._make_request('user')
    
    def create_project(self, name, orientation='landscape', purpose=''):
        data = {
            'name': name,
            'orientation': orientation,
            'purpose': purpose
        }
        return self._make_request('project', method='POST', data=data)
    
    def list_projects(self):
        return self._make_request('project/list')

# Usage
api = StorylinezAPIWrapper('your_api_key', 'your_api_secret')
user_info = api.get_user_info()
projects = api.list_projects()
```

## Monitoring and Debugging

### 1. Check API Usage
Monitor your API usage in the Storylinez dashboard:
- Go to Settings > Developer > API Keys
- Click "View Usage" on your API key
- Review usage statistics and recent requests

### 2. Debug Common Issues
- **Authentication errors**: Verify API key and secret
- **Permission errors**: Check allowed methods on your API key
- **Rate limiting**: Monitor your request frequency
- **Network issues**: Implement proper timeout handling

### 3. Logging

```python
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_api_call(url, headers, method='GET', data=None):
    logger.info(f"Making {method} request to {url}")
    
    try:
        response = requests.request(method, url, headers=headers, json=data)
        logger.info(f"Response: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return None
```

## Next Steps

1. **Explore the SDK**: Use the Python SDK for easier integration
2. **Read API Documentation**: Review the full API reference
3. **Build Your Application**: Start integrating Storylinez into your project
4. **Join the Community**: Connect with other developers using Storylinez

## Resources

- [Storylinez SDK Documentation](https://docs.storylinezads.com/sdk)
- [API Reference](https://docs.storylinezads.com/api)
- [Knowledge Base](https://docs.storylinezads.com)
- [LinkedIn Community](https://www.linkedin.com/company/storylinez)

---

*Last updated: January 2025*
