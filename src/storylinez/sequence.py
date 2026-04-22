import os
import json
import requests
import warnings
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
from .base_client import BaseClient
from .shared.validation import normalize_engine, normalize_model, validate_eco_model_conflict, get_allowed_engines, get_allowed_models

class SequenceClient(BaseClient):
    """
    Client for interacting with Storylinez Sequence API.
    Provides methods for creating, retrieving, and managing sequences for video generation.
    
    This client offers a chat-like experience with the AI where you can:
    - View previous versions of sequences
    - Send natural language instructions as regeneration prompts
    - Leverage conversation history for contextual regeneration
    - Alternate between precise manual edits and AI-guided creative changes
    
    IMPORTANT: Sequence operations are only supported for v1 (legacy) projects.
    For v2 (sequence builder) projects, use the /v2/sequence workflows instead.
    """
    
    # Cache for project types to avoid redundant lookups
    _project_type_cache = {}
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinezads.com", default_org_id: str = None):
        """
        Initialize the SequenceClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.sequence_url = f"{self.base_url}/sequence"
    
    @staticmethod
    def _normalize_project_type_hint(project_type: Optional[str]) -> Optional[str]:
        """Normalize project type string to 'v1' or 'v2'."""
        if not project_type:
            return None
        pt = project_type.lower().strip()
        if pt in ('v1', 'legacy', '1'):
            return 'v1'
        if pt in ('v2', 'sequence_builder', '2'):
            return 'v2'
        return None
    
    def _get_project_type(self, project_id: str, project_type_hint: Optional[str] = None) -> str:
        """
        Get project type from cache or by fetching project details.
        
        Args:
            project_id: ID of the project
            project_type_hint: Optional project type hint ('v1', 'v2', etc.)
            
        Returns:
            Project type ('v1' or 'v2')
        """
        normalized_hint = self._normalize_project_type_hint(project_type_hint)
        if normalized_hint:
            self._project_type_cache[project_id] = normalized_hint
            return normalized_hint
        
        if project_id in self._project_type_cache:
            return self._project_type_cache[project_id]
        
        # Fetch project to determine type
        try:
            project_url = f"{self.base_url}/projects/get"
            response = self._make_request("GET", project_url, params={"project_id": project_id})
            project_type = response.get('type', 'v1')
            self._project_type_cache[project_id] = project_type
            return project_type
        except Exception:
            return 'v1'  # Default to v1 for backward compatibility
    
    def _ensure_legacy_sequence_supported(self, project_id: str, project_type_hint: Optional[str] = None) -> None:
        """
        Ensure the project supports legacy sequence operations (v1 only).
        
        Args:
            project_id: ID of the project
            project_type_hint: Optional project type hint
            
        Raises:
            ValueError: If project is v2 (not supported for legacy sequences)
        """
        project_type = self._get_project_type(project_id, project_type_hint)
        if project_type == 'v2':
            raise ValueError(
                "Sequence operations are disabled for v2 sequence builder projects via legacy endpoints. "
                "Use the /v2/sequence workflows instead."
            )
    
    # Sequence Creation and Retrieval
    
    def create_sequence(
        self, 
        project_id: str, 
        apply_template: bool = False, 
        apply_grade: bool = False, 
        grade_type: str = "single",
        orientation: str = None, 
        deepthink: bool = False, 
        overdrive: bool = False, 
        web_search: bool = False,
        eco: bool = False,
        enable_content_analysis: Optional[bool] = None,
        temperature: float = 0.7,
        iterations: int = 1,
        engine: Optional[str] = None,
        model_override: Optional[str] = None,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Create a new sequence for a project.
        
        Args:
            project_id: ID of the project to create the sequence for
            apply_template: Whether to apply a template to the sequence
            apply_grade: Whether to apply color grading to the sequence
            grade_type: Type of grading to apply ("single" or "multi")
            orientation: Video orientation ("landscape", "portrait", or "square") - defaults to project setting
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            enable_content_analysis: Toggle context augmentation/content analysis for regeneration (defaults to project setting)
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            engine: Optional AI engine selection (e.g., 'gpt-4', 'claude-3.5-sonnet', etc.)
            model_override: Optional model override for advanced control
            project_type: Optional project type hint ('v1', 'v2', 'legacy', 'sequence_builder') to avoid extra API calls
            
        Returns:
            Dictionary with the created sequence details and job information
        
        Raises:
            ValueError: For invalid parameter values or if project is v2
            Exception: If API request fails
        """
        if not project_id:
            raise ValueError("project_id is required")
        
        # Ensure project supports legacy sequences
        self._ensure_legacy_sequence_supported(project_id, project_type)
        
        # Validate grade_type
        if grade_type not in ["single", "multi"]:
            raise ValueError("grade_type must be either 'single' or 'multi'")
        
        # Validate orientation if provided
        if orientation and orientation not in ["landscape", "portrait", "square"]:
            raise ValueError("orientation must be one of: 'landscape', 'portrait', 'square'")
        
        # Validate temperature range
        if not (0.0 <= temperature <= 1.0):
            raise ValueError("temperature must be between 0.0 and 1.0")
        
        # Validate iterations
        if iterations < 1:
            raise ValueError("iterations must be at least 1")
        
        # Display helpful tips based on settings
        if deepthink and temperature < 0.5:
            warnings.warn("Using deepthink with low temperature (<0.5) may result in very conservative outputs.")
        
        if overdrive and eco:
            warnings.warn("'overdrive' and 'eco' modes have opposite effects. Consider using only one.")
        
        data = {
            "project_id": project_id,
            "apply_template": apply_template,
            "apply_grade": apply_grade,
            "grade_type": grade_type,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
            "temperature": float(temperature),  # Ensure it's a float
            "iterations": int(iterations)       # Ensure it's an integer
        }
        
        if orientation:
            data["orientation"] = orientation
        
        if enable_content_analysis is not None:
            data["enable_content_analysis"] = bool(enable_content_analysis)

        # Normalize and validate engine parameter
        if engine is not None:
            try:
                data["engine"] = normalize_engine(engine)
            except ValueError as e:
                raise ValueError(f"{e}. Hint: Use one of {get_allowed_engines()}")
        
        # Normalize and validate model parameter
        if model_override is not None:
            try:
                normalized_model = normalize_model(model_override, domain='narrative_v1')
                # Validate eco + custom model conflict
                validate_eco_model_conflict(eco, normalized_model, domain='narrative_v1')
                data["model_override"] = normalized_model
            except ValueError as e:
                raise ValueError(f"{e}. Hint: Allowed models are {get_allowed_models('narrative_v1')}")
            
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
        
        return self._make_request("POST", f"{self.sequence_url}/create", json_data=data)
    
    def get_sequence(
        self, 
        sequence_id: str = None, 
        project_id: str = None,
        include_results: bool = True, 
        include_storyboard: bool = False,
        **kwargs
    ) -> Dict:
        """
        Get details of a sequence by either sequence ID or project ID.
        
        Args:
            sequence_id: ID of the sequence to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the sequence for (either this or sequence_id must be provided)
            include_results: Whether to include job results
            include_storyboard: Whether to include the storyboard data
            
        Returns:
            Dictionary with sequence details
            
        Raises:
            ValueError: If neither sequence_id nor project_id is provided
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        params = {
            "include_results": str(include_results).lower(),
            "include_storyboard": str(include_storyboard).lower()
        }
        
        if sequence_id:
            params["sequence_id"] = sequence_id
        if project_id:
            params["project_id"] = project_id
            
        # Add any additional kwargs for backward compatibility
        params.update(kwargs)
            
        return self._make_request("GET", f"{self.sequence_url}/get", params=params)
    
    def redo_sequence(
        self, 
        sequence_id: str = None, 
        project_id: str = None,
        include_history: bool = True,
        regenerate_prompt: str = None,
        engine: Optional[str] = None,
        model_override: Optional[str] = None,
        enable_content_analysis: Optional[bool] = None,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Regenerate a sequence with the latest storyboard data.
        
        Args:
            sequence_id: ID of the sequence to regenerate (either this or project_id must be provided)
            project_id: ID of the project whose sequence to regenerate (either this or sequence_id must be provided)
            include_history: Whether to include sequence history as context for regeneration (defaults to True)
            regenerate_prompt: Custom prompt to guide regeneration with specific instructions
            engine: Optional engine override to use for regeneration (e.g., "openai-gpt4", "anthropic-claude")
            model_override: Optional model override for fine-grained control of the AI model
            enable_content_analysis: Whether to enable or disable content analysis/context augmentation during regeneration
            project_type: Optional project type hint to avoid extra API calls
            
        Returns:
            Dictionary with the regeneration job details
            
        Raises:
            ValueError: If neither sequence_id nor project_id is provided or if project is v2
            
        Chat Experience Notes:
            - This method is key to the chat-like experience, enabling you to send instructions
              to the AI to improve your sequence through natural language prompts
            - The regenerate_prompt is your message to the AI, guiding how it should modify
              the sequence from its current state
            - Setting include_history=True creates a more conversational experience as the
              AI considers the previous interactions as context
            - Example prompts:
              * "Make transitions between scenes smoother and use more dynamic camera movements"
              * "Keep my edits to clips 2-4, but make all other clips more vibrant"
              * "Create a more dramatic feel with slower motion in the climax scene"
            - The AI will respond with a new sequence version, advancing the conversation
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
        
        # If we have project_id directly, validate it
        sequence_data: Optional[Dict] = None
        pid_to_check = project_id
        if sequence_id:
            sequence_data = self.get_sequence(
                sequence_id=sequence_id,
                include_results=False,
                include_storyboard=False
            )
            if not pid_to_check:
                pid_to_check = sequence_data.get('project_id')
        
        if pid_to_check:
            self._ensure_legacy_sequence_supported(pid_to_check, project_type)
            
        data = {"include_history": include_history}

        if engine is not None:
            try:
                data["engine"] = normalize_engine(engine)
            except ValueError as e:
                raise ValueError(f"{e}. Hint: Use one of {get_allowed_engines()}")

        if model_override is not None:
            try:
                normalized_model = normalize_model(model_override, domain='narrative_v1')
            except ValueError as e:
                raise ValueError(f"{e}. Hint: Allowed models are {get_allowed_models('narrative_v1')}")

            if sequence_data is None:
                if sequence_id:
                    sequence_data = self.get_sequence(
                        sequence_id=sequence_id,
                        include_results=False,
                        include_storyboard=False
                    )
                elif project_id:
                    sequence_data = self.get_sequence(
                        project_id=project_id,
                        include_results=False,
                        include_storyboard=False
                    )

            eco_enabled = bool(sequence_data.get('eco', False)) if sequence_data else False
            validate_eco_model_conflict(eco_enabled, normalized_model, domain='narrative_v1')
            data["model_override"] = normalized_model

        if enable_content_analysis is not None:
            data["enable_content_analysis"] = bool(enable_content_analysis)
        
        if sequence_id:
            data["sequence_id"] = sequence_id
        if project_id:
            data["project_id"] = project_id
        if regenerate_prompt:
            data["regenerate_prompt"] = regenerate_prompt
            
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
            
        return self._make_request("POST", f"{self.sequence_url}/redo", json_data=data)
    
    def update_sequence(
        self, 
        sequence_id: str = None, 
        project_id: str = None, 
        update_ai_params: bool = True,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Update a sequence with the latest storyboard and voiceover data without regenerating it.
        This is useful when upstream components like storyboard or voiceover have changed.
        
        Args:
            sequence_id: ID of the sequence to update (either this or project_id must be provided)
            project_id: ID of the project whose sequence to update (either this or sequence_id must be provided)
            update_ai_params: Whether to update AI parameters from the project's storyboard
            project_type: Optional project type hint to avoid extra API calls
            
        Returns:
            Dictionary with update confirmation
            
        Raises:
            ValueError: If neither sequence_id nor project_id is provided or if project is v2
            
        Notes:
            This method only updates the sequence with the latest data but does not regenerate it.
            To regenerate the sequence after updating, use redo_sequence().
            Typical workflow: modify storyboard → update_sequence() → redo_sequence()
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
        
        # If we have project_id directly, validate it
        pid_to_check = project_id
        if not pid_to_check and sequence_id:
            # Need to fetch sequence to get project_id
            seq = self.get_sequence(sequence_id=sequence_id)
            pid_to_check = seq.get('project_id')
        
        if pid_to_check:
            self._ensure_legacy_sequence_supported(pid_to_check, project_type)
            
        data = {"update_ai_params": update_ai_params}
        
        if sequence_id:
            data["sequence_id"] = sequence_id
        if project_id:
            data["project_id"] = project_id
            
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
            
        return self._make_request("PUT", f"{self.sequence_url}/selfupdate", json_data=data)
    
    def update_sequence_settings(
        self,
        sequence_id: str = None, 
        project_id: str = None,
        apply_template: bool = None, 
        apply_grade: bool = None,
        grade_type: str = None, 
        orientation: str = None,
        deepthink: bool = None, 
        overdrive: bool = None,
    web_search: bool = None, 
    eco: bool = None,
    engine: Optional[str] = None,
    model_override: Optional[str] = None,
    enable_content_analysis: Optional[bool] = None,
    temperature: float = None, 
    iterations: int = None,
        regenerate_prompt: str = None, 
        edited_sequence: Dict = None,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Update sequence settings without regenerating.
        
        Args:
            sequence_id: ID of the sequence to update (either this or project_id must be provided)
            project_id: ID of the project whose sequence to update (either this or sequence_id must be provided)
            apply_template: Whether to apply a template to the sequence
            apply_grade: Whether to apply color grading to the sequence
            grade_type: Type of grading to apply ("single" or "multi")
            orientation: Video orientation ("landscape", "portrait", or "square")
            deepthink: Enable advanced thinking for complex topics
            overdrive: Enable maximum quality and detail
            web_search: Enable web search for up-to-date information
            eco: Enable eco mode for faster processing
            engine: Optional AI engine override to persist for subsequent regenerations
            model_override: Optional model alias override (use 'auto' to return to default model selection)
            enable_content_analysis: Toggle context augmentation/content analysis for downstream regenerations
            temperature: AI temperature parameter (0.0-1.0)
            iterations: Number of refinement iterations
            regenerate_prompt: Optional prompt to guide regeneration
            edited_sequence: Complete edited sequence structure
            project_type: Optional project type hint to avoid extra API calls
            
        Returns:
            Dictionary with the update confirmation
            
        Raises:
            ValueError: If neither sequence_id nor project_id is provided, for invalid parameters, or if project is v2
            
        Notes:
            Changes are only saved but not applied - use redo_sequence() after updating to regenerate
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
        
        # If we have project_id directly, validate it
        sequence_data: Optional[Dict] = None
        pid_to_check = project_id
        if not pid_to_check and sequence_id:
            sequence_data = self.get_sequence(
                sequence_id=sequence_id,
                include_results=False,
                include_storyboard=False
            )
            pid_to_check = sequence_data.get('project_id')
        
        if pid_to_check:
            self._ensure_legacy_sequence_supported(pid_to_check, project_type)
        
        # Validate parameters if provided
        if grade_type is not None and grade_type not in ["single", "multi"]:
            raise ValueError("grade_type must be either 'single' or 'multi'")
        
        if orientation is not None and orientation not in ["landscape", "portrait", "square"]:
            raise ValueError("orientation must be one of: 'landscape', 'portrait', 'square'")
        
        if temperature is not None and not (0.0 <= temperature <= 1.0):
            raise ValueError("temperature must be between 0.0 and 1.0")
        
        if iterations is not None and iterations < 1:
            raise ValueError("iterations must be at least 1")
            
        data = {}
        
        if sequence_id:
            data["sequence_id"] = sequence_id
        if project_id:
            data["project_id"] = project_id
        if apply_template is not None:
            data["apply_template"] = apply_template
        if apply_grade is not None:
            data["apply_grade"] = apply_grade
        if grade_type is not None:
            data["grade_type"] = grade_type
        if orientation is not None:
            data["orientation"] = orientation
        if deepthink is not None:
            data["deepthink"] = deepthink
        if overdrive is not None:
            data["overdrive"] = overdrive
        if web_search is not None:
            data["web_search"] = web_search
        if eco is not None:
            data["eco"] = eco
        if engine is not None:
            try:
                data["engine"] = normalize_engine(engine)
            except ValueError as e:
                raise ValueError(f"{e}. Hint: Use one of {get_allowed_engines()}")
        if model_override is not None:
            if isinstance(model_override, str) and model_override.strip().lower() == "auto":
                data["model_override"] = "auto"
            else:
                try:
                    normalized_model = normalize_model(model_override, domain='narrative_v1')
                except ValueError as e:
                    allowed_models = get_allowed_models('narrative_v1')
                    raise ValueError(f"{e}. Hint: Allowed models are {allowed_models}")

                if sequence_data is None:
                    if sequence_id:
                        sequence_data = self.get_sequence(
                            sequence_id=sequence_id,
                            include_results=False,
                            include_storyboard=False
                        )
                    elif project_id:
                        sequence_data = self.get_sequence(
                            project_id=project_id,
                            include_results=False,
                            include_storyboard=False
                        )

                if eco is not None:
                    eco_enabled = bool(eco)
                elif sequence_data:
                    eco_enabled = bool(sequence_data.get('eco', False))
                else:
                    eco_enabled = False
                validate_eco_model_conflict(eco_enabled, normalized_model, domain='narrative_v1')
                data["model_override"] = normalized_model
        if enable_content_analysis is not None:
            data["enable_content_analysis"] = bool(enable_content_analysis)
        if temperature is not None:
            data["temperature"] = float(temperature)
        if iterations is not None:
            data["iterations"] = int(iterations)
        if regenerate_prompt is not None:
            data["regenerate_prompt"] = regenerate_prompt
        if edited_sequence is not None:
            data["edited_sequence"] = edited_sequence
        
        # Check if any settings are being updated
        if len(data) <= 1:  # Just the ID
            raise ValueError("At least one setting must be provided to update")
            
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
            
        return self._make_request("PUT", f"{self.sequence_url}/update", json_data=data)
    
    def get_sequence_history(
        self,
        sequence_id: str, 
        page: int = 1, 
        limit: int = 10,
        history_type: str = None, 
        include_current: bool = False,
        **kwargs
    ) -> Dict:
        """
        Get history of changes for a sequence.
        
        Args:
            sequence_id: ID of the sequence
            page: Page number for pagination
            limit: Number of items per page
            history_type: Filter by history type ("update", "generation", "prompt", "media_change", or "selfupdate")
            include_current: Whether to include the current state
            
        Returns:
            Dictionary with history entries
            
        Raises:
            ValueError: If sequence_id is not provided or parameters are invalid
            
        Chat Experience Notes:
            - The history represents the complete conversation between you and the AI
            - Different history_types correspond to different types of interactions:
              * 'prompt': Your messages/instructions to the AI (like chat messages)
              * 'generation': AI's responses as generated sequence content
              * 'update': Manual edits you've made (outside the AI conversation)
              * 'selfupdate': System updates from cascade changes
              * 'media_change': Specific media file replacements
            - This timeline creates a full record of your creative process
            - Use this data to build a chat-like interface showing the back-and-forth
              between you and the AI as you refine the sequence together
            - Manual edits can be displayed as special actions in the chat timeline
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
            
        # Validate history_type if provided
        if history_type and history_type not in ["update", "generation", "prompt", "media_change", "selfupdate"]:
            raise ValueError("history_type must be one of: 'update', 'generation', 'prompt', 'media_change', 'selfupdate'")
        
        # Validate pagination parameters
        if page < 1:
            raise ValueError("page must be at least 1")
        if limit < 1:
            raise ValueError("limit must be at least 1")
            
        params = {
            "sequence_id": sequence_id,
            "page": page,
            "limit": limit,
            "include_current": str(include_current).lower()
        }
        
        if history_type:
            params["history_type"] = history_type
            
        # Add any additional kwargs for backward compatibility
        params.update(kwargs)
            
        return self._make_request("GET", f"{self.sequence_url}/history", params=params)
    
    def get_sequence_media(
        self,
        sequence_id: str = None, 
        project_id: str = None,
        include_analysis: bool = False, 
        generate_thumbnail: bool = True,
        generate_streamable: bool = True, 
        generate_download: bool = False,
        **kwargs
    ) -> Dict:
        """
        Get media files used in a sequence.
        
        Args:
            sequence_id: ID of the sequence (either this or project_id must be provided)
            project_id: ID of the project (either this or sequence_id must be provided)
            include_analysis: Whether to include detailed analysis data
            generate_thumbnail: Whether to generate thumbnail URLs
            generate_streamable: Whether to generate streamable URLs
            generate_download: Whether to generate download URLs
            
        Returns:
            Dictionary with media files grouped by type (clips, audios, voiceover)
            
        Raises:
            ValueError: If neither sequence_id nor project_id is provided
            
        Notes:
            Set generate_download=True only when you need to download the original files.
            For preview purposes, use generate_streamable=True instead.
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        params = {
            "include_analysis": str(include_analysis).lower(),
            "generate_thumbnail": str(generate_thumbnail).lower(),
            "generate_streamable": str(generate_streamable).lower(),
            "generate_download": str(generate_download).lower()
        }
        
        if sequence_id:
            params["sequence_id"] = sequence_id
        if project_id:
            params["project_id"] = project_id
            
        # Add any additional kwargs for backward compatibility
        params.update(kwargs)
            
        return self._make_request("GET", f"{self.sequence_url}/media_involved", params=params)
    
    # Sequence Editing Operations
    
    def reorder_sequence_items(
        self,
        sequence_id: str, 
        array_type: str, 
        new_order: List[int],
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Reorder items in a sequence array.
        
        Args:
            sequence_id: ID of the sequence to modify
            array_type: Type of array to modify ("clips" or "audios")
            new_order: List of indices in the new order
            project_type: Optional project type hint to avoid extra API calls
            
        Returns:
            Dictionary with operation confirmation
            
        Raises:
            ValueError: If parameters are invalid, missing, or if project is v2
            
        Example:
            # Swap first and second clips
            reorder_sequence_items(sequence_id="seq_123", array_type="clips", new_order=[1, 0, 2, 3])
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
        
        # Fetch sequence to get project_id and validate
        seq = self.get_sequence(sequence_id=sequence_id)
        pid_to_check = seq.get('project_id')
        if pid_to_check:
            self._ensure_legacy_sequence_supported(pid_to_check, project_type)
            
        if array_type not in ['clips', 'audios']:
            raise ValueError("array_type must be either 'clips' or 'audios'")
            
        if not isinstance(new_order, list) or not all(isinstance(i, int) for i in new_order):
            raise ValueError("new_order must be a list of integers")
            
        data = {
            "sequence_id": sequence_id,
            "array_type": array_type,
            "new_order": new_order
        }
        
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
        
        return self._make_request("PUT", f"{self.sequence_url}/reorder", json_data=data)
    
    def edit_sequence_item(
        self,
        sequence_id: str, 
        item_type: str, 
        item_index: int = None, 
        updated_item: Dict = None,
        file_id: str = None,
        stock_id: str = None,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Edit an item in a sequence.
        
        Args:
            sequence_id: ID of the sequence to modify
            item_type: Type of item to edit ("clips", "audios", or "voiceover")
            item_index: Index of the item to update (required for clips and audios)
            updated_item: Updated item data
            file_id: Optional file ID to replace the media (alternative to providing in updated_item)
            stock_id: Optional stock media ID to replace the media
            project_type: Optional project type hint to avoid extra API calls
            
        Returns:
            Dictionary with operation confirmation
            
        Raises:
            ValueError: If parameters are invalid, missing, or if project is v2
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
        
        # Fetch sequence to get project_id and validate
        seq = self.get_sequence(sequence_id=sequence_id)
        pid_to_check = seq.get('project_id')
        if pid_to_check:
            self._ensure_legacy_sequence_supported(pid_to_check, project_type)
            
        if item_type not in ['clips', 'audios', 'voiceover']:
            raise ValueError("item_type must be one of: 'clips', 'audios', 'voiceover'")
            
        if item_type != 'voiceover' and item_index is None:
            raise ValueError(f"item_index is required for item_type '{item_type}'")
            
        if not updated_item and not (file_id or stock_id):
            raise ValueError("Either updated_item, file_id, or stock_id must be provided")
            
        data = {
            "sequence_id": sequence_id,
            "item_type": item_type
        }
        
        if item_index is not None:
            data["item_index"] = item_index
            
        if updated_item:
            data["updated_item"] = updated_item
            
        if file_id:
            data["file_id"] = file_id
            
        if stock_id:
            data["stock_id"] = stock_id
        
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
            
        return self._make_request("PUT", f"{self.sequence_url}/edit/item", json_data=data)
    
    def change_sequence_media(
        self,
        sequence_id: str, 
        item_type: str, 
        item_index: int = None,
        file_id: str = None, 
        stock_id: str = None, 
        path: str = None,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Change media for an item in a sequence.
        
        Args:
            sequence_id: ID of the sequence to modify
            item_type: Type of item to modify ("clips", "audios", or "voiceover")
            item_index: Index of the item to update (required for clips and audios)
            file_id: ID of the file to use (one of file_id, stock_id, or path must be provided)
            stock_id: ID of the stock media to use (one of file_id, stock_id, or path must be provided)
            path: Direct path to the media file (one of file_id, stock_id, or path must be provided)
            project_type: Optional project type hint to avoid extra API calls
            
        Returns:
            Dictionary with operation confirmation
            
        Raises:
            ValueError: If parameters are invalid, missing, or if project is v2
            
        Notes:
            Use this method for simple media replacement. For more complex changes,
            use edit_sequence_item() instead.
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
        
        # Fetch sequence to get project_id and validate
        seq = self.get_sequence(sequence_id=sequence_id)
        pid_to_check = seq.get('project_id')
        if pid_to_check:
            self._ensure_legacy_sequence_supported(pid_to_check, project_type)
            
        if item_type not in ['clips', 'audios', 'voiceover']:
            raise ValueError("item_type must be one of: 'clips', 'audios', 'voiceover'")
            
        if item_type != 'voiceover' and item_index is None:
            raise ValueError(f"item_index is required for item_type '{item_type}'")
            
        if not any([file_id, stock_id, path]):
            raise ValueError("One of file_id, stock_id, or path must be provided")
            
        data = {
            "sequence_id": sequence_id,
            "item_type": item_type
        }
        
        if item_index is not None:
            data["item_index"] = item_index
            
        if file_id:
            data["file_id"] = file_id
        elif stock_id:
            data["stock_id"] = stock_id
        elif path:
            data["path"] = path
        
        # Add any additional kwargs for backward compatibility
        data.update(kwargs)
            
        return self._make_request("PUT", f"{self.sequence_url}/change_media", json_data=data)
        
    # Convenience methods and workflows
    
    def update_and_regenerate(
        self,
        sequence_id: str = None,
        project_id: str = None,
        regenerate_prompt: str = None,
        include_history: bool = True,
        wait_for_completion: bool = False,
        check_interval: int = 5,
        timeout: int = 600
    ) -> Dict:
        """
        Update a sequence with latest data and then regenerate it in one operation.
        This is a convenience method that combines update_sequence() and redo_sequence().
        
        Args:
            sequence_id: ID of the sequence (either this or project_id must be provided)
            project_id: ID of the project (either this or sequence_id must be provided)
            regenerate_prompt: Optional prompt to guide the regeneration
            include_history: Whether to include sequence history as context
            wait_for_completion: Whether to wait for job completion
            check_interval: Seconds between job status checks (if waiting)
            timeout: Maximum seconds to wait (if waiting)
            
        Returns:
            Dictionary with the regeneration job details
            
        Raises:
            ValueError: If parameters are invalid
            TimeoutError: If job doesn't complete within the timeout period
            
        Notes:
            This is particularly useful when upstream components (storyboard or voiceover)
            have been modified and you want to regenerate the sequence with those changes.
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
            
        # First update the sequence with latest data
        update_result = self.update_sequence(
            sequence_id=sequence_id,
            project_id=project_id,
            update_ai_params=True
        )
        
        # Then regenerate the sequence
        redo_result = self.redo_sequence(
            sequence_id=sequence_id if sequence_id else update_result.get('sequence_id'),
            project_id=project_id,
            include_history=include_history,
            regenerate_prompt=regenerate_prompt
        )
        
        if wait_for_completion:
            # TODO: Implement job status checking until completion or timeout
            # This would likely need a get_job_status method and polling logic
            pass
            
        return redo_result
    
    def swap_media(
        self, 
        sequence_id: str,
        first_item_index: int,
        second_item_index: int,
        array_type: str = "clips"
    ) -> Dict:
        """
        Swap two media items in a sequence.
        
        Args:
            sequence_id: ID of the sequence to modify
            first_item_index: Index of the first item
            second_item_index: Index of the second item
            array_type: Type of array to modify ("clips" or "audios")
            
        Returns:
            Dictionary with operation confirmation
            
        Raises:
            ValueError: If parameters are invalid
            
        Notes:
            This is a convenience method that uses reorder_sequence_items() under the hood.
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
            
        if array_type not in ["clips", "audios"]:
            raise ValueError("array_type must be either 'clips' or 'audios'")
            
        # Get the sequence to determine the array length
        sequence = self.get_sequence(sequence_id=sequence_id)
        
        # Get edited_sequence if available, otherwise use job results
        sequence_data = None
        if sequence.get('edited_sequence'):
            sequence_data = sequence.get('edited_sequence')
        elif sequence.get('old_job_result'):
            sequence_data = sequence.get('old_job_result').get('results')
        
        if not sequence_data:
            raise ValueError("No sequence data available")
            
        # Get the array to work with
        items_array = sequence_data.get(array_type, [])
        if not items_array:
            raise ValueError(f"No {array_type} found in the sequence")
            
        # Validate indices
        array_length = len(items_array)
        if not (0 <= first_item_index < array_length and 0 <= second_item_index < array_length):
            raise ValueError(f"Indices must be between 0 and {array_length-1}")
            
        # Create the new order
        new_order = list(range(array_length))
        new_order[first_item_index], new_order[second_item_index] = new_order[second_item_index], new_order[first_item_index]
        
        # Reorder the items
        return self.reorder_sequence_items(
            sequence_id=sequence_id,
            array_type=array_type,
            new_order=new_order
        )
    
    # New methods for chat-like experience
    
    def send_chat_prompt(
        self,
        sequence_id: str = None, 
        project_id: str = None,
        prompt: str = None,
        include_history: bool = True,
        wait_for_completion: bool = False,
        polling_interval: int = 5,
        timeout: int = 300
    ) -> Dict:
        """
        Send a chat prompt to guide sequence regeneration (convenience method).
        
        Args:
            sequence_id: ID of the sequence (either this or project_id must be provided)
            project_id: ID of the project (either this or sequence_id must be provided)
            prompt: Natural language instructions for the AI
            include_history: Whether to include previous history as context
            wait_for_completion: Whether to wait for the job to complete before returning
            polling_interval: Seconds between status checks if waiting
            timeout: Maximum seconds to wait if waiting
            
        Returns:
            Dictionary with job information or completed sequence if waiting
            
        Raises:
            ValueError: If required parameters are missing
            TimeoutError: If waiting times out
            
        Chat Experience Notes:
            - This is the primary method for "chatting" with the AI about your sequence
            - Use natural language to describe the changes you want, as if talking to a human editor
            - For better results, be specific about what you like and what you want to change
            - The AI will consider the conversation history when include_history=True
            - Examples of effective prompts:
              * "Make the transitions between scenes smoother and more professional"
              * "I like my edits to the first clip. Now adjust the audio levels to match the new visual pacing"
              * "The sequence feels too slow. Can you make it more energetic while keeping my color grading?"
              
        Example:
            ```python
            # Start a conversation
            result = client.send_chat_prompt(
                sequence_id="seq_12345",
                prompt="Make the transitions between scenes smoother"
            )
            
            # Continue the conversation
            result = client.send_chat_prompt(
                sequence_id="seq_12345",
                prompt="I like the smooth transitions. Now make the color grade more cinematic."
            )
            ```
        """
        if not sequence_id and not project_id:
            raise ValueError("Either sequence_id or project_id must be provided")
        
        if not prompt:
            raise ValueError("A prompt message is required")
        
        # Send the regeneration prompt
        result = self.redo_sequence(
            sequence_id=sequence_id,
            project_id=project_id,
            regenerate_prompt=prompt,
            include_history=include_history
        )
        
        job_id = result.get('job_id')
        result_sequence_id = result.get('sequence_id') or sequence_id
        
        # If requested to wait for completion
        if wait_for_completion and job_id and result_sequence_id:
            start_time = datetime.now()
            elapsed = 0
            
            while elapsed < timeout:
                # Check job status by getting the sequence
                sequence = self.get_sequence(sequence_id=result_sequence_id, include_results=True)
                
                # Check if job is complete
                if sequence.get('old_job_result', {}).get('status') == 'COMPLETED':
                    return sequence
                
                # Wait before checking again
                import time
                time.sleep(polling_interval)
                
                # Update elapsed time
                elapsed = (datetime.now() - start_time).total_seconds()
            
            # If we get here, we timed out
            raise TimeoutError(f"Job did not complete within {timeout} seconds")
        
        return result
    
    def get_chat_history(
        self,
        sequence_id: str,
        limit: int = 20,
        include_generations: bool = True
    ) -> Dict:
        """
        Get sequence history formatted as a chat conversation.
        
        Args:
            sequence_id: ID of the sequence
            limit: Maximum number of history entries to return
            include_generations: Whether to include AI generations (output) or just prompts
            
        Returns:
            Dictionary with conversation entries formatted as a chat
            
        Raises:
            ValueError: If sequence_id is not provided
            
        Chat Experience Notes:
            - Returns history in a format suitable for rendering as a chat interface
            - Each entry has a role ('user' for prompts, 'assistant' for AI responses)
            - Entries are ordered chronologically to show the conversation flow
            - Use this to build the chat history panel in your UI
            - Can be displayed with user prompts on one side and AI generations on the other
            - Manual edits can be shown as system messages or special user actions
            - This format makes it easy to build a UI that mimics familiar chat applications
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
        
        # Get history entries with appropriate filters
        history_entries = []
        
        # Always get prompt entries (user messages)
        prompt_history = self.get_sequence_history(
            sequence_id=sequence_id,
            limit=limit,
            history_type="prompt"
        )
        
        if "history" in prompt_history:
            history_entries.extend([
                {
                    "role": "user",
                    "content": entry.get("prompt_text", ""),
                    "timestamp": entry.get("timestamp"),
                    "type": "prompt"
                }
                for entry in prompt_history.get("history", [])
            ])
        
        # Optionally get generation entries (AI responses)
        if include_generations:
            generation_history = self.get_sequence_history(
                sequence_id=sequence_id,
                limit=limit,
                history_type="generation"
            )
            
            if "history" in generation_history:
                history_entries.extend([
                    {
                        "role": "assistant",
                        "timestamp": entry.get("timestamp"),
                        "type": "generation",
                        "sequence_data_summary": self._summarize_sequence_data(entry.get("sequence_data", {}))
                    }
                    for entry in generation_history.get("history", [])
                ])
        
        # Sort all entries by timestamp
        history_entries.sort(key=lambda x: x.get("timestamp", ""), reverse=False)
        
        return {
            "sequence_id": sequence_id,
            "conversation": history_entries,
            "count": len(history_entries)
        }
    
    def _summarize_sequence_data(self, sequence_data: Dict) -> Dict:
        """
        Create a summary of sequence data for display in chat history.
        
        Args:
            sequence_data: The full sequence data
            
        Returns:
            Dictionary with summarized information
        """
        summary = {}
        
        # Count clips and total duration
        clips = sequence_data.get("clips", [])
        summary["clip_count"] = len(clips)
        
        # Calculate approximate total duration
        total_duration = 0
        for clip in clips:
            if "in" in clip and "out" in clip:
                clip_duration = clip.get("out", 0) - clip.get("in", 0)
                total_duration += clip_duration
        
        summary["approximate_duration"] = round(total_duration, 2)
        
        # Count audio tracks
        audios = sequence_data.get("audios", [])
        summary["audio_track_count"] = len(audios)
        
        # Check if sequence has voiceover
        summary["has_voiceover"] = "voiceover" in sequence_data and bool(sequence_data.get("voiceover"))
        
        return summary
    
    def restore_version(
        self,
        sequence_id: str,
        history_timestamp: str,
        apply_as_edit: bool = True,
        regenerate: bool = False,
        regenerate_prompt: str = None
    ) -> Dict:
        """
        Restore a previous version of a sequence from history.
        
        Args:
            sequence_id: ID of the sequence
            history_timestamp: Timestamp of the history entry to restore (from get_sequence_history)
            apply_as_edit: Whether to apply as an edit or directly regenerate
            regenerate: Whether to regenerate the sequence after restoring
            regenerate_prompt: Optional prompt to include with regeneration
            
        Returns:
            Dictionary with the update or regeneration result
            
        Raises:
            ValueError: If required parameters are missing
            
        Chat Experience Notes:
            - This method acts like a "restore" button in a chat interface
            - Allows you to go back to any point in the conversation history
            - You can either restore exactly as is (apply_as_edit=True, regenerate=False)
            - Or use it as a starting point for a new branch of conversation
              by adding a new prompt (regenerate=True, regenerate_prompt="New instructions")
            - This is useful for exploring different creative directions from a common starting point
            - In a chat UI, this could be implemented as a "Restore this version" button next to 
              each history entry
        """
        if not sequence_id or not history_timestamp:
            raise ValueError("Both sequence_id and history_timestamp are required")
        
        # Get full history to find the specific entry
        history_response = self.get_sequence_history(
            sequence_id=sequence_id,
            limit=100  # Fetch a large number to increase chances of finding the entry
        )
        
        target_entry = None
        for entry in history_response.get("history", []):
            if entry.get("timestamp") == history_timestamp and entry.get("history_type") in ["generation", "update"]:
                target_entry = entry
                break
                
        if not target_entry:
            raise ValueError(f"No history entry found with timestamp {history_timestamp}")
        
        sequence_data = target_entry.get("sequence_data")
        if not sequence_data:
            raise ValueError("Selected history entry does not contain sequence data")
            
        if apply_as_edit:
            # Apply as an edit to the sequence
            result = self.update_sequence_settings(
                sequence_id=sequence_id,
                edited_sequence=sequence_data
            )
            
            if regenerate:
                return self.redo_sequence(
                    sequence_id=sequence_id,
                    regenerate_prompt=regenerate_prompt,
                    include_history=True
                )
                
            return result
        else:
            # Apply by directly regenerating with this data as context
            prompt = "Restore this previous version" if not regenerate_prompt else regenerate_prompt
            
            # Update with the sequence data first
            self.update_sequence_settings(
                sequence_id=sequence_id,
                edited_sequence=sequence_data
            )
            
            # Then regenerate
            return self.redo_sequence(
                sequence_id=sequence_id, 
                regenerate_prompt=prompt,
                include_history=True
            )
    
    def combine_manual_and_ai_edits(
        self,
        sequence_id: str,
        manual_edits: Dict,
        ai_prompt: str = "Refine this sequence while keeping my manual edits intact",
        wait_for_completion: bool = False
    ) -> Dict:
        """
        Apply manual edits to a sequence and then use AI to further improve it.
        
        Args:
            sequence_id: ID of the sequence
            manual_edits: Dictionary with manual edit operations to perform
            ai_prompt: Natural language prompt guiding the AI about your edits
            wait_for_completion: Whether to wait for the AI job to complete
            
        Returns:
            Dictionary with the operation result
            
        Raises:
            ValueError: If required parameters are missing
            
        Chat Experience Notes:
            - This method exemplifies the collaborative workflow between human and AI
            - First applies your precise manual edits (technical changes)
            - Then lets the AI make creative improvements while respecting your edits
            - The ai_prompt should reference your manual edits to guide the AI
            - Example workflow:
              1. Make specific timing adjustments with manual_edits
              2. Ask AI to "improve the overall pacing while keeping my timing adjustments"
              3. Review the result and iterate again if needed
            - This hybrid approach combines the precision of manual editing with the
              creative power of AI-guided regeneration
        """
        if not sequence_id:
            raise ValueError("sequence_id is required")
            
        if not manual_edits or not isinstance(manual_edits, dict):
            raise ValueError("manual_edits must be a valid dictionary of edit operations")
            
        # First apply manual edits
        # Here we're simplifying by just using update_sequence_settings
        # In a real implementation, this might involve multiple specific edit operations
        result = self.update_sequence_settings(
            sequence_id=sequence_id,
            edited_sequence=manual_edits
        )
        
        # Then use AI to refine while keeping edits
        regeneration_result = self.send_chat_prompt(
            sequence_id=sequence_id,
            prompt=ai_prompt,
            include_history=True,
            wait_for_completion=wait_for_completion
        )
        
        return regeneration_result
