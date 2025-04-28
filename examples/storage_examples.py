import os
from storylinez import StorylinezClient

# Replace these with your actual credentials
API_KEY = "api_your_key_here"
API_SECRET = "your_secret_here"
ORG_ID = "your_org_id_here"

# For local development, you might want to use a local server
# BASE_URL = "http://localhost:5000"
BASE_URL = "https://api.storylinez.com"

def main():
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET, 
        base_url=BASE_URL,
        org_id=ORG_ID  # Setting default org_id
    )
    
    # Now you can access specific services via properties
    # Example 1: Upload a file with analysis parameters
    # Note: No need to specify org_id in each call
    print("Uploading a file...")
    result = client.storage.upload_file(
        file_path="path/to/your/file.mp4",
        folder_path="/demo",
        context="This is a product demonstration video",
        tags=["product", "demo", "marketing"],
        web_search=True,
        deepthink=True
        # org_id is automatically used from the client initialization
    )
    file_id = result["file"]["file_id"]
    print(f"File uploaded with ID: {file_id}")
    
    # Example 2: Create a folder structure
    print("\nCreating folders...")
    folder_result = client.storage.create_folder(
        folder_name="Projects",
        parent_path="/"
        # org_id is automatically used from the client initialization
    )
    projects_folder_id = folder_result["folder"]["folder_id"]
    print(f"Projects folder created with ID: {projects_folder_id}")
    
    # Create a subfolder
    subfolder_result = client.storage.create_folder(
        folder_name="Project Alpha",
        parent_path="/Projects"
        # org_id is automatically used from the client initialization
    )
    print(f"Subfolder created with ID: {subfolder_result['folder']['folder_id']}")
    
    # Example 3: List folder contents
    print("\nListing folder contents...")
    contents = client.storage.get_folder_contents(
        path="/",
        recursive=False
        # org_id is automatically used from the client initialization
    )
    print(f"Found {len(contents['folders'])} folders and {len(contents['files'])} files at root")
    
    # Example 4: Search for files semantically
    print("\nPerforming vector search...")
    search_results = client.storage.vector_search(
        queries=["product demonstration video showing features"],
        detailed=False
        # org_id is automatically used from the client initialization
    )
    print(f"Found {len(search_results['files'])} relevant files")
    
    # Example 5: Get file analysis
    if file_id:
        print(f"\nGetting analysis for file {file_id}...")
        analysis = client.storage.get_file_analysis(file_id)
        status = analysis.get("processing_status", "unknown")
        print(f"File processing status: {status}")
        
        if status == "completed":
            # Show some analysis data if available
            data = analysis.get("analysis_data", {})
            if "summary" in data:
                print(f"File summary: {data['summary'][:100]}...")
    
    # Example 6: Get storage usage
    print("\nGetting storage usage...")
    usage = client.storage.get_storage_usage()  # No need to specify org_id
    print(f"Storage used: {usage['storage_used_gb']} GB of {usage['storage_limit_gb']} GB")
    print(f"Usage percentage: {usage['percentage_used']}%")
    
    # Example 7: You can still override the default org_id if needed
    print("\nOverriding default org_id for a specific call...")
    other_org_contents = client.storage.get_folder_contents(
        path="/",
        org_id="different_org_id"  # This overrides the default org_id
    )
    print(f"Found {len(other_org_contents['folders'])} folders in the other organization")

if __name__ == "__main__":
    main()
