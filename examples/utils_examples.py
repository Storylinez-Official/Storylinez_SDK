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

    # Example: Enhance a prompt using company_details_id
    print("\n=== Enhancing a Prompt with Company Details ID ===")
    try:
        # Assume we have a company details profile ID
        company_details_id = "company_example_id"  # Replace with actual ID in real usage
        
        old_prompt = "Create a video about our new product launch."
        
        # Start the prompt enhancement job using company_details_id
        enhance_result = client.utils.alter_prompt(
            old_prompt=old_prompt,
            job_name="Product launch prompt with company profile",
            alter_type="enhance",
            prompt_type="prompt",
            company_details_id=company_details_id  # Using company profile ID instead of direct details
        )
        
        job_id = enhance_result.get("job_id")
        print(f"Started prompt enhancement job with company profile ID: {job_id}")
        
        # In production, you'd wait for the job to complete
        print("This would use the company details profile from your saved profiles")
        
    except Exception as e:
        print(f"Error enhancing prompt with company profile: {str(e)}")
    
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
    
    # Example 9: Extract brand settings from a website
    # This example uses the `/extract-brand-settings` endpoint, matching the backend and SDK.
    print("\n=== Extracting Brand Settings from Website ===")
    try:
        website_url = "https://bgiving.one"  # Replace with a real website
        brand_job = client.utils.extract_brand_settings(
            website_url=website_url,
            org_id=ORG_ID,
            job_name=f"Brand Settings Extraction - {website_url}",
            temperature=0.7,
            timeout=15,
            include_palette=True,
            dynamic_extraction=False,
            max_elements=100,
            web_search=False
        )
        job_id = brand_job.get("job_id")
        print(f"Started brand settings extraction job with ID: {job_id}")
        # In a real app, you would poll for job completion and fetch the result
    except Exception as e:
        print(f"Error extracting brand settings: {str(e)}")

    # Example 6: Enhance a prompt with advanced control parameters
    print("\n=== Enhancing a Prompt with Advanced Control Parameters ===")
    try:
        old_prompt = "Create a video about our new AI-powered software for businesses."
        
        # Start the prompt enhancement job with control parameters
        enhance_result = client.utils.alter_prompt(
            old_prompt=old_prompt,
            job_name="AI Software Video with Control Parameters",
            alter_type="enhance",
            prompt_type="sequence",
            company_details="Technology startup specializing in AI business solutions",
            # Advanced control parameters (0-100)
            creativity=85,          # High creativity for innovative content
            formality=70,          # Professional but not overly formal
            detail_level=90,       # Very detailed explanations
            urgency=60,            # Moderate sense of urgency
            emotional_tone=75,     # Engaging and exciting
            energy_level=80,       # High energy for software demo
            retention_focus=95,    # Maximum retention for business audience
            pacing=70,             # Fast-paced for modern audience
            cut_frequency=80,      # Frequent cuts for engagement
            clip_length=60,        # Shorter clips for attention span
            narrative_structure=85  # Complex storytelling for business case
        )
        
        job_id = enhance_result.get("job_id")
        print(f"Started advanced prompt enhancement job with ID: {job_id}")
        print("Control parameters used:")
        print("  - Creativity: 85 (High innovation)")
        print("  - Formality: 70 (Professional)")
        print("  - Detail Level: 90 (Very detailed)")
        print("  - Retention Focus: 95 (Maximum engagement)")
        print("  - Energy Level: 80 (High energy)")
        
        # In a real application, you'd wait for the job to complete
        print("Waiting for job to complete...")
        time.sleep(2)
        
        # Check job result
        try:
            job_result = client.utils.get_job_result(job_id=job_id)
            
            has_result = "result" in job_result and job_result.get("result")
            has_error = job_result.get("error") is not None
            
            if has_result:
                print(f"Advanced enhancement completed successfully")
                result = job_result.get("result", {})
                enhanced_prompt = result.get("prompt", "")
                print(f"Enhanced prompt (first 150 chars): {enhanced_prompt[:150]}...")
            elif has_error:
                print(f"Job failed with error: {job_result.get('error')}")
            else:
                print("Job still processing. Check back later.")
        except Exception as job_e:
            print(f"Error checking job result: {str(job_e)}")
            
    except Exception as e:
        print(f"Error enhancing prompt with control parameters: {str(e)}")

    # Example 7: Creative randomization with control parameters for social media
    print("\n=== Creative Randomization for Social Media Content ===")
    try:
        old_prompt = "Showcase our eco-friendly product benefits."
        
        # Start a randomization job optimized for social media
        randomize_result = client.utils.alter_prompt(
            old_prompt=old_prompt,
            job_name="Social Media Creative Variation",
            alter_type="randomize",
            prompt_type="prompt",
            company_details="Sustainable lifestyle brand targeting millennials",
            # Social media optimized parameters
            creativity=95,          # Maximum creativity for viral content
            sarcasm=40,            # Light humor but not too sarcastic
            formality=20,          # Very casual for social media
            detail_level=60,       # Moderate detail for quick consumption
            urgency=80,            # High urgency for action
            emotional_tone=90,     # Highly emotional for engagement
            energy_level=95,       # Maximum energy for social platforms
            retention_focus=100,   # Maximum retention tactics
            pacing=90,             # Very fast pacing
            cut_frequency=95,      # Very frequent cuts
            clip_length=90,        # Short, punchy clips
            narrative_structure=70  # Engaging but not overly complex
        )
        
        job_id = randomize_result.get("job_id")
        print(f"Started social media randomization job with ID: {job_id}")
        print("Social media optimization parameters:")
        print("  - Creativity: 95 (Maximum for viral potential)")
        print("  - Formality: 20 (Very casual)")
        print("  - Energy Level: 95 (High energy)")
        print("  - Retention Focus: 100 (Maximum engagement)")
        print("  - Cut Frequency: 95 (Fast cuts)")
        
    except Exception as e:
        print(f"Error creating social media variation: {str(e)}")

    # Example 8: Corporate presentation with control parameters
    print("\n=== Corporate Presentation Enhancement ===")
    try:
        old_prompt = "Present our quarterly business results and future strategy."
        
        # Start enhancement job optimized for corporate presentation
        corporate_result = client.utils.alter_prompt(
            old_prompt=old_prompt,
            job_name="Q4 Results Corporate Presentation",
            alter_type="enhance",
            prompt_type="storyboard",
            company_details="Fortune 500 technology company with focus on enterprise solutions",
            # Corporate presentation parameters
            creativity=30,          # Conservative creativity
            sarcasm=5,             # Minimal humor
            formality=95,          # Very formal and professional
            detail_level=85,       # Detailed but not overwhelming
            urgency=40,            # Low urgency, methodical
            emotional_tone=50,     # Neutral to positive
            energy_level=60,       # Moderate, professional energy
            retention_focus=70,    # Good engagement without being flashy
            pacing=40,             # Slower, methodical pacing
            cut_frequency=30,      # Longer scenes for depth
            clip_length=25,        # Longer segments for detail
            narrative_structure=90  # Complex, well-structured presentation
        )
        
        job_id = corporate_result.get("job_id")
        print(f"Started corporate presentation job with ID: {job_id}")
        print("Corporate optimization parameters:")
        print("  - Formality: 95 (Very professional)")
        print("  - Creativity: 30 (Conservative approach)")
        print("  - Narrative Structure: 90 (Well-structured)")
        print("  - Pacing: 40 (Methodical, detailed)")
        
    except Exception as e:
        print(f"Error creating corporate presentation: {str(e)}")
    
    print("\n" + "="*60)
    print("ADVANCED CONTROL PARAMETERS GUIDE")
    print("="*60)
    print("The alter_prompt method now supports advanced control parameters (0-100):")
    print()
    print("🎨 CREATIVE CONTROLS:")
    print("  • creativity: Controls creative freedom (0=conservative, 100=maximum innovation)")
    print("  • sarcasm: Adds wit and humor (0=serious, 100=witty/sarcastic)")
    print("  • narrative_structure: Storytelling complexity (0=simple, 100=multi-layered)")
    print()
    print("📝 CONTENT STYLE:")
    print("  • formality: Communication style (0=casual, 100=formal professional)")
    print("  • detail_level: Depth of information (0=high-level, 100=extremely detailed)")
    print("  • emotional_tone: Engagement level (0=neutral, 100=highly emotional)")
    print()
    print("⚡ PACING & ENERGY:")
    print("  • urgency: Sense of immediacy (0=relaxed, 100=high urgency)")
    print("  • energy_level: Overall enthusiasm (0=calm, 100=high energy)")
    print("  • pacing: Content rhythm (0=slow methodical, 100=fast dynamic)")
    print()
    print("🎬 VIDEO-SPECIFIC:")
    print("  • cut_frequency: Scene changes (0=long scenes, 100=frequent cuts)")
    print("  • clip_length: Segment duration (0=longer, 100=short punchy clips)")
    print("  • retention_focus: Audience attention (0=standard, 100=maximum tactics)")
    print()
    print("💡 USAGE TIPS:")
    print("  • All parameters are optional - omit them for standard behavior")
    print("  • Parameters work together harmoniously")
    print("  • Higher values aren't always better - find the right balance")
    print("  • Invalid values (outside 0-100) are silently ignored")
    print("="*60)
    
if __name__ == "__main__":
    main()
