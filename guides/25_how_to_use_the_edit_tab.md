# How to Use the Edit Tab on Storylinez

Master the Edit tab to fine-tune your video sequences, adjust timing, manage audio, and prepare your final video for rendering.

## What is the Edit Tab?

The Edit tab is where you:
- Transform storyboard scenes into detailed video sequences
- Edit clip timing, transitions, and effects
- Manage audio tracks and voiceover synchronization
- Apply templates and color grading
- Preview your complete video timeline

## Accessing the Edit Tab

1. Complete your storyboard first (required)
2. Navigate to the **Edit** tab in Project Workflow
3. If no sequence exists, create one from your storyboard
4. The sequence will load automatically for editing

## Creating a Sequence

### From Storyboard
1. Click **Create Sequence** if none exists
2. Configure sequence settings:
   - **Apply Template**: Add text overlays and graphics
   - **Apply Grade**: Enable color correction
   - **Grade Type**: Single grade for all clips or multi for individual grading
   - **AI Settings**: DeepThink, Overdrive, Web Search, Eco mode
   - **Temperature & Iterations**: Control AI creativity and refinement

**System Intelligence Features:**
- **Automatic Web Search**: When content needs current information, the system automatically searches Google with AI-generated queries
- **Built-in Tools**: Calculator and statistical tools activate automatically when needed for your content
- **Smart Processing**: No manual controls required - AI decides when to use these advanced features

### Generation Process
1. Monitor sequence generation progress
2. Wait for completion (typically 3-7 minutes)
3. The generated sequence loads automatically

## Understanding the Edit Interface

### Timeline View
- **Video Clips**: Main video content arranged sequentially
- **Audio Tracks**: Background music and sound effects
- **Voiceover Track**: Generated or uploaded voiceover audio
- **Playhead**: Shows current playback position
- **Time Ruler**: Displays timeline in seconds

### Clip Properties
Each clip includes:
- **In/Out Points**: Start and end times within the source media
- **Duration**: Length of the clip in the sequence
- **Transitions**: Effects between clips (cut, fade, dissolve)
- **Templates**: Text overlays and graphics
- **Color Grading**: Visual enhancement effects

## Editing Video Clips

### Selecting Clips
1. Click any clip on the timeline to select it
2. Selected clip highlights in blue
3. Properties panel shows editable values

### Timing Adjustments
1. **In Point**: Change where the clip starts in source media
2. **Out Point**: Change where the clip ends in source media
3. **Duration**: Automatically updates based on in/out points
4. Use precise values or drag handles on timeline

### Clip Operations
- **Duplicate**: Right-click → Duplicate to copy clips
- **Split**: Position playhead and split clips at that point
- **Move**: Drag clips left/right to reorder
- **Delete**: Select and press Delete key

### Transitions
1. Select any clip to see its incoming transition
2. Choose from: Cut, Fade, Dissolve, Slide, Zoom
3. Transitions affect how clips connect to previous clips

## Working with Audio

### Audio Tracks
- Multiple audio tracks can play simultaneously
- Each track has independent volume and timing
- Tracks can overlap for layered sound design

### Audio Editing
1. **In/Out Points**: Trim audio start and end times
2. **Volume**: Adjust playback level (0-100%)
3. **Timing**: Position audio at specific timeline points
4. **Fade**: Add smooth fade in/out effects

### Voiceover Management
- Generated voiceover appears as single track
- Adjust timing to sync with video content
- Cannot edit content, only timing and volume

## Templates and Graphics

### Applying Templates
1. Select any video clip
2. Choose template from available options
3. Customize text content:
   - **Heading**: Main title text
   - **Description**: Subtitle or body text
4. Adjust template positioning and timing

### Template Settings
- Duration and positioning
- Text styling and effects
- Animation timing and transitions

## Color Grading

### Grade Types
- **Single Grade**: One color treatment for entire video
- **Multi Grade**: Individual grading per clip
- **None**: No color enhancement

### Grade Application
1. Enable grading in sequence settings
2. Select clips to apply specific grades
3. AI applies appropriate color correction
4. Preview changes in real-time

## Timeline Controls

### Playback
- **Play/Pause**: Spacebar or play button
- **Scrub**: Drag playhead to specific time
- **Skip**: Arrow keys for frame-by-frame movement

### Zoom and Navigation
- **Zoom In/Out**: Mouse wheel or zoom controls
- **Fit to Timeline**: View entire sequence
- **Scroll**: Horizontal scrolling for long sequences

### Selection Tools
- Click individual elements to select
- Multiple selection for batch operations
- Context menus for quick actions

## Sequence Settings

### Regeneration Options
1. **Update Settings**: Modify AI parameters
2. **Save & Regenerate**: Apply new settings and regenerate
3. **Regeneration Prompt**: Add specific instructions for changes

### AI Parameters
- **Temperature**: Creativity level (0.1-1.0)
- **Iterations**: Refinement passes
- **DeepThink**: Enhanced analysis
- **Overdrive**: Maximum quality processing
- **Web Search**: Current information inclusion
- **Eco Mode**: Faster processing

## Preview and Review

### Real-time Preview
- Click play to preview current sequence
- See transitions, timing, and effects
- Audio plays synchronized with video

### Quality Check
- Review clip boundaries and transitions
- Check audio synchronization
- Verify template positioning and text
- Ensure smooth narrative flow

## Saving and History

### Auto-save
- Changes save automatically as you work
- No manual save required for most edits
- History tracks all modifications

### Version Control
- Previous versions accessible through history
- Compare different sequence iterations
- Revert to earlier versions if needed

## Understanding Workflow Dependencies

### Cascade Outdated Markers
When upstream workflow steps change, you'll see red cascade outdated markers in the Edit tab. This indicates you're working with outdated data.

**Dependency Chain:**
Project Settings → Import → Prompt → Storyboard → Voiceover → Edit → Render

**Important**: Import tab changes affect ALL downstream tabs, even though Import appears after Prompt visually.

**To resolve cascade outdated markers:**
1. Update all previous tabs first (Prompt, Storyboard, Voiceover)
2. Then click "Update" in the Edit tab
3. This refreshes your sequence with the latest data

### Stale Markers
Appear when you change sequence settings but haven't regenerated:
- AI parameters (Temperature, Iterations, DeepThink, etc.)
- Apply Template or Apply Grade settings
- Other sequence configuration options

**To resolve**: Use the chat panel to regenerate your sequence with new settings

## Best Practices

### Workflow Organization
- Complete storyboard before starting sequence editing
- Make broad structural changes first, details last
- Preview frequently to check flow and timing

### Performance Tips
- Use Eco mode for iterative testing
- Apply DeepThink only for final versions
- Close unnecessary browser tabs for better performance

### Creative Guidelines
- Maintain consistent pacing throughout
- Balance audio levels between tracks
- Use transitions purposefully, not excessively
- Ensure templates enhance rather than distract

## Troubleshooting

### Sequence Won't Load
- Verify storyboard is complete
- Check internet connection
- Refresh browser and try again

### Editing Lag
- Reduce browser memory usage
- Switch to Eco mode for faster processing
- Avoid making many simultaneous changes

### Audio Sync Issues
- Check voiceover timing alignment
- Verify audio track positioning
- Use precise timing values for critical sync points

### Template Problems
- Ensure text content fits available space
- Check template timing doesn't exceed clip duration
- Verify template positioning is appropriate for clip content

The Edit tab gives you complete control over your video's final form, allowing you to create polished, professional content from your storyboard foundation.
