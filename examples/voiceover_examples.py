import os
import time
from dotenv import load_dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables or use placeholders
API_KEY = os.environ.get("STORYLINEZ_API_KEY", "api_your_key_here")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_secret_here")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

def main():
    # Check if API credentials are properly set
    if API_KEY == "api_your_key_here" or API_SECRET == "your_secret_here":
        print("Warning: API credentials not found in environment variables.")
        print("Please set STORYLINEZ_API_KEY and STORYLINEZ_API_SECRET in your .env file.")
    
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Create a voiceover for a project
    print("\n=== Creating a Voiceover ===")
    try:
        # First, make sure you have a project with a storyboard
        # For this example, assume we have a project with completed storyboard
        project_id = os.environ.get("EXAMPLE_PROJECT_ID", "project_123abc")
        
        # Get available voice types to choose from
        try:
            voices = client.voiceover.get_voice_types()
            print(f"Available voices: {list(voices.get('voice_types', {}).keys())[:3]}...")  # Show first 3 voices
            
            # You might want to find voices by language
            english_voices = [name for name, data in voices.get('voice_types', {}).items() 
                             if name.startswith('en-')]
            print(f"English voices: {english_voices[:3]}...")
        except Exception as e:
            print(f"Could not fetch voice types: {str(e)}")
        
        # Create voiceover with a specific voice
        voiceover_result = client.voiceover.create_voiceover(
            project_id=project_id,
            voiceover_code="en-US-Neural2-F"  # Example voice code
        )
        
        voiceover_id = voiceover_result.get("voiceover", {}).get("voiceover_id")
        job_id = voiceover_result.get("job_id")
        
        print(f"Created voiceover with ID: {voiceover_id}")
        print(f"Voiceover generation job ID: {job_id}")
    except Exception as e:
        print(f"Error creating voiceover: {str(e)}")
    
    # Example 2: Get voiceover details with enhanced error checking
    print("\n=== Getting Voiceover Details ===")
    try:
        # You would use an actual voiceover_id or project_id here
        voiceover = client.voiceover.get_voiceover(
            project_id=project_id,
            include_results=True,
            include_storyboard=False,
            generate_audio_link="true"  # Demonstrating string boolean conversion
        )
        
        # Check if the voiceover processing is complete
        job_status = voiceover.get('job_result', {}).get('status', 'Unknown')
        print(f"Voiceover job status: {job_status}")
        
        # If the voiceover is complete, get the audio URL
        if job_status == 'COMPLETED' and 'audio_url' in voiceover:
            print(f"Voiceover audio available at: {voiceover.get('audio_url')[:50]}...")
            
            # Check for certain properties
            if 'storyboard' in voiceover:
                print("Voiceover includes storyboard data")
            
            # Get useful metadata
            created_at = voiceover.get('created_at', 'Unknown')
            print(f"Voiceover was created at: {created_at}")
    except Exception as e:
        print(f"Error getting voiceover: {str(e)}")
    
    # Example 3: Using wait_for_completion to monitor a job until it's done
    print("\n=== Creating and Waiting for Voiceover Completion ===")
    try:
        # Create a new project ID for this example
        # In real usage, you would use an actual project ID
        test_project_id = "project_wait_test"
        
        print("Starting create_and_wait operation (shortcut method)...")
        # This will create a new voiceover and wait for it to complete
        try:
            # Setting a short timeout for example purposes
            completed_voiceover = client.voiceover.create_and_wait(
                project_id=test_project_id,
                voiceover_code="en-GB-Neural2-B",
                timeout_seconds=30,  # Short timeout for example
                poll_interval=2
            )
            print("Voiceover completed successfully!")
            print(f"Audio URL: {completed_voiceover.get('audio_url', 'Not available')[:50]}...")
        except TimeoutError:
            print("Voiceover didn't complete within the timeout period.")
            print("(This is expected in this example due to the short timeout)")
    except Exception as e:
        print(f"Error in create and wait: {str(e)}")
    
    # Example 4: Get or create voiceover pattern
    print("\n=== Get or Create Voiceover Pattern ===")
    try:
        # This will check if a voiceover exists for the project and create one if not
        existing_project_id = os.environ.get("EXAMPLE_EXISTING_PROJECT_ID", "project_with_existing_voiceover")
        
        print(f"Checking if voiceover exists for project {existing_project_id}...")
        voiceover = client.voiceover.get_or_create_voiceover(
            project_id=existing_project_id,
            voiceover_code="en-US-Neural2-D",
            wait_for_completion=False  # Set to True to wait for completion
        )
        
        if 'job_id' in voiceover:
            print("New voiceover was created.")
        else:
            print("Existing voiceover was found.")
    except Exception as e:
        print(f"Error in get_or_create: {str(e)}")
    
    # Example 5: Retrieving and downloading voiceover history
    print("\n=== Viewing and Using Voiceover History ===")
    try:
        # Get history of a specific voiceover
        sample_voiceover_id = os.environ.get("EXAMPLE_VOICEOVER_ID", "voiceover_xyz123")
        
        try:
            history = client.voiceover.get_voiceover_history(
                voiceover_id=sample_voiceover_id,
                page=1,
                limit=5
            )
            
            total_history = history.get("total_history", 0)
            jobs = history.get("jobs", [])
            
            print(f"Found {total_history} voiceover job history entries")
            
            # Demonstrate parsing the job history data
            for i, job_entry in enumerate(jobs[:3]):  # Show up to 3 entries
                job_id = job_entry.get('job_id')
                job = job_entry.get('job', {})
                status = job.get('status', 'unknown')
                created_at = job.get('created_at', 'unknown')
                
                # Format created_at if it's an ISO timestamp
                try:
                    if isinstance(created_at, str) and 'T' in created_at:
                        from datetime import datetime
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        created_at = dt.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    pass  # Keep original if parsing fails
                
                print(f"{i+1}. Job ID: {job_id}, Status: {status}, Created: {created_at}")
                
                # If job has results, check for specific properties
                if 'results' in job:
                    result_size = len(str(job['results']))
                    print(f"   Results size: {result_size} characters")
        except Exception as e:
            print(f"Could not fetch voiceover history: {str(e)}")
            
        # Example of downloading a voiceover
        print("\nDownloading a voiceover file (example):")
        try:
            # In a real application, uncomment this code to actually download the file
            # output_path = client.voiceover.download_voiceover(
            #     voiceover_id=sample_voiceover_id,
            #     output_path="./downloaded_voiceover.wav"
            # )
            # print(f"Successfully downloaded voiceover to {output_path}")
            
            print("Download example (commented out to prevent actual download)")
        except Exception as e:
            print(f"Could not download voiceover: {str(e)}")
    except Exception as e:
        print(f"Error in history example: {str(e)}")
    
    # Example 6: Using a custom uploaded voiceover file
    print("\n=== Working with Custom Uploaded Voiceover Files ===")
    try:
        # In a real application, you would specify an actual audio file path and project ID
        # file_path = "./my_custom_voiceover.mp3"
        # project_id = "my_project_123"
        
        # Example of the upload workflow
        print("Custom voiceover upload workflow (example):")
        print("1. Prepare your audio file in a supported format (mp3, wav, etc.)")
        print("2. Use upload_voiceover_file() to upload and associate with a project")
        print("3. The system will automatically update the project's voiceover mode")
        
        # Example of converting a text file to audio locally before uploading
        print("\nExample workflow for text-to-speech and then upload:")
        print("1. Extract text from your storyboard")
        print("2. Use a local TTS library to create an audio file")
        print("3. Upload the resulting audio file using upload_voiceover_file()")
        
        # Demonstrate code pattern (commented out)
        print("\nExample code (not executed):")
        print("```python")
        print("# Extract text from storyboard")
        print("voiceover_text = extract_text_from_storyboard(storyboard_data)")
        print("# Create audio with local TTS library")
        print("audio_path = create_audio_with_local_tts(voiceover_text)")
        print("# Upload to project")
        print("client.voiceover.upload_voiceover_file(")
        print("    project_id=project_id,")
        print("    file_path=audio_path,")
        print("    voice_name='My Custom Professional Voice'")
        print(")")
        print("```")
    except Exception as e:
        print(f"Error in custom voiceover example: {str(e)}")
    
    print("\n=== Completed Voiceover Examples ===")

if __name__ == "__main__":
    main()
