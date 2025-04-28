from storylinez import StorylinezClient

# Replace these with your actual credentials
API_KEY = "api_your_generated_key"
API_SECRET = "your_generated_secret"
ORG_ID = "your_org_id_here"

def main():
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Create a text prompt for a project
    print("\n=== Creating a Text Prompt ===")
    try:
        text_prompt_result = client.prompt.create_text_prompt(
            project_id="project_123abc",
            main_prompt="Create a promotional video for our new eco-friendly product line",
            document_context="The product uses recycled materials and reduces carbon footprint by 30%.",
            temperature=0.7,
            total_length=30,
            iterations=3,
            web_search=True,
            deepthink=True
        )
        prompt_id = text_prompt_result.get("prompt_id")
        print(f"Created text prompt with ID: {prompt_id}")
    except Exception as e:
        print(f"Error creating text prompt: {str(e)}")

    # Example 2: Upload a reference video
    print("\n=== Uploading Reference Video ===")
    try:
        # First, get an upload link
        upload_link_result = client.prompt.get_reference_video_upload_link(
            filename="product_demo.mp4",
            file_size=15000000  # ~15 MB
        )
        
        upload_url = upload_link_result.get("upload_link")
        upload_id = upload_link_result.get("upload_id")
        
        print(f"Generated upload link, upload_id: {upload_id}")
        print("URL: " + upload_url)
        
        # In a real application, you would upload the file to the upload_url here
        # using requests.put(upload_url, data=file_data)
        
        # After uploading to the URL, complete the upload
        print("\nNot actually uploading file in this example...")
        
        # This would be the real code after uploading
        """
        upload_complete_result = client.prompt.complete_reference_video_upload(
            upload_id=upload_id,
            context="Product demo showing key features",
            tags=["product", "demo", "eco-friendly"]
        )
        
        reference_video_id = upload_complete_result.get("file", {}).get("file_id")
        print(f"Uploaded reference video with ID: {reference_video_id}")
        
        # Example 3: Create a video-based prompt
        video_prompt_result = client.prompt.create_video_prompt(
            project_id="project_456def",
            reference_video_id=reference_video_id,
            temperature=0.7,
            total_length=30
        )
        video_prompt_id = video_prompt_result.get("prompt_id")
        print(f"Created video prompt with ID: {video_prompt_id}")
        """
    except Exception as e:
        print(f"Error with reference video operations: {str(e)}")
        
    # Example 4: List all reference videos
    print("\n=== Listing Reference Videos ===")
    try:
        videos_list = client.prompt.list_reference_videos(
            detailed=False,
            generate_thumbnail=True,
            include_usage=True
        )
        
        count = videos_list.get("count", 0)
        videos = videos_list.get("reference_videos", [])
        
        print(f"Found {count} reference videos")
        for i, video in enumerate(videos[:3]):  # Show up to 3 videos
            usage_count = video.get("usage", {}).get("count", 0)
            print(f"{i+1}. {video.get('filename')} (Used in {usage_count} prompts)")
    except Exception as e:
        print(f"Error listing reference videos: {str(e)}")
        
    # Example 5: Search for content based on a prompt
    print("\n=== Generating Content Search ===")
    try:
        # In a real application, you would have a valid project_id or prompt_id
        """
        search_result = client.prompt.generate_search(
            project_id="project_123abc",
            num_videos=5,
            num_audio=2,
            num_images=3,
            temperature=0.8
        )
        
        job_id = search_result.get("job_id")
        print(f"Started search job with ID: {job_id}")
        
        # After some time, get the search results
        time.sleep(3)  # Just for demonstration
        
        search_results = client.prompt.get_search_results(
            project_id="project_123abc"
        )
        
        status = search_results.get("status")
        print(f"Search status: {status}")
        
        if status == "COMPLETED":
            videos = search_results.get("results", {}).get("videos", [])
            audio = search_results.get("results", {}).get("audio", [])
            images = search_results.get("results", {}).get("images", [])
            
            print(f"Found {len(videos)} videos, {len(audio)} audio files, and {len(images)} images")
        """
    except Exception as e:
        print(f"Error with content search: {str(e)}")
        
    # Example 6: Update a prompt
    print("\n=== Updating a Prompt ===")
    try:
        # In a real application, you would have a valid prompt_id
        """
        update_result = client.prompt.update_prompt(
            prompt_id="prompt_789ghi",
            temperature=0.8,
            iterations=5,
            web_search=True
        )
        
        print("Prompt updated successfully")
        print(f"Updated fields: {', '.join(update_result.get('updated_fields', {}).keys())}")
        """
    except Exception as e:
        print(f"Error updating prompt: {str(e)}")

if __name__ == "__main__":
    main()
