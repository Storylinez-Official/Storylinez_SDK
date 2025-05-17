from storylinez import StorylinezClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load credentials from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.getenv("STORYLINEZ_API_KEY")
API_SECRET = os.getenv("STORYLINEZ_API_SECRET")
# You can also store ORG_ID in .env if preferred
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

def main():
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Create a project folder
    print("\n=== Creating Project Folder ===")
    folder_result = client.project.create_folder(
        name="Marketing Videos",
        description="Folder for all marketing campaign videos"
    )
    folder_id = folder_result.get("folder_id")
    print(f"Created folder with ID: {folder_id}")
    
    # Example 2: Create a project in the folder
    print("\n=== Creating Project ===")
    project_result = client.project.create_project(
        name="Q1 Product Launch",
        orientation="landscape",
        purpose="Showcase new product features for Q1 launch",
        target_audience="Existing customers and prospects",
        folder_id=folder_id
    )
    project_id = project_result.get("project").get("project_id")
    print(f"Created project with ID: {project_id}")
    
    # Example 3: Add a file to the project
    print("\n=== Uploading and Adding a File to Project ===")
    try:
        # First upload a file
        upload_result = client.storage.upload_file(
            file_path="path/to/demo.mp4",
            folder_path="/demos",
            context="Product demo for marketing video"
        )
        file_id = upload_result.get("file", {}).get("file_id")
        
        # Add file to project
        client.project.add_associated_file(
            project_id=project_id,
            file_id=file_id
        )
        print(f"Added file {file_id} to project")
    except Exception as e:
        print(f"Error with file operations: {str(e)}")
    
    # Example 4: Search for projects with datetime filtering
    print("\n=== Searching Projects with Date Filters ===")
    # Demo of using datetime objects instead of ISO strings
    one_month_ago = datetime.now() - timedelta(days=30)
    
    search_results = client.project.search_projects(
        query="product",
        search_fields=["name", "purpose"],
        created_after=one_month_ago,  # SDK will convert to ISO format
        generate_thumbnail_links=True,
        limit=5
    )
    print(f"Found {search_results.get('pagination', {}).get('total', 0)} matching projects")
    for proj in search_results.get('projects', [])[:2]:
        print(f"- {proj.get('name')}: {proj.get('purpose', '')[:50]}...")
    
    # Example 5: Get projects by folder
    print("\n=== Getting Projects in a Folder ===")
    folder_projects = client.project.get_projects_by_folder(
        folder_id=folder_id,
        generate_thumbnail_links=True
    )
    print(f"Found {len(folder_projects.get('projects', []))} projects in the folder")
    
    # Example 6: Add stock media to the project
    print("\n=== Adding Stock Media ===")
    try:
        # Search for stock videos
        stock_results = client.stock.search(
            queries=["business presentation"],
            collections=["videos"],
            num_results_videos=1
        )
        
        if stock_results.get('videos'):
            stock_video = stock_results['videos'][0]
            stock_id = stock_video.get('stock_id') or stock_video.get('_id')
            
            # Add stock video to project
            client.project.add_stock_file(
                project_id=project_id,
                stock_id=stock_id,
                media_type="videos"
            )
            print(f"Added stock video {stock_id} to project")
    except Exception as e:
        print(f"Error with stock operations: {str(e)}")
    
    # Example 7: Duplicate a project
    print("\n=== Duplicating Project ===")
    duplicate_result = client.project.duplicate_project(
        project_id=project_id,
        name="Q1 Product Launch - Copy"
    )
    duplicate_id = duplicate_result.get("new_project_id")
    print(f"Created duplicate project with ID: {duplicate_id}")
    
    # Example 8: Move project to a different folder
    print("\n=== Creating Another Folder and Moving Project ===")
    second_folder = client.project.create_folder(
        name="Archive Projects",
        description="Archived project materials"
    )
    second_folder_id = second_folder.get("folder_id")
    
    move_result = client.project.move_project_to_folder(
        project_id=duplicate_id,
        folder_id=second_folder_id
    )
    print(f"Moved project to folder: {second_folder.get('name')}")
    
    # Example 9: Use the new convenience method to create a project with files in one step
    print("\n=== Using Convenience Method to Create Project with Files ===")
    try:
        combined_project = client.project.create_project_with_files(
            name="Combined Workflow Project",
            orientation="portrait",
            files=[file_id],
            folder_name="Quick Projects",
            purpose="Demonstrating combined workflows"
        )
        print(f"Created project with ID: {combined_project.get('project', {}).get('project_id')}")
    except Exception as e:
        print(f"Error with convenience method: {str(e)}")
    
    # Example 10: Adding Multiple Files to a Project
    print("\n=== Adding Multiple Files to a Project ===")
    try:
        # First, let's create or get some file IDs
        file_ids = []
        
        # Upload multiple files (or use existing ones)
        for file_path in ["path/to/logo.png", "path/to/background.jpg", "path/to/audio.mp3"]:
            try:
                upload_result = client.storage.upload_file(
                    file_path=file_path,
                    folder_path="/bulk_demo"
                )
                file_ids.append(upload_result.get("file", {}).get("file_id"))
            except FileNotFoundError:
                # In a real example, you'd handle this better
                print(f"File {file_path} not found, using placeholder")
        
        # If we couldn't upload real files, use some example IDs
        if not file_ids:
            file_ids = ["file_id_1", "file_id_2", "file_id_3"]  # Example IDs - would fail in actual usage
        
        # Add files in bulk
        bulk_result = client.project.add_associated_files_bulk(
            project_id=project_id,
            file_ids=file_ids
        )
        
        print(f"Added {len(bulk_result.get('results', {}).get('successful', []))} files successfully")
        print(f"Failed to add {len(bulk_result.get('results', {}).get('failed', []))} files")
        
        # Show failure reasons if any
        if bulk_result.get('results', {}).get('failed'):
            print("Failures:")
            for failure in bulk_result.get('results', {}).get('failed'):
                print(f"- {failure.get('file_id')}: {failure.get('reason')}")
        
    except Exception as e:
        print(f"Error with bulk file operations: {str(e)}")

    # Example 11: Adding Multiple Stock Media Files
    print("\n=== Adding Multiple Stock Media Files ===")
    try:
        # Search for multiple stock videos
        stock_results = client.stock.search(
            queries=["business presentation", "technology"],
            collections=["videos"],
            num_results_videos=3
        )
        
        if stock_results.get('videos'):
            # Extract stock IDs from results
            stock_ids = [video.get('stock_id') or str(video.get('_id')) 
                         for video in stock_results['videos'][:3]]
            
            # Add stock videos in bulk
            bulk_stock_result = client.project.add_stock_files_bulk(
                project_id=project_id,
                stock_ids=stock_ids,
                media_type="videos"
            )
            
            print(f"Added {len(bulk_stock_result.get('results', {}).get('successful', []))} stock videos")
            print(f"Failed to add {len(bulk_stock_result.get('results', {}).get('failed', []))} stock videos")
            
    except Exception as e:
        print(f"Error with bulk stock operations: {str(e)}")

    # Example 12: Processing Multiple Voiceovers
    print("\n=== Processing Multiple Voiceovers ===")
    try:
        # Let's assume we have some audio file IDs
        audio_files = []
        
        # Upload or use existing audio files
        for audio_path in ["path/to/narration1.mp3", "path/to/narration2.mp3"]:
            try:
                upload_result = client.storage.upload_file(
                    file_path=audio_path,
                    folder_path="/voiceovers"
                )
                audio_files.append({
                    "file_id": upload_result.get("file", {}).get("file_id"),
                    "voice_name": f"Narration from {os.path.basename(audio_path)}"
                })
            except FileNotFoundError:
                # In a real example, you'd handle this better
                print(f"File {audio_path} not found, using placeholder")
        
        # If we couldn't upload real files, use example voiceovers
        if not audio_files:
            audio_files = [
                {"file_id": "audio_file_id_1", "voice_name": "Male Narrator"},
                {"file_id": "audio_file_id_2", "voice_name": "Female Narrator"}
            ]  # Example IDs - would fail in actual usage
        
        # Process voiceovers in bulk and select the second one (if available)
        selected_index = 1 if len(audio_files) > 1 else 0
        
        voiceover_result = client.project.add_voiceovers_bulk(
            project_id=project_id,
            voiceovers=audio_files,
            selected_index=selected_index
        )
        
        print(f"Processed {len(voiceover_result.get('results', {}).get('successful', []))} voiceovers")
        print(f"Failed {len(voiceover_result.get('results', {}).get('failed', []))} voiceovers")
        
        # Show which voiceover was selected
        selected = voiceover_result.get('results', {}).get('selected', {})
        if selected:
            print(f"Selected voiceover: {selected.get('voice_name')}")
        
    except Exception as e:
        print(f"Error with bulk voiceover operations: {str(e)}")

if __name__ == "__main__":
    main()
