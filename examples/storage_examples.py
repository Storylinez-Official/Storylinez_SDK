import os
import sys
from dotenv import load_dotenv
from storylinez import StorylinezClient
from pprint import pprint
import time

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.environ.get("STORYLINEZ_API_KEY")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

# Fallbacks and validation
if not API_KEY:
    API_KEY = "api_your_key_here"
    print("WARNING: STORYLINEZ_API_KEY not found in environment. Using placeholder value.")

if not API_SECRET:
    API_SECRET = "your_secret_here"
    print("WARNING: STORYLINEZ_API_SECRET not found in environment. Using placeholder value.")

if ORG_ID == "your_org_id_here":
    print("WARNING: STORYLINEZ_ORG_ID not found in environment. Using placeholder value.")

# For local development, you might want to use a local server
# Uncomment this line to use local server
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
    
    # Display demo menu
    print("\n=== Storylinez Storage SDK Demo ===\n")
    print("Available demonstrations:")
    print("1. Upload a file with custom analysis parameters")
    print("2. Create folder structure")
    print("3. Browse folder contents")
    print("4. Semantic vector search")
    print("5. Get file analysis")
    print("6. Check storage usage")
    print("7. Upload a directory recursively")
    print("8. Run all demos sequentially")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-8): ")
    
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid choice. Please enter a number.")
        return
    
    if choice == 0:
        print("Exiting demo.")
        return
    elif choice == 1:
        demo_file_upload(client)
    elif choice == 2:
        demo_create_folders(client)
    elif choice == 3:
        demo_browse_contents(client)
    elif choice == 4:
        demo_vector_search(client)
    elif choice == 5:
        demo_file_analysis(client)
    elif choice == 6:
        demo_storage_usage(client)
    elif choice == 7:
        demo_upload_directory(client)
    elif choice == 8:
        print("\nRunning all demos sequentially...\n")
        file_id = demo_file_upload(client)
        demo_create_folders(client)
        demo_browse_contents(client)
        demo_vector_search(client)
        if file_id:
            demo_file_analysis(client, file_id)
        demo_storage_usage(client)
    else:
        print("Invalid choice.")

def demo_file_upload(client):
    """Demo for uploading a file with custom parameters"""
    print("\n=== File Upload Demo ===")
    
    # Ask for file path
    while True:
        file_path = input("Enter path to a file to upload (e.g., C:\\path\\to\\file.mp4): ")
        if os.path.isfile(file_path):
            break
        print("File not found. Please enter a valid file path.")
    
    # Basic parameters
    folder_path = input("Enter target folder path (default: '/'): ") or "/"
    context = input("Enter context for AI analysis (optional): ")
    tags_input = input("Enter tags separated by commas (optional): ")
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
    
    # Advanced parameters
    print("\nAdvanced options (press Enter for defaults):")
    analyze_audio = input("Analyze audio in media? (y/n, default: y): ").lower() != 'n'
    deepthink = input("Enable DeepThink for detailed analysis? (y/n, default: n): ").lower() == 'y'
    web_search = input("Enable web search during analysis? (y/n, default: n): ").lower() == 'y'
    
    print(f"\nUploading {os.path.basename(file_path)} to {folder_path}...")
    
    try:
        # Upload the file with specified parameters
        result = client.storage.upload_file(
            file_path=file_path,
            folder_path=folder_path,
            context=context,
            tags=tags,
            analyze_audio=analyze_audio,
            deepthink=deepthink,
            web_search=web_search
        )
        
        file_id = result["file"]["file_id"]
        print(f"\nSuccess! File uploaded with ID: {file_id}")
        print(f"Analysis job started with ID: {result.get('job_id')}")
        
        # Show the file's URLs
        if "urls" in result["file"]:
            print("\nGenerated URLs:")
            for url_type, url in result["file"]["urls"].items():
                print(f"- {url_type}: {url[:60]}...") # Truncate for display
        
        return file_id
        
    except Exception as e:
        print(f"\nError uploading file: {str(e)}")
        return None

def demo_create_folders(client):
    """Demo for creating folder structure"""
    print("\n=== Create Folders Demo ===")
    
    try:
        # Example: Create top-level folder
        folder_name = input("Enter name for a new folder: ") or "Demo Folder"
        parent_path = input("Enter parent path (default: '/'): ") or "/"
        
        print(f"Creating folder '{folder_name}' at '{parent_path}'...")
        folder_result = client.storage.create_folder(
            folder_name=folder_name,
            parent_path=parent_path
        )
        
        folder_id = folder_result["folder"]["folder_id"]
        folder_path = folder_result["folder"]["path"]
        print(f"Folder created with ID: {folder_id} at path: {folder_path}")
        
        # Example: Create subfolder
        create_sub = input("\nCreate a subfolder? (y/n): ").lower() == 'y'
        if create_sub:
            subfolder_name = input("Enter name for the subfolder: ") or "Subfolder"
            
            print(f"Creating subfolder '{subfolder_name}' at '{folder_path}'...")
            subfolder_result = client.storage.create_folder(
                folder_name=subfolder_name,
                parent_path=folder_path
            )
            
            subfolder_id = subfolder_result["folder"]["folder_id"]
            subfolder_path = subfolder_result["folder"]["path"]
            print(f"Subfolder created with ID: {subfolder_id} at path: {subfolder_path}")
        
        # Example: Use the helper workflow to create nested paths
        create_nested = input("\nCreate a multi-level folder path in one step? (y/n): ").lower() == 'y'
        if create_nested:
            nested_path = input("Enter nested path to create (e.g., /path/to/nested/folder): ") or "/demo/nested/path"
            
            print(f"Ensuring path exists: {nested_path}")
            result = client.storage.ensure_folder_path(nested_path)
            
            print(f"Created folder path. Final folder: {result.get('name')} at {result.get('path')}")
            
        return True
        
    except Exception as e:
        print(f"\nError creating folders: {str(e)}")
        return False

def demo_browse_contents(client):
    """Demo for browsing folder contents"""
    print("\n=== Browse Folder Contents Demo ===")
    
    try:
        path = input("Enter folder path to browse (default: '/'): ") or "/"
        recursive = input("Include files from subfolders? (y/n, default: n): ").lower() == 'y'
        detailed = input("Include detailed analysis? (y/n, default: n): ").lower() == 'y'
        
        print(f"\nFetching contents of folder: {path} (recursive: {recursive})...")
        contents = client.storage.get_folder_contents(
            path=path,
            recursive=recursive,
            detailed=detailed,
            generate_thumbnail=True,
            generate_streamable=False
        )
        
        folders = contents.get("folders", [])
        files = contents.get("files", [])
        
        print(f"\nFound {len(folders)} folders and {len(files)} files")
        
        # Display folders
        if folders:
            print("\nFolders:")
            for i, folder in enumerate(folders[:5]):  # Show first 5
                print(f"  {i+1}. {folder.get('name')} (path: {folder.get('path')})")
            if len(folders) > 5:
                print(f"  ... and {len(folders) - 5} more folders")
        
        # Display files
        if files:
            print("\nFiles:")
            for i, file in enumerate(files[:5]):  # Show first 5
                print(f"  {i+1}. {file.get('filename')} (ID: {file.get('file_id')}, size: {file.get('size', 0) // 1024} KB)")
                # Show processing status if available
                if 'processing_status' in file:
                    print(f"     Status: {file.get('processing_status')}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more files")
        
        return True
        
    except Exception as e:
        print(f"\nError browsing contents: {str(e)}")
        return False

def demo_vector_search(client):
    """Demo for semantic vector search"""
    print("\n=== Vector Search Demo ===")
    
    try:
        # Get search queries
        query = input("Enter a search query (e.g., 'product demonstration video'): ") or "product demonstration video"
        
        # Create a list of queries (could be multiple)
        queries = [query]
        
        # Optional path to restrict search
        search_all = input("Search across ALL folders? (y/n, default: y): ").lower() != 'n'
        path = None if search_all else input("Enter folder path to search within: ") or "/"
        
        # Search parameters
        num_results = int(input("Max results per query (1-100, default: 10): ") or "10")
        similarity = float(input("Similarity threshold (0.0-1.0, default: 0.5): ") or "0.5")
        
        # File type filter
        file_type_input = input("File types to search (all, video, audio, image or comma-separated, default: all): ") or "all"
        file_types = file_type_input.lower()
        
        print(f"\nPerforming vector search for: '{query}'...")
        if not search_all:
            print(f"Restricting to folder: {path}")
        
        search_results = client.storage.vector_search(
            queries=queries,
            path=path,
            detailed=False,
            generate_thumbnail=True,
            num_results=num_results,
            similarity_threshold=similarity,
            file_types=file_types
        )
        
        files = search_results.get("files", [])
        
        print(f"\nFound {len(files)} relevant files")
        
        # Display results
        if files:
            print("\nSearch results:")
            for i, file in enumerate(files):
                similarity = file.get('vector_similarity', 0) * 100
                print(f"  {i+1}. {file.get('filename')} (Relevance: {similarity:.1f}%)")
                # Show which query matched if multiple queries were used
                if 'vector_query' in file and len(queries) > 1:
                    print(f"     Matched query: \"{file.get('vector_query')}\"")
        
        return True
        
    except Exception as e:
        print(f"\nError performing search: {str(e)}")
        return False

def demo_file_analysis(client, provided_file_id=None):
    """Demo for retrieving file analysis"""
    print("\n=== File Analysis Demo ===")
    
    try:
        # Use provided file ID or ask for one
        if provided_file_id:
            file_id = provided_file_id
            print(f"Using provided file ID: {file_id}")
        else:
            file_id = input("Enter file ID to analyze: ")
            if not file_id:
                print("No file ID provided. Aborting.")
                return False
        
        print(f"Retrieving analysis for file {file_id}...")
        analysis = client.storage.get_file_analysis(
            file_id=file_id,
            detailed=True,
            generate_thumbnail=True,
            generate_streamable=True
        )
        
        # Basic file info
        print("\nFile information:")
        print(f"Name: {analysis.get('filename')}")
        print(f"Size: {analysis.get('size', 0) // 1024} KB")
        print(f"MIME type: {analysis.get('mimetype')}")
        print(f"Uploaded: {analysis.get('upload_date')}")
        
        # Processing status
        status = analysis.get("processing_status", "unknown")
        print(f"Processing status: {status}")
        
        # If processing is complete, show some analysis data
        if status == "completed" and "analysis_data" in analysis:
            data = analysis.get("analysis_data", {})
            
            # Show summary if available
            if "summary" in data:
                print("\nSummary:")
                print(data["summary"][:200] + "..." if len(data["summary"]) > 200 else data["summary"])
            
            # Show detected entities if available
            if "entities" in data and data["entities"]:
                print("\nDetected entities:")
                entities = data["entities"][:5]  # Show first 5
                for entity in entities:
                    print(f"- {entity.get('name')}: {entity.get('type', 'Unknown')}")
                if len(data["entities"]) > 5:
                    print(f"...and {len(data['entities']) - 5} more entities")
            
            # Show transcript snippet if available
            if "transcript" in data and data["transcript"]:
                print("\nTranscript snippet:")
                print(data["transcript"][:200] + "..." if len(data["transcript"]) > 200 else data["transcript"])
        
        # Show URLs
        if "urls" in analysis:
            print("\nGenerated URLs:")
            for url_type, url in analysis["urls"].items():
                print(f"- {url_type}: {url[:60]}...") # Truncate for display
        
        return True
        
    except Exception as e:
        print(f"\nError retrieving file analysis: {str(e)}")
        return False

def demo_storage_usage(client):
    """Demo for checking storage usage"""
    print("\n=== Storage Usage Demo ===")
    
    try:
        print("Fetching storage usage information...")
        usage = client.storage.get_storage_usage()
        
        # Display storage info
        print("\nStorage Usage:")
        print(f"Plan: {usage.get('plan_name', 'Unknown')}")
        print(f"Used: {usage.get('storage_used_gb', 0):.2f} GB of {usage.get('storage_limit_gb', 0):.2f} GB")
        print(f"Usage percentage: {usage.get('percentage_used', 0):.1f}%")
        
        # Display content processing info
        print("\nContent Processing:")
        print(f"Total processed: {usage.get('content_processed_gb', 0):.2f} GB")
        print(f"Current period: {usage.get('period_content_processed_gb', 0):.2f} GB of {usage.get('period_content_processed_limit_gb', 0):.2f} GB")
        print(f"Period usage: {usage.get('percentage_processing_used', 0):.1f}%")
        
        # Display period dates if available
        if "period_start" in usage and "period_end" in usage:
            print(f"\nCurrent period: {usage.get('period_start')} to {usage.get('period_end')}")
        
        return True
        
    except Exception as e:
        print(f"\nError retrieving storage usage: {str(e)}")
        return False

def demo_upload_directory(client):
    """Demo for uploading a directory recursively"""
    print("\n=== Upload Directory Demo ===")
    
    try:
        # Get directory path
        while True:
            local_dir = input("Enter path to local directory to upload: ")
            if os.path.isdir(local_dir):
                break
            print("Directory not found. Please enter a valid directory path.")
        
        # Get upload parameters
        remote_folder = input("Enter target remote folder path (default: '/'): ") or "/"
        include_subdirs = input("Include subdirectories? (y/n, default: y): ").lower() != 'n'
        
        # Optional file extensions filter
        filter_extensions = input("Filter by file extensions? (y/n, default: n): ").lower() == 'y'
        file_extensions = None
        if filter_extensions:
            extensions_input = input("Enter comma-separated extensions without dots (e.g., mp4,jpg,pdf): ")
            if extensions_input:
                file_extensions = [ext.strip().lower() for ext in extensions_input.split(',')]
        
        # Context and tags
        context = input("Enter context for AI analysis (optional): ")
        tags_input = input("Enter tags separated by commas (optional): ")
        tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
        
        print(f"\nUploading directory: {local_dir} to {remote_folder} (with subdirs: {include_subdirs})")
        if file_extensions:
            print(f"Filtering for extensions: {', '.join(file_extensions)}")
        
        # Perform the upload
        results = client.storage.upload_directory(
            local_dir=local_dir,
            remote_folder=remote_folder,
            include_subdirs=include_subdirs,
            file_extensions=file_extensions,
            context=context,
            tags=tags
        )
        
        # Show results
        counts = results.get("counts", {})
        print(f"\nUpload complete!")
        print(f"Successful uploads: {counts.get('success', 0)}")
        print(f"Failed uploads: {counts.get('failed', 0)}")
        print(f"Skipped files: {counts.get('skipped', 0)}")
        
        # Show some examples of successful uploads
        if results.get("success"):
            print("\nExample successful uploads:")
            for i, upload in enumerate(results["success"][:3]):  # Show first 3
                print(f"  {i+1}. {os.path.basename(upload['local_path'])} -> {upload['remote_folder']}")
            if len(results["success"]) > 3:
                print(f"  ... and {len(results['success']) - 3} more files")
        
        # Show some examples of failed uploads
        if results.get("failed"):
            print("\nExample failed uploads:")
            for i, failure in enumerate(results["failed"][:3]):  # Show first 3
                print(f"  {i+1}. {os.path.basename(failure['path'])}: {failure['error']}")
            if len(results["failed"]) > 3:
                print(f"  ... and {len(results['failed']) - 3} more files")
        
        return True
        
    except Exception as e:
        print(f"\nError uploading directory: {str(e)}")
        return False

if __name__ == "__main__":
    main()
