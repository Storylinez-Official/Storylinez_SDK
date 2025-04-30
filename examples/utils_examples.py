from storylinez import StorylinezClient
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables or use fallbacks
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
    
    # Example 1: Get available voice types
    print("\n=== Getting Voice Types ===")
    try:
        voices = client.utils.get_voice_types()
        print(f"Available voice types:")
        for language, voices in list(voices.get("voice_types", {}).items())[:3]:  # Show first 3 languages only
            print(f"  {language}: {len(voices)} voices")
        print("  ... (more languages available)")
    except Exception as e:
        print(f"Error getting voice types: {str(e)}")
    
    # Example 2: Get transition types
    print("\n=== Getting Transition Types ===")
    try:
        transitions = client.utils.get_transition_types()
        print(f"Available transitions: {list(transitions.get('transition_types', {}).keys())}")
    except Exception as e:
        print(f"Error getting transition types: {str(e)}")
    
    # Example 3: Get template types
    print("\n=== Getting Template Types ===")
    try:
        templates = client.utils.get_template_types()
        print(f"Available template categories:")
        for category, templates_list in list(templates.get("template_types", {}).items())[:3]:  # Show first 3 categories
            print(f"  {category}: {len(templates_list)} templates")
    except Exception as e:
        print(f"Error getting template types: {str(e)}")
    
    # Example 4: Get color grades
    print("\n=== Getting Color Grades ===")
    try:
        grades = client.utils.get_color_grades()
        print(f"Available color grades:")
        color_grades = grades.get("color_grades", {})
        print(f"  Single grades: {len(color_grades.get('single', []))} options")
        print(f"  Multiple grades: {len(color_grades.get('multiple', []))} options")
    except Exception as e:
        print(f"Error getting color grades: {str(e)}")
    
    # Example 5: Enhance a prompt
    print("\n=== Enhancing a Prompt ===")
    try:
        old_prompt = "Create a video about sustainable packaging solutions."
        
        # Start the prompt enhancement job
        enhance_result = client.utils.alter_prompt(
            old_prompt=old_prompt,
            job_name="Enhanced packaging prompt",
            alter_type="enhance",
            prompt_type="prompt",
            company_details="Eco-friendly packaging company focused on reducing plastic waste."
        )
        
        job_id = enhance_result.get("job_id")
        print(f"Started prompt enhancement job with ID: {job_id}")
        
        # In a real application, you'd wait for the job to complete
        # For this example, we'll simulate waiting briefly
        print("Waiting for job to complete...")
        time.sleep(2)  # In a real app, you'd poll or use webhooks
        
        # Check job result
        try:
            job_result = client.utils.get_job_result(job_id=job_id)
            
            # Determine job status by checking fields
            has_result = "result" in job_result and job_result.get("result")
            has_error = job_result.get("error") is not None
            
            if has_result:
                print(f"Job completed successfully")
                result = job_result.get("result", {})
                enhanced_prompt = result.get("prompt", "")
                print(f"Enhanced prompt: {enhanced_prompt[:100]}...")  # Show first 100 chars
            elif has_error:
                print(f"Job failed with error: {job_result.get('error')}")
            else:
                print("Job still processing. Check back later.")
        except Exception as job_e:
            print(f"Error checking job result: {str(job_e)}")
            
    except Exception as e:
        print(f"Error enhancing prompt: {str(e)}")
    
    # Example 6: Get search recommendations
    print("\n=== Getting Search Recommendations ===")
    try:
        user_query = "stock videos of people in business meetings"
        
        search_job = client.utils.search_recommendations(
            user_query=user_query,
            job_name="Business meeting search help",
            deepthink=True,
            temperature=0.7
        )
        
        job_id = search_job.get("job_id")
        print(f"Started search recommendations job with ID: {job_id}")
        
        # In a real app, you would check the result after some time
        
    except Exception as e:
        print(f"Error getting search recommendations: {str(e)}")
    
    # Example 7: Extract organization info from website
    print("\n=== Extracting Organization Information ===")
    try:
        website_url = "https://www.example.com"  # Replace with a real website
        
        info_job = client.utils.get_organization_info(
            website_url=website_url,
            job_name="Example.com info extraction",
            deepthink=True,
            web_search=True,
            temperature=0.7
        )
        
        job_id = info_job.get("job_id")
        print(f"Started organization info extraction job with ID: {job_id}")
        
        # Again, in a real app, you would check the result after job completion
        
    except Exception as e:
        print(f"Error extracting organization info: {str(e)}")
    
    # Example 8: List utility jobs for the organization
    print("\n=== Listing Utility Jobs ===")
    try:
        jobs = client.utils.list_jobs(
            job_type="alter_prompt",  # Optional filter by job type
            page=1,
            limit=5
        )
        
        total_jobs = jobs.get("total", 0)
        job_list = jobs.get("jobs", [])
        print(f"Found {total_jobs} jobs of type 'alter_prompt'")
        
        for i, job in enumerate(job_list):
            print(f"{i+1}. {job.get('job_name')} - Created: {job.get('created_at')} - Type: {job.get('job_type')}")
            
    except Exception as e:
        print(f"Error listing jobs: {str(e)}")

if __name__ == "__main__":
    main()
