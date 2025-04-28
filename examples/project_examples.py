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
    
    # Example 4: Search for projects
    print("\n=== Searching Projects ===")
    search_results = client.project.search_projects(
        query="product",
        search_fields=["name", "purpose"],
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

if __name__ == "__main__":
    main()
