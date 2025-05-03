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

# Verify credentials were loaded
if not API_KEY or API_KEY == "api_your_key_here":
    raise ValueError("Please set STORYLINEZ_API_KEY in your .env file")
if not API_SECRET or API_SECRET == "your_secret_here":
    raise ValueError("Please set STORYLINEZ_API_SECRET in your .env file")

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
    
    # Example 3: Upload a logo for branding (Improved with error handling)
    print("\n=== Uploading Brand Logo ===")
    try:
        # Example path to logo file
        logo_path = "path/to/logo.png"
        
        # Check if the file exists to provide a better error message
        if not os.path.exists(logo_path):
            print(f"Logo file not found at {logo_path}")
            print("Using alternative method to create a brand without a logo")
            
            # Example 4: Create a brand without a logo
            print("\n=== Creating Brand Preset Without Logo ===")
            brand_result = client.brand.create(
                name="Modern Teal",
                is_public=True,
                # Using hex color instead of RGB list - SDK will convert automatically
                outro_bg_color="#008080",  # Teal
                main_text_color="#ffffff",  # White
                company_font="Montserrat-Bold",
                company_font_size=80,
                subtitle_font="Montserrat-Bold",
                subtitle_color="#ffffff"  # White
            )
            brand_id = brand_result.get("brand_id")
            print(f"Created brand preset with ID: {brand_id}")
        else:
            # Example of full logo upload workflow in one call
            brand_result = client.brand.upload_logo(
                file_path=logo_path,
                name="Modern Teal",
                is_public=True,
                company_font="Montserrat-Bold",
                company_font_size=80,
                # Using RGB lists - both formats are supported
                outro_bg_color=[0, 128, 128],  # Teal
                main_text_color=[255, 255, 255],  # White
                subtitle_font="Montserrat-Bold", 
                subtitle_color=[255, 255, 255]  # White
            )
            brand_id = brand_result.get("brand_id")
            print(f"Created brand preset with logo, ID: {brand_id}")
            
            # Example: Updating brand with new settings
            print("\n=== Updating Brand Preset ===")
            update_result = client.brand.update(
                brand_id=brand_id,
                subtitle_bg_opacity=0.8,
                subtitle_bg_rounded=True,
                # Using hex color with alpha in the update
                subtitle_bg_color="#FF5733"  # Orange-red
            )
            print(f"Updated brand preset with new subtitle styling")
            
            # Example: Using the workflow method that combines logo upload and brand creation/update
            if False:  # Set to True to run this example
                workflow_result = client.brand.create_or_update_brand_with_logo(
                    name="Updated Brand Style",
                    logo_path=logo_path,
                    brand_id=brand_id,  # Providing brand ID means update
                    outro_bg_color="#336699",  # Blue
                    subtitle_position=2  # Center position
                )
                print("Updated brand with new logo and styling")
                
            # New example: Update an existing brand with a new logo using logo_upload_id
            print("\n=== Updating Brand with New Logo (Using logo_upload_id) ===")
            if os.path.exists(logo_path):
                updated_brand = client.brand.update_brand_with_logo(
                    brand_id=brand_id,
                    logo_path=logo_path,
                    # Can also update other brand parameters at the same time
                    subtitle_position=3,  # Above bottom edge
                )
                print(f"Updated brand '{updated_brand.get('name')}' with new logo using logo_upload_id")
            
    except Exception as e:
        print(f"Error in logo/brand examples: {str(e)}")
    
    # Example 5: Get public brands
    print("\n=== Finding Public Brand Presets ===")
    public_brands = client.brand.get_public_brands(
        limit=5,
        include_logos=True  # Get temporary URLs for brand logos
    )
    print(f"Found {public_brands.get('count', 0)} public brand presets")
    for brand in public_brands.get('public_brands', []):
        org_name = brand.get('org_name', 'Unknown')
        name = brand.get('name', 'Unnamed')
        has_logo = 'logo_url' in brand
        print(f"- {name} (by {org_name}){' with logo' if has_logo else ''}")
    
    # Example 6: Search company details
    print("\n=== Searching Company Details ===")
    search_results = client.company_details.search(
        query="Tech",  # Search for "Tech" in company names
        limit=5
    )
    print(f"Found {search_results.get('count', 0)} matching company profiles")
    for result in search_results.get('results', []):
        print(f"- {result.get('company_name')}")
    
    # Example 7: Find or create a default brand
    print("\n=== Finding or Creating Default Brand ===")
    try:
        default_brand = client.brand.find_or_create_default_brand(
            brand_name="Organization Default",
            create_if_missing=True,
            # Brand settings if creation is needed
            is_public=False,
            outro_bg_color="#0066cc",  # Blue
            main_text_color="#ffffff"   # White
        )
        print(f"Found/created default brand: {default_brand.get('name')}")
    except Exception as e:
        print(f"Error with default brand: {str(e)}")
        
    # Example 8: Find or create a default company
    print("\n=== Finding or Creating Default Company ===")
    try:
        default_company = client.company_details.find_or_create_default_company(
            company_name="Default Company",
            create_if_missing=True,
            company_type="Software",
            tag_line="Innovating Every Day",
            description="Our default company profile"
        )
        print(f"Found/created default company: {default_company.get('company_name')}")
    except Exception as e:
        print(f"Error with default company: {str(e)}")
    
    # Example 9: Get available fonts
    print("\n=== Getting Available Fonts ===")
    try:
        fonts = client.brand.get_fonts()
        font_list = fonts.get('fonts', [])
        print(f"Found {len(font_list)} available fonts")
        # Print first 5 fonts
        for font in font_list[:5]:
            print(f"- {font}")
        if len(font_list) > 5:
            print(f"...and {len(font_list) - 5} more")
    except Exception as e:
        print(f"Error fetching fonts: {str(e)}")

if __name__ == "__main__":
    main()
