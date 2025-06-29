"""
Storylinez Bulk Content Uploader CLI Tool

A comprehensive command-line interface for bulk uploading and processing
media files to Storylinez using the API.

Features:
- Browse and select local folders
- Filter by content type (videos, audio, images)
- Browse and manage Storylinez folders
- Configure advanced processing options
- Real-time upload progress tracking
- Detailed file analysis and statistics
- Error handling and recovery

Supported formats:
- Videos: MP4
- Audio: MP3, WAV  
- Images: JPG, JPEG, PNG

Usage:
    python bulk_content_uploader.py

Author: Storylinez SDK
Version: 1.0.0
"""

import os
import glob
import time
import math
from pathlib import Path
from dotenv import load_dotenv
import ultraprint.common as p
from storylinez import StorylinezClient

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

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    'VIDEO': ['.mp4'],
    'AUDIO': ['.mp3', '.wav'],
    'IMAGE': ['.jpg', '.jpeg', '.png']
}

ALL_EXTENSIONS = []
for formats in SUPPORTED_EXTENSIONS.values():
    ALL_EXTENSIONS.extend(formats)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_key():
    p.lgray("\nPress Enter to continue...")
    input()

def print_banner():
    p.cyan_bg(" STORYLINEZ CONTENT BULK UPLOADER ")
    p.n()
    p.lgray("Bulk upload and process content to Storylinez using the API.")
    p.n()
    return None

def print_tip(msg):
    p.yellow("Tip: " + msg)
    p.n()
    return None

def print_error(msg):
    p.red("Error: " + msg)
    p.n()
    return None

def print_success(msg):
    p.green("Success: " + msg)
    p.n()
    return None

def print_warning(msg):
    p.orange("Warning: " + msg)
    p.n()
    return None

def select_from_list(options, prompt="Select an option:"):
    """Display a numbered list and get user selection"""
    for idx, opt in enumerate(options):
        p.green(f"[{idx + 1}] {opt}")
    p.n()
    while True:
        try:
            choice = input(f"{prompt} (1-{len(options)}): ").strip()
            if choice == "?" or choice.lower() == "help":
                p.lgray("Select a number from the list above.")
                continue
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(options):
                return choice_idx
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")

def get_input(msg, default=None, required=False, help_text=None, choices=None):
    """Enhanced input with help and choices"""
    prompt = f"{msg}"
    if default is not None:
        prompt += f" (default: {default})"
    if help_text:
        p.lgray(f"  {help_text}")
    prompt += ": "
    
    while True:
        user_input = input(prompt).strip()
        if user_input == "?" or user_input.lower() == "help":
            if help_text:
                p.lgray(help_text)
                continue
            else:
                p.lgray("No additional help available.")
                continue
        
        if not user_input and default is not None:
            return default
        
        if not user_input and required:
            print_error("This field is required")
            continue
            
        if choices and user_input not in choices:
            print_error(f"Please choose from: {', '.join(choices)}")
            continue
            
        return user_input

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def get_file_type(filename):
    """Determine file type based on extension"""
    ext = os.path.splitext(filename)[1].lower()
    for file_type, extensions in SUPPORTED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return "UNKNOWN"

def scan_folder(folder_path, file_types=None, recursive=True):
    """
    Scan folder for supported files
    
    Args:
        folder_path: Path to scan
        file_types: List of file types to include (VIDEO, AUDIO, IMAGE) or None for all
        recursive: Whether to scan subdirectories
        
    Returns:
        Dictionary with file information
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not os.path.isdir(folder_path):
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    # Determine which extensions to look for
    target_extensions = []
    if file_types is None:
        target_extensions = ALL_EXTENSIONS
    else:
        for file_type in file_types:
            if file_type in SUPPORTED_EXTENSIONS:
                target_extensions.extend(SUPPORTED_EXTENSIONS[file_type])
    
    found_files = {
        'VIDEO': [],
        'AUDIO': [],
        'IMAGE': [],
        'UNKNOWN': []
    }
    
    total_size = 0
    
    if recursive:
        search_pattern = os.path.join(folder_path, "**", "*")
        files = glob.glob(search_pattern, recursive=True)
    else:
        search_pattern = os.path.join(folder_path, "*")
        files = glob.glob(search_pattern)
    
    for file_path in files:
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext in target_extensions:
                file_type = get_file_type(file_path)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                
                file_info = {
                    'path': file_path,
                    'name': os.path.basename(file_path),
                    'size': file_size,
                    'size_formatted': format_file_size(file_size),
                    'extension': ext,
                    'relative_path': os.path.relpath(file_path, folder_path)
                }
                
                found_files[file_type].append(file_info)
    
    return {
        'files': found_files,
        'total_files': sum(len(files) for files in found_files.values()),
        'total_size': total_size,
        'total_size_formatted': format_file_size(total_size),
        'folder_path': folder_path
    }

def display_scan_results(scan_result):
    """Display the results of folder scan"""
    p.n()
    p.bold("📁 Folder Scan Results")
    p.lgray(f"   Folder: {scan_result['folder_path']}")
    p.n()
    
    files = scan_result['files']
    
    # Summary
    p.cyan("📊 Summary:")
    for file_type, file_list in files.items():
        if file_list:
            total_size = sum(f['size'] for f in file_list)
            p.lgray(f"   {file_type}: {len(file_list)} files ({format_file_size(total_size)})")
    
    p.lgray(f"   TOTAL: {scan_result['total_files']} files ({scan_result['total_size_formatted']})")
    p.n()
    
    # Detailed listing (first 10 files of each type)
    for file_type, file_list in files.items():
        if file_list:
            p.yellow(f"📹 {file_type} Files:")
            for i, file_info in enumerate(file_list[:10]):
                p.lgray(f"   • {file_info['name']} ({file_info['size_formatted']})")
            
            if len(file_list) > 10:
                p.lgray(f"   ... and {len(file_list) - 10} more files")
            p.n()

def progress_callback(summary):
    """Enhanced callback function to display detailed upload progress"""
    try:
        # Handle the new enhanced progress reporting structure
        phase = summary.get('phase', 'unknown') if isinstance(summary, dict) else 'unknown'
        
        # Handle different phases of progress
        if phase == "file_start":
            current = summary.get('current_index', 0)
            total = summary.get('total', 1)
            filename = summary.get('filename', 'unknown')
            overall_progress = summary.get('overall_progress_percent', 0)
            
            # Create progress bar
            progress_bar = "█" * int((overall_progress / 100) * 20)
            remaining_bar = "░" * (20 - int((overall_progress / 100) * 20))
            
            p.n()
            p.cyan(f"🚀 Starting file {current}/{total}: {filename}")
            p.cyan(f"📊 Overall: [{progress_bar}{remaining_bar}] {overall_progress:.1f}%")
        
        elif phase == "upload_start":
            filename = summary.get('filename', 'unknown')
            p.yellow(f"📤 Uploading: {filename}")
        
        elif phase == "upload_complete":
            filename = summary.get('filename', 'unknown')
            duration = summary.get('upload_duration', 0)
            p.green(f"✅ Upload complete: {filename} ({duration:.1f}s)")
        
        elif phase == "processing_start":
            filename = summary.get('filename', 'unknown')
            file_id = summary.get('file_id', 'unknown')
            p.yellow(f"🔄 Processing started: {filename}")
            p.lgray(f"   File ID: {file_id}")
        
        elif phase == "polling":
            filename = summary.get('filename', 'unknown')
            status = summary.get('status', 'UNKNOWN')
            poll_count = summary.get('poll_count', 0)
            progress = summary.get('file_progress_percent', 0)
            elapsed = summary.get('elapsed_time', 0)
            
            # Create progress bar for file processing
            progress_bar = "█" * int((progress / 100) * 15)
            remaining_bar = "░" * (15 - int((progress / 100) * 15))
            
            p.yellow(f"⏳ Processing: [{progress_bar}{remaining_bar}] {progress:.0f}% | Poll #{poll_count} | {elapsed:.0f}s")
            
            # Show analysis status if available
            analysis_data = summary.get('analysis_data', {})
            if analysis_data and status:
                p.lgray(f"   Status: {status}")
        
        elif phase == "polling_error":
            error = summary.get('error', 'Unknown error')
            poll_count = summary.get('poll_count', 0)
            p.orange(f"⚠️  Polling error #{poll_count}: {error}")
        
        elif phase == "file_complete":
            filename = summary.get('filename', 'unknown')
            success = summary.get('success', False)
            total_duration = summary.get('total_file_duration', 0)
            overall_progress = summary.get('overall_progress_percent', 0)
            
            # Create progress bar
            progress_bar = "█" * int((overall_progress / 100) * 20)
            remaining_bar = "░" * (20 - int((overall_progress / 100) * 20))
            
            if success:
                p.green(f"✅ {filename} completed successfully ({total_duration:.1f}s)")
            else:
                p.red(f"❌ {filename} failed ({total_duration:.1f}s)")
            
            p.cyan(f"📊 Overall: [{progress_bar}{remaining_bar}] {overall_progress:.1f}%")
        
        elif phase == "file_error":
            filename = summary.get('filename', 'unknown')
            error = summary.get('error', 'Unknown error')
            overall_progress = summary.get('overall_progress_percent', 0)
            
            # Truncate long error messages
            if len(error) > 100:
                error = error[:100] + "..."
            
            p.red(f"❌ {filename} failed: {error}")
            
            # Create progress bar
            progress_bar = "█" * int((overall_progress / 100) * 20)
            remaining_bar = "░" * (20 - int((overall_progress / 100) * 20))
            p.cyan(f"📊 Overall: [{progress_bar}{remaining_bar}] {overall_progress:.1f}%")
        
        elif phase == "bulk_complete":
            total = summary.get('total', 0)
            done = summary.get('done', 0)
            failed = summary.get('failed', 0)
            success_rate = summary.get('success_rate', 0)
            total_duration = summary.get('total_duration', 0)
            
            p.n()
            p.green_bg(" BULK UPLOAD COMPLETE! ")
            p.n()
            p.green(f"📊 Results: {done}/{total} files successful ({success_rate:.1f}%)")
            if failed > 0:
                p.red(f"❌ Failed: {failed} files")
            p.lgray(f"⏱️  Total time: {total_duration:.1f} seconds")
            p.n()
        
        else:
            # Fallback for legacy or unknown phase - handle old callback format
            current = summary.get('current_index', 0) if isinstance(summary, dict) else 0
            total = summary.get('total', 1) if isinstance(summary, dict) else 1
            done = summary.get('done', 0) if isinstance(summary, dict) else 0
            failed = summary.get('failed', 0) if isinstance(summary, dict) else 0
            remaining = summary.get('remaining', 0) if isinstance(summary, dict) else 0
            
            file_path = summary.get('file_path', 'unknown') if isinstance(summary, dict) else 'unknown'
            file_name = os.path.basename(file_path) if file_path else 'unknown'
            upload_status = summary.get('upload_status', 'uploading') if isinstance(summary, dict) else 'uploading'
            processing_status = summary.get('processing_status', 'processing') if isinstance(summary, dict) else 'processing'
            result = summary.get('result') if isinstance(summary, dict) else None
            
            # Create progress bar with safe division
            if total > 0:
                progress_bar = "█" * int((current / total) * 20)
                remaining_bar = "░" * (20 - int((current / total) * 20))
            else:
                progress_bar = "░" * 20
                remaining_bar = ""
            
            p.n()
            p.cyan(f"📤 Progress: [{progress_bar}{remaining_bar}] {current}/{total}")
            p.lgray(f"   Current: {file_name}")
            p.lgray(f"   Upload: {upload_status} | Processing: {processing_status}")
            p.green(f"   ✅ Completed: {done} | ❌ Failed: {failed} | ⏳ Remaining: {remaining}")
            
            # Handle upload and processing status
            if upload_status == 'failed':
                # Upload failed
                error_detail = result if isinstance(result, str) else str(result) if result else 'Unknown upload error'
                if len(error_detail) > 100:
                    error_detail = error_detail[:100] + "..."
                p.red(f"   ❌ {file_name} upload failed: {error_detail}")
            
            elif upload_status == 'success':
                # Upload succeeded, check processing status
                # The wait_for_file_processing function returns the analysis dict when complete
                # Status is nested under analysis_data
                if isinstance(result, dict):
                    analysis_data = result.get('analysis_data', {})
                    result_status = analysis_data.get('status', '').upper()
                    if result_status == 'COMPLETED':
                        p.green(f"   ✅ {file_name} completed successfully")
                    elif result_status == 'FAILED':
                        error = analysis_data.get('error', 'Processing failed')
                        p.red(f"   ❌ {file_name} processing failed: {error}")
                    elif processing_status == 'COMPLETED':
                        p.green(f"   ✅ {file_name} completed successfully")
                    elif processing_status == 'FAILED':
                        error = str(result) if result else 'Processing failed'
                        p.red(f"   ❌ {file_name} processing failed: {error}")
                    elif processing_status in ['PROCESSING', 'processing']:
                        p.yellow(f"   ⏳ {file_name} still processing...")
                    else:
                        # Processing status is something else, show what we have
                        p.lgray(f"   ℹ️ {file_name} status: {processing_status}")
                elif processing_status == 'COMPLETED':
                    p.green(f"   ✅ {file_name} completed successfully")
                elif processing_status == 'FAILED':
                    if isinstance(result, str) and ('TimeoutError' in result or 'timeout' in result.lower()):
                        error = "Processing timed out (file may still complete in background)"
                    else:
                        error = str(result) if result else 'Processing failed'
                    p.red(f"   ❌ {file_name} processing failed: {error}")
                elif processing_status in ['PROCESSING', 'processing']:
                    p.yellow(f"   ⏳ {file_name} still processing...")
                else:
                    # Processing status is something else, show what we have
                    p.lgray(f"   ℹ️ {file_name} status: {processing_status}")
            
            else:
                # Still uploading or unknown status
                p.yellow(f"   ⏳ {file_name} uploading...")
    
    except Exception as e:
        # If there's any error in the callback, at least show something
        print(f"ERROR in progress callback: {str(e)}")
        print(f"Summary data: {summary}")
        p.red(f"   ❌ Progress callback error: {str(e)}")

def main_menu():
    """Display main menu and get user choice"""
    clear_screen()
    print_banner()
    p.blue("Welcome to the Storylinez Bulk Content Uploader!")
    p.n()
    p.lgray("Upload multiple files to Storylinez with full control over processing options.")
    p.n()
    
    options = [
        "📁 Browse and select local folder to upload",
        "📂 Browse Storylinez folders (destination)",
        "🔧 Configure upload settings",
        "📊 Quick folder analysis (no upload)",
        "❌ Exit"
    ]
    
    choice = select_from_list(options, "Choose an option")
    return choice + 1  # Convert to 1-based

def browse_local_folder_menu():
    """Browse and select local folder for upload"""
    clear_screen()
    print_banner()
    p.bold("📁 Select Local Folder to Upload")
    p.n()
    
    print_tip("Enter the full path to the folder containing your media files.")
    p.yellow("Supported formats: MP4, MP3, WAV, JPG, JPEG, PNG")
    p.n()
    
    while True:
        folder_path = get_input(
            "Enter folder path", 
            required=True,
            help_text="Full path to folder (e.g., C:\\Users\\YourName\\Videos)"
        )
        
        if folder_path == "?":
            continue
            
        # Handle quotes
        folder_path = folder_path.strip('"\'')
        
        if not os.path.exists(folder_path):
            print_error(f"Folder does not exist: {folder_path}")
            continue
            
        if not os.path.isdir(folder_path):
            print_error(f"Path is not a directory: {folder_path}")
            continue
            
        return folder_path

def filter_content_menu():
    """Let user choose which content types to include"""
    clear_screen()
    print_banner()
    p.bold("🔍 Filter Content Types")
    p.n()
    
    print_tip("Choose which types of content to include in the upload.")
    p.n()
    
    options = [
        "📹 Videos only (MP4)",
        "🎵 Audio only (MP3, WAV)", 
        "🖼️ Images only (JPG, JPEG, PNG)",
        "📹🎵 Videos + Audio",
        "📹🖼️ Videos + Images",
        "🎵🖼️ Audio + Images",
        "📹🎵🖼️ All content types"
    ]
    
    choice = select_from_list(options, "Select content filter")
    
    filter_map = {
        0: ['VIDEO'],
        1: ['AUDIO'],
        2: ['IMAGE'],
        3: ['VIDEO', 'AUDIO'],
        4: ['VIDEO', 'IMAGE'],
        5: ['AUDIO', 'IMAGE'],
        6: ['VIDEO', 'AUDIO', 'IMAGE']
    }
    
    return filter_map[choice]

def scan_options_menu():
    """Configure scanning options"""
    clear_screen()
    print_banner()
    p.bold("⚙️ Scan Options")
    p.n()
    
    recursive = get_input(
        "Include subdirectories? (y/n)", 
        default="y",
        help_text="Scan all folders and subfolders for content"
    ).lower() == "y"
    
    return {
        'recursive': recursive
    }

def folder_analysis_menu():
    """Analyze a folder without uploading"""
    clear_screen()
    print_banner()
    p.bold("📊 Folder Analysis")
    p.n()
    
    print_tip("Analyze folder contents without uploading anything.")
    p.n()
    
    # Get folder path
    folder_path = browse_local_folder_menu()
    if not folder_path:
        return
    
    # Get content filter
    content_types = filter_content_menu()
    
    # Get scan options
    scan_options = scan_options_menu()
    
    # Perform scan
    clear_screen()
    print_banner()
    p.bold("🔍 Scanning Folder...")
    p.n()
    
    try:
        scan_result = scan_folder(
            folder_path, 
            file_types=content_types,
            recursive=scan_options['recursive']
        )
        
        display_scan_results(scan_result)
        
        # Detailed analysis
        p.bold("📈 Detailed Analysis:")
        files = scan_result['files']
        
        for file_type, file_list in files.items():
            if file_list:
                sizes = [f['size'] for f in file_list]
                avg_size = sum(sizes) / len(sizes) if sizes else 0
                max_size = max(sizes) if sizes else 0
                min_size = min(sizes) if sizes else 0
                
                p.yellow(f"{file_type} Statistics:")
                p.lgray(f"   Count: {len(file_list)}")
                p.lgray(f"   Total Size: {format_file_size(sum(sizes))}")
                p.lgray(f"   Average Size: {format_file_size(avg_size)}")
                p.lgray(f"   Largest File: {format_file_size(max_size)}")
                p.lgray(f"   Smallest File: {format_file_size(min_size)}")
                p.n()
        
        # Estimate upload time (rough calculation)
        total_mb = scan_result['total_size'] / (1024 * 1024)
        estimated_minutes = total_mb / 10  # Assume ~10MB/min average
        
        p.cyan("⏱️ Upload Estimates:")
        p.lgray(f"   Total Data: {scan_result['total_size_formatted']}")
        p.lgray(f"   Estimated Upload Time: ~{estimated_minutes:.1f} minutes")
        p.lgray(f"   (Actual time depends on internet speed and file processing)")
        
    except Exception as e:
        print_error(f"Failed to scan folder: {str(e)}")
    
    wait_key()

def browse_storylinez_folders_menu(client):
    """Browse Storylinez folders to select destination"""
    current_path = "/"
    
    while True:
        clear_screen()
        print_banner()
        p.bold("📂 Browse Storylinez Folders")
        p.n()
        
        p.cyan(f"Current Path: {current_path}")
        p.n()
        
        try:
            # Get folder contents
            folder_contents = client.storage.get_folder_contents(
                path=current_path,
                recursive=False,
                detailed=False,
                org_id=ORG_ID
            )
            
            folders = folder_contents.get('folders', [])
            
            options = []
            if current_path != "/":
                options.append("⬆️ Go to parent folder")
            
            for folder in folders:
                folder_name = folder.get('name', 'Unnamed')
                options.append(f"📁 {folder_name}")
            
            options.extend([
                "➕ Create new folder here",
                "✅ Select this folder as destination",
                "❌ Back to main menu"
            ])
            
            if not folders and current_path == "/":
                p.lgray("No folders found. You can create a new folder or use the root directory.")
                p.n()
            
            choice = select_from_list(options, "Choose action")
            
            # Handle parent folder
            if current_path != "/" and choice == 0:
                current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
                continue
            
            # Adjust choice if we have parent folder option
            if current_path != "/":
                choice -= 1
            
            # Handle folder selection
            if choice < len(folders):
                selected_folder = folders[choice]
                folder_name = selected_folder.get('name', 'Unnamed')
                current_path = current_path.rstrip("/") + "/" + folder_name
                if current_path.startswith("//"):
                    current_path = current_path[1:]
                continue
            
            # Handle other options
            remaining_choice = choice - len(folders)
            
            if remaining_choice == 0:  # Create new folder
                new_folder_name = get_input(
                    "Enter new folder name",
                    required=True,
                    help_text="Name for the new folder"
                )
                
                if new_folder_name:
                    try:
                        result = client.storage.create_folder(
                            folder_name=new_folder_name,
                            parent_path=current_path,
                            org_id=ORG_ID
                        )
                        print_success(f"Created folder: {new_folder_name}")
                        time.sleep(1)
                    except Exception as e:
                        print_error(f"Failed to create folder: {str(e)}")
                        time.sleep(2)
            
            elif remaining_choice == 1:  # Select this folder
                return current_path
            
            elif remaining_choice == 2:  # Back to main menu
                return None
                
        except Exception as e:
            print_error(f"Failed to browse folders: {str(e)}")
            wait_key()
            return None

def configure_upload_settings():
    """Configure upload and processing settings"""
    clear_screen()
    print_banner()
    p.bold("🔧 Configure Upload Settings")
    p.n()
    
    print_tip("These settings control how your files are processed after upload.")
    p.n()
    
    # Basic settings
    context = get_input(
        "Context/Description for files",
        help_text="Describe what these files are about (helps with AI analysis)"
    )
    
    tags_input = get_input(
        "Tags (comma-separated)",
        help_text="Tags to help organize and find your content later"
    )
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    
    # Processing options
    p.n()
    p.yellow("🔬 Processing Options:")
    p.n()
    
    analyze_audio = get_input(
        "Analyze audio in media files? (y/n)",
        default="y",
        help_text="Extract audio information and transcripts from videos"
    ).lower() == "y"
    
    auto_company_details = get_input(
        "Use company details for analysis? (y/n)",
        default="y",
        help_text="Apply your company profile to improve analysis"
    ).lower() == "y"
    
    deepthink = get_input(
        "Enable deepthink analysis? (y/n)",
        default="n",
        help_text="More thorough analysis (slower but better results)"
    ).lower() == "y"
    
    overdrive = get_input(
        "Enable overdrive processing? (y/n)",
        default="n",
        help_text="Maximum quality analysis (slowest but best results)"
    ).lower() == "y"
    
    web_search = get_input(
        "Enable web search enhancement? (y/n)",
        default="n",
        help_text="Use web search to enhance analysis with current information"
    ).lower() == "y"
    
    eco = get_input(
        "Enable eco mode? (y/n)",
        default="y",
        help_text="Faster, more efficient processing (recommended for bulk uploads)"
    ).lower() == "y"
    
    try:
        temperature = float(get_input(
            "AI creativity temperature (0.0-1.0)",
            default="0.7",
            help_text="0.0 = conservative, 1.0 = creative analysis"
        ))
        if not 0.0 <= temperature <= 1.0:
            temperature = 0.7
    except ValueError:
        temperature = 0.7
    
    # Polling settings
    p.n()
    p.yellow("⏱️ Processing Settings:")
    p.n()
    
    try:
        max_wait_time = int(get_input(
            "Max wait time per file (seconds)",
            default="1800",
            help_text="Maximum time to wait for each file to process (recommended: 1800-3600 for large files)"
        ))
        if max_wait_time < 300:
            print_warning("Very short timeout may cause false failures. Minimum recommended: 300 seconds.")
            max_wait_time = max(max_wait_time, 300)
    except ValueError:
        max_wait_time = 1800
    
    try:
        poll_interval = int(get_input(
            "Check status every X seconds",
            default="15",
            help_text="How often to check if processing is complete (recommended: 15-30 seconds)"
        ))
        if poll_interval < 5:
            print_warning("Very frequent polling may cause API rate limits. Minimum recommended: 5 seconds.")
            poll_interval = max(poll_interval, 5)
    except ValueError:
        poll_interval = 15
    
    return {
        'context': context,
        'tags': tags,
        'analyze_audio': analyze_audio,
        'auto_company_details': auto_company_details,
        'deepthink': deepthink,
        'overdrive': overdrive,
        'web_search': web_search,
        'eco': eco,
        'temperature': temperature,
        'max_wait_time': max_wait_time,
        'poll_interval': poll_interval
    }

def confirm_upload_menu(scan_result, destination_path, upload_settings):
    """Show upload confirmation with all details"""
    clear_screen()
    print_banner()
    p.bold("✅ Confirm Upload")
    p.n()
    
    # Source info
    p.cyan("📁 Source:")
    p.lgray(f"   Local Folder: {scan_result['folder_path']}")
    p.lgray(f"   Total Files: {scan_result['total_files']}")
    p.lgray(f"   Total Size: {scan_result['total_size_formatted']}")
    p.n()
    
    # File breakdown
    for file_type, file_list in scan_result['files'].items():
        if file_list:
            total_size = sum(f['size'] for f in file_list)
            p.lgray(f"   {file_type}: {len(file_list)} files ({format_file_size(total_size)})")
    p.n()
    
    # Destination
    p.cyan("📂 Destination:")
    p.lgray(f"   Storylinez Folder: {destination_path}")
    p.n()
    
    # Settings
    p.cyan("🔧 Settings:")
    if upload_settings['context']:
        p.lgray(f"   Context: {upload_settings['context']}")
    if upload_settings['tags']:
        p.lgray(f"   Tags: {', '.join(upload_settings['tags'])}")
    
    processing_options = []
    if upload_settings['analyze_audio']:
        processing_options.append("Audio Analysis")
    if upload_settings['deepthink']:
        processing_options.append("Deepthink")
    if upload_settings['overdrive']:
        processing_options.append("Overdrive")
    if upload_settings['web_search']:
        processing_options.append("Web Search")
    if upload_settings['eco']:
        processing_options.append("Eco Mode")
    
    if processing_options:
        p.lgray(f"   Processing: {', '.join(processing_options)}")
    
    p.lgray(f"   Temperature: {upload_settings['temperature']}")
    p.lgray(f"   Max Wait: {upload_settings['max_wait_time']}s per file")
    p.n()
    
    # Estimate
    total_mb = scan_result['total_size'] / (1024 * 1024)
    estimated_minutes = total_mb / 10  # Rough estimate
    processing_time = scan_result['total_files'] * 2  # Rough processing estimate
    
    p.yellow("⏱️ Estimates:")
    p.lgray(f"   Upload Time: ~{estimated_minutes:.1f} minutes")
    p.lgray(f"   Processing Time: ~{processing_time:.1f} minutes")
    p.lgray(f"   Total Time: ~{estimated_minutes + processing_time:.1f} minutes")
    p.n()
    
    p.red("⚠️ Warning: This will upload and process all files. Make sure you have sufficient quota.")
    p.n()
    
    confirm = get_input(
        "Proceed with upload? (yes/no)",
        required=True,
        help_text="Type 'yes' to start the upload process"
    ).lower()
    
    return confirm in ['yes', 'y']

def perform_bulk_upload(client, file_paths, destination_path, upload_settings):
    """Perform the actual bulk upload"""
    clear_screen()
    print_banner()
    p.bold("🚀 Starting Bulk Upload")
    p.n()
    
    p.cyan(f"Uploading {len(file_paths)} files to {destination_path}")
    p.lgray("You can press Ctrl+C to cancel (uploaded files will continue processing)")
    p.n()
    
    start_time = time.time()
    
    try:
        # Prepare file paths list
        file_paths_list = [f['path'] for f in file_paths]
        
        # Debug output
        print(f"DEBUG: Starting upload of {len(file_paths_list)} files")
        print(f"DEBUG: First file: {file_paths_list[0] if file_paths_list else 'None'}")
        print(f"DEBUG: Upload settings: {upload_settings}")
        
        # Start bulk upload
        results = client.storage.upload_and_process_files_bulk(
            file_paths=file_paths_list,
            folder_path=destination_path,
            context=upload_settings['context'],
            tags=upload_settings['tags'],
            analyze_audio=upload_settings['analyze_audio'],
            auto_company_details=upload_settings['auto_company_details'],
            deepthink=upload_settings['deepthink'],
            overdrive=upload_settings['overdrive'],
            web_search=upload_settings['web_search'],
            eco=upload_settings['eco'],
            temperature=upload_settings['temperature'],
            org_id=ORG_ID,
            progress_callback=progress_callback,
            poll_interval=upload_settings['poll_interval'],
            max_wait_time=upload_settings['max_wait_time']
        )
        
        print(f"DEBUG: Upload completed, results type: {type(results)}")
        print(f"DEBUG: Results length: {len(results) if hasattr(results, '__len__') else 'N/A'}")
        
        # Final results
        end_time = time.time()
        duration = end_time - start_time
        
        clear_screen()
        print_banner()
        p.bold("📊 Upload Complete!")
        p.n()
        
        successful = sum(1 for r in results if r.get('success', False))
        failed = len(results) - successful
        
        p.green(f"✅ Successful: {successful}")
        p.red(f"❌ Failed: {failed}")
        p.cyan(f"⏱️ Duration: {duration/60:.1f} minutes")
        p.n()
        
        if failed > 0:
            p.yellow("❌ Failed Files:")
            for result in results:
                if not result.get('success', False):
                    file_name = os.path.basename(result['file_path'])
                    error = result.get('error', 'Unknown error')
                    p.red(f"   • {file_name}: {error}")
            p.n()
        
        return results
        
    except KeyboardInterrupt:
        p.yellow("\n🛑 Upload cancelled by user")
        p.lgray("Note: Files already uploaded will continue processing in the background")
        return None
    
    except Exception as e:
        print_error(f"Upload failed: {str(e)}")
        return None

def bulk_upload_workflow():
    """Main workflow for bulk uploading"""
    # Initialize client
    try:
        client = StorylinezClient(API_KEY, API_SECRET, org_id=ORG_ID)
    except Exception as e:
        print_error(f"Failed to initialize client: {str(e)}")
        return
    
    # Step 1: Select local folder
    clear_screen()
    print_banner()
    p.bold("Step 1: Select Local Folder")
    p.n()
    
    local_folder = browse_local_folder_menu()
    if not local_folder:
        return
    
    # Step 2: Filter content types
    content_types = filter_content_menu()
    
    # Step 3: Scan options
    scan_options = scan_options_menu()
    
    # Step 4: Scan folder
    clear_screen()
    print_banner()
    p.bold("Step 2: Scanning Folder...")
    p.n()
    
    try:
        scan_result = scan_folder(
            local_folder,
            file_types=content_types,
            recursive=scan_options['recursive']
        )
    except Exception as e:
        print_error(f"Failed to scan folder: {str(e)}")
        wait_key()
        return
    
    if scan_result['total_files'] == 0:
        print_warning("No supported files found in the selected folder.")
        wait_key()
        return
    
    display_scan_results(scan_result)
    
    if not get_input("Continue with these files? (y/n)", default="y").lower().startswith('y'):
        return
    
    # Step 5: Select destination folder
    clear_screen()
    print_banner()
    p.bold("Step 3: Select Destination Folder")
    p.n()
    
    destination_path = browse_storylinez_folders_menu(client)
    if destination_path is None:
        return
    
    # Step 6: Configure upload settings
    upload_settings = configure_upload_settings()
    
    # Step 7: Confirmation
    # Collect all file info for upload
    all_files = []
    for file_type, files in scan_result['files'].items():
        all_files.extend(files)
    
    if not confirm_upload_menu(scan_result, destination_path, upload_settings):
        p.yellow("Upload cancelled.")
        wait_key()
        return
    
    # Step 8: Perform upload
    results = perform_bulk_upload(client, all_files, destination_path, upload_settings)
    
    if results:
        wait_key()

def run():
    """Main application loop"""
    try:
        # Validate API credentials
        if not API_KEY or not API_SECRET or not ORG_ID:
            clear_screen()
            print_banner()
            print_error("Missing API credentials!")
            p.lgray("Please set STORYLINEZ_API_KEY, STORYLINEZ_API_SECRET, and STORYLINEZ_ORG_ID")
            p.lgray("in your .env file or environment variables.")
            return
        
        # Test client connection
        try:
            client = StorylinezClient(API_KEY, API_SECRET, org_id=ORG_ID)
            # Test connection with a simple call
            client.storage.get_storage_usage(org_id=ORG_ID)
        except Exception as e:
            clear_screen()
            print_banner()
            print_error("Failed to connect to Storylinez API!")
            p.lgray(f"Error: {str(e)}")
            p.lgray("Please check your API credentials and internet connection.")
            return
        
        while True:
            try:
                choice = main_menu()
                
                if choice == 1:  # Browse and upload
                    bulk_upload_workflow()
                
                elif choice == 2:  # Browse Storylinez folders
                    clear_screen()
                    print_banner()
                    p.bold("📂 Browse Storylinez Folders")
                    p.n()
                    
                    selected_path = browse_storylinez_folders_menu(client)
                    if selected_path:
                        p.green(f"Selected folder: {selected_path}")
                        wait_key()
                
                elif choice == 3:  # Configure settings
                    settings = configure_upload_settings()
                    p.green("Settings configured (will be used in next upload)")
                    wait_key()
                
                elif choice == 4:  # Quick analysis
                    folder_analysis_menu()
                
                elif choice == 5:  # Exit
                    clear_screen()
                    p.cyan("👋 Thank you for using Storylinez Bulk Uploader!")
                    p.lgray("Visit https://storylinez.com for more tools and documentation.")
                    break
            
            except KeyboardInterrupt:
                clear_screen()
                p.yellow("\n🛑 Operation cancelled by user")
                if get_input("Return to main menu? (y/n)", default="y").lower().startswith('y'):
                    continue
                else:
                    break
            
            except Exception as e:
                clear_screen()
                print_error(f"An error occurred: {str(e)}")
                p.lgray("Returning to main menu...")
                time.sleep(2)
                continue
                
    except KeyboardInterrupt:
        clear_screen()
        p.yellow("👋 Goodbye!")
    except Exception as e:
        clear_screen()
        print_error(f"Critical application error: {str(e)}")
        p.lgray("Please check your API credentials and internet connection.")
        p.lgray("If the problem persists, contact support at support@storylinez.com")

if __name__ == "__main__":
    run()