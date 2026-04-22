import os
from dotenv import load_dotenv
import ultraprint.common as p
from storylinez import StorylinezClient
import time

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.environ.get("STORYLINEZ_API_KEY")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID")

# Accept keys if not set in .env
if not API_KEY:
    API_KEY = input("Enter your Storylinez API Key: ")
if not API_SECRET:
    API_SECRET = input("Enter your Storylinez API Secret: ")
if not ORG_ID:
    ORG_ID = input("Enter your Storylinez Org ID: ")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_key():
    p.lgray("\nPress Enter to continue...")
    input()

def print_banner():
    p.cyan_bg(" STORYLINEZ VIDEO BUILDER ")
    p.n()
    p.lgray("Create stunning videos using the Storylinez SDK, with full control and helpful tips at every step.")
    p.n()
    return None

def print_tip(msg):
    _ = p.yellow("Tip: " + msg)
    _ = p.n()
    return None

def print_error(msg):
    _ = p.red("Error: " + msg)
    _ = p.n()
    return None

def select_from_list(options, prompt="Select an option:"):
    for idx, opt in enumerate(options):
        p.green(f"[{idx+1}] {opt}")
    while True:
        try:
            p.lgray(prompt + " ")
            choice = int(input())
            if 1 <= choice <= len(options):
                return choice - 1
        except Exception:
            pass
        print_error("Invalid selection. Please enter a number from the list.")

def get_input(msg, default=None, required=False, help_text=None, choices=None):
    """
    Enhanced input with help and choices.
    """
    prompt = f"{msg}"
    if default is not None:
        prompt += f" [{default}]"
    if help_text:
        prompt += " (type '?' for help)"
    prompt += ": "
    while True:
        val = input(prompt) 
        
        if val.strip() == "?" and help_text:
            _ = p.cyan(help_text)  # Capture the return value in throwaway variable
            if choices:
                _ = p.yellow("Choices: " + ", ".join(str(c) for c in choices))
            continue
            
        if choices and val.strip() and val.strip() not in choices:
            _ = print_error(f"Invalid choice. Valid options: {', '.join(choices)}")
            continue
            
        if val.strip() == "" and default is not None:
            return default
            
        if val.strip() or not required:
            return val.strip()
            
        _ = print_error("This field is required.")

def main_menu():
    clear_screen()
    print_banner()  # Don't capture or use the return value
    p.blue("Welcome to the Storylinez Video Builder CLI!")
    p.n()
    p.lgray("Follow the menu to create a video from start to finish, with full control at each step.")
    p.n()
    p.green("[1] Start a new video project")
    p.green("[2] Browse and continue existing projects")
    p.green("[3] Exit")
    p.yellow("Tip: You can type '?' at any prompt for more information.")
    return get_input("Choose an option", required=True, help_text="Type 1 to start a new project, 2 to browse existing projects, or 3 to exit.", choices=["1", "2", "3"])

def project_menu(client):
    clear_screen()
    print_banner()
    p.bold("Step 1: Create a Project")
    print_tip("Project orientation cannot be changed later. Choose wisely based on your target platform.")
    p.yellow("Trick: Use 'landscape' for YouTube, 'portrait' for TikTok/Reels.")
    name = get_input("Project name", required=True, help_text="A descriptive name for your project. Example: 'Spring Campaign Video'")
    orientation = ""
    while orientation not in ["landscape", "portrait"]:
        orientation = get_input("Orientation", default="landscape", help_text="Choose 'landscape' (16:9) or 'portrait' (9:16)", choices=["landscape", "portrait"]).lower()
    purpose = get_input("Project purpose (optional)", help_text="Describe the goal of this video. E.g. 'Brand awareness for eco line'")
    target_audience = get_input("Target audience (optional)", help_text="Who is this video for? E.g. 'Millennials, eco-conscious buyers'")
    p.n()
    p.lgray("Creating project...")
    try:
        project = client.project.create_project(
            name=name,
            orientation=orientation,
            purpose=purpose,
            target_audience=target_audience
        )
        project_id = project["project"]["project_id"]
        p.green(f"Project created with ID: {project_id}")
        p.yellow("Tip: You can upload custom media to this project at any time.")
        wait_key()
        return project_id
    except Exception as e:
        print_error(str(e))
        wait_key()
        return None

def prompt_menu(client, project_id):
    clear_screen()
    print_banner()
    p.bold("Step 2: Create a Prompt")
    print_tip("You can use a text prompt or a reference video. Text prompts are more flexible, video prompts extract style from an example video.")
    p.yellow("Trick: Use detailed prompts for better results. Reference videos are great for matching style/tone.")
    prompt_type = select_from_list(["Text Prompt", "Reference Video Prompt"], "Prompt type?")
    if prompt_type == 0:
        main_prompt = get_input("Main prompt", required=True, help_text="Describe your video. E.g. 'Showcase our eco-friendly products in a fun, upbeat way.'")
        document_context = get_input("Document context (optional)", help_text="Extra info for the AI, e.g. company background, product details.")
        temperature = float(get_input("AI temperature", default="0.7", help_text="0.0=conservative, 1.0=creative. Try 0.5-0.8 for most cases."))
        total_length = int(get_input("Target video length (seconds)", default="20", help_text="10-60 seconds is typical for social videos."))
        iterations = int(get_input("Refinement iterations", default="3", help_text="More iterations = better results, but slower. 3-5 is a good range."))
        deepthink = get_input("Enable deepthink? (y/n)", default="n", help_text="Deepthink gives more thoughtful, detailed results. Slower.").lower() == "y"
        overdrive = get_input("Enable overdrive? (y/n)", default="n", help_text="Overdrive maximizes quality/detail. Use with deepthink for best results.").lower() == "y"
        web_search = get_input("Enable web search? (y/n)", default="n", help_text="Web search brings in up-to-date info. Useful for trending topics.").lower() == "y"
        eco = get_input("Enable eco mode? (y/n)", default="n", help_text="Eco mode is faster/cheaper but less detailed.").lower() == "y"
        skip_voiceover = get_input("Skip voiceover? (y/n)", default="n", help_text="Skip if you want to add your own voiceover later.").lower() == "y"
        voiceover_mode = get_input("Voiceover mode", default="generated", help_text="Choose 'generated' for AI voice, 'uploaded' to use your own.", choices=["generated", "uploaded"])
        p.yellow("Tip: Use deepthink+overdrive for best scripts. Lower temperature for more factual content.")
        p.lgray("Creating text prompt...")
        try:
            client.prompt.create_text_prompt(
                project_id=project_id,
                main_prompt=main_prompt,
                document_context=document_context,
                temperature=temperature,
                total_length=total_length,
                iterations=iterations,
                deepthink=deepthink,
                overdrive=overdrive,
                web_search=web_search,
                eco=eco,
                skip_voiceover=skip_voiceover,
                voiceover_mode=voiceover_mode
            )
            p.green("Prompt created successfully.")
        except Exception as e:
            print_error(str(e))
    else:
        reference_video_id = get_input("Reference video ID", required=True, help_text="ID of a video already uploaded to your org.")
        temperature = float(get_input("AI temperature", default="0.7"))
        total_length = int(get_input("Target video length (seconds)", default="20"))
        iterations = int(get_input("Refinement iterations", default="3"))
        deepthink = get_input("Enable deepthink? (y/n)", default="n").lower() == "y"
        overdrive = get_input("Enable overdrive? (y/n)", default="n").lower() == "y"
        web_search = get_input("Enable web search? (y/n)", default="n").lower() == "y"
        eco = get_input("Enable eco mode? (y/n)", default="n").lower() == "y"
        skip_voiceover = get_input("Skip voiceover? (y/n)", default="n").lower() == "y"
        voiceover_mode = get_input("Voiceover mode", default="generated", choices=["generated", "uploaded"])
        include_detailed_analysis = get_input("Include detailed analysis? (y/n)", default="n", help_text="Get more info about the reference video.").lower() == "y"
        p.lgray("Creating video prompt...")
        try:
            client.prompt.create_video_prompt(
                project_id=project_id,
                reference_video_id=reference_video_id,
                temperature=temperature,
                total_length=total_length,
                iterations=iterations,
                deepthink=deepthink,
                overdrive=overdrive,
                web_search=web_search,
                eco=eco,
                skip_voiceover=skip_voiceover,
                voiceover_mode=voiceover_mode,
                include_detailed_analysis=include_detailed_analysis
            )
            p.green("Prompt created successfully.")
        except Exception as e:
            print_error(str(e))
    wait_key()

def search_menu(client, project_id):
    clear_screen()
    print_banner()
    p.bold("Step 3: Generate Search Queries")
    print_tip("Let the AI suggest search queries for stock videos, audio, and images. You can customize the number of each.")
    
    # Add option for automatic search and add
    p.n()
    p.green("[1] Manual search and add (step-by-step)")
    p.green("[2] Automatic search and add (let AI do it)")
    p.n()
    
    auto_mode = get_input("Choose search mode", default="1", choices=["1", "2"]) == "2"
    
    if auto_mode:
        p.yellow("Using automatic search and add mode")
        auto_add_stock_media_to_project(client, project_id)
        # Return empty lists since we've already added the stock media
        return [], [], []
    
    # Original manual search code
    p.yellow("Trick: Use more queries for more variety. Use company details for more brand-appropriate results.")
    num_videos = int(get_input("Number of video queries", default="3", help_text="More queries = more stock video options."))
    num_audio = int(get_input("Number of audio queries", default="2", help_text="More queries = more music options."))
    num_images = int(get_input("Number of image queries", default="0", help_text="Set >0 to use images in your video."))
    company_details = get_input("Company details (optional)", help_text="Paste your company summary for more relevant results.")
    max_wait = int(get_input("Max wait seconds for AI to finish", default="60", help_text="Increase if you want to wait longer for results."))
    poll_interval = int(get_input("Polling interval (seconds)", default="3", help_text="How often to check for results."))
    p.yellow("Tip: If you get empty results, try increasing the number of queries or lowering the similarity threshold in the next step.")
    p.lgray("Generating search queries...")
    try:
        search_query_results = client.prompt.start_query_gen_and_wait(
            project_id=project_id,
            num_videos=num_videos,
            num_audio=num_audio,
            num_images=num_images,
            company_details=company_details,
            max_wait_seconds=max_wait,
            poll_interval_seconds=poll_interval
        )
        p.green("Search queries generated.")
        videos = search_query_results["result"]["results"].get("videos", [])
        audios = search_query_results["result"]["results"].get("audio", [])
        images = search_query_results["result"]["results"].get("images", [])
        p.cyan("Video queries:"); p.lgray(str(videos))
        p.cyan("Audio queries:"); p.lgray(str(audios))
        p.cyan("Image queries:"); p.lgray(str(images))
        wait_key()
        return videos, audios, images
    except Exception as e:
        print_error(str(e))
        wait_key()
        return [], [], []

def stock_menu(client, queries, media_type, orientation=None):
    clear_screen()
    print_banner()
    p.bold(f"Step 4: Search for Stock {media_type.capitalize()}")
    print_tip("You can adjust the number of results and filters for better matches.")
    p.yellow("Trick: Lower similarity threshold for more results. Use orientation for best fit.")
    num_results = int(get_input(f"Number of {media_type} results", default="3", help_text="How many stock items to fetch per query."))
    similarity = float(get_input("Similarity threshold (0.0-1.0, lower=more results)", default="0.1", help_text="Lower = more results, higher = more precise."))
    collections = [media_type]
    kwargs = {
        "queries": queries,
        "collections": collections,
        "detailed": True,
        "generate_thumbnail": True,
        "generate_streamable": True,
        "generate_download": True,
        f"num_results_{media_type}s": num_results,
        "similarity_threshold": similarity,
    }
    if media_type == "videos" and orientation:
        kwargs["orientation"] = orientation
    p.lgray(f"Searching for stock {media_type}...")
    try:
        stock = client.stock.search(**kwargs)
        ids = [item["stock_id"] for item in stock.get(media_type, [])]
        p.green(f"Found {len(ids)} stock {media_type}.")
        p.yellow("Tip: If you want to use your own media, upload it and add to the project before storyboarding.")
        wait_key()
        return ids
    except Exception as e:
        print_error(str(e))
        wait_key()
        return []

def add_stock_menu(client, project_id, stock_ids, media_type):
    clear_screen()
    print_banner()
    p.bold(f"Step 5: Add Stock {media_type.capitalize()} to Project")
    print_tip("Adding stock media to your project makes them available for storyboarding and rendering.")
    p.yellow("Trick: You can mix stock and custom media for unique results.")
    for stock_id in stock_ids:
        try:
            res = client.project.add_stock_file(
                project_id=project_id,
                stock_id=stock_id,
                media_type=media_type
            )
            p.green(f"Added {media_type[:-1]}: {stock_id}")
            time.sleep(1)
        except Exception as e:
            print_error(str(e))
    wait_key()

def storyboard_menu(client, project_id):
    clear_screen()
    print_banner()
    p.bold("Step 6: Create the Storyboard")
    print_tip("Storyboards define the structure and flow of your video. More iterations and deepthink can improve quality.")
    p.yellow("Trick: Use deepthink+overdrive for best storyboards. Use uploaded voiceover for more control.")
    deepthink = get_input("Enable deepthink? (y/n)", default="n", help_text="Deepthink gives more thoughtful, detailed results.").lower() == "y"
    overdrive = get_input("Enable overdrive? (y/n)", default="n", help_text="Overdrive maximizes quality/detail. Use with deepthink for best results.").lower() == "y"
    web_search = get_input("Enable web search? (y/n)", default="n", help_text="Web search brings in up-to-date info. Useful for trending topics.").lower() == "y"
    eco = get_input("Enable eco mode? (y/n)", default="y", help_text="Eco mode is faster/cheaper but less detailed.").lower() == "y"
    temperature = float(get_input("AI temperature", default="0.7", help_text="0.0=conservative, 1.0=creative."))
    iterations = int(get_input("Refinement iterations", default="3", help_text="More iterations = better results, but slower."))
    full_length = int(get_input("Storyboard length (seconds)", default="10", help_text="Target length for the storyboard."))
    voiceover_mode = get_input("Voiceover mode", default="generated", help_text="Choose 'generated' for AI voice, 'uploaded' to use your own.", choices=["generated", "uploaded"])
    skip_voiceover = get_input("Skip voiceover? (y/n)", default="n", help_text="Skip if you want to add your own voiceover later.").lower() == "y"
    p.lgray("Creating storyboard...")
    try:
        storyboard_job = client.storyboard.create_storyboard(
            project_id=project_id,
            deepthink=deepthink,
            overdrive=overdrive,
            web_search=web_search,
            eco=eco,
            temperature=temperature,
            iterations=iterations,
            full_length=full_length,
            voiceover_mode=voiceover_mode,
            skip_voiceover=skip_voiceover
        )
        storyboard_id = storyboard_job["storyboard"]["storyboard_id"]
        p.green(f"Storyboard created with ID: {storyboard_id}")
        p.yellow("Tip: You can edit the storyboard before rendering for more control.")
        wait_key()
        return storyboard_id
    except Exception as e:
        print_error(str(e))
        wait_key()
        return None

def voiceover_menu(client, project_id):
    clear_screen()
    print_banner()
    p.bold("Step 7: Create the Voiceover")
    print_tip("Voiceovers bring your story to life. You can choose a voice or upload your own.")
    p.yellow("Trick: Upload your own voiceover for a personal touch. Use generated for speed.")
    use_custom = get_input("Use custom voiceover file? (y/n)", default="n", help_text="Upload a .wav file to your org first.").lower() == "y"
    if use_custom:
        file_id = get_input("Enter voiceover file_id", required=True, help_text="File ID of your uploaded .wav file.")
        try:
            client.project.add_voiceover(project_id=project_id, file_id=file_id)
            p.green("Custom voiceover added to project.")
            wait_key()
            return None
        except Exception as e:
            print_error(str(e))
            wait_key()
            return None
    else:
        p.lgray("Creating AI-generated voiceover...")
        try:
            voiceover_job = client.voiceover.create_voiceover(project_id=project_id)
            voiceover_id = voiceover_job["voiceover"]["voiceover_id"]
            p.green(f"Voiceover job started with ID: {voiceover_id}")
            p.yellow("Tip: You can download the generated voiceover and replace it with your own if desired.")
            wait_key()
            return voiceover_id
        except Exception as e:
            print_error(str(e))
            wait_key()
            return None

def sequence_menu(client, project_id, orientation):
    clear_screen()
    print_banner()
    p.bold("Step 8: Create the Sequence")
    print_tip("Sequences combine storyboard, voiceover, and media into a timeline. You can apply templates or grading.")
    p.yellow("Trick: Use templates for fast results. Use grading for cinematic color.")
    apply_template = get_input("Apply template? (y/n)", default="n", help_text="Templates add style and structure.").lower() == "y"
    apply_grade = get_input("Apply color grading? (y/n)", default="n", help_text="Color grading gives a cinematic look.").lower() == "y"
    grade_type = get_input("Grade type", default="single", help_text="Choose 'single' for one grade, 'multi' for different grades per scene.", choices=["single", "multi"])
    deepthink = get_input("Enable deepthink? (y/n)", default="n").lower() == "y"
    overdrive = get_input("Enable overdrive? (y/n)", default="n").lower() == "y"
    web_search = get_input("Enable web search? (y/n)", default="n").lower() == "y"
    eco = get_input("Enable eco mode? (y/n)", default="y").lower() == "y"
    temperature = float(get_input("AI temperature", default="0.7"))
    iterations = int(get_input("Refinement iterations", default="1"))
    p.lgray("Creating sequence...")
    try:
        sequence_job = client.sequence.create_sequence(
            project_id=project_id,
            apply_template=apply_template,
            apply_grade=apply_grade,
            grade_type=grade_type,
            orientation=orientation,
            deepthink=deepthink,
            overdrive=overdrive,
            web_search=web_search,
            eco=eco,
            temperature=temperature,
            iterations=iterations
        )
        sequence_id = sequence_job["sequence"]["sequence_id"]
        p.green(f"Sequence created with ID: {sequence_id}")
        p.yellow("Tip: You can edit the sequence before rendering for advanced control.")
        wait_key()
        return sequence_id
    except Exception as e:
        print_error(str(e))
        wait_key()
        return None

def render_menu(client, project_id):
    """Display render options and handle rendering a project"""
    while True:
        clear_screen()
        print_banner()
        p.bold("Render Project")
        
        # Get project details
        project = client.project.get_project(project_id)
        project_name = project.get('name', 'Unknown Project')
        orientation = project.get('orientation', 'landscape')
        
        p.cyan(f"Project: {project_name}")
        p.cyan(f"Orientation: {orientation}")
        p.n()
        
        # Define default render settings
        target_width = 1280 if orientation == 'landscape' else 720
        target_height = 720 if orientation == 'landscape' else 1280
        
        p.bold("Render Settings")
        p.green(f"1. Resolution: {target_width}x{target_height}")
        p.green("2. Background Music Volume: 0.5")
        p.green("3. Video Audio Volume: 0.0")
        p.green("4. Voiceover Volume: 0.5")
        p.green("5. Enable Subtitles: Yes")
        p.green("6. Company name: Default")
        p.green("7. Call to action: Default")
        p.n()
        
        p.bold("Options:")
        p.green("[R] Start Rendering")
        p.green("[B] Back to Project")
        p.n()
        
        choice = input("Enter your choice: ").strip().upper()
        
        if choice == 'R':
            # Start render process
            render_job = client.render.create_render(
                project_id=project_id,
                target_width=target_width,
                target_height=target_height,
                bg_music_volume=0.5,
                video_audio_volume=0.0,
                voiceover_volume=0.5,
                subtitle_enabled=True,
                outro_duration=5.0,
                company_name="My Company",
                company_subtext="My Tagline",
                call_to_action="Visit our website",
                call_to_action_subtext="Learn more about us",
                enable_cta=True,
                extend_short_clips=True,
                extension_method="freeze"
            )
            
            render_job_id = render_job["job_id"]
            p.green(f"Render job started with ID: {render_job_id}")
            
            # Wait for render to complete
            wait_for_render(client, project_id)
            
            break
        elif choice == 'B':
            break

def wait_for_render(client, project_id):
    """Wait for render to complete and display progress"""
    p.yellow("Waiting for render to complete. This may take several minutes...")
    p.yellow("Press Ctrl+C to return to menu (render will continue in background)")
    
    try:
        while True:
            render_results = client.render.get_render(
                project_id=project_id,
                include_results=True,
                generate_streamable_link=True
            )
            
            status = render_results.get("status", "PENDING")
            
            if status == "COMPLETED":
                p.green("Render completed successfully!")
                streamable_url = render_results.get("streamable_url")
                if streamable_url:
                    p.green(f"Video available at: {streamable_url}")
                break
            elif status == "FAILED":
                p.red("Render failed")
                error = render_results.get("error", "Unknown error")
                p.red(f"Error: {error}")
                break
            elif status == "PENDING" or status == "PROCESSING":
                p.yellow(f"Status: {status} - please wait...")
                time.sleep(5)  # Poll every 5 seconds
            else:
                p.yellow(f"Status: {status}")
                time.sleep(5)
    
    except KeyboardInterrupt:
        p.yellow("Returning to menu. Render will continue in background.")

def browse_projects_menu(client):
    """Browse and select an existing project to continue working with"""
    current_page = 1
    page_size = 10
    selected_folder_id = None
    org_id = ORG_ID
    
    while True:
        clear_screen()
        print_banner()
        p.bold("Browse Projects")
        
        if selected_folder_id:
            folder_result = client.project.get_projects_by_folder(
                folder_id=selected_folder_id,
                page=current_page,
                limit=page_size,
                generate_thumbnail_links=True,
                org_id=org_id
            )
            folder = client.project.get_all_folders(org_id=org_id).get("folders", [])
            folder_name = next((f["name"] for f in folder if f["folder_id"] == selected_folder_id), "Unknown Folder")
            p.cyan(f"Current Folder: {folder_name}")
        else:
            folder_result = client.project.get_projects_by_folder(
                folder_id=None,  # Root projects
                page=current_page,
                limit=page_size,
                generate_thumbnail_links=True,
                org_id=org_id
            )
            p.cyan("Viewing: Root Projects (no folder)")
        
        # Show pagination info
        pagination = folder_result.get("pagination", {})
        total_pages = pagination.get("total_pages", 1)
        total_items = pagination.get("total", 0)
        p.lgray(f"Page {current_page} of {total_pages} (Total Projects: {total_items})")
        
        # Show folder options
        p.n()
        p.bold("Options:")
        p.green("[F] Browse Folders")
        if selected_folder_id:
            p.green("[R] Return to Root")
        p.green("[N] Next Page") if current_page < total_pages else None
        p.green("[P] Previous Page") if current_page > 1 else None
        p.green("[C] Create New Project")
        p.green("[B] Back to Main Menu")
        p.n()
        
        # List projects
        projects = folder_result.get("projects", [])
        if not projects:
            p.yellow("No projects found in this location.")
        else:
            p.bold("Projects:")
            for idx, project in enumerate(projects):
                status_emoji = "🔄" if project.get("status") == "ongoing" else "✅" if project.get("status") == "completed" else "📝"
                p.green(f"[{idx+1}] {status_emoji} {project.get('name')} ({project.get('orientation')})")
        
        p.n()
        p.lgray("Enter option or project number to view details: ")
        choice = input().strip().upper()
        
        # Handle pagination and navigation options
        if choice == "F":
            selected_folder_id = browse_folders_menu(client, org_id)
            current_page = 1  # Reset to first page when changing folders
        elif choice == "R" and selected_folder_id:
            selected_folder_id = None
            current_page = 1
        elif choice == "N" and current_page < total_pages:
            current_page += 1
        elif choice == "P" and current_page > 1:
            current_page -= 1
        elif choice == "C":
            return "create_new"
        elif choice == "B":
            return None
        elif choice.isdigit() and 1 <= int(choice) <= len(projects):
            # View project details and potentially select it
            selected_project = projects[int(choice)-1]
            selected_project_id = selected_project.get("project_id")
            if project_details_menu(client, selected_project_id):
                return selected_project_id
            # If False is returned, we go back to project browsing

def browse_folders_menu(client, org_id):
    """Browse and select folders to navigate to"""
    current_page = 1
    page_size = 10
    
    while True:
        clear_screen()
        print_banner()
        p.bold("Browse Folders")
        
        # Fetch folders for the organization
        folder_result = client.project.get_all_folders(org_id=org_id)
        folders = folder_result.get("folders", [])
        
        if not folders:
            p.yellow("No folders found in this organization.")
            p.green("[C] Create New Folder")
            p.green("[B] Back to Projects")
            p.n()
            
            choice = input("Enter your choice: ").strip().upper()
            
            if choice == 'C':
                create_folder_menu(client, org_id)
            elif choice == 'B':
                return None
        else:
            # Calculate pagination
            total_folders = len(folders)
            total_pages = (total_folders + page_size - 1) // page_size
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, total_folders)
            displayed_folders = folders[start_idx:end_idx]
            
            p.lgray(f"Page {current_page} of {total_pages}")
            p.n()
            
            p.bold("Options:")
            p.green("[C] Create New Folder")
            p.green("[N] Next Page") if current_page < total_pages else None
            p.green("[P] Previous Page") if current_page > 1 else None
            p.green("[B] Back to Projects")
            p.n()
            
            p.bold("Folders:")
            for idx, folder in enumerate(displayed_folders):
                p.green(f"[{idx+1}] {folder.get('name')}")
            
            p.n()
            p.lgray("Enter folder number or option: ")
            choice = input().strip().upper()
            
            if choice == 'C':
                create_folder_menu(client, org_id)
            elif choice == 'N' and current_page < total_pages:
                current_page += 1
            elif choice == 'P' and current_page > 1:
                current_page -= 1
            elif choice == 'B':
                return None
            elif choice.isdigit() and 1 <= int(choice) <= len(displayed_folders):
                selected_folder = displayed_folders[int(choice)-1]
                return selected_folder.get("folder_id")

def create_folder_menu(client, org_id):
    """Create a new folder"""
    clear_screen()
    print_banner()
    p.bold("Create New Folder")
    p.n()
    
    folder_name = input("Enter folder name: ").strip()
    if not folder_name:
        p.yellow("Folder name cannot be empty.")
        input("Press Enter to continue...")
        return
    
    folder_description = input("Enter folder description (optional): ").strip()
    
    try:
        result = client.project.create_folder(
            name=folder_name,
            description=folder_description,
            org_id=org_id
        )
        
        p.green(f"Folder '{folder_name}' created successfully!")
        input("Press Enter to continue...")
        return result.get("folder_id")
    except Exception as e:
        p.red(f"Error creating folder: {str(e)}")
        input("Press Enter to continue...")
        return None

def browse_user_files_menu(client, org_id, current_path="/", select_mode=False, multi_select=False):
    """
    Browse user's own files in storage.
    
    Args:
        client: Storylinez client instance
        org_id: Organization ID
        current_path: Current folder path
        select_mode: If True, allows selecting files to return
        multi_select: If True, allows selecting multiple files (only used if select_mode is True)
        
    Returns:
        If select_mode is True: Selected file ID(s) or None
        If select_mode is False: None
    """
    selected_files = [] if multi_select else None
    
    while True:
        clear_screen()
        print_banner()
        p.bold("Browse Files")
        p.cyan(f"Current path: {current_path}")
        p.n()
        
        # Get folder contents
        try:
            contents = client.storage.get_folder_contents(
                path=current_path,
                recursive=False,
                detailed=True,
                generate_thumbnail=True,
                generate_streamable=False,
                org_id=org_id
            )
            
            folders = contents.get("folders", [])
            files = contents.get("files", [])
            
            p.bold("Options:")
            if current_path != "/":
                p.green("[U] Up to Parent Folder")
            p.green("[B] Back to Previous Menu")
            
            if select_mode:
                if multi_select and selected_files:
                    p.green(f"[D] Done (Selected {len(selected_files)} files)")
                elif not multi_select:
                    p.green("[Enter file number to select]")
            p.n()
            
            # Display folders first
            if folders:
                p.bold("Folders:")
                for idx, folder in enumerate(folders):
                    p.green(f"[F{idx+1}] 📁 {folder.get('name')}")
                p.n()
            
            # Then display files
            if files:
                p.bold("Files:")
                for idx, file in enumerate(files):
                    # Determine file type icon
                    mimetype = file.get('mimetype', '')
                    if mimetype.startswith('video/'):
                        icon = "🎬"
                    elif mimetype.startswith('audio/'):
                        icon = "🔊"
                    elif mimetype.startswith('image/'):
                        icon = "🖼️"
                    else:
                        icon = "📄"
                    
                    # Check if file is selected (in multi-select mode)
                    selected_marker = ""
                    if multi_select and file.get('file_id') in selected_files:
                        selected_marker = "✓ "
                    
                    p.green(f"[{idx+1}] {selected_marker}{icon} {file.get('filename')}")
            
            if not folders and not files:
                p.yellow("This folder is empty.")
            
            p.n()
            choice = input("Enter your choice: ").strip().upper()
            
            # Handle navigation
            if choice == 'U' and current_path != "/":
                # Go up to parent folder
                parts = current_path.split('/')
                current_path = '/'.join(parts[:-1])
                if not current_path:
                    current_path = "/"
            elif choice == 'B':
                return None if not multi_select else []
            elif choice == 'D' and multi_select and selected_files:
                return selected_files
            # Handle folder selection
            elif choice.startswith('F') and choice[1:].isdigit():
                folder_idx = int(choice[1:]) - 1
                if 0 <= folder_idx < len(folders):
                    selected_folder = folders[folder_idx]
                    current_path = selected_folder.get('path', current_path)
            # Handle file selection
            elif choice.isdigit():
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(files):
                    selected_file = files[file_idx]
                    file_id = selected_file.get('file_id')
                    
                    if select_mode:
                        if multi_select:
                            # Toggle selection
                            if file_id in selected_files:
                                selected_files.remove(file_id)
                                p.yellow(f"Unselected: {selected_file.get('filename')}")
                            else:
                                selected_files.append(file_id)
                                p.green(f"Selected: {selected_file.get('filename')}")
                            input("Press Enter to continue...")
                        else:
                            # Single select mode - return the selected file ID
                            return file_id
                    else:
                        # View file details
                        view_file_details(client, selected_file, org_id)
        
        except Exception as e:
            p.red(f"Error browsing files: {str(e)}")
            input("Press Enter to continue...")
            if current_path != "/":
                # Try going up a level if there's an error
                parts = current_path.split('/')
                current_path = '/'.join(parts[:-1])
                if not current_path:
                    current_path = "/"
            else:
                return None

def view_file_details(client, file, org_id):
    """View detailed information about a file"""
    while True:
        clear_screen()
        print_banner()
        
        p.bold("File Details")
        p.n()
        
        filename = file.get('filename', 'Unknown')
        mimetype = file.get('mimetype', 'Unknown')
        file_id = file.get('file_id', 'Unknown')
        
        p.cyan(f"Filename: {filename}")
        p.cyan(f"Type: {mimetype}")
        p.cyan(f"ID: {file_id}")
        
        # Get file size in readable format
        size_bytes = file.get('size', 0)
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
        
        p.cyan(f"Size: {size_str}")
        
        # Show upload date
        upload_date = file.get('upload_date')
        if upload_date:
            p.cyan(f"Uploaded: {upload_date}")
        
        p.n()
        
        # Show analysis data if available
        analysis_data = file.get('analysis_data', {})
        if analysis_data:
            p.bold("Analysis")
            results = analysis_data.get('results', {})
            
            # Show description if available
            description = results.get('description')
            if description:
                p.cyan(f"Description: {description}")
            
            # Show tags if available
            tags = results.get('tags', [])
            if tags:
                tag_str = ", ".join(tags[:5])
                if len(tags) > 5:
                    tag_str += f" and {len(tags) - 5} more"
                p.cyan(f"Tags: {tag_str}")
            
            p.n()
        
        # Show streamable link if available
        if 'streamable_url' in file:
            p.cyan(f"Preview URL: {file.get('streamable_url')}")
            p.n()
        
        p.bold("Options:")
        p.green("[B] Back")
        
        choice = input("\nEnter your choice: ").strip().upper()
        
        if choice == 'B':
            break

def view_project_files(client, project_id):
    """View files associated with a project"""
    while True:
        clear_screen()
        print_banner()
        p.bold("Project Files")
        
        # Get project files
        try:
            files_result = client.project.get_project_files(
                project_id=project_id,
                include_details=True,
                generate_thumbnail_links=True,
                generate_streamable_links=True
            )
            
            associated_files = files_result.get('associated_file_details', [])
            stock_files = files_result.get('stock_files', {})
            voiceover = files_result.get('voiceover')
            
            # Show associated files
            p.bold("Your Files:")
            if associated_files:
                for idx, file in enumerate(associated_files):
                    filename = file.get('filename', 'Unknown')
                    mimetype = file.get('mimetype', 'Unknown')
                    
                    # Determine file type icon
                    if mimetype.startswith('video/'):
                        icon = "🎬"
                    elif mimetype.startswith('audio/'):
                        icon = "🔊"
                    elif mimetype.startswith('image/'):
                        icon = "🖼️"
                    else:
                        icon = "📄"
                    
                    p.green(f"[{idx+1}] {icon} {filename}")
            else:
                p.yellow("No user files added to this project")
            p.n()
            
            # Show stock files
            p.bold("Stock Media:")
            
            # Videos
            stock_videos = stock_files.get('videos', [])
            if stock_videos:
                p.cyan("Videos:")
                for idx, stock_id in enumerate(stock_videos):
                    p.green(f"[V{idx+1}] 🎬 Stock ID: {stock_id}")
            
            # Audios
            stock_audios = stock_files.get('audios', [])
            if stock_audios:
                p.cyan("Audio:")
                for idx, stock_id in enumerate(stock_audios):
                    p.green(f"[A{idx+1}] 🔊 Stock ID: {stock_id}")
            
            # Images
            stock_images = stock_files.get('images', [])
            if stock_images:
                p.cyan("Images:")
                for idx, stock_id in enumerate(stock_images):
                    p.green(f"[I{idx+1}] 🖼️ Stock ID: {stock_id}")
            
            if not stock_videos and not stock_audios and not stock_images:
                p.yellow("No stock media added to this project")
            p.n()
            
            # Show voiceover
            p.bold("Voiceover:")
            if voiceover:
                voice_name = voiceover.get('voice_name', 'Custom Voiceover')
                voiceover_file = files_result.get('voiceover_file_details', {})
                voiceover_filename = voiceover_file.get('filename', 'Unknown File')
                p.green(f"[VO] 🔊 {voice_name} - {voiceover_filename}")
            else:
                p.yellow("No voiceover added to this project")
            p.n()
            
            # Options
            p.bold("Options:")
            p.green("[A] Add User File")
            p.green("[S] Add Stock Media")
            p.green("[V] Add/Change Voiceover")
            p.green("[R] Remove File")
            p.green("[AA] Auto-Add User Files") # New option
            p.green("[AS] Auto-Add Stock Media") # New option
            p.green("[B] Back to Project")
            p.n()
            
            choice = input("Enter your choice: ").strip().upper()
            
            if choice == 'A':
                # Add user file
                add_user_file_to_project(client, project_id)
            elif choice == 'S':
                # Add stock media
                add_stock_media_menu(client, project_id)
            elif choice == 'V':
                # Add/change voiceover
                add_voiceover_to_project(client, project_id)
            elif choice == 'R':
                # Remove file
                remove_file_from_project(client, project_id)
            elif choice == 'AA':
                # Auto-add user files
                auto_add_user_files_to_project(client, project_id)
            elif choice == 'AS':
                # Auto-add stock media
                auto_add_stock_media_to_project(client, project_id)
            elif choice == 'B':
                break
            elif choice.isdigit():
                # View file details
                idx = int(choice) - 1
                if 0 <= idx < len(associated_files):
                    view_file_details(client, associated_files[idx], None)
        
        except Exception as e:
            p.red(f"Error viewing project files: {str(e)}")
            input("Press Enter to continue...")
            break

def add_user_file_to_project(client, project_id):
    """Browse user files and add selected file to the project"""
    # Get the project details to know which org_id to use
    try:
        project = client.project.get_project(project_id)
        org_id = project.get('org_id')
        
        if not org_id:
            p.red("Could not determine organization ID for this project")
            input("Press Enter to continue...")
            return
        
        p.yellow("Select a file to add to the project:")
        selected_file = browse_user_files_menu(
            client, 
            org_id, 
            select_mode=True,
            multi_select=False
        )
        
        if selected_file:
            result = client.project.add_associated_file(
                project_id=project_id,
                file_id=selected_file
            )
            p.green("File added to project successfully!")
            input("Press Enter to continue...")
    
    except Exception as e:
        p.red(f"Error adding file to project: {str(e)}")
        input("Press Enter to continue...")

def add_voiceover_to_project(client, project_id):
    """Browse user audio files and add selected file as voiceover"""
    # Get the project details to know which org_id to use
    try:
        project = client.project.get_project(project_id)
        org_id = project.get('org_id')
        
        if not org_id:
            p.red("Could not determine organization ID for this project")
            input("Press Enter to continue...")
            return
        
        p.yellow("Select an audio file to use as voiceover:")
        selected_file = browse_user_files_menu(
            client, 
            org_id, 
            select_mode=True,
            multi_select=False
        )
        
        if selected_file:
            voice_name = input("Enter a name for this voice (or leave blank for default): ").strip()
            if not voice_name:
                voice_name = "Custom Voiceover"
                
            result = client.project.add_voiceover(
                project_id=project_id,
                file_id=selected_file,
                voice_name=voice_name
            )
            p.green("Voiceover added to project successfully!")
            input("Press Enter to continue...")
    
    except Exception as e:
        p.red(f"Error adding voiceover to project: {str(e)}")
        input("Press Enter to continue...")

def remove_file_from_project(client, project_id):
    """Remove a file from the project"""
    while True:
        clear_screen()
        print_banner()
        p.bold("Remove File from Project")
        
        try:
            # Get project files
            files_result = client.project.get_project_files(
                project_id=project_id,
                include_details=True
            )
            
            associated_files = files_result.get('associated_file_details', [])
            stock_files = files_result.get('stock_files', {})
            voiceover = files_result.get('voiceover')
            
            # Options for removal
            if not associated_files and not voiceover:
                p.yellow("No files to remove from this project")
                input("Press Enter to continue...")
                break
            
            # Show user files
            if associated_files:
                p.bold("Your Files:")
                for idx, file in enumerate(associated_files):
                    filename = file.get('filename', 'Unknown')
                    p.green(f"[{idx+1}] Remove: {filename}")
            
            # Show voiceover option
            if voiceover:
                p.n()
                p.bold("Voiceover:")
                p.green("[V] Remove voiceover")
            
            p.n()
            p.green("[B] Back to Files")
            p.n()
            
            choice = input("Enter your choice: ").strip().upper()
            
            if choice == 'B':
                break
            elif choice == 'V' and voiceover:
                # Remove voiceover
                confirm = input("Are you sure you want to remove the voiceover? (y/n): ").strip().lower()
                if confirm == 'y':
                    result = client.project.remove_voiceover(project_id=project_id)
                    p.green("Voiceover removed successfully")
                    input("Press Enter to continue...")
                    break
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(associated_files):
                    file = associated_files[idx]
                    filename = file.get('filename', 'Unknown')
                    file_id = file.get('file_id')
                    
                    confirm = input(f"Are you sure you want to remove '{filename}'? (y/n): ").strip().lower()
                    if confirm == 'y':
                        result = client.project.remove_associated_file(
                            project_id=project_id,
                            file_id=file_id
                        )
                        p.green(f"File '{filename}' removed successfully")
                        input("Press Enter to continue...")
                        break
        
        except Exception as e:
            p.red(f"Error removing file from project: {str(e)}")
            input("Press Enter to continue...")
            break

def auto_add_user_files_to_project(client, project_id):
    """Automatically search for and add user files to a project based on project context"""
    clear_screen()
    print_banner()
    p.bold("Auto-Add User Files to Project")
    
    try:
        # Get project details to understand context and org ID
        project = client.project.get_project(project_id)
        project_data = project if isinstance(project, dict) else {}
        org_id = project_data.get('org_id')
        
        if not org_id:
            p.red("Could not determine organization ID for this project")
            input("Press Enter to continue...")
            return
        
        # Get project info to use as context
        project_name = project_data.get('name', '')
        project_purpose = project_data.get('purpose', '')
        project_audience = project_data.get('target_audience', '')
        
        # Generate search queries based on project content
        p.yellow("Generating search queries based on project context...")
        
        # Try to get any prompt text that might exist
        prompt_text = ""
        try:
            prompt_result = client.prompt.get_prompt_by_project(project_id)
            if prompt_result and "error" not in prompt_result:
                prompt_data = prompt_result.get("prompt", {})
                prompt_text = prompt_data.get("main_prompt", "")
        except:
            pass
        
        # Build context from project and any prompt info
        context = f"Project: {project_name}\nPurpose: {project_purpose}\nTarget Audience: {project_audience}"
        if prompt_text:
            context += f"\nPrompt: {prompt_text}"
        
        # Let user select content types to search for
        p.n()
        p.bold("Select which types of content to search for:")
        p.green("[1] Videos only")
        p.green("[2] Audio only")
        p.green("[3] Images only")
        p.green("[4] All media types")
        
        content_choice = get_input("Choose an option", default="4", choices=["1", "2", "3", "4"])
        
        # Set file types based on choice
        file_types = "all"
        if content_choice == "1":
            file_types = "video"
        elif content_choice == "2":
            file_types = "audio"
        elif content_choice == "3":
            file_types = "image"
        
        # Ask for number of results
        num_results = int(get_input("Maximum number of files to find per query", default="3", help_text="Higher numbers will return more matches but may be less relevant"))
        
        # Ask for similarity threshold
        similarity = float(get_input("Similarity threshold (0.0-1.0, lower=more results)", default="0.2", help_text="Lower values return more results, higher values ensure better relevance"))
        
        # Generate search queries using the AI
        p.yellow("Sending request to AI to generate search queries...")
        queries = []
        
        # Option 1: Try to use the prompt-based query generator
        try:
            search_query_results = client.prompt.start_query_gen_and_wait(
                project_id=project_id,
                num_videos=3 if file_types in ["video", "all"] else 0,
                num_audio=3 if file_types in ["audio", "all"] else 0,
                num_images=3 if file_types in ["image", "all"] else 0,
                company_details=context,
                max_wait_seconds=60,
                poll_interval_seconds=3
            )
            
            result_data = search_query_results.get("result", {}).get("results", {})
            
            if file_types in ["video", "all"]:
                queries.extend(result_data.get("videos", []))
            
            if file_types in ["audio", "all"]:
                queries.extend(result_data.get("audio", []))
            
            if file_types in ["image", "all"]:
                queries.extend(result_data.get("images", []))
                
        except Exception as e:
            # Option 2: If that fails, create some generic search queries
            p.yellow(f"Could not generate queries with AI: {str(e)}")
            p.yellow("Using fallback generic queries...")
            
            # Create generic queries based on project content
            queries = [project_name]
            if project_purpose:
                queries.append(project_purpose)
            if project_audience:
                queries.append(f"content for {project_audience}")
            
            # Add some media type specific queries
            if file_types in ["video", "all"]:
                queries.append(f"video about {project_name}")
            
            if file_types in ["audio", "all"]:
                queries.append(f"audio for {project_name}")
                
            if file_types in ["image", "all"]:
                queries.append(f"image of {project_name}")
        
        # Ensure we have at least some queries
        if not queries:
            queries = [project_name, "relevant content"]
        
        p.green(f"Generated {len(queries)} search queries")
        for i, q in enumerate(queries):
            p.cyan(f"Query {i+1}: {q}")
        
        # Ask user if they want to proceed with these queries
        proceed = get_input("Do you want to proceed with these queries? (y/n)", default="y").lower() == "y"
        
        if not proceed:
            p.yellow("Operation cancelled by user")
            input("Press Enter to continue...")
            return
        
        # Search user files using vector search
        p.yellow("Searching your files using semantic vector search...")
        
        search_results = client.storage.vector_search(
            queries=queries,
            path=None,  # Search all folders
            detailed=True,
            generate_thumbnail=True,
            generate_streamable=True,
            num_results=num_results,
            similarity_threshold=similarity,
            file_types=file_types,
            org_id=org_id
        )
        
        # Extract file IDs
        files = search_results.get("files", [])
        if not files:
            p.yellow("No matching files found in your storage")
            input("Press Enter to continue...")
            return
        
        p.green(f"Found {len(files)} matching files!")
        
        # Show the files and ask which ones to add
        p.bold("Matching Files:")
        for idx, file in enumerate(files):
            # Determine file type icon
            mimetype = file.get('mimetype', '')
            if mimetype.startswith('video/'):
                icon = "🎬"
            elif mimetype.startswith('audio/'):
                icon = "🔊"
            elif mimetype.startswith('image/'):
                icon = "🖼️"
            else:
                icon = "📄"
                
            filename = file.get('filename', 'Unknown')
            similarity = file.get('vector_similarity', 0)
            p.green(f"[{idx+1}] {icon} {filename} (Relevance: {similarity:.2f})")
        
        p.n()
        
        # Give options for auto-adding
        p.bold("Options:")
        p.green("[A] Add all files")
        p.green("[S] Select specific files")
        p.green("[T] Add top N files")
        p.green("[C] Cancel")
        
        option = get_input("Choose an option", default="A", help_text="How would you like to add files to your project?").upper()
        
        files_to_add = []
        
        if option == "A":
            # Add all files
            files_to_add = [file.get('file_id') for file in files if file.get('file_id')]
            
        elif option == "S":
            # Let user select specific files
            p.yellow("Enter file numbers to add, separated by spaces (e.g. '1 3 5')")
            selection = input("File numbers: ").strip()
            selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
            
            for idx in selected_indices:
                if 0 <= idx < len(files) and files[idx].get('file_id'):
                    files_to_add.append(files[idx].get('file_id'))
                    
        elif option == "T":
            # Add top N files
            top_n = int(get_input("How many top files to add?", default="3"))
            files_to_add = [file.get('file_id') for file in files[:top_n] if file.get('file_id')]
            
        else:
            p.yellow("Operation cancelled by user")
            input("Press Enter to continue...")
            return
        
        # Add files to the project
        p.yellow(f"Adding {len(files_to_add)} files to the project...")
        
        added_count = 0
        for file_id in files_to_add:
            try:
                result = client.project.add_associated_file(
                    project_id=project_id,
                    file_id=file_id
                )
                added_count += 1
            except Exception as e:
                p.red(f"Could not add file {file_id}: {str(e)}")
        
        p.green(f"Successfully added {added_count} files to the project")
        input("Press Enter to continue...")
        
    except Exception as e:
        p.red(f"Error auto-adding files to project: {str(e)}")
        input("Press Enter to continue...")

def auto_add_stock_media_to_project(client, project_id):
    """Automatically search for and add stock media to a project based on project context"""
    clear_screen()
    print_banner()
    p.bold("Auto-Add Stock Media to Project")
    
    try:
        # Get project details to understand context
        project = client.project.get_project(project_id)
        project_data = project if isinstance(project, dict) else {}
        
        # Get project info to use as context
        project_name = project_data.get('name', '')
        project_purpose = project_data.get('purpose', '')
        project_audience = project_data.get('target_audience', '')
        project_orientation = project_data.get('orientation', 'landscape')
        
        # Let user select content types to search for
        p.n()
        p.bold("Select which types of content to search for:")
        p.green("[1] Videos only")
        p.green("[2] Audio only") 
        p.green("[3] Images only")
        p.green("[4] Videos and Audio")
        p.green("[5] All media types")
        
        content_choice = get_input("Choose an option", default="4", choices=["1", "2", "3", "4", "5"])
        
        # Set up query configuration based on content choice
        num_videos = 0
        num_audio = 0
        num_images = 0
        
        if content_choice == "1":
            num_videos = 3
        elif content_choice == "2":
            num_audio = 3
        elif content_choice == "3":
            num_images = 3
        elif content_choice == "4":
            num_videos = 3
            num_audio = 2
        else:  # Option 5
            num_videos = 3
            num_audio = 2
            num_images = 3
        
        # Build context from project info
        context = f"Project: {project_name}\nPurpose: {project_purpose}\nTarget Audience: {project_audience}"
        
        # Generate search queries using the notebook-style approach
        p.yellow("Generating search queries for stock media...")
        
        search_query_results = client.prompt.start_query_gen_and_wait(
            project_id=project_id,
            num_videos=num_videos,
            num_audio=num_audio,
            num_images=num_images,
            company_details=context,
            max_wait_seconds=60,
            poll_interval_seconds=3
        )
        
        results = search_query_results.get("result", {}).get("results", {})
        video_queries = results.get("videos", [])
        audio_queries = results.get("audio", [])
        image_queries = results.get("images", [])
        
        p.green("Generated search queries:")
        if video_queries:
            p.cyan("Video queries:")
            for i, query in enumerate(video_queries):
                p.cyan(f"  {i+1}. {query}")
        
        if audio_queries:
            p.cyan("Audio queries:")
            for i, query in enumerate(audio_queries):
                p.cyan(f"  {i+1}. {query}")
                
        if image_queries:
            p.cyan("Image queries:")
            for i, query in enumerate(image_queries):
                p.cyan(f"  {i+1}. {query}")
        
        # Get user parameters for search
        num_results_per_query = int(get_input("Number of results per query", default="3", help_text="How many items to find for each search query"))
        similarity_threshold = float(get_input("Similarity threshold (0.0-1.0, lower=more results)", default="0.1", help_text="Lower values return more results but may be less relevant"))
        
        # Ask user if they want to proceed with the search
        proceed = get_input("Do you want to proceed with these queries? (y/n)", default="y").lower() == "y"
        
        if not proceed:
            p.yellow("Operation cancelled by user")
            input("Press Enter to continue...")
            return
        
        # Search for stock media
        added_videos = []
        added_audio = []
        added_images = []
        
        if video_queries:
            p.yellow("Searching for stock videos...")
            try:
                stock_videos = client.stock.search(
                    queries=video_queries,
                    collections=["videos"],
                    detailed=True,
                    generate_thumbnail=True,
                    generate_streamable=True,
                    generate_download=True,
                    num_results_videos=num_results_per_query,
                    num_results_audios=0,
                    num_results_images=0,
                    similarity_threshold=similarity_threshold,
                    orientation=project_orientation
                )
                
                video_results = stock_videos.get("videos", [])
                p.green(f"Found {len(video_results)} matching stock videos")
                
                # Show the videos
                p.bold("Stock Videos:")
                for idx, video in enumerate(video_results):
                    stock_id = video.get("stock_id", "Unknown")
                    title = video.get("title", "Untitled")
                    p.green(f"[{idx+1}] 🎬 {title} (ID: {stock_id})")
                
                # Add the videos to the project
                add_all = get_input("Add all videos to project? (y/n)", default="y").lower() == "y"
                
                if add_all:
                    p.yellow("Adding all videos to project...")
                    for video in video_results:
                        stock_id = video.get("stock_id")
                        if stock_id:
                            try:
                                result = client.project.add_stock_file(
                                    project_id=project_id,
                                    stock_id=stock_id,
                                    media_type="videos"
                                )
                                added_videos.append(stock_id)
                                time.sleep(0.5)  # Small delay to avoid rate limits
                            except Exception as e:
                                p.red(f"Could not add video {stock_id}: {str(e)}")
                else:
                    p.yellow("Enter video numbers to add, separated by spaces (e.g. '1 3 5')")
                    selection = input("Video numbers: ").strip()
                    selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
                    
                    for idx in selected_indices:
                        if 0 <= idx < len(video_results):
                            stock_id = video_results[idx].get("stock_id")
                            if stock_id:
                                try:
                                    result = client.project.add_stock_file(
                                        project_id=project_id,
                                        stock_id=stock_id,
                                        media_type="videos"
                                    )
                                    added_videos.append(stock_id)
                                    time.sleep(0.5)  # Small delay to avoid rate limits
                                except Exception as e:
                                    p.red(f"Could not add video {stock_id}: {str(e)}")
            
            except Exception as e:
                p.red(f"Error searching for stock videos: {str(e)}")
        
        if audio_queries:
            p.yellow("Searching for stock audio...")
            try:
                stock_audios = client.stock.search(
                    queries=audio_queries,
                    collections=["audios"],
                    detailed=True,
                    generate_thumbnail=True,
                    generate_streamable=True,
                    generate_download=True,
                    num_results_videos=0,
                    num_results_audios=num_results_per_query,
                    num_results_images=0,
                    similarity_threshold=similarity_threshold
                )
                
                audio_results = stock_audios.get("audios", [])
                p.green(f"Found {len(audio_results)} matching stock audio tracks")
                
                # Show the audio tracks
                p.bold("Stock Audio:")
                for idx, audio in enumerate(audio_results):
                    stock_id = audio.get("stock_id", "Unknown")
                    title = audio.get("title", "Untitled")
                    p.green(f"[{idx+1}] 🔊 {title} (ID: {stock_id})")
                
                # Add the audio to the project
                add_all = get_input("Add all audio tracks to project? (y/n)", default="y").lower() == "y"
                
                if add_all:
                    p.yellow("Adding all audio tracks to project...")
                    for audio in audio_results:
                        stock_id = audio.get("stock_id")
                        if stock_id:
                            try:
                                result = client.project.add_stock_file(
                                    project_id=project_id,
                                    stock_id=stock_id,
                                    media_type="audios"
                                )
                                added_audio.append(stock_id)
                                time.sleep(0.5)  # Small delay to avoid rate limits
                            except Exception as e:
                                p.red(f"Could not add audio {stock_id}: {str(e)}")
                else:
                    p.yellow("Enter audio numbers to add, separated by spaces (e.g. '1 3 5')")
                    selection = input("Audio numbers: ").strip()
                    selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
                    
                    for idx in selected_indices:
                        if 0 <= idx < len(audio_results):
                            stock_id = audio_results[idx].get("stock_id")
                            if stock_id:
                                try:
                                    result = client.project.add_stock_file(
                                        project_id=project_id,
                                        stock_id=stock_id,
                                        media_type="audios"
                                    )
                                    added_audio.append(stock_id)
                                    time.sleep(0.5)  # Small delay to avoid rate limits
                                except Exception as e:
                                    p.red(f"Could not add audio {stock_id}: {str(e)}")
            
            except Exception as e:
                p.red(f"Error searching for stock audio: {str(e)}")
        
        if image_queries:
            p.yellow("Searching for stock images...")
            try:
                stock_images = client.stock.search(
                    queries=image_queries,
                    collections=["images"],
                    detailed=True,
                    generate_thumbnail=True,
                    generate_streamable=True,
                    generate_download=True,
                    num_results_videos=0,
                    num_results_audios=0,
                    num_results_images=num_results_per_query,
                    similarity_threshold=similarity_threshold
                )
                
                image_results = stock_images.get("images", [])
                p.green(f"Found {len(image_results)} matching stock images")
                
                # Show the images
                p.bold("Stock Images:")
                for idx, image in enumerate(image_results):
                    stock_id = image.get("stock_id", "Unknown")
                    title = image.get("title", "Untitled")
                    p.green(f"[{idx+1}] 🖼️ {title} (ID: {stock_id})")
                
                # Add the images to the project
                add_all = get_input("Add all images to project? (y/n)", default="y").lower() == "y"
                
                if add_all:
                    p.yellow("Adding all images to project...")
                    for image in image_results:
                        stock_id = image.get("stock_id")
                        if stock_id:
                            try:
                                result = client.project.add_stock_file(
                                    project_id=project_id,
                                    stock_id=stock_id,
                                    media_type="images"
                                )
                                added_images.append(stock_id)
                                time.sleep(0.5)  # Small delay to avoid rate limits
                            except Exception as e:
                                p.red(f"Could not add image {stock_id}: {str(e)}")
                else:
                    p.yellow("Enter image numbers to add, separated by spaces (e.g. '1 3 5')")
                    selection = input("Image numbers: ").strip()
                    selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
                    
                    for idx in selected_indices:
                        if 0 <= idx < len(image_results):
                            stock_id = image_results[idx].get("stock_id")
                            if stock_id:
                                try:
                                    result = client.project.add_stock_file(
                                        project_id=project_id,
                                        stock_id=stock_id,
                                        media_type="images"
                                    )
                                    added_images.append(stock_id)
                                    time.sleep(0.5)  # Small delay to avoid rate limits
                                except Exception as e:
                                    p.red(f"Could not add image {stock_id}: {str(e)}")
            
            except Exception as e:
                p.red(f"Error searching for stock images: {str(e)}")
        
        # Summarize what was added
        p.n()
        p.green(f"Added {len(added_videos)} videos, {len(added_audio)} audio tracks, and {len(added_images)} images to the project")
        input("Press Enter to continue...")
        
    except Exception as e:
        p.red(f"Error auto-adding stock media to project: {str(e)}")
        input("Press Enter to continue...")

def add_stock_media_menu(client, project_id):
    """Menu to search and add stock media to a project"""
    clear_screen()
    print_banner()
    p.bold("Add Stock Media to Project")
    
    # Let user choose search method
    p.bold("Search Method:")
    p.green("[1] Search by keyword")
    p.green("[2] Vector search (semantic)")
    p.green("[3] Back to Project Files")
    
    choice = get_input("Choose a method", default="1").strip()
    
    if choice == "1":
        # Keyword search
        keyword = get_input("Enter search keyword", required=True)
        media_type = get_input("Media type (videos, audios, images)", default="videos", choices=["videos", "audios", "images"])
        
        # Get project orientation if searching for videos
        orientation = None
        if media_type == "videos":
            try:
                project = client.project.get_project(project_id)
                orientation = project.get("orientation", "landscape")
            except:
                pass
        
        # Search for media
        try:
            p.yellow(f"Searching for {media_type} with keyword: {keyword}")
            
            # Set up search parameters based on media type
            collections = [media_type]
            kwargs = {
                "queries": [keyword],
                "collections": collections,
                "detailed": True,
                "generate_thumbnail": True,
                "generate_streamable": True,
                "generate_download": True,
                f"num_results_{media_type}": 10,
                "similarity_threshold": 0.1,
            }
            
            if media_type == "videos" and orientation:
                kwargs["orientation"] = orientation
                
            stock_results = client.stock.search(**kwargs)
            results = stock_results.get(media_type, [])
            
            if not results:
                p.yellow(f"No {media_type} found for keyword: {keyword}")
                input("Press Enter to continue...")
                return
            
            # Show results
            p.green(f"Found {len(results)} {media_type}")
            for idx, item in enumerate(results):
                stock_id = item.get("stock_id", "Unknown")
                title = item.get("title", "Untitled")
                
                icon = "🎬" if media_type == "videos" else "🔊" if media_type == "audios" else "🖼️"
                p.green(f"[{idx+1}] {icon} {title} (ID: {stock_id})")
            
            # Select items to add
            p.yellow("Enter item numbers to add, separated by spaces (e.g. '1 3 5'), or 'all' to add all:")
            selection = input("Selection: ").strip().lower()
            
            if selection == "all":
                # Add all items
                for item in results:
                    stock_id = item.get("stock_id")
                    if stock_id:
                        try:
                            result = client.project.add_stock_file(
                                project_id=project_id,
                                stock_id=stock_id,
                                media_type=media_type
                            )
                            p.green(f"Added {media_type[:-1]}: {stock_id}")
                            time.sleep(0.5)  # Small delay to avoid rate limits
                        except Exception as e:
                            p.red(f"Could not add {media_type[:-1]} {stock_id}: {str(e)}")
            else:
                # Add selected items
                selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
                
                for idx in selected_indices:
                    if 0 <= idx < len(results):
                        stock_id = results[idx].get("stock_id")
                        if stock_id:
                            try:
                                result = client.project.add_stock_file(
                                    project_id=project_id,
                                    stock_id=stock_id,
                                    media_type=media_type
                                )
                                p.green(f"Added {media_type[:-1]}: {stock_id}")
                            except Exception as e:
                                p.red(f"Could not add {media_type[:-1]} {stock_id}: {str(e)}")
            
            input("Press Enter to continue...")
            
        except Exception as e:
            p.red(f"Error searching stock media: {str(e)}")
            input("Press Enter to continue...")
            
    elif choice == "2":
        # Vector search
        query = get_input("Enter semantic search query", required=True, 
                         help_text="Describe what you're looking for in natural language")
        media_type = get_input("Media type (videos, audios, images)", default="videos", 
                              choices=["videos", "audios", "images"])
        
        # Get project orientation if searching for videos
        orientation = None
        if media_type == "videos":
            try:
                project = client.project.get_project(project_id)
                orientation = project.get("orientation", "landscape")
            except:
                pass
        
        # Search for media
        try:
            p.yellow(f"Searching for {media_type} with query: {query}")
            
            # Set up search parameters based on media type
            collections = [media_type]
            kwargs = {
                "queries": [query],
                "collections": collections,
                "detailed": True,
                "generate_thumbnail": True,
                "generate_streamable": True,
                "generate_download": True,
                "num_results_videos": 10 if media_type == "videos" else 0,
                "num_results_audios": 10 if media_type == "audios" else 0,
                "num_results_images": 10 if media_type == "images" else 0,
                "similarity_threshold": 0.2,
            }
            
            if media_type == "videos" and orientation:
                kwargs["orientation"] = orientation
                
            stock_results = client.stock.search(**kwargs)
            results = stock_results.get(media_type, [])
            
            if not results:
                p.yellow(f"No {media_type} found for query: {query}")
                input("Press Enter to continue...")
                return
            
            # Show results
            p.green(f"Found {len(results)} {media_type}")
            for idx, item in enumerate(results):
                stock_id = item.get("stock_id", "Unknown")
                title = item.get("title", "Untitled")
                similarity = item.get("similarity", 0)
                
                icon = "🎬" if media_type == "videos" else "🔊" if media_type == "audios" else "🖼️"
                p.green(f"[{idx+1}] {icon} {title} (ID: {stock_id}, Relevance: {similarity:.2f})")
            
            # Select items to add
            p.yellow("Enter item numbers to add, separated by spaces (e.g. '1 3 5'), or 'all' to add all:")
            selection = input("Selection: ").strip().lower()
            
            if selection == "all":
                # Add all items
                for item in results:
                    stock_id = item.get("stock_id")
                    if stock_id:
                        try:
                            result = client.project.add_stock_file(
                                project_id=project_id,
                                stock_id=stock_id,
                                media_type=media_type
                            )
                            p.green(f"Added {media_type[:-1]}: {stock_id}")
                            time.sleep(0.5)  # Small delay to avoid rate limits
                        except Exception as e:
                            p.red(f"Could not add {media_type[:-1]} {stock_id}: {str(e)}")
            else:
                # Add selected items
                selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
                
                for idx in selected_indices:
                    if 0 <= idx < len(results):
                        stock_id = results[idx].get("stock_id")
                        if stock_id:
                            try:
                                result = client.project.add_stock_file(
                                    project_id=project_id,
                                    stock_id=stock_id,
                                    media_type=media_type
                                )
                                p.green(f"Added {media_type[:-1]}: {stock_id}")
                            except Exception as e:
                                p.red(f"Could not add {media_type[:-1]} {stock_id}: {str(e)}")
            
            input("Press Enter to continue...")
            
        except Exception as e:
            p.red(f"Error searching stock media: {str(e)}")
            input("Press Enter to continue...")
    
    elif choice == "3":
        return

def project_details_menu(client, project_id):
    """Show project details and options"""
    while True:
        clear_screen()
        print_banner()
        
        try:
            # Get project details
            project = client.project.get_project(
                project_id=project_id, 
                generate_thumbnail_links=True
            )
            
            project_name = project.get('name', 'Unknown Project')
            p.bold(f"Project: {project_name}")
            
            # Show basic project info
            status = project.get('status', 'draft')
            status_emoji = "🔄" if status == "ongoing" else "✅" if status == "completed" else "📝"
            orientation = project.get('orientation', 'Unknown')
            created_at = project.get('created_at', 'Unknown')
            
            p.cyan(f"Status: {status_emoji} {status}")
            p.cyan(f"Orientation: {orientation}")
            p.cyan(f"Created: {created_at}")
            
            # Show project purpose if available
            purpose = project.get('purpose')
            if purpose:
                p.cyan(f"Purpose: {purpose}")
            
            p.n()
            p.bold("Project Actions:")
            p.green("[1] View and Manage Files")
            p.green("[2] Create/Edit Storyboard")
            p.green("[3] Create/Edit Voiceover")
            p.green("[4] Create/Edit Sequence")
            p.green("[5] Render Video")
            p.green("[6] Edit Project Details")
            p.green("[7] Auto-Add Content")  # New option
            p.n()
            p.green("[B] Back to Projects")
            p.n()
            
            choice = input("Enter your choice: ").strip().upper()
            
            if choice == '1':
                view_project_files(client, project_id)
            elif choice == '2':
                p.yellow("Storyboard functionality will be implemented here")
                input("Press Enter to continue...")
            elif choice == '3':
                p.yellow("Voiceover functionality will be implemented here")
                input("Press Enter to continue...")
            elif choice == '4':
                p.yellow("Sequence functionality will be implemented here")
                input("Press Enter to continue...")
            elif choice == '5':
                render_menu(client, project_id)
            elif choice == '6':
                edit_project_details(client, project_id)
            elif choice == '7':
                # Handle auto-add content option
                auto_add_content_menu(client, project_id)
            elif choice == 'B':
                return False
        
        except Exception as e:
            p.red(f"Error loading project details: {str(e)}")
            input("Press Enter to continue...")
            return False

def auto_add_content_menu(client, project_id):
    """Menu for auto-adding various types of content to a project"""
    clear_screen()
    print_banner()
    p.bold("Auto-Add Content to Project")
    p.yellow("Let the AI help you find and add content to your project")
    p.n()
    
    p.bold("Choose content type to auto-add:")
    p.green("[1] Auto-Add Your Own Files")
    p.green("[2] Auto-Add Stock Media")
    p.green("[3] Auto-Add Both")
    p.green("[B] Back to Project")
    p.n()
    
    choice = input("Enter your choice: ").strip().upper()
    
    if choice == '1':
        auto_add_user_files_to_project(client, project_id)
    elif choice == '2':
        auto_add_stock_media_to_project(client, project_id)
    elif choice == '3':
        # Run both auto-add processes
        auto_add_user_files_to_project(client, project_id)
        auto_add_stock_media_to_project(client, project_id)
    elif choice == 'B':
        return

def edit_project_details(client, project_id):
    """Edit project name, purpose, and other details"""
    while True:
        clear_screen()
        print_banner()
        
        try:
            # Get current project details
            project = client.project.get_project(project_id)
            
            project_name = project.get('name', '')
            purpose = project.get('purpose', '')
            target_audience = project.get('target_audience', '')
            
            p.bold("Edit Project Details")
            p.n()
            p.cyan(f"Current Name: {project_name}")
            p.cyan(f"Current Purpose: {purpose}")
            p.cyan(f"Current Target Audience: {target_audience}")
            p.n()
            
            p.bold("What would you like to edit?")
            p.green("[1] Project Name")
            p.green("[2] Project Purpose")
            p.green("[3] Target Audience")
            p.green("[B] Back to Project")
            p.n()
            
            choice = input("Enter your choice: ").strip().upper()
            
            if choice == '1':
                new_name = input(f"Enter new project name (current: {project_name}): ").strip()
                if new_name:
                    client.project.update_project(project_id=project_id, name=new_name)
                    p.green("Project name updated successfully!")
                else:
                    p.yellow("Project name cannot be empty. No changes made.")
            elif choice == '2':
                new_purpose = input(f"Enter new project purpose (current: {purpose}): ").strip()
                client.project.update_project(project_id=project_id, purpose=new_purpose)
                p.green("Project purpose updated successfully!")
            elif choice == '3':
                new_target = input(f"Enter new target audience (current: {target_audience}): ").strip()
                client.project.update_project(project_id=project_id, target_audience=new_target)
                p.green("Target audience updated successfully!")
            elif choice == 'B':
                break
            
            if choice in ['1', '2', '3']:
                input("Press Enter to continue...")
        
        except Exception as e:
            p.red(f"Error updating project details: {str(e)}")
            input("Press Enter to continue...")
            break

def continue_project_workflow(client, project_id):
    """Continue working on an existing project"""
    project = client.project.get_project(project_id)["project"]
    orientation = project.get('orientation', 'landscape')
    
    # Check which components exist and continue from there
    try:
        # Check for prompt
        has_prompt = False
        try:
            prompt = client.prompt.get_prompt_by_project(project_id)
            has_prompt = prompt and not "error" in prompt
        except Exception:
            pass
        
        if not has_prompt:
            prompt_menu(client, project_id)
        
        # Check for stock content
        videos, audios, images = search_menu(client, project_id)
        if videos:
            video_ids = stock_menu(client, videos, "videos", orientation)
            add_stock_menu(client, project_id, video_ids, "videos")
        if audios:
            audio_ids = stock_menu(client, audios, "audios")
            add_stock_menu(client, project_id, audio_ids, "audios")
        
        # Check for storyboard
        has_storyboard = False
        try:
            storyboard = client.storyboard.get_storyboard(project_id=project_id)
            has_storyboard = storyboard and not "error" in storyboard
        except Exception:
            pass
        
        if not has_storyboard:
            storyboard_id = storyboard_menu(client, project_id)
        else:
            storyboard_id = storyboard.get("storyboard", {}).get("storyboard_id")
            update_storyboard = get_input("Storyboard exists. Update and regenerate it? (y/n)", default="n").lower() == "y"
            if update_storyboard:
                # Let user update storyboard parameters
                update_storyboard_menu(client, project_id, storyboard_id)
                storyboard_id = redo_storyboard_menu(client, project_id, storyboard_id)
        
        # Check for voiceover
        has_voiceover = False
        try:
            voiceover = client.voiceover.get_voiceover(project_id=project_id)
            has_voiceover = voiceover and not "error" in voiceover
        except Exception:
            pass
        
        if not has_voiceover:
            voiceover_id = voiceover_menu(client, project_id)
        else:
            voiceover_id = voiceover.get("voiceover", {}).get("voiceover_id")
            update_voiceover = get_input("Voiceover exists. Regenerate it? (y/n)", default="n").lower() == "y"
            if update_voiceover:
                voiceover_id = client.voiceover.redo_voiceover(project_id=project_id).get("voiceover", {}).get("voiceover_id")
                p.green(f"Voiceover regenerated with ID: {voiceover_id}")
                wait_key()
        
        # Check for sequence
        has_sequence = False
        try:
            sequence = client.sequence.get_sequence(project_id=project_id)
            has_sequence = sequence and not "error" in sequence
        except Exception:
            pass
        
        if not has_sequence:
            sequence_id = sequence_menu(client, project_id, orientation)
        else:
            sequence_id = sequence.get("sequence", {}).get("sequence_id")
            update_sequence = get_input("Sequence exists. Update and regenerate it? (y/n)", default="n").lower() == "y"
            if update_sequence:
                # Let user update sequence parameters
                sequence_id = redo_sequence_menu(client, project_id, sequence_id)
        
        # Check for render
        has_render = False
        try:
            render = client.render.get_render(project_id=project_id)
            has_render = render and not "error" in render
        except Exception:
            pass
        
        if not has_render:
            render_job_id = render_menu(client, project_id)
        else:
            render_id = render.get("render", {}).get("render_id")
            update_render = get_input("Render exists. Create a new render? (y/n)", default="n").lower() == "y"
            if update_render:
                render_job_id = render_menu(client, project_id)
            else:
                render_job_id = render.get("job_id")
        
        wait_for_render(client, project_id)
        
    except Exception as e:
        print_error(str(e))
        wait_key()
    
    return None

def update_storyboard_menu(client, project_id, storyboard_id):
    """Menu to update storyboard parameters before redoing"""
    clear_screen()
    print_banner()
    p.bold("Update Storyboard Parameters")
    print_tip("You can update storyboard parameters before regenerating it.")
    
    try:
        # Get current storyboard data
        storyboard = client.storyboard.get_storyboard(storyboard_id=storyboard_id)["storyboard"]
        
        # Let user update parameters
        deepthink = get_input("Enable deepthink? (y/n)", 
                             default="y" if storyboard.get("deepthink") else "n").lower() == "y"
        overdrive = get_input("Enable overdrive? (y/n)", 
                             default="y" if storyboard.get("overdrive") else "n").lower() == "y"
        web_search = get_input("Enable web search? (y/n)", 
                              default="y" if storyboard.get("web_search") else "n").lower() == "y"
        eco = get_input("Enable eco mode? (y/n)", 
                       default="y" if storyboard.get("eco") else "n").lower() == "y"
        temperature = float(get_input("AI temperature", 
                                     default=str(storyboard.get("temperature", 0.7))))
        iterations = int(get_input("Refinement iterations", 
                                  default=str(storyboard.get("iterations", 3))))
        full_length = int(get_input("Storyboard length (seconds)", 
                                   default=str(storyboard.get("full_length", 20))))
        regeneration_prompt = get_input("Add regeneration prompt?", 
                                       default="",
                                       help_text="Give specific instructions for regeneration")
        
        # Update storyboard values
        client.storyboard.update_storyboard_values(
            storyboard_id=storyboard_id,
            deepthink=deepthink,
            overdrive=overdrive,
            web_search=web_search,
            eco=eco,
            temperature=temperature,
            iterations=iterations,
            full_length=full_length,
            regeneration_prompt=regeneration_prompt if regeneration_prompt else None
        )
        
        p.green("Storyboard parameters updated successfully.")
        wait_key()
        
    except Exception as e:
        print_error(str(e))
        wait_key()

def redo_storyboard_menu(client, project_id, storyboard_id):
    """Redo an existing storyboard"""
    clear_screen()
    print_banner()
    p.bold("Regenerating Storyboard")
    p.yellow("Tip: This will create a new version of your storyboard with the updated parameters.")
    p.lgray("Regenerating storyboard...")
    
    try:
        storyboard_job = client.storyboard.redo_storyboard(storyboard_id=storyboard_id)
        storyboard_id = storyboard_job["storyboard"]["storyboard_id"]
        p.green(f"Storyboard regenerated with ID: {storyboard_id}")
        wait_key()
        return storyboard_id
    except Exception as e:
        print_error(str(e))
        wait_key()
        return None

def redo_sequence_menu(client, project_id, sequence_id):
    """Redo an existing sequence"""
    clear_screen()
    print_banner()
    p.bold("Update Sequence Parameters")
    
    try:
        # Get project for orientation
        project = client.project.get_project(project_id)["project"]
        orientation = project.get('orientation', 'landscape')
        
        # Let user update parameters
        apply_template = get_input("Apply template? (y/n)", default="n").lower() == "y"
        apply_grade = get_input("Apply color grading? (y/n)", default="n").lower() == "y"
        grade_type = get_input("Grade type", default="single", help_text="Choose 'single' for one grade, 'multi' for different grades per scene.", choices=["single", "multi"])
        deepthink = get_input("Enable deepthink? (y/n)", default="n").lower() == "y"
        overdrive = get_input("Enable overdrive? (y/n)", default="n").lower() == "y"
        web_search = get_input("Enable web search? (y/n)", default="n").lower() == "y"
        eco = get_input("Enable eco mode? (y/n)", default="y").lower() == "y"
        temperature = float(get_input("AI temperature", default="0.7"))
        
        p.lgray("Regenerating sequence...")
        sequence_job = client.sequence.redo_sequence(
            sequence_id=sequence_id,
            apply_template=apply_template,
            apply_grade=apply_grade,
            grade_type=grade_type,
            orientation=orientation,
            deepthink=deepthink,
            overdrive=overdrive,
            web_search=web_search,
            eco=eco,
            temperature=temperature
        )
        
        new_sequence_id = sequence_job["sequence"]["sequence_id"]
        p.green(f"Sequence regenerated with ID: {new_sequence_id}")
        wait_key()
        return new_sequence_id
    except Exception as e:
        print_error(str(e))
        wait_key()
        return sequence_id

def run():
    load_dotenv()
    API_KEY = os.environ.get("STORYLINEZ_API_KEY")
    API_SECRET = os.environ.get("STORYLINEZ_API_SECRET")
    ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")
    client = StorylinezClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    while True:
        choice = main_menu()
        if choice == "3":
            p.green("Goodbye!")
            break
        elif choice == "1":
            project_id = project_menu(client)
            if not project_id:
                continue
            prompt_menu(client, project_id)
            videos, audios, images = search_menu(client, project_id)
            orientation = client.project.get_project(project_id).get("project", {}).get("orientation", "landscape")
            video_ids = stock_menu(client, videos, "videos", orientation)
            audio_ids = stock_menu(client, audios, "audios")
            add_stock_menu(client, project_id, video_ids, "videos")
            add_stock_menu(client, project_id, audio_ids, "audios")
            storyboard_id = storyboard_menu(client, project_id)
            voiceover_id = voiceover_menu(client, project_id)
            sequence_id = sequence_menu(client, project_id, orientation)
            render_job_id = render_menu(client, project_id)
            wait_for_render(client, project_id)
        elif choice == "2":
            project_id = browse_projects_menu(client)
            if project_id == "create_new":
                # User selected to create a new project from browse menu
                project_id = project_menu(client)
                if not project_id:
                    continue
                prompt_menu(client, project_id)
                videos, audios, images = search_menu(client, project_id)
                orientation = client.project.get_project(project_id).get("project", {}).get("orientation", "landscape")
                video_ids = stock_menu(client, videos, "videos", orientation)
                audio_ids = stock_menu(client, audios, "audios")
                add_stock_menu(client, project_id, video_ids, "videos")
                add_stock_menu(client, project_id, audio_ids, "audios")
                storyboard_id = storyboard_menu(client, project_id)
                voiceover_id = voiceover_menu(client, project_id)
                sequence_id = sequence_menu(client, project_id, orientation)
                render_job_id = render_menu(client, project_id)
                wait_for_render(client, project_id)
            elif project_id:
                # Continue with existing project
                continue_project_workflow(client, project_id)
        else:
            print_error("Unknown option.")

if __name__ == "__main__":
    run()