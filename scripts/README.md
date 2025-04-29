# Storylinez Auto Video Builder

## Overview

The Auto Video Builder is a powerful tool that automates the end-to-end process of creating professional videos using the Storylinez SDK. It leverages AI to handle everything from content planning to rendering, with customizable options at each step. This tool is designed to simplify video creation while providing flexibility and control throughout the process.

## Design Philosophy

The Auto Video Builder was designed with several core principles in mind:

1. **Accessibility**: Make professional video creation accessible to users regardless of their technical expertise or creative background.
2. **Flexibility**: Provide options for both automated workflows and manual intervention at any stage.
3. **Quality**: Leverage advanced AI capabilities to produce professional-grade results.
4. **Efficiency**: Automate repetitive or complex tasks to dramatically speed up the video creation process.
5. **Education**: Help users learn about video production through self-documenting interfaces and contextual guidance.

These principles guided the development of both the CLI tool and Jupyter notebook implementations, with each designed to serve different use cases and user preferences.

## How It Works

The Auto Video Builder follows a structured workflow based on Storylinez's video creation pipeline:

1. **Project Creation**: Establishes a project container with basic metadata
2. **Prompt Generation**: Creates an AI prompt that defines the video's content and style
3. **Media Search**: Intelligently searches for relevant stock media (videos, audio, images)
4. **Storyboard Generation**: AI translates the prompt into a structured storyboard
5. **Voiceover Creation**: Generates professional voiceover based on the storyboard
6. **Sequence Assembly**: Creates a video sequence combining storyboard and media
7. **Rendering**: Renders the final video with customized settings

The process is available both as a CLI tool (`auto_video_builder.py`) and a Jupyter notebook (`auto_video_builder.ipynb`), offering flexibility for different use cases.

### Complete Workflow Visualization

```
┌─────────────────┐
│  Upload Files   │
└─────────────────┘  
        │
        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Create Project │────▶│   Add Files     │────▶│  Create Prompt  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Create Sequence │◀────│Create Voiceover │◀────│Create Storyboard│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Render Video   │
└─────────────────┘
```

Each step can be performed automatically or with manual intervention, allowing users to control exactly how their video is created.

## Architecture Design

### CLI Implementation

The CLI tool (`auto_video_builder.py`) is structured using a menu-driven approach for several reasons:

- **User Flexibility**: Allows users to jump in at any stage of the video creation process
- **Error Recovery**: If one step fails, users can retry just that step rather than starting over
- **Step-by-Step Guidance**: Each menu provides contextual help and tips
- **Educational Value**: Teaches users about the video creation workflow

#### CLI Architecture

The CLI tool is organized as a series of interconnected menu functions, each handling a specific part of the video creation process. The main modules include:

1. **UI Components**: Functions like `print_banner()`, `print_tip()`, and `get_input()` provide a consistent user interface
2. **Menu Handlers**: Functions like `main_menu()`, `project_menu()`, etc. handle user navigation
3. **Process Functions**: Functions like `wait_for_render()` perform actual operations
4. **Auto-Add Components**: Intelligence-driven functions that automatically find and add relevant content

This modular design allows for easy maintenance and extensibility. Each function has a single responsibility, making the code more maintainable and easier to understand.

### Notebook Implementation

The Jupyter notebook (`auto_video_builder.ipynb`) offers a more exploratory approach:

- **Visual Workflow**: Shows the full process from start to finish in sequential cells
- **Result Inspection**: Allows examination of intermediate results (JSON responses)
- **Educational Resource**: Includes detailed comments explaining each step
- **Customization**: Easier to modify parameters and experiment with different settings

#### Notebook Architecture

The notebook is organized into logical sections following the video creation pipeline:

1. **Setup**: Initialize the client and import dependencies
2. **Project Creation**: Create and configure a project
3. **Prompt Generation**: Define what the video should be about
4. **Media Search**: Generate queries and find stock media
5. **Storyboard Generation**: Create a visual plan
6. **Voiceover Creation**: Generate audio narration
7. **Sequence Assembly**: Arrange media into a timeline
8. **Rendering**: Produce the final video

Each section includes:
- Markdown cells explaining concepts and options
- Code cells demonstrating the API calls
- Additional cells showing how to inspect and modify results

## Key Design Decisions

### 1. Two-Mode Operation

**Decision**: Implement both CLI and notebook interfaces for the same functionality.

**Rationale**: Different users have different needs:
- **CLI benefits:**
  - Better for production environments with repeatable processes
  - Ideal for users who prefer guided step-by-step interfaces
  - More practical for scheduled or automated operations
  - More approachable for non-technical users or those new to Python

- **Notebook benefits:**
  - Better for experimentation and learning
  - Ideal for data scientists and developers used to notebook environments
  - Provides better visibility into API responses and data structures
  - Easier to customize and extend the code

Providing both interfaces ensures that all users can work in their preferred environment while accessing the same capabilities.

### 2. AI-Driven Media Search

**Decision**: Use AI to generate search queries rather than relying on user input.

**Rationale**:
- **Better results:** AI can generate more varied and contextually appropriate search terms than humans typically would
- **Reduced cognitive load:** Users don't need to think about what might make a good search term
- **Domain knowledge:** Leverages the AI's understanding of video production and what visuals might pair well with specific content
- **Consistency with project:** Generated queries align better with the overall project goals and style
- **Time savings:** Drastically reduces the time spent searching for appropriate media

This approach transforms what would traditionally be a time-consuming, manual process into a quick, automated one that often produces better results.

### 3. Auto-Add Content Feature

**Decision**: Implement a feature to automatically find and add appropriate content.

**Rationale**:
- **Workflow acceleration:** Removes the most time-consuming part of video creation
- **AI curation:** Uses context-aware selection to find the most relevant media
- **Customizable thresholds:** Allows users to control how strict the matching should be
- **Learning from examples:** The system improves over time by observing which media works well with which content
- **Optional use:** Users can still manually select media if preferred

The auto-add feature represents the most significant time-saving element of the tool, reducing what might take hours of searching and selection to just minutes.

### 4. Interactive Help System

**Decision**: Implement a detailed help system with contextual tips.

**Rationale**:
- **Makes the tool self-documenting** and accessible to new users
- **Provides just-in-time guidance** rather than requiring users to read documentation
- **Shows "tricks" that advanced users might not discover** on their own
- **Reduces support requirements** by answering common questions proactively
- **Encourages best practices** by providing expert guidance at decision points

By integrating help directly into the workflow, users learn while creating, leading to better videos and a reduced learning curve.

## Implementation Details

### Project Management

Projects are created with metadata that guides the AI:
- `name`: Used in AI prompt generation and final branding
- `orientation`: Determines video dimensions and layout
- `purpose`: Helps the AI understand the video's goals
- `target_audience`: Influences tone, style, and content selection

```python
project = client.project.create_project(
    name="Product Introduction",
    orientation="landscape",
    purpose="Introduce our new sustainable product line"
)
```

The project container serves as the foundation for the entire video creation process, organizing all assets, metadata, and components in one place. The metadata fields are carefully chosen to provide the AI with the context it needs to make intelligent decisions throughout the process.

### Prompt Generation

The system supports two types of prompts:
1. **Text prompts**: User-provided descriptions of desired content
2. **Video prompts**: Reference videos that AI analyzes for style and structure

Text prompts include elements like:
- Main content description
- Document context for additional information
- Temperature for controlling creativity vs. consistency
- Iteration settings for refinement quality

The dual-prompt approach was implemented to accommodate different user preferences and use cases. Text prompts offer more control over content and are ideal for most cases. Video prompts are better for matching an existing style or format.

### Media Search Query Generation

The media search system uses a sophisticated AI-driven approach:

1. **Context Analysis**: The system analyzes the project details and any prompt information
2. **Query Generation**: Multiple search queries are created, each targeting different aspects of the content
3. **Media Type Targeting**: Separate queries are optimized for videos, audio, and images
4. **Semantic Encoding**: Queries are converted to vector embeddings for semantic search

This approach yields far better results than traditional keyword search:

```python
search_query_results = client.prompt.start_query_gen_and_wait(
    project_id=project_id,
    num_videos=3,  # Get 3 video search terms
    num_audio=2,   # Get 2 audio search terms
    company_details="Company context helps generate better queries",
    max_wait_seconds=60
)
```

The system might generate queries like "sustainable bamboo products in nature setting," "eco-friendly packaging close up," and "happy customers using reusable products" from a simple project description about sustainable goods. These diverse angles ensure comprehensive media options.

### Storyboard Generation

The storyboard is the blueprint for the video, created by AI based on the prompt:

```python
storyboard_job = client.storyboard.create_storyboard(
    project_id=project_id,
    deepthink=True,  # Enable more thoughtful analysis
    overdrive=True,  # Maximize quality
    iterations=3,    # Multiple refinement passes
    full_length=20   # Target length in seconds
)
```

The storyboard generator uses several sophisticated techniques:

1. **Scene Planning**: Divides content into logical scenes with timing
2. **Visual Direction**: Creates detailed visual descriptions for each scene
3. **Script Writing**: Generates professional narration text for each segment
4. **Pacing Control**: Manages timing between scenes for narrative flow
5. **Coherence Checking**: Ensures the story makes sense as a whole

With `deepthink` and `overdrive` options enabled, the storyboard undergoes additional analysis and refinement passes, looking for improvements in clarity, engagement, and effectiveness. The `iterations` parameter controls how many refinement passes the AI performs.

### Sequence Assembly

The sequence stage combines the storyboard with selected media:

```python
sequence_job = client.sequence.create_sequence(
    project_id=project_id,
    apply_template=True,  # Use professional templates
    apply_grade=True,     # Apply color grading
    grade_type="single"   # Consistent color scheme
)
```

During sequence creation, the system performs complex operations:

1. **Media Matching**: Finds the best stock media match for each storyboard scene
2. **Timing Adjustment**: Ensures media timing aligns with scene durations
3. **Transition Selection**: Chooses appropriate transitions between scenes
4. **Audio Alignment**: Synchronizes voiceover with visuals
5. **Color Consistency**: Applies color grading to unify diverse media

The sequence generator uses AI to understand both the content of the scenes and the available media, making sophisticated matching decisions based on semantic understanding rather than simple keywords.

### Rendering

The final step produces the complete video with customizable settings:

```python
render_job = client.render.create_render(
    project_id=project_id,
    target_width=1920,
    target_height=1080,
    bg_music_volume=0.5,
    voiceover_volume=0.7,
    subtitle_enabled=True
)
```

The renderer handles several complex tasks:

1. **Audio Mixing**: Combines background music, voiceover, and video sound
2. **Subtitle Generation**: Creates and times subtitles from the script
3. **Resolution Optimization**: Renders at the specified quality level
4. **Branding Elements**: Adds logo, outro, and call-to-action
5. **Color Correction**: Applies final color adjustments for consistency

The rendering engine optimizes the output for quality while balancing file size considerations, ensuring the video is suitable for various distribution channels.

## Auto-Add Content Feature

One of the most powerful features of the Auto Video Builder is the ability to automatically find and add relevant content to a project. This feature is implemented in two functions:

1. `auto_add_stock_media_to_project`: Finds and adds stock media based on project context
2. `auto_add_user_files_to_project`: Finds and adds the user's own relevant files

### How Auto-Add Stock Media Works

The auto-add stock media feature follows a sophisticated workflow:

1. **Context Extraction**: Analyzes the project name, purpose, and any existing prompt
2. **Query Generation**: Uses AI to generate multiple search queries targeted to the content
3. **Semantic Search**: Performs vector-based semantic search across stock libraries
4. **Relevance Ranking**: Scores results based on semantic similarity to the project
5. **Media Selection**: Selects the most appropriate media based on relevance scores
6. **Project Addition**: Adds the selected media to the project

The entire process is automated but customizable. Users can select:
- Which types of media to find (video, audio, images)
- How many results to return per query
- The similarity threshold for matching

The system uses vector embeddings and semantic similarity rather than keyword matching, allowing it to find conceptually related media even when terminology differs.

### How Auto-Add User Files Works

The auto-add user files feature takes a similar approach but works with the user's own content:

1. **Context Building**: Combines project metadata and prompt information
2. **Query Generation**: Creates search queries based on this context
3. **Vector Search**: Searches the user's file storage using semantic vectors
4. **Result Presentation**: Shows matching files with relevance scores
5. **Selection Options**: Lets users add all files, top N files, or manually select

This feature helps users discover relevant content they may have forgotten about or wouldn't have thought to search for, making use of their existing assets more efficient.

## Usage Examples

### Basic CLI Usage

```
python auto_video_builder.py
```

The CLI will guide you through the following steps:
1. Creating or selecting a project
2. Adding media (auto or manual)
3. Creating a prompt
4. Generating a storyboard
5. Creating a voiceover
6. Building a sequence
7. Rendering the final video

### Running in a Jupyter Notebook

Simply open the `auto_video_builder.ipynb` file in Jupyter and run the cells sequentially. The notebook implements the same workflow but allows for more experimentation and visualization of intermediate results.

### API Integration Example

```python
from storylinez import StorylinezClient

# Initialize the client
client = StorylinezClient(api_key=API_KEY, api_secret=API_SECRET)

# Create a project
project = client.project.create_project(
    name="Product Demo",
    orientation="landscape"
)

# Use the auto-add functionality (from the auto_video_builder)
from scripts.auto_video_builder import auto_add_stock_media_to_project

auto_add_stock_media_to_project(client, project["project"]["project_id"])
```

## Advanced Features

### Content Auto-Addition

The `auto_add_stock_media_to_project` and `auto_add_user_files_to_project` functions demonstrate sophisticated AI integration:

1. Analyze project context (name, purpose, audience)
2. Generate optimal search queries using AI
3. Perform semantic vector search across media libraries
4. Rank results by relevance to the project
5. Add the most appropriate media automatically

This dramatically speeds up the most time-consuming part of video creation.

### Job Monitoring

Both implementations include job monitoring capabilities:

```python
# Notebook style - manual checking
render_results = client.render.get_render(
    project_id=project_id,
    include_results=True
)

# CLI style - automatic polling with feedback
wait_for_render(client, project_id)
```

The job monitoring systems handle:
- Polling at appropriate intervals
- User-friendly status updates
- Timeout handling
- Error detection and reporting

### Error Handling

The system includes robust error handling:
- API error detection and friendly messages
- Rate limit handling with appropriate delays
- Recovery options when steps fail
- Detailed logging of process steps

## Detailed Workflow Explanation

### 1. Project Creation

The workflow begins with creating a project container. The auto_video_builder helps users create projects with appropriate metadata:

- **Name**: A descriptive name that helps the AI understand the content
- **Orientation**: Landscape (16:9) or Portrait (9:16) based on intended platform
- **Purpose**: Explanation of the video's goal to guide AI decisions
- **Target Audience**: Information about intended viewers to inform tone and style

This metadata influences every subsequent step, from media selection to tone of script.

### 2. File Management

Users have three options for adding media to their project:

1. **Auto-add stock media**: Let the AI find and add relevant stock videos and audio
2. **Auto-add user files**: Have the AI search the user's own media library
3. **Manual selection**: Browse and choose specific media files

The auto-add options use sophisticated AI to understand the project context and find the most relevant media, saving significant time in the creation process.

### 3. Prompt Creation

The prompt defines what the video should be about and how it should feel. Options include:

- **Text prompt**: Describe the video content in natural language
- **Reference video prompt**: Use an existing video as a style reference

Advanced options like `deepthink`, `overdrive`, and `web_search` control how much effort the AI puts into understanding and developing the prompt.

### 4. Storyboard Generation

The storyboard is the blueprint for the video, defining:

- **Scenes**: What appears visually in each segment
- **Script**: What will be said in the voiceover
- **Timing**: How long each scene should last
- **Transitions**: How scenes connect together

The tool offers granular control over storyboard creation, with options to regenerate specific scenes or the entire storyboard.

### 5. Voiceover Creation

The voiceover brings the script to life. Options include:

- **Generated voiceover**: AI-created voice based on the storyboard script
- **Custom voiceover**: Upload your own voice recordings

The system ensures timing alignment between the voiceover and visual elements.

### 6. Sequence Assembly

The sequence assembles all elements into a coherent timeline:

- Combines storyboard guidance with selected media
- Applies templates for professional structure
- Adds color grading for visual consistency
- Ensures proper timing of all elements

This step transforms individual components into a coherent video.

### 7. Rendering

The final step produces a completed video with options for:

- Resolution and quality settings
- Audio levels for music, voiceover, and video sound
- Subtitle generation and styling
- Branding elements like logos and call-to-action
- Special effects and transitions

## Conclusion

The Auto Video Builder represents a significant advancement in automated video creation. By combining AI-driven content generation with sophisticated media management, it makes professional video production accessible to everyone.

The two implementations (CLI and notebook) provide flexibility for different use cases, while the modular design allows for future expansion and customization. The tool demonstrates how AI can transform complex creative processes into streamlined workflows without sacrificing quality or creative control.

Whether you're creating a single video or managing a large-scale content production pipeline, the Auto Video Builder provides the tools to do it efficiently and effectively.
