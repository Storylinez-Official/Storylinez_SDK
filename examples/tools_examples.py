import os
import time
import dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
dotenv.load_dotenv()

# Get credentials from environment variables with fallbacks
API_KEY = os.environ.get("STORYLINEZ_API_KEY", "api_your_key_here")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_secret_here")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

def main():
    # Check if credentials are properly loaded
    if API_KEY == "api_your_key_here" or API_SECRET == "your_secret_here":
        print("Warning: API credentials not found in environment variables.")
        print("Please set STORYLINEZ_API_KEY and STORYLINEZ_API_SECRET in your .env file.")
    
    if ORG_ID == "your_org_id_here":
        print("Warning: Organization ID not found in environment variables.")
        print("Please set STORYLINEZ_ORG_ID in your .env file or provide it in the function calls.")
    
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Get available tool types
    print("\n=== Getting Tool Types ===")
    try:
        result = client.tools.get_tool_types()
        tool_types = result.get('tool_types', [])
        print(f"Available tool types ({len(tool_types)}):")
        for tool in tool_types:
            print(f"  - {tool.get('name')} ({tool.get('type')})")
    except Exception as e:
        print(f"Error getting tool types: {str(e)}")
    
    # Example 2: Create a creative brief
    print("\n=== Creating a Creative Brief ===")
    try:
        brief_result = client.tools.create_creative_brief(
            name="Product Launch Campaign",
            user_input="Create a creative brief for our new eco-friendly product line launch",
            auto_company_details=True,  # Use company details from the org's default profile
            temperature=0.7,
            deepthink=True,
            web_search=True
        )
        
        tool_id = brief_result.get('tool', {}).get('tool_id')
        job_id = brief_result.get('job_id')
        
        print(f"Created creative brief with ID: {tool_id}")
        print(f"Job ID: {job_id}")
        
        # In a real application, you'd wait for the job to complete
        # For this example, we'll simulate waiting briefly
        print("Waiting for job to start processing...")
        time.sleep(2)  # In a real app, you'd poll or use webhooks
    except Exception as e:
        print(f"Error creating creative brief: {str(e)}")
    
    # Example 3: Create audience research
    print("\n=== Creating Audience Research ===")
    try:
        audience_result = client.tools.create_audience_research(
            name="Gen Z Market Analysis",
            user_input="Research the Gen Z audience and their preferences for sustainable products",
            additional_context="Focus on 18-24 year olds in urban areas",
            auto_company_details=True,
            temperature=0.7
        )
        
        tool_id = audience_result.get('tool', {}).get('tool_id')
        print(f"Created audience research with ID: {tool_id}")
    except Exception as e:
        print(f"Error creating audience research: {str(e)}")
    
    # Example 4: Create a video plan
    print("\n=== Creating a Video Plan ===")
    try:
        video_plan_result = client.tools.create_video_plan(
            name="Product Demo Video Plan",
            user_input="Create a comprehensive video plan for demonstrating our new product features",
            additional_context="Must highlight eco-friendly aspects and user benefits. The video should be 2-3 minutes long and suitable for our website homepage.",
            auto_company_details=True,
            temperature=0.7
        )
        
        tool_id = video_plan_result.get('tool', {}).get('tool_id')
        print(f"Created video plan with ID: {tool_id}")
    except Exception as e:
        print(f"Error creating video plan: {str(e)}")
    
    # Example 5: Create a shotlist
    print("\n=== Creating a Shotlist ===")
    try:
        shotlist_result = client.tools.create_shotlist(
            name="Office Introduction Shotlist",
            user_input="Create a shotlist for introducing our company headquarters",
            scene_details="Modern office with open workspace, meeting rooms, and relaxation areas. The office has large windows with natural light and plants throughout.",
            visual_style="Bright, airy, with smooth camera movements. Professional but welcoming. Use steady cam for walking shots and wide angles to show space.",
            temperature=0.7
        )
        
        tool_id = shotlist_result.get('tool', {}).get('tool_id')
        print(f"Created shotlist with ID: {tool_id}")
    except Exception as e:
        print(f"Error creating shotlist: {str(e)}")
    
    # Example 6: Create an ad concept
    print("\n=== Creating an Ad Concept ===")
    try:
        ad_concept_result = client.tools.create_ad_concept(
            name="Holiday Special Ad Concept",
            user_input="Create an ad concept for our holiday season promotion",
            campaign_goals="Increase sales by 30% during the holiday season. Drive traffic to our website and increase social media engagement by 25%.",
            target_audience="Working professionals, 25-45, with disposable income. Tech-savvy consumers who value quality and sustainability.",
            auto_company_details=True,
            temperature=0.7
        )
        
        tool_id = ad_concept_result.get('tool', {}).get('tool_id')
        print(f"Created ad concept with ID: {tool_id}")
    except Exception as e:
        print(f"Error creating ad concept: {str(e)}")
    
    # Example 7: Create scene transitions
    print("\n=== Creating Scene Transitions ===")
    try:
        scene_transitions_result = client.tools.create_scene_transitions(
            name="Product Journey Transitions",
            scene_descriptions=[
                "Raw materials being harvested sustainably in a lush forest setting",
                "Manufacturing process with eco-friendly methods in a clean, modern factory",
                "Product packaging and assembly with workers carefully handling items",
                "Customer unboxing and using the product with visible satisfaction"
            ],
            project_style="Documentary style with cinematic quality. 4K footage with professional color grading.",
            mood="Inspiring and educational. Should evoke a sense of responsibility and connection to nature.",
            auto_company_details=True,
            temperature=0.7
        )
        
        tool_id = scene_transitions_result.get('tool', {}).get('tool_id')
        print(f"Created scene transitions with ID: {tool_id}")
    except Exception as e:
        print(f"Error creating scene transitions: {str(e)}")
    
    # Example 8: Create scene splitter (requires an existing video in S3)
    print("\n=== Creating Scene Splitter (MP4 ONLY) ===")
    try:
        print("Note: Currently only MP4 video files are supported!")
        # In a real application, you would have a real S3 path to a video
        # splitter_result = client.tools.create_scene_splitter(
        #     name="Product Demo Scene Analysis",
        #     video_path="userdata/my_org/videos/product_demo.mp4",  # Must be .mp4 format
        #     bucket_name="storylinez-media"
        # )
        # print(f"Created scene splitter with ID: {splitter_result.get('tool', {}).get('tool_id')}")
        print("Scene splitter example (commented out to avoid errors)")
    except Exception as e:
        print(f"Error creating scene splitter: {str(e)}")
    
    # Example 9: List tools for an organization with filtering
    print("\n=== Listing Tools with Filtering ===")
    try:
        tools_list = client.tools.list_tools(
            tool_type="creative_brief",  # Optional filter by tool type
            include_results=False,  # Don't include large job results for faster response
            page=1,
            limit=5
        )
        
        total = tools_list.get('total', 0)
        tools = tools_list.get('tools', [])
        
        print(f"Found {total} creative briefs:")
        for i, tool in enumerate(tools):
            print(f"{i+1}. {tool.get('name')} - Created: {tool.get('created_at')}")
    except Exception as e:
        print(f"Error listing tools: {str(e)}")
    
    # Example 10: Get a specific tool with job results
    print("\n=== Getting Tool Details ===")
    try:
        # Use tool_id from a previous operation
        # In a real app, you would use an actual tool_id
        tool_id = brief_result.get('tool', {}).get('tool_id') if 'brief_result' in locals() else None
        
        if tool_id:
            tool = client.tools.get_tool(
                tool_id=tool_id,
                include_job=True
            )
            
            print(f"Tool name: {tool.get('name')}")
            print(f"Tool type: {tool.get('tool_type')}")
            print(f"Created at: {tool.get('created_at')}")
            
            # Check if job result is available
            if 'job_result' in tool:
                job_status = tool.get('job_result', {}).get('status', 'Unknown')
                print(f"Job status: {job_status}")
                
                if job_status.upper() == 'COMPLETED':
                    print("Job completed successfully!")
                    # In a real app, you would access and use the result data
                    # result_data = tool.get('job_result', {}).get('result', {})
        else:
            print("No tool_id available from previous operations")
    except Exception as e:
        print(f"Error getting tool details: {str(e)}")
    
    # Example 11: Redo a tool with modified parameters
    print("\n=== Redoing a Tool ===")
    try:
        # Use tool_id from a previous operation if available
        tool_id = brief_result.get('tool', {}).get('tool_id') if 'brief_result' in locals() else None
        
        if tool_id:
            redo_result = client.tools.redo_tool(
                tool_id=tool_id,
                # Override specific input parameters
                input_data={
                    "user_input": "Create a more detailed creative brief with focus on sustainability"
                },
                deepthink=True,
                overdrive=True
            )
            
            print(f"Restarted tool job with ID: {redo_result.get('job_id')}")
        else:
            print("No tool_id available from previous operations")
    except Exception as e:
        print(f"Error redoing tool: {str(e)}")
    
    # Example 12: Using the wait_for_tool_completion utility method
    print("\n=== Using wait_for_tool_completion ===")
    print("Example commented out to avoid waiting in demo")
    # try:
    #     # Create a new tool
    #     result = client.tools.create_creative_brief(
    #         name="Quick Brief",
    #         user_input="Create a simple creative brief"
    #     )
    #     
    #     tool_id = result.get("tool", {}).get("tool_id")
    #     print(f"Created tool with ID: {tool_id}")
    #     
    #     # Wait for completion (with timeout)
    #     print("Waiting for job to complete...")
    #     completed_tool = client.tools.wait_for_tool_completion(
    #         tool_id=tool_id,
    #         max_wait_time=60,  # Wait up to 60 seconds
    #         polling_interval=2  # Check every 2 seconds
    #     )
    #     
    #     print("Job completed!")
    #     # Access the completed results
    #     # result_data = completed_tool.get('job_result', {}).get('result', {})
    # except TimeoutError as e:
    #     print(f"Timeout waiting for job: {str(e)}")
    # except Exception as e:
    #     print(f"Error: {str(e)}")

    # Example 13: Using the create_and_wait convenience method
    print("\n=== Using create_and_wait ===")
    print("Example commented out to avoid waiting in demo")
    # try:
    #     # Create a tool and wait for completion in one call
    #     completed_tool = client.tools.create_and_wait(
    #         tool_type="creative_brief",
    #         name="One-step Brief",
    #         user_input="Create a brief for a quick campaign",
    #         max_wait_time=60  # Wait up to 60 seconds
    #     )
    #     
    #     print("Tool created and job completed!")
    #     # Access the completed results
    #     # result_data = completed_tool.get('job_result', {}).get('result', {})
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    
    # Example 14: Create a web scraper advanced job
    print("\n=== Creating Web Scraper Advanced Job ===")
    try:
        web_scraper_result = client.tools.create_web_scraper_advanced(
            name="BGiving Scrape",
            website_url="https://bgiving.one",
            depth=2,
            max_pages=5,
            max_text_chars=20000,
            enable_js=True,
            parallel=True,
            retry_count=2,
            retry_delay=1,
            timeout=16
        )
        tool_id = web_scraper_result.get('tool', {}).get('tool_id')
        job_id = web_scraper_result.get('job_id')
        print(f"Created web scraper advanced job with ID: {tool_id}")
        print(f"Job ID: {job_id}")
    except Exception as e:
        print(f"Error creating web scraper advanced job: {str(e)}")
    
if __name__ == "__main__":
    main()
