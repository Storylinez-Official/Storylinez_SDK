from storylinez import StorylinezClient

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
    
    # Example 1: Create a voiceover for a project
    print("\n=== Creating a Voiceover ===")
    try:
        # First, make sure you have a project with a storyboard
        # For this example, assume we have a project with completed storyboard
        project_id = "project_123abc"
        
        # Get available voice types to choose from
        voices = client.voiceover.get_voice_types()
        print(f"Available voices: {list(voices.keys())[:3]}...")  # Show first 3 voices
        
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
    
    # Example 2: Get voiceover details
    print("\n=== Getting Voiceover Details ===")
    try:
        # You would use an actual voiceover_id or project_id here
        voiceover = client.voiceover.get_voiceover(
            project_id=project_id,
            include_results=True,
            include_storyboard=False,
            generate_audio_link=True
        )
        
        # Check if the voiceover processing is complete
        job_status = voiceover.get('job_result', {}).get('status', 'Unknown')
        print(f"Voiceover job status: {job_status}")
        
        # If the voiceover is complete, get the audio URL
        if job_status == 'COMPLETED' and 'audio_url' in voiceover:
            print(f"Voiceover audio available at: {voiceover.get('audio_url')[:50]}...")
    except Exception as e:
        print(f"Error getting voiceover: {str(e)}")
    
    # Example 3: Regenerate a voiceover
    print("\n=== Regenerating Voiceover ===")
    try:
        # Regenerate the voiceover with a different voice
        redo_result = client.voiceover.redo_voiceover(
            project_id=project_id,
            voiceover_code="en-US-Neural2-M"  # Different voice
        )
        
        new_job_id = redo_result.get("job_id")
        print(f"Started new voiceover generation job with ID: {new_job_id}")
    except Exception as e:
        print(f"Error regenerating voiceover: {str(e)}")
    
    # Example 4: Update voiceover data from storyboard
    print("\n=== Updating Voiceover Data ===")
    try:
        update_result = client.voiceover.update_voiceover_data(
            project_id=project_id
        )
        
        print(f"Voiceover data updated with latest storyboard information")
        print(f"Note: {update_result.get('note')}")
    except Exception as e:
        print(f"Error updating voiceover data: {str(e)}")
    
    # Example 5: Upload a custom voiceover file
    print("\n=== Uploading Custom Voiceover File ===")
    try:
        # Upload a local audio file to use as voiceover
        # In a real scenario, this would be a path to an actual audio file
        # client.voiceover.upload_voiceover_file(
        #     project_id=project_id,
        #     file_path="path/to/custom_voiceover.mp3",
        #     voice_name="Professional Voice Actor"
        # )
        
        print("Custom voiceover upload example (commented out to avoid errors)")
    except Exception as e:
        print(f"Error uploading custom voiceover: {str(e)}")
    
    # Example 6: Get voiceover history
    print("\n=== Viewing Voiceover History ===")
    try:
        # Get history of voiceover jobs for a specific voiceover
        history_result = client.voiceover.get_voiceover_history(
            voiceover_id="voiceover_xyz123",  # Replace with actual ID
            page=1,
            limit=5
        )
        
        total_history = history_result.get("total_history", 0)
        jobs = history_result.get("jobs", [])
        
        print(f"Found {total_history} voiceover job history entries")
        for i, job_entry in enumerate(jobs[:3]):  # Show up to 3 entries
            job_id = job_entry.get('job_id')
            job = job_entry.get('job', {})
            status = job.get('status', 'unknown')
            timestamp = job.get('created_at', 'unknown')
            print(f"{i+1}. Job ID: {job_id}, Status: {status}, Created: {timestamp}")
    except Exception as e:
        print(f"Error getting voiceover history: {str(e)}")
    
    # Example 7: Remove voiceover from project
    print("\n=== Removing Voiceover from Project ===")
    try:
        # This would remove the voiceover from the project
        # client.voiceover.remove_voiceover_from_project(
        #     project_id=project_id
        # )
        
        print("Remove voiceover example (commented out to avoid errors)")
    except Exception as e:
        print(f"Error removing voiceover: {str(e)}")

if __name__ == "__main__":
    main()
