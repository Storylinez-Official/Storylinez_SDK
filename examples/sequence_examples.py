from storylinez import StorylinezClient
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
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
    
    # Example 1: Create a sequence for a project
    print("\n=== Creating a Sequence ===")
    try:
        # First, let's assume we have a project with a storyboard already
        project_id = "project_123abc"
        
        # Create a sequence with custom settings
        # Note: The SDK now validates parameters before making API calls
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
        
        # Display some detailed information about each clip
        print("\nClip details:")
        for i, clip in enumerate(media_result.get("media", {}).get("clips", [])):
            print(f"  Clip {i+1}: {clip.get('file_id')} - Duration: {clip.get('sequence_metadata', {}).get('out', 0) - clip.get('sequence_metadata', {}).get('in', 0):.1f}s")
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
            grade_type="multi",
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

    # Example 11: Using the convenience method to update and regenerate in one step
    print("\n=== Update and Regenerate Sequence ===")
    try:
        result = client.sequence.update_and_regenerate(
            sequence_id="sequence_abc123",  # Replace with actual ID
            regenerate_prompt="Make transitions smoother and use more dynamic shots",
            include_history=True
        )
        
        print(f"Sequence updated and regeneration job started with ID: {result.get('job_id')}")
    except Exception as e:
        print(f"Error updating and regenerating sequence: {str(e)}")

    # Example 12: Swap two clips in the sequence
    print("\n=== Swapping Two Clips ===")
    try:
        swap_result = client.sequence.swap_media(
            sequence_id="sequence_abc123",  # Replace with actual ID
            first_item_index=0,
            second_item_index=2,
            array_type="clips"
        )
        
        print("First and third clips swapped successfully")
    except Exception as e:
        print(f"Error swapping clips: {str(e)}")
    
    # Example 13: Using the chat-like experience with sequences
    print("\n=== Chat-Like Experience with Sequences ===")
    try:
        # Get a sequence to work with
        sequence_id = "sequence_abc123"  # Replace with actual ID
        
        # Start a conversation with the AI using a natural language prompt
        print("Sending first prompt to the AI...")
        chat_result = client.sequence.send_chat_prompt(
            sequence_id=sequence_id,
            prompt="Make transitions between scenes smoother and use more dynamic camera movements",
            include_history=True
        )
        
        print(f"Chat prompt sent, job ID: {chat_result.get('job_id')}")
        print("Processing request (in a real app, you'd handle this asynchronously)...")
        
        # In a real app, you'd poll for job completion or use webhooks
        # For this example, we'll just wait a moment and then continue the conversation
        time.sleep(2)  # This is just for the example - don't actually do this in production
        
        # Continue the conversation with a follow-up prompt
        print("\nAI has responded. Sending follow-up prompt...")
        followup_result = client.sequence.send_chat_prompt(
            sequence_id=sequence_id,
            prompt="I like the smooth transitions. Now make the color grade more cinematic and dramatic.",
            include_history=True
        )
        
        print(f"Follow-up prompt sent, job ID: {followup_result.get('job_id')}")
        
        # Retrieve the conversation history
        print("\nRetrieving conversation history...")
        chat_history = client.sequence.get_chat_history(
            sequence_id=sequence_id,
            limit=10
        )
        
        # Display the conversation in a chat-like format
        print("\n=== Sequence Chat History ===")
        for entry in chat_history.get("conversation", []):
            role = entry.get("role", "unknown")
            timestamp = entry.get("timestamp", "")
            
            if role == "user":
                print(f"\n👤 USER ({timestamp}):")
                print(f"  {entry.get('content', '')}")
            elif role == "assistant":
                print(f"\n🤖 AI ({timestamp}):")
                summary = entry.get("sequence_data_summary", {})
                print(f"  Generated sequence with {summary.get('clip_count', 0)} clips")
                print(f"  Approximate duration: {summary.get('approximate_duration', 0):.1f} seconds")
                print(f"  Audio tracks: {summary.get('audio_track_count', 0)}")
        
        print("\n=== End of Conversation ===")
        
        # Example of restoring a previous version from history
        print("\n=== Restoring a Previous Version ===")
        # Get the first generation timestamp from history
        history_entries = client.sequence.get_sequence_history(
            sequence_id=sequence_id,
            history_type="generation",
            limit=5
        ).get("history", [])
        
        if history_entries:
            # Get the timestamp of the first generation
            timestamp = history_entries[0].get("timestamp")
            print(f"Found history entry from {timestamp}")
            
            # Restore this version
            restore_result = client.sequence.restore_version(
                sequence_id=sequence_id,
                history_timestamp=timestamp,
                regenerate_prompt="Restore this version but make colors more vibrant"
            )
            
            print(f"Previous version restored and regeneration job started with ID: {restore_result.get('job_id')}")
        else:
            print("No history entries found to restore")
        
    except Exception as e:
        print(f"Error using chat-like experience: {str(e)}")
    
    # Example 14: Progressive conversation with references to previous changes
    print("\n=== Progressive Conversation with Context ===")
    try:
        # Example showing how the AI maintains context between messages
        sequence_id = "sequence_abc123"  # Replace with actual ID
        
        print("Starting a progressive conversation referencing previous changes...")
        steps = [
            "Start with smoother transitions between clips",
            "Keep the transitions but make the music more upbeat in the middle section",
            "I like the music changes. Now adjust the timing of clips 3-5 to be faster paced"
        ]
        
        # Send each prompt in sequence, building a conversation
        for i, prompt in enumerate(steps):
            print(f"\nStep {i+1}: {prompt}")
            result = client.sequence.send_chat_prompt(
                sequence_id=sequence_id,
                prompt=prompt,
                include_history=True  # This is key for maintaining context
            )
            
            print(f"Prompt sent, job ID: {result.get('job_id')}")
            
            # In a real app, you'd wait for job completion before sending next prompt
            # This is just to simulate the conversation flow
            if i < len(steps) - 1:
                print("AI is processing... (simulated)")
                time.sleep(1)  # This is just for the example
        
        print("\nThis progressive conversation demonstrates how the AI maintains context")
        print("Each prompt builds on previous ones, creating a natural editing workflow")
    
    except Exception as e:
        print(f"Error in progressive conversation: {str(e)}")

if __name__ == "__main__":
    main()
