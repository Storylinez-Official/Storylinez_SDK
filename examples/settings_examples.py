import os
from dotenv import load_dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables, with fallbacks
API_KEY = os.environ.get("STORYLINEZ_API_KEY", "api_your_key_here")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_secret_here")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

def main():
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Get user settings
    print("\n=== Getting User Settings ===")
    try:
        settings = client.settings.get_settings()
        print("User Settings:")
        print(f"AI Parameters: {settings.get('ai_params', {})}")
        print(f"Link Preferences: {settings.get('link_preferences', {})}")
        print(f"UI Preferences: {settings.get('ui_preferences', {})}")
    except Exception as e:
        print(f"Error getting settings: {str(e)}")
    
    # Example 2: Save all settings using category dictionaries
    print("\n=== Saving All Settings (Using Dictionaries) ===")
    try:
        result = client.settings.save_settings(
            ai_params={
                "temperature": 0.7,
                "iterations": 3,
                "deepthink": True,
                "web_search": False
            },
            link_preferences={
                "generate_thumbnail": True,
                "generate_streamable": False,
                "generate_download": False
            },
            ui_preferences={
                "dark_mode": True,
                "default_view": "list",
                "language": "en"
            }
        )
        print(f"Settings saved successfully: {result.get('message')}")
    except Exception as e:
        print(f"Error saving settings: {str(e)}")
    
    # Example 2B: Save settings using individual parameters
    print("\n=== Saving Settings (Using Individual Parameters) ===")
    try:
        result = client.settings.save_settings(
            temperature=0.75,
            iterations=4,
            dark_mode=True,
            language="en-US",
            generate_thumbnail=True,
            generate_download=True
        )
        print(f"Settings saved successfully: {result.get('message')}")
    except Exception as e:
        print(f"Error saving settings: {str(e)}")
    
    # Example 3: Update specific settings
    print("\n=== Updating Specific Settings ===")
    try:
        result = client.settings.update_settings(
            ai_params={"temperature": 0.8},
            ui_preferences={"current_tab": "projects"}
        )
        print(f"Settings updated successfully: {result.get('message')}")
        print(f"Updated fields: {result.get('updated_fields')}")
    except Exception as e:
        print(f"Error updating settings: {str(e)}")
    
    # Example 4: Reset settings
    print("\n=== Resetting Settings Category ===")
    try:
        result = client.settings.reset_settings(category="ai_params")
        print(f"AI parameters reset to default: {result.get('message')}")
    except Exception as e:
        print(f"Error resetting settings: {str(e)}")
    
    # Example 5: Update theme preference
    print("\n=== Updating Theme ===")
    try:
        result = client.settings.update_theme(dark_mode=True)
        print(f"Theme updated: {result.get('message')}")
        print(f"Dark mode: {result.get('dark_mode')}")
    except Exception as e:
        print(f"Error updating theme: {str(e)}")
    
    # Example 6: Update AI defaults
    print("\n=== Updating AI Defaults ===")
    try:
        result = client.settings.update_ai_defaults(
            temperature=0.6,
            deepthink=True,
            web_search=True
        )
        print(f"AI defaults updated: {result.get('message')}")
        print(f"AI parameters: {result.get('ai_params')}")
    except Exception as e:
        print(f"Error updating AI defaults: {str(e)}")
    
    # Example 7: Add temporary job
    print("\n=== Adding Temporary Job ===")
    try:
        result = client.settings.add_job(
            job_id="job_abc123",
            job_type="query_generation",
            metadata={"query": "product marketing video", "timestamp": "2023-07-29T10:15:00Z"}
        )
        print(f"Job added: {result.get('message')}")
        print(f"Entry ID: {result.get('entry_id')}")
    except Exception as e:
        print(f"Error adding job: {str(e)}")
    
    # Example 8: List jobs
    print("\n=== Listing Temporary Jobs ===")
    try:
        jobs = client.settings.list_jobs(
            job_type="query_generation",
            page=1,
            limit=5
        )
        total_jobs = jobs.get("total", 0)
        job_list = jobs.get("jobs", [])
        print(f"Found {total_jobs} jobs")
        
        for i, job in enumerate(job_list):
            print(f"{i+1}. Job ID: {job.get('job_id')}, Type: {job.get('job_type')}, Created: {job.get('created_at')}")
    except Exception as e:
        print(f"Error listing jobs: {str(e)}")
    
    # Example 9: Fetch job results
    print("\n=== Fetching Job Results ===")
    try:
        job_results = client.settings.fetch_job_results(job_id="job_abc123")
        print(f"Job ID: {job_results.get('job_id')}")
        print(f"Job type: {job_results.get('job_type')}")
        
        # Access result data (depends on job type)
        result_data = job_results.get("result", {})
        if result_data:
            print(f"Status: {result_data.get('status')}")
            if result_data.get('status') == 'completed':
                print(f"Completed at: {result_data.get('completed_at')}")
    except Exception as e:
        print(f"Error fetching job results: {str(e)}")
    
    # Example 10: Delete job
    print("\n=== Deleting Job ===")
    try:
        result = client.settings.delete_job(job_id="job_abc123")
        print(f"Job deleted: {result.get('message')}")
    except Exception as e:
        print(f"Error deleting job: {str(e)}")
    
    # Example 11: Using convenience methods
    print("\n=== Using Helper Methods ===")
    try:
        # Apply a settings preset
        print("Applying 'creative' preset...")
        result = client.settings.apply_preset("creative")
        print(f"Preset applied: {result.get('message')}")
        
        # Toggle theme
        print("\nToggling theme...")
        result = client.settings.toggle_theme()
        print(f"Theme toggled: {result.get('message')}")
        print(f"New theme: {'Dark' if result.get('dark_mode') else 'Light'} mode")
        
        # Backup settings to file
        print("\nBacking up settings...")
        backup_file = client.settings.backup_settings()
        print(f"Settings backed up to: {backup_file}")
        
    except Exception as e:
        print(f"Error using helper methods: {str(e)}")

if __name__ == "__main__":
    main()
