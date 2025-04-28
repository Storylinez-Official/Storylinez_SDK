from storylinez import StorylinezClient
import time

# Replace these with your actual credentials
API_KEY = "api_your_key_here"
API_SECRET = "your_secret_here"
ORG_ID = "your_org_id_here"

def main():
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Create a render for a project
    print("\n=== Creating a Render ===")
    try:
        # For this example, assume we have a project with a completed sequence
        project_id = "project_123abc"
        
        # Create a render with custom settings
        render_result = client.render.create_render(
            project_id=project_id,
            # Video dimensions (must match project orientation)
            target_width=1920,
            target_height=1080,
            # Audio settings
            bg_music_volume=0.5,
            video_audio_volume=0.7,
            voiceover_volume=1.0,
            # Subtitle settings
            subtitle_enabled=True,
            subtitle_font_size=36,
            subtitle_color=(255, 255, 255, 255),
            subtitle_bg_color=(0, 0, 0, 180),
            # Outro settings
            outro_duration=5.0,
            company_name="Acme Corporation",
            company_subtext="Building the Future Today",
            # CTA settings
            call_to_action="Visit Our Website",
            call_to_action_subtext="www.acmecorp.com",
            enable_cta=True
        )
        
        render_id = render_result.get("render", {}).get("render_id")
        job_id = render_result.get("job_id")
        
        print(f"Created render with ID: {render_id}")
        print(f"Render job ID: {job_id}")
    except Exception as e:
        print(f"Error creating render: {str(e)}")
    
    # Example 2: Get render details and status
    print("\n=== Getting Render Details ===")
    try:
        # Use an actual render_id here
        render_id = "render_abc123"  # Replace with actual ID
        
        render = client.render.get_render(
            render_id=render_id,
            include_results=True,
            include_sequence=False,  # Skip large sequence data
            generate_download_link=True
        )
        
        # Check job status
        if 'job_result' in render:
            job_status = render.get('job_result', {}).get('status', 'Unknown')
            print(f"Render status: {job_status}")
            
            # If completed, print download link
            if job_status == 'COMPLETED' and 'download_url' in render:
                print(f"Download URL available: {render.get('download_url')[:50]}...")
        else:
            print("Job result not available yet")
    except Exception as e:
        print(f"Error getting render details: {str(e)}")
    
    # Example 3: Update render settings
    print("\n=== Updating Render Settings ===")
    try:
        # Update render settings without regenerating
        update_result = client.render.update_render_settings(
            render_id="render_abc123",  # Replace with actual ID
            bg_music_volume=0.4,  # Lower background music
            subtitle_bg_opacity=0.6,  # More transparent subtitle background
            outro_duration=6.0  # Longer outro
        )
        
        print(f"Settings updated: {update_result.get('message')}")
        print(f"Note: {update_result.get('note')}")
    except Exception as e:
        print(f"Error updating render settings: {str(e)}")
    
    # Example 4: Redo a render with updated settings
    print("\n=== Redoing Render ===")
    try:
        # Regenerate the render with some new settings
        redo_result = client.render.redo_render(
            render_id="render_abc123",  # Replace with actual ID
            color_exposure_fix=True,  # Enable exposure correction
            color_contrast_fix=True   # Enable contrast correction
        )
        
        new_job_id = redo_result.get("job_id")
        print(f"Started new render job with ID: {new_job_id}")
    except Exception as e:
        print(f"Error redoing render: {str(e)}")
    
    # Example 5: Get render status
    print("\n=== Checking Render Status ===")
    try:
        # Get simplified status info
        status_info = client.render.get_render_status(
            render_id="render_abc123"  # Replace with actual ID
        )
        
        print(f"Render status: {status_info.get('status')}")
        print(f"Created: {status_info.get('created_at')}")
        print(f"Updated: {status_info.get('updated_at')}")
        print(f"Is stale: {status_info.get('is_stale', False)}")
    except Exception as e:
        print(f"Error checking render status: {str(e)}")
    
    # Example 6: Get render download links
    print("\n=== Getting Render Download Links ===")
    try:
        # For this example, let's assume the render is completed
        # In a real app, you would poll for status or use a webhook
        links = client.render.get_render_download_links(
            render_id="render_abc123"  # Replace with actual ID
        )
        
        if 'download_url' in links:
            print(f"Download URL: {links['download_url'][:50]}...")
        if 'streamable_url' in links:
            print(f"Streaming URL: {links['streamable_url'][:50]}...")
        if 'thumbnail_streamable_url' in links:
            print(f"Thumbnail URL: {links['thumbnail_streamable_url'][:50]}...")
        if 'srt_download_url' in links:
            print(f"Subtitles URL: {links['srt_download_url'][:50]}...")
    except Exception as e:
        print(f"Error getting download links or render not complete: {str(e)}")
    
    # Example 7: Update render with latest sequence data
    print("\n=== Updating Render from Sequence ===")
    try:
        # Update the render with the latest sequence data
        update_result = client.render.update_render(
            render_id="render_abc123",  # Replace with actual ID
            # Optional list of specific fields to update
            fields_to_update=["sequence", "subtitles"]
        )
        
        print(f"Render updated: {update_result.get('message')}")
        print(f"Note: {update_result.get('note')}")
    except Exception as e:
        print(f"Error updating render from sequence: {str(e)}")

if __name__ == "__main__":
    main()
