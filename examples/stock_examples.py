import os
from dotenv import load_dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.environ.get("STORYLINEZ_API_KEY", "your_key_here")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_secret_here")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

def main():
    # Check if environment variables are set
    if API_KEY == "your_key_here" or API_SECRET == "your_secret_here":
        print("Please set STORYLINEZ_API_KEY and STORYLINEZ_API_SECRET in your .env file")
        print("Example .env file:")
        print("STORYLINEZ_API_KEY=api_your_actual_key")
        print("STORYLINEZ_API_SECRET=your_actual_secret")
        print("STORYLINEZ_ORG_ID=your_org_id")
        return

    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Using the convenience method to search for videos
    print("\n=== Using Convenience Method to Search Videos ===")
    video_results = client.stock.search_videos(
        query="aerial view of mountains",
        num_results=3,
        orientation="landscape",
        generate_thumbnail=True,
        generate_streamable=True
    )
    
    print(f"Found {len(video_results)} videos matching the query")
    
    # Example 2: Search for stock media
    print("\n=== Searching Multiple Stock Media Types ===")
    search_results = client.stock.search(
        queries=["aerial view of mountains", "beach sunset"],
        collections=["videos", "images"],
        generate_thumbnail=True,
        num_results_videos=3, 
        num_results_images=3
    )
    
    # Print search results overview
    videos_count = search_results.get('counts', {}).get('videos', 0)
    images_count = search_results.get('counts', {}).get('images', 0)
    print(f"Found {videos_count} videos and {images_count} images")
    
    # Get the first video result if available
    videos = search_results.get('videos', [])
    if videos:
        video = videos[0]
        video_id = video.get('stock_id') or video.get('_id')
        print(f"First video ID: {video_id}")
        
        # Example 3: Get detailed information about a specific stock video
        print("\n=== Getting Stock Video Details ===")
        video_details = client.stock.get_by_id(
            stock_id=video_id,
            media_type="videos",
            generate_thumbnail=True,
            generate_streamable=True
        )
        
        # Show video metadata
        if 'original_metadata' in video_details:
            metadata = video_details.get('original_metadata', {})
            print(f"Video title: {metadata.get('title', 'Untitled')}")
            print(f"Duration: {metadata.get('duration', 0)} seconds")
            print(f"Resolution: {metadata.get('width', 0)}x{metadata.get('height', 0)}")
        
        # Example 4: Find similar media to this video
        print("\n=== Finding Similar Media ===")
        try:
            similar_media = client.stock.find_similar_media(
                stock_id=video_id,
                media_type="videos",
                num_results=2
            )
            
            similar_videos = similar_media.get('videos', [])
            similar_images = similar_media.get('images', [])
            similar_audios = similar_media.get('audios', [])
            
            total_similar = len(similar_videos) + len(similar_images) + len(similar_audios)
            print(f"Found {total_similar} similar media items across all types")
        except ValueError as e:
            print(f"Could not find similar media: {e}")
    
    # Example 5: List stock audios with pagination
    print("\n=== Listing Stock Audio ===")
    try:
        audio_list = client.stock.list_media(
            media_type="audios",
            page=1,
            limit=5,
            sort_by="processed_at",
            sort_order="desc",
            generate_thumbnail=True
        )
        
        # Print audio list overview
        total_audios = audio_list.get('total', 0)
        page = audio_list.get('page', 1)
        total_pages = audio_list.get('total_pages', 1)
        print(f"Page {page} of {total_pages} (Total: {total_audios} audios)")
        
        audios = audio_list.get('results', [])
        for i, audio in enumerate(audios):
            metadata = audio.get('original_metadata', {})
            print(f"{i+1}. {metadata.get('title', 'Untitled')} - {metadata.get('duration', 0)} seconds")
    except ValueError as e:
        print(f"Error listing audio: {e}")
    
    # Example 6: Using the batch_get_items utility method
    if videos:
        print("\n=== Using Batch Get Items Utility ===")
        
        # Create a dictionary of IDs by media type
        ids_by_media_type = {
            'videos': [],
            'images': []
        }
        
        # Add video IDs
        for i in range(min(2, len(videos))):
            video_id = videos[i].get('stock_id') or video[i].get('_id')
            ids_by_media_type['videos'].append(video_id)
        
        # Add image IDs if available
        images = search_results.get('images', [])
        for i in range(min(2, len(images))):
            image_id = images[i].get('stock_id') or images[i].get('_id')
            ids_by_media_type['images'].append(image_id)
        
        # Get items in batch
        try:
            batch_results = client.stock.batch_get_items(
                ids_by_media_type=ids_by_media_type,
                detailed=True,
                generate_thumbnail=True
            )
            
            # Print results
            for media_type, items in batch_results.items():
                print(f"Retrieved {len(items)} {media_type}")
        except ValueError as e:
            print(f"Error in batch get: {e}")

if __name__ == "__main__":
    main()
