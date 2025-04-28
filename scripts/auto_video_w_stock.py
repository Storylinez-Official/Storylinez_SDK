from storylinez import StorylinezClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.environ.get("STORYLINEZ_API_KEY")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET")
# You can also store ORG_ID in .env if preferred
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

client = StorylinezClient(
    api_key=API_KEY, 
    api_secret=API_SECRET,
    org_id=ORG_ID
)

# 1. Create a project
project = client.project.create_project(
    name="Product Introduction",
    orientation="landscape",
    purpose="Introduce our new sustainable product line"
)
project_id = project["project"]["project_id"]

# 2. Create a text prompt
client.prompt.create_text_prompt(
    project_id=project_id,
    main_prompt="Create a 30-second video introducing our eco-friendly product line that reduces plastic waste by 75%",
    document_context="Our products are made from bamboo and recycled materials. The target audience is environmentally conscious millennials.",
    temperature=0.7,
    total_length=30
)

# 2.5 Generate search queries
print("Generating search queries...")
search_results = client.prompt.search_and_wait(
    project_id=project_id,
    num_videos=3,
    num_audio=2,
    num_images=5,
    company_details="Eco Solutions Inc. is a sustainable products company focused on reducing plastic waste.",
    max_wait_seconds=120,
    poll_interval_seconds=3
)

# Print search results
print(f"Search completed with status: {search_results.get('status', 'unknown')}")
if search_results.get('status') == 'COMPLETED':
    # Print video results
    if 'videos' in search_results and search_results['videos']:
        print("\nSuggested Videos:")
        for i, video in enumerate(search_results['videos'], 1):
            print(f"{i}. {video.get('title', 'Untitled')} - {video.get('source_url', 'No URL')}")
    
    # Print audio results
    if 'audio' in search_results and search_results['audio']:
        print("\nSuggested Audio:")
        for i, audio in enumerate(search_results['audio'], 1):
            print(f"{i}. {audio.get('title', 'Untitled')} - {audio.get('source_url', 'No URL')}")
    
    # Print image results
    if 'images' in search_results and search_results['images']:
        print("\nSuggested Images:")
        for i, image in enumerate(search_results['images'], 1):
            print(f"{i}. {image.get('title', 'Untitled')} - {image.get('source_url', 'No URL')}")

# 3. Generate a storyboard
storyboard_job = client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,
    web_search=True
)
print(f"Storyboard job started: {storyboard_job['job_id']}")

# 4. Wait for storyboard completion
storyboard = client.storyboard.wait_for_storyboard(
    project_id=project_id,
    timeout_seconds=300,
    polling_interval=5
)
print(f"Storyboard created with {len(storyboard['scenes'])} scenes")

# 5. Create a sequence
sequence_job = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,
    apply_grade=True
)
print(f"Sequence job started: {sequence_job['job_id']}")

# 6. Wait for sequence completion
sequence = client.sequence.get_sequence(
    project_id=project_id,
    include_results=True
)
while sequence.get("status") != "COMPLETED":
    import time
    time.sleep(5)
    sequence = client.sequence.get_sequence(project_id=project_id)
print("Sequence completed")

# 7. Render the final video
render_job = client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    subtitle_enabled=True,
    company_name="Eco Solutions Inc.",
    call_to_action="Visit eco-solutions.com today"
)
print(f"Render job started: {render_job['job_id']}")

# 8. Get the download link when complete
render = client.render.wait_for_render(
    project_id=project_id,
    timeout_seconds=1800,
    polling_interval=20
)
if render["status"] == "COMPLETED":
    download_info = client.render.get_render(
        project_id=project_id,
        generate_download_link=True,
        generate_streamable_link=True
    )
    print(f"Video ready! Download URL: {download_info['download_url']}")
    print(f"Stream URL: {download_info['streamable_url']}")
else:
    print(f"Render failed with status: {render['status']}")