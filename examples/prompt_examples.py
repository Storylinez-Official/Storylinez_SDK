import os
import time
import requests
from dotenv import load_dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables with fallbacks
API_KEY = os.environ.get("STORYLINEZ_API_KEY", "api_your_generated_key")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_generated_secret")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

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
        print(f"Project ID: {text_prompt_result.get('project_id')}")
        print(f"Temperature: {text_prompt_result.get('temperature')}")
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
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
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Error with reference video operations: {str(e)}")
    
    # Example 3: Direct file upload (if you have a local file)
    print("\n=== Direct File Upload (Simulated) ===")
    try:
        print("This example shows the code but doesn't run it since the file doesn't exist")
        
        # This is how you would upload a local video file directly
        """
        local_file_path = "./videos/product_demo.mp4"
        
        # Upload the file and register it in one call
        upload_result = client.prompt.upload_reference_video(
            file_path=local_file_path,
            context="Product demo for our eco-friendly product line",
            tags=["product", "demo", "eco-friendly"]
        )
        
        reference_video_id = upload_result.get("file", {}).get("file_id")
        print(f"Uploaded reference video with ID: {reference_video_id}")
        """
    except Exception as e:
        print(f"Error with direct file upload: {str(e)}")
        
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
            
            # If video has a thumbnail, show the URL
            if "urls" in video and video["urls"].get("thumbnail"):
                print(f"   Thumbnail: {video['urls']['thumbnail']}")
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Error listing reference videos: {str(e)}")
    
    # Example 5: Search for reference videos
    print("\n=== Searching Reference Videos ===")
    try:
        # Search for videos with "demo" in the filename
        search_results = client.prompt.search_reference_videos(
            query="demo",
            limit=5,
            generate_thumbnail=True
        )
        
        count = search_results.get("count", 0)
        videos = search_results.get("reference_videos", [])
        
        print(f"Found {count} videos matching 'demo'")
        for i, video in enumerate(videos[:3]):  # Show up to 3 videos
            print(f"{i+1}. {video.get('filename')}")
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Error searching reference videos: {str(e)}")
        
    # Example 6: Search for content based on a prompt
    print("\n=== Generating Content Search ===")
    try:
        # In a real application, you would have a valid project_id or prompt_id
        """
        # Start the search
        search_result = client.prompt.generate_search_query(
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
        
        # Pass the job_id to properly identify the specific search job
        search_results = client.prompt.get_search_query_results(
            project_id="project_123abc",
            job_id=job_id  # Important: Include job_id for reliable results
        )
        
        status = search_results.get("status")
        print(f"Search status: {status}")
        
        if status == "COMPLETED":
            results = search_results.get("results", {})
            videos = results.get("videos", [])
            audio = results.get("audio", [])
            images = results.get("images", [])
            
            print(f"Found {len(videos)} videos, {len(audio)} audio files, and {len(images)} images")
            
            # Access the first video description
            if videos:
                print(f"First video: {videos[0].get('description')}")
        
        # Alternatively, use the convenience method to search and wait for results
        # This method automatically passes the job_id internally
        search_results = client.prompt.start_query_gen_and_wait(
            project_id="project_123abc",
            num_videos=5,
            num_audio=2,
            num_images=3,
            max_wait_seconds=30  # Wait up to 30 seconds for results
        )
        
        if search_results.get("status") == "COMPLETED":
            print("Search completed successfully")
            
            # Access the counts directly from the results
            results = search_results.get("results", {})
            video_count = results.get("video_count", 0)
            audio_count = results.get("audio_count", 0)
            image_count = results.get("image_count", 0)
            
            print(f"Found {video_count} videos, {audio_count} audio files, and {image_count} images")
        else:
            print(f"Search not completed in time. Status: {search_results.get('status')}")
        """
        
        # Simple example - demonstrating real search (uncomment to test)
        """
        # This combines the search generation and polling in one convenience method
        search_results = client.prompt.start_query_gen_and_wait(
            project_id="project_123abc",
            num_videos=3,
            num_audio=2,
            num_images=5,
            company_details="Eco Solutions Inc. is a sustainable products company focused on reducing plastic waste.",
            max_wait_seconds=120,
            poll_interval_seconds=3
        )
        """
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Error with content search: {str(e)}")
        
    # Example 7: Update a prompt
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
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Error updating prompt: {str(e)}")
        
    # Example 8: Get storage usage information
    print("\n=== Get Storage Usage ===")
    try:
        storage_info = client.prompt.get_storage_usage()
        
        print("Storage Usage Information:")
        print(f"Used Storage: {storage_info.get('used_bytes', 0) / (1024 * 1024):.2f} MB")
        print(f"Total Storage: {storage_info.get('total_bytes', 0) / (1024 * 1024):.2f} MB")
        print(f"Usage Percentage: {storage_info.get('usage_percentage', 0)::.2f}%")
        
        # Get subscription details
        subscription = storage_info.get('subscription', {})
        if subscription:
            print(f"Subscription Plan: {subscription.get('plan_name', 'Unknown')}")
            print(f"Status: {subscription.get('status', 'Unknown')}")
    except ValueError as e:
        # Catch SDK validation errors
        print(f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Error getting storage usage: {str(e)}")

if __name__ == "__main__":
    main()
