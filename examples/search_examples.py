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
    
    # Example 1: Search for video scenes
    print("\n=== Searching Video Scenes ===")
    scene_results = client.search.search_video_scenes(
        query="person talking to camera about product features",
        generate_thumbnail=True
    )
    
    print(f"Found {scene_results.get('pagination', {}).get('total_results', 0)} matching video scenes")
    for item in scene_results.get('results', [])[:2]:
        print(f"- {item.get('filename')} (Matches: {len(item.get('matched_scenes', []))})")
        for scene in item.get('matched_scenes', [])[:1]:
            print(f"  * {scene.get('description', '')[:100]}...")
    
    # Example 2: Search for objects in videos
    print("\n=== Searching for Objects in Videos ===")
    object_results = client.search.search_video_objects(
        objects=["laptop", "phone", "coffee"],
        generate_thumbnail=True
    )
    
    print(f"Found {object_results.get('pagination', {}).get('total_results', 0)} videos with matching objects")
    for item in object_results.get('results', [])[:2]:
        print(f"- {item.get('filename')}")
        for obj, matches in item.get('matched_objects', {}).items():
            print(f"  * Found {obj}: {len(matches)} instances")
    
    # Example 3: Search audio by genre
    print("\n=== Searching Audio by Genre ===")
    genre_results = client.search.search_audio_by_genre(
        genres=["rock", "electronic"],
        min_probability=0.3,
        generate_thumbnail=True,
        media_source="stock"  # Search in stock audio
    )
    
    print(f"Found {genre_results.get('pagination', {}).get('total_results', 0)} matching audio files")
    for item in genre_results.get('results', [])[:2]:
        print(f"- {item.get('original_metadata', {}).get('title', 'Untitled')}")
        for genre, prob in item.get('matched_genres', {}).items():
            print(f"  * {genre}: {prob:.2f} confidence")
    
    # Example 4: Search for images by color
    print("\n=== Searching Images by Color ===")
    color_results = client.search.search_image_by_color(
        color_moods=["warm", "vibrant"],
        dominant_hues={"min": 0, "max": 30},  # Red-orange range
        generate_thumbnail=True
    )
    
    print(f"Found {color_results.get('pagination', {}).get('total_results', 0)} matching images")
    for item in color_results.get('results', [])[:2]:
        color_info = item.get('color_analysis', {})
        print(f"- {item.get('filename')}")
        print(f"  * Dominant hue: {color_info.get('dominant_hue')}")
        print(f"  * Color mood: {color_info.get('color_mood')}")
    
    # Example 5: Combined semantic search
    print("\n=== Combined Semantic Search ===")
    combined_results = client.search.search_combined(
        query="business presentation with charts",
        media_types=["video", "image"],
        generate_thumbnail=True
    )
    
    print(f"Found {combined_results.get('pagination', {}).get('total_results', 0)} matching items")
    for item in combined_results.get('results', [])[:3]:
        print(f"- {item.get('filename')} ({item.get('media_type')})")
        print(f"  * {item.get('summary', '')[:100]}...")
    
    # Example 6: Search by tags across all media
    print("\n=== Searching by Tags ===")
    tags_results = client.search.search_by_tags(
        tags=["marketing", "presentation", "corporate"],
        match_all=False,  # Match any of the tags
        generate_thumbnail=True
    )
    
    print(f"Found {tags_results.get('pagination', {}).get('total_results', 0)} items with matching tags")
    for item in tags_results.get('results', [])[:3]:
        print(f"- {item.get('filename')} ({item.get('media_type')})")
        print(f"  * Matched tags: {', '.join(item.get('matched_tags', []))}")

if __name__ == "__main__":
    main()
