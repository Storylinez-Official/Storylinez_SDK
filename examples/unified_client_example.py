from storylinez import StorylinezClient

# Replace these with your actual credentials
API_KEY = "api_your_key_here"
API_SECRET = "your_secret_here" 
ORG_ID = "your_org_id_here"

def main():
    # Create the client once with your credentials
    client = StorylinezClient(API_KEY, API_SECRET)
    
    # Work with storage
    print("=== Storage Operations ===")
    # Create a folder
    folder = client.storage.create_folder(
        org_id=ORG_ID,
        folder_name="Demo",
        parent_path="/"
    )
    folder_id = folder["folder"]["folder_id"]
    print(f"Created folder with ID: {folder_id}")
    
    # Upload a file
    file_result = client.storage.upload_file(
        org_id=ORG_ID,
        file_path="example.mp4",
        folder_path="/Demo"
    )
    file_id = file_result["file"]["file_id"]
    print(f"Uploaded file with ID: {file_id}")
    
    # As more services are implemented, they'll be available through the same client
    
    # Future examples (once implemented):
    # print("\n=== Project Operations ===")
    # Create a project
    # project = client.projects.create_project(
    #    org_id=ORG_ID,
    #    name="Demo Project",
    #    description="Created via SDK"
    # )
    # project_id = project["project_id"]
    # print(f"Created project with ID: {project_id}")
    
    # print("\n=== Organization Operations ===")
    # List organizations
    # orgs = client.organizations.list_organizations()
    # print(f"You have access to {len(orgs['organizations'])} organizations")
    
if __name__ == "__main__":
    main()
