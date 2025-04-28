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
    
    # Example 1: Create a storyboard for a project
    print("\n=== Creating a Storyboard ===")
    try:
        # First, create a project (if you don't have one already)
        project_result = client.project.create_project(
            name="Product Launch Video",
            orientation="landscape",
            purpose="Showcase new product features"
        )
        project_id = project_result.get("project", {}).get("project_id")
        
        # Then, create a text prompt for the project
        prompt_result = client.prompt.create_text_prompt(
            project_id=project_id,
            main_prompt="Create a promotional video for our new eco-friendly product line",
            document_context="The product uses recycled materials and reduces carbon footprint by 30%.",
            temperature=0.7
        )
        
        # Now create the storyboard
        storyboard_result = client.storyboard.create_storyboard(
            project_id=project_id,
            deepthink=True,
            web_search=True,
            temperature=0.7
        )
        
        storyboard_id = storyboard_result.get("storyboard", {}).get("storyboard_id")
        job_id = storyboard_result.get("job_id")
        
        print(f"Created storyboard with ID: {storyboard_id}")
        print(f"Storyboard generation job ID: {job_id}")
    except Exception as e:
        print(f"Error creating storyboard: {str(e)}")
    
    # Example 2: Get storyboard details
    print("\n=== Getting Storyboard Details ===")
    try:
        # You would use an actual storyboard_id here
        storyboard_id = "your_storyboard_id_here"  # Replace with actual ID
        
        storyboard = client.storyboard.get_storyboard(
            storyboard_id=storyboard_id,
            include_results=True
        )
        
        print(f"Storyboard status: {'Edited' if storyboard.get('edited_storyboard') else 'Original'}")
        print(f"Created at: {storyboard.get('created_at')}")
        print(f"Last updated: {storyboard.get('updated_at')}")
        
        # For demonstration, we'll print just a few key details
        if 'old_job_result' in storyboard:
            job_status = storyboard.get('old_job_result', {}).get('status', 'Unknown')
            print(f"Job status: {job_status}")
    except Exception as e:
        print(f"Error getting storyboard: {str(e)}")
    
    # Example 3: Update a storyboard with the latest project data
    print("\n=== Updating Storyboard ===")
    try:
        # Use an actual storyboard_id
        update_result = client.storyboard.update_storyboard(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            update_ai_params=True  # Update AI parameters from the project's prompt
        )
        
        print("Storyboard updated successfully")
    except Exception as e:
        print(f"Error updating storyboard: {str(e)}")
    
    # Example 4: Modify storyboard values
    print("\n=== Modifying Storyboard Values ===")
    try:
        # Update parameters and add regeneration prompt
        modify_result = client.storyboard.update_storyboard_values(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            regeneration_prompt="Add more close-up shots of the product features",
            temperature=0.8,
            deepthink=True
        )
        
        print("Storyboard values modified successfully")
    except Exception as e:
        print(f"Error modifying storyboard: {str(e)}")
    
    # Example 5: Redo a storyboard generation job
    print("\n=== Redoing Storyboard Generation ===")
    try:
        redo_result = client.storyboard.redo_storyboard(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            include_history=True  # Include history for context
        )
        
        new_job_id = redo_result.get("job_id")
        print(f"Started new storyboard generation job with ID: {new_job_id}")
    except Exception as e:
        print(f"Error redoing storyboard: {str(e)}")
    
    # Example 6: Get storyboard media
    print("\n=== Getting Storyboard Media ===")
    try:
        media_result = client.storyboard.get_storyboard_media(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            generate_thumbnail=True,
            generate_streamable=True
        )
        
        video_count = media_result.get("counts", {}).get("videos", 0)
        music_count = media_result.get("counts", {}).get("background_music", 0)
        has_voiceover = media_result.get("counts", {}).get("has_voiceover", False)
        
        print(f"Storyboard contains {video_count} videos and {music_count} audio tracks")
        print(f"Has voiceover: {has_voiceover}")
    except Exception as e:
        print(f"Error getting storyboard media: {str(e)}")
    
    # Example 7: Reorder items in a storyboard
    print("\n=== Reordering Storyboard Items ===")
    try:
        # Reorder videos - first becomes last
        reorder_result = client.storyboard.reorder_storyboard_items(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            array_type="videos",
            new_order=[1, 2, 3, 0]  # Move first video to the end
        )
        
        print("Videos reordered successfully")
    except Exception as e:
        print(f"Error reordering storyboard items: {str(e)}")
    
    # Example 8: Edit a storyboard item
    print("\n=== Editing Storyboard Item ===")
    try:
        # Update a video's properties
        updated_item = {
            "dir": "path/to/video.mp4",  # Keep the same media path
            "frame": 2.5,  # Adjusted timing
            "scene": "Product demonstration",  # Updated description
            "details": "Close-up of product being used, highlighting sustainable materials",
            "highlight": True,
            "transition_in": "fade"
        }
        
        edit_result = client.storyboard.edit_storyboard_item(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            item_type="videos",
            item_index=0,  # Edit the first video
            updated_item=updated_item
        )
        
        print("Storyboard item edited successfully")
    except Exception as e:
        print(f"Error editing storyboard item: {str(e)}")
    
    # Example 9: Change media in a storyboard
    print("\n=== Changing Storyboard Media ===")
    try:
        # Replace a video with another one
        change_result = client.storyboard.change_storyboard_media(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
            item_type="videos",
            item_index=1,  # Change the second video
            file_id="file_abc123"  # Replace with actual file ID
        )
        
        print(f"Media changed successfully with path: {change_result.get('media_path')}")
    except Exception as e:
        print(f"Error changing storyboard media: {str(e)}")
    
    # Example 10: View storyboard history
    print("\n=== Viewing Storyboard History ===")
    try:
        history_result = client.storyboard.get_storyboard_history(
            storyboard_id="your_storyboard_id_here",  # Replace with actual ID
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
        print(f"Error getting storyboard history: {str(e)}")

if __name__ == "__main__":
    main()
