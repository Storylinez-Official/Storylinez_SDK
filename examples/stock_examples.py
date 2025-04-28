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
    
    # Example 1: Search for stock media
    print("\n=== Searching Stock Media ===")
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
        
        # Example 2: Get detailed information about a specific stock video
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
    
    # Example 3: List stock audios with pagination
    print("\n=== Listing Stock Audio ===")
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
    
    # Example 4: Get multiple stock items by their IDs
    if videos and len(videos) >= 2:
        print("\n=== Getting Multiple Stock Items ===")
        
        # Get IDs from search results
        item_ids = []
        media_types = []
        
        # Add up to 2 videos
        for i in range(min(2, len(videos))):
            video_id = videos[i].get('stock_id') or videos[i].get('_id')
            item_ids.append(video_id)
            media_types.append("videos")
        
        # Add images if available
        images = search_results.get('images', [])
        for i in range(min(2, len(images))):
            image_id = images[i].get('stock_id') or images[i].get('_id')
            item_ids.append(image_id)
            media_types.append("images")
        
        # Get items by IDs
        items = client.stock.get_by_ids(
            ids=item_ids,
            media_types=media_types,
            generate_thumbnail=True
        )
        
        # Print results
        found_items = items.get('items', [])
        print(f"Retrieved {len(found_items)} items by ID")
        missing_items = items.get('missing', [])
        if missing_items:
            print(f"Missing items: {len(missing_items)}")

if __name__ == "__main__":
    main()
