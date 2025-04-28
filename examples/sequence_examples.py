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
    
    # Example 1: Create a sequence for a project
    print("\n=== Creating a Sequence ===")
    try:
        # First, let's assume we have a project with a storyboard already
        project_id = "project_123abc"
        
        # Create a sequence with custom settings
        sequence_result = client.sequence.create_sequence(
            project_id=project_id,
            apply_template=True,
            apply_grade=True,
            grade_type="single",
            deepthink=True,
            web_search=True,
            temperature=0.8
        )
        
        sequence_id = sequence_result.get("sequence", {}).get("sequence_id")
        job_id = sequence_result.get("job_id")
        
        print(f"Created sequence with ID: {sequence_id}")
        print(f"Sequence generation job ID: {job_id}")
    except Exception as e:
        print(f"Error creating sequence: {str(e)}")
    
    # Example 2: Get sequence details
    print("\n=== Getting Sequence Details ===")
    try:
        # Use an actual sequence_id here
        sequence_id = "sequence_abc123"  # Replace with actual ID
        
        sequence = client.sequence.get_sequence(
            sequence_id=sequence_id,
            include_results=True,
            include_storyboard=False
        )
        
        print(f"Sequence for project: {sequence.get('project_id')}")
        
        # Check if the sequence has been edited
        if sequence.get('edited_sequence'):
            print("This sequence has been edited manually")
            
        # Check job status if available
        if 'old_job_result' in sequence:
            job_status = sequence.get('old_job_result', {}).get('status', 'Unknown')
            print(f"Job status: {job_status}")
    except Exception as e:
        print(f"Error getting sequence: {str(e)}")
    
    # Example 3: Update sequence from storyboard
    print("\n=== Updating Sequence from Storyboard ===")
    try:
        update_result = client.sequence.update_sequence(
            sequence_id="sequence_abc123",  # Replace with actual ID
            update_ai_params=True  # Update AI parameters from the storyboard
        )
        
        print(f"Sequence updated: {update_result.get('message')}")
        print(f"Note: {update_result.get('note')}")
    except Exception as e:
        print(f"Error updating sequence: {str(e)}")
    
    # Example 4: Regenerate a sequence
    print("\n=== Regenerating Sequence ===")
    try:
        redo_result = client.sequence.redo_sequence(
            sequence_id="sequence_abc123",  # Replace with actual ID
            include_history=True,  # Include past history for context
            regenerate_prompt="Add more close-up shots of the product features"
        )
        
        new_job_id = redo_result.get("job_id")
        print(f"Started new sequence generation job with ID: {new_job_id}")
    except Exception as e:
        print(f"Error regenerating sequence: {str(e)}")
    
    # Example 5: Get sequence media information
    print("\n=== Getting Sequence Media ===")
    try:
        media_result = client.sequence.get_sequence_media(
            sequence_id="sequence_abc123",  # Replace with actual ID
            generate_thumbnail=True,
            generate_streamable=True
        )
        
        clips_count = len(media_result.get("media", {}).get("clips", []))
        audios_count = len(media_result.get("media", {}).get("audios", []))
        has_voiceover = media_result.get("media", {}).get("voiceover") is not None
        
        print(f"Sequence contains {clips_count} video clips and {audios_count} audio tracks")
        print(f"Has voiceover: {has_voiceover}")
    except Exception as e:
        print(f"Error getting sequence media: {str(e)}")
    
    # Example 6: Reorder sequence items
    print("\n=== Reordering Sequence Clips ===")
    try:
        # Swap the first and second clips
        reorder_result = client.sequence.reorder_sequence_items(
            sequence_id="sequence_abc123",  # Replace with actual ID
            array_type="clips",
            new_order=[1, 0, 2, 3]  # Swap first two clips, keep others in order
        )
        
        print("Video clips reordered successfully")
    except Exception as e:
        print(f"Error reordering sequence items: {str(e)}")
    
    # Example 7: Edit a sequence item
    print("\n=== Editing a Sequence Item ===")
    try:
        # Update properties of the first clip
        updated_item = {
            "file": "s3://footage/product_demo.mp4",  # Keep same media file
            "in": 10.5,  # Start at 10.5 seconds
            "out": 15.2,  # End at 15.2 seconds
            "transition_in": "fade"  # Add fade transition
        }
        
        edit_result = client.sequence.edit_sequence_item(
            sequence_id="sequence_abc123",  # Replace with actual ID
            item_type="clips",
            item_index=0,  # Edit the first clip
            updated_item=updated_item
        )
        
        print("Sequence item edited successfully")
    except Exception as e:
        print(f"Error editing sequence item: {str(e)}")
    
    # Example 8: Change media in a sequence
    print("\n=== Changing Sequence Media ===")
    try:
        # Replace the second clip with a different file
        change_result = client.sequence.change_sequence_media(
            sequence_id="sequence_abc123",  # Replace with actual ID
            item_type="clips",
            item_index=1,  # Change the second clip
            file_id="file_xyz789"  # Replace with actual file ID
        )
        
        print(f"Media changed successfully to path: {change_result.get('media_path')}")
    except Exception as e:
        print(f"Error changing sequence media: {str(e)}")
    
    # Example 9: Update sequence settings
    print("\n=== Updating Sequence Settings ===")
    try:
        update_settings_result = client.sequence.update_sequence_settings(
            sequence_id="sequence_abc123",  # Replace with actual ID
            apply_grade=True,
            grade_type="multiple",
            temperature=0.7,
            regenerate_prompt="Create a more dynamic flow between clips"
        )
        
        print(f"Sequence settings updated: {update_settings_result.get('message')}")
    except Exception as e:
        print(f"Error updating sequence settings: {str(e)}")
    
    # Example 10: View sequence history
    print("\n=== Viewing Sequence History ===")
    try:
        history_result = client.sequence.get_sequence_history(
            sequence_id="sequence_abc123",  # Replace with actual ID
            page=1,
            limit=5,
            include_current=True
        )
        
        total_history = history_result.get("total_history", 0)
        entries = history_result.get("history", [])
        
        print(f"Found {total_history} history entries")
        for i, entry in enumerate(entries[:3]):  # Show up to 3 entries
            entry_type = entry.get("history_type", "unknown")
            timestamp = entry.get("timestamp", "unknown")
            print(f"{i+1}. Type: {entry_type}, Time: {timestamp}")
    except Exception as e:
        print(f"Error getting sequence history: {str(e)}")

if __name__ == "__main__":
    main()
