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
    
    # Example 1: Create company details
    print("\n=== Creating Company Details ===")
    company_result = client.company_details.create(
        company_name="Acme Corporation",
        company_type="Technology",
        tag_line="Building the Future, Today",
        vision="To revolutionize how people interact with technology",
        products="AI Assistant, Cloud Storage, Content Creation Tools",
        description="Acme Corporation is a technology leader focused on innovative solutions.",
        is_default=True
    )
    company_id = company_result.get("company_details_id")
    print(f"Created company details with ID: {company_id}")
    
    # Example 2: Get all company details
    print("\n=== Listing Company Details ===")
    company_profiles = client.company_details.get_all(
        limit=5
    )
    print(f"Found {company_profiles.get('count', 0)} company profiles")
    for profile in company_profiles.get('company_details', []):
        print(f"- {profile.get('company_name')}: {profile.get('tag_line', 'No tagline')}")
    
    # Example 3: Upload a logo for branding
    print("\n=== Uploading Brand Logo ===")
    try:
        # Example assumes you have a logo file at this path
        logo_path = "path/to/logo.png"
        upload_result = client.brand.upload_logo(
            file_path=logo_path
        )
        logo_key = upload_result.get("key")
        print(f"Uploaded logo with key: {logo_key}")
        
        # Example 4: Create a brand with the uploaded logo
        print("\n=== Creating Brand Preset ===")
        brand_result = client.brand.create(
            name="Modern Teal",
            logo_key=logo_key,
            is_public=True,
            company_font="Montserrat-Bold",
            company_font_size=80,
            outro_bg_color=[0, 128, 128],  # Teal
            main_text_color=[255, 255, 255],  # White
            subtitle_font="Montserrat-Bold",
            subtitle_color=[255, 255, 255]  # White
        )
        brand_id = brand_result.get("brand_id")
        print(f"Created brand preset with ID: {brand_id}")
    except FileNotFoundError:
        print("Logo file not found, skipping brand creation examples")
    
    # Example 5: Get public brands
    print("\n=== Finding Public Brand Presets ===")
    public_brands = client.brand.get_public_brands(
        limit=5
    )
    print(f"Found {public_brands.get('count', 0)} public brand presets")
    for brand in public_brands.get('public_brands', []):
        org_name = brand.get('org_name', 'Unknown')
        name = brand.get('name', 'Unnamed')
        print(f"- {name} (by {org_name})")
    
    # Example 6: Search company details
    print("\n=== Searching Company Details ===")
    search_results = client.company_details.search(
        query="Tech",  # Search for "Tech" in company names
        limit=5
    )
    print(f"Found {search_results.get('count', 0)} matching company profiles")
    for result in search_results.get('results', []):
        print(f"- {result.get('company_name')}")

if __name__ == "__main__":
    main()
