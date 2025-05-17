import os
import dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
dotenv.load_dotenv()

# Get credentials from environment variables or use placeholders
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
    
    # Example 3: Search audio by genre with improved parameter handling
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
    
    # Example 4: Search for images by color using hex color conversion
    print("\n=== Searching Images by Color ===")
    # Using new hex_color parameter for easier color search
    color_results = client.search.search_image_by_color(
        hex_color="#FF5500",  # Using hex color instead of hue range
        color_moods=["warm", "vibrant"],
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
        
        # Show match details if available
        match_details = item.get('match_details', {})
        if match_details:
            print("  * Match details:")
            # Show summary matches
            if 'summary' in match_details:
                for match in match_details['summary'][:1]:  # Show first match only
                    print(f"    - In summary: \"{match.get('context', '')}\"")
            
            # Show tag matches
            if 'tags' in match_details:
                matched_tags = [m.get('text') for m in match_details['tags'][:3]]
                if matched_tags:
                    print(f"    - In tags: {', '.join(matched_tags)}")
            
            # Show media-specific matches
            if item.get('media_type') == 'video' and 'video_scenes' in match_details:
                for match in match_details['video_scenes'][:1]:
                    print(f"    - In scene: \"{match.get('context', '')}\"")
            
            elif item.get('media_type') == 'audio' and 'audio_transcription' in match_details:
                for match in match_details['audio_transcription'][:1]:
                    print(f"    - In transcription: \"{match.get('context', '')}\"")
            
            elif item.get('media_type') == 'image' and 'image_ocr' in match_details:
                for match in match_details['image_ocr'][:1]:
                    print(f"    - In image text: \"{match.get('context', '')}\"")
    
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

    # Example 7: Advanced workflow method - Topic-based search
    print("\n=== Topic-Based Search (Workflow Method) ===")
    topic_results = client.search.search_topics(
        topic="technology",
        subtopics=["artificial intelligence", "machine learning"],
        media_types=["video", "audio"],
        page_size=5
    )

    print(f"Found {topic_results.get('pagination', {}).get('total_results', 0)} items related to the topic")
    for item in topic_results.get('results', [])[:3]:
        print(f"- {item.get('filename')} ({item.get('media_type')})")
        print(f"  * {item.get('summary', '')[:100]}...")

    # Example 8: Audio search by transcription
    print("\n=== Searching Audio by Transcription ===")
    transcript_results = client.search.search_audio_by_transcription(
        query="important announcement about the company",
        generate_thumbnail=True
    )

    print(f"Found {transcript_results.get('pagination', {}).get('total_results', 0)} matching audio files")
    for item in transcript_results.get('results', [])[:2]:
        print(f"- {item.get('filename')}")
        for match in item.get('transcript_matches', [])[:1]:
            print(f"  * Match: \"{match.get('text', '')[:100]}...\"")

if __name__ == "__main__":
    main()
