import os
import json
import requests
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, TypeVar, Union, cast
from datetime import datetime
from .base_client import BaseClient
import re
import warnings
import time

# Type alias for RGB colors
RGB = Tuple[int, int, int]
# Type alias for RGBA colors
RGBA = Tuple[int, int, int, int]
# Type for either RGB or RGBA
ColorType = TypeVar('ColorType', RGB, RGBA)

class RenderClient(BaseClient):
    """
    Client for interacting with Storylinez Render API.
    Provides methods for creating and managing video renders based on sequences.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinezads.com", default_org_id: str = None):
        """
        Initialize the RenderClient.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            default_org_id: Default organization ID to use for all API calls (optional)
        """
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self.render_url = f"{self.base_url}/render"
        self._project_type_cache: Dict[str, str] = {}
    
    # Utility functions for parameter handling
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> RGB:
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return (int(hex_color[0:2], 16), 
                int(hex_color[2:4], 16), 
                int(hex_color[4:6], 16))
    
    @staticmethod
    def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> RGBA:
        """Convert hex color string to RGBA tuple with specified alpha"""
        rgb = RenderClient._hex_to_rgb(hex_color)
        return (rgb[0], rgb[1], rgb[2], min(255, max(0, int(alpha * 255))))
    
    @staticmethod
    def _normalize_color(color: Union[str, List[int], Tuple[int, ...]], include_alpha: bool = False) -> Union[RGB, RGBA]:
        """
        Normalize a color value to RGB or RGBA tuple
        
        Args:
            color: Color in hex string format or RGB(A) list/tuple
            include_alpha: Whether to include alpha channel (defaults to False)
            
        Returns:
            RGB or RGBA tuple
        """
        if isinstance(color, str):
            # Handle hex color strings
            if color.startswith('#') or re.match(r'^[0-9a-fA-F]{6}$', color):
                rgb = RenderClient._hex_to_rgb(color)
                if include_alpha:
                    return (rgb[0], rgb[1], rgb[2], 255)  # Full opacity
                return rgb
            else:
                raise ValueError(f"Invalid hex color format: {color}")
        elif isinstance(color, (list, tuple)):
            # Handle RGB(A) lists/tuples
            if include_alpha:
                if len(color) == 3:
                    return (color[0], color[1], color[2], 255)  # Add full opacity
                elif len(color) == 4:
                    return (color[0], color[1], color[2], color[3])
                else:
                    raise ValueError(f"Color must have 3 or 4 components: {color}")
            else:
                if len(color) >= 3:
                    return (color[0], color[1], color[2])  # Take only RGB components
                else:
                    raise ValueError(f"Color must have at least 3 components: {color}")
        else:
            raise TypeError(f"Color must be a hex string or RGB(A) list/tuple: {color}")

    @staticmethod
    def _normalize_int_sequence(value: Union[List[int], Tuple[int, ...]], expected_length: Optional[int] = None, param_name: str = "value") -> List[int]:
        """Normalize lists/tuples containing integer data."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"{param_name} must be provided as a list or tuple of integers")

        normalized = [int(component) for component in value]
        if expected_length is not None and len(normalized) != expected_length:
            raise ValueError(f"{param_name} must contain exactly {expected_length} integers")
        return normalized
    
    @staticmethod
    def _validate_volume(volume: float) -> float:
        """
        Validate and normalize a volume value
        
        Args:
            volume: Volume value (should be between 0.0 and 1.0)
            
        Returns:
            Normalized volume value
        """
        try:
            volume = float(volume)
            if volume < 0.0:
                warnings.warn(f"Volume {volume} is negative, clamping to 0.0")
                return 0.0
            if volume > 1.2:
                warnings.warn(f"Volume {volume} exceeds 1.2, which may cause distortion. Values between 0.0 and 1.0 are recommended.")
            return volume
        except (ValueError, TypeError):
            raise ValueError(f"Volume must be a number between 0.0 and 1.0: {volume}")
    
    @staticmethod
    def _validate_dimensions(width: int, height: int, orientation: str) -> bool:
        """
        Validate video dimensions based on orientation
        
        Args:
            width: Video width in pixels
            height: Video height in pixels
            orientation: 'landscape' or 'portrait'
            
        Returns:
            True if dimensions are valid, False otherwise
        """
        # Minimum and maximum resolution limits
        MIN_WIDTH = 640
        MIN_HEIGHT = 360
        MAX_WIDTH = 7680
        MAX_HEIGHT = 4320
        
        # Check minimum resolution
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            raise ValueError(f"Resolution too small. Minimum dimensions: {MIN_WIDTH}x{MIN_HEIGHT}")
            
        # Check maximum resolution
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            raise ValueError(f"Resolution too large. Maximum dimensions: {MAX_WIDTH}x{MAX_HEIGHT}")
            
        # Aspect ratio validation
        if orientation == 'landscape' and width <= height:
            raise ValueError("For landscape orientation, width must be greater than height")
        elif orientation == 'portrait' and height <= width:
            raise ValueError("For portrait orientation, height must be greater than width")
            
        return True

    @staticmethod
    def _normalize_project_type_hint(project_type: Optional[str]) -> Optional[str]:
        """Normalize optional project_type hints provided by callers."""
        if project_type is None:
            return None
        if not isinstance(project_type, str):
            return None
        candidate = project_type.strip().lower()
        if candidate in ("v1", "v2"):
            return candidate
        return None

    def _get_project_type(self, project_id: str) -> str:
        """Fetch and cache project type information for render guard rails."""
        cached = self._project_type_cache.get(project_id)
        if cached:
            return cached

        response = self._make_request(
            "GET",
            f"{self.base_url}/projects/get_one",
            params={"project_id": project_id}
        )
        project_type = (response.get("type") or "v1").lower()
        self._project_type_cache[project_id] = project_type
        return project_type

    def _ensure_legacy_render_supported(self, project_id: str, project_type_hint: Optional[str]) -> str:
        """Raise when attempting to use legacy render APIs for v2 projects."""
        normalized_hint = self._normalize_project_type_hint(project_type_hint)
        resolved_type = normalized_hint or self._get_project_type(project_id)
        if resolved_type == "v2":
            raise ValueError(
                "Renders are disabled for v2 sequence builder projects via legacy endpoints. Use the /v2/render workflows instead."
            )
        return resolved_type

    def _resolve_project_id_from_render(self, render_id: str) -> str:
        """Resolve the owning project_id for a given render."""
        params = {
            "render_id": render_id,
            "include_results": "false",
            "include_sequence": "false",
            "include_subtitles": "false",
            "generate_download_link": "false",
            "generate_streamable_link": "false",
            "generate_thumbnail_stream_link": "false"
        }
        response = self._make_request("GET", f"{self.render_url}/get", params=params)
        if isinstance(response, dict):
            project_id = response.get("project_id")
            if project_id:
                return project_id
        raise ValueError("Could not determine project_id for the provided render_id")

    _BOOL_OPTION_KEYS: Tuple[str, ...] = (
        "standardize_resolution_enabled",
        "subtitle_enabled",
        "enable_cta",
        "color_balance_fix",
        "color_exposure_fix",
        "color_contrast_fix",
        "extend_short_clips",
        "image_slideshow",
        "adaptive_complexity",
        "enable_emergency_mode",
        "include_outro",
        "include_branding_outro",
        "subtitle_bg_rounded",
        "template_bg_rounded",
        "lingering_fix_enabled",
        "audio_lingering_fix_enabled",
        "allow_extend_last_clip",
        "add_blurred_background",
    )

    _INT_OPTION_KEYS: Tuple[str, ...] = (
        "min_video_length",
        "fallback_vo_length",
        "subtitle_font_size",
        "outro_logo_mode",
        "company_font_size",
        "subtext_font_size",
        "text_spacing",
        "logo_text_spacing",
        "cta_company_font_size",
        "cta_subtext_font_size",
        "subtitle_position",
        "subtitle_bg_padding",
        "subtitle_bg_corner_radius",
        "subtitle_squeeze_xp",
        "subtitle_max_group_size",
        "fps",
        "template_heading_font_size",
        "template_description_font_size",
        "template_text_spacing",
        "template_xp",
        "template_yp",
        "template_bg_corner_radius",
        "max_retries",
        "memory_threshold",
    )

    _FLOAT_OPTION_KEYS: Tuple[str, ...] = (
        "subtitle_bg_opacity",
        "outro_duration",
        "outro_transition_duration",
        "transition_duration",
        "text_transition_delay",
        "text_transition_duration",
        "template_bg_opacity",
        "template_text_transition_delay",
        "template_text_transition_duration",
        "subtitle_bridge_small_gaps_threshold",
        "scene_threshold",
        "scene_min_scene_duration",
        "scene_min_scene_gap",
        "lingering_max_window",
        "audio_lingering_max_window",
        "framing_fill_bias",
        "blur_strength",
        "background_opacity",
    )

    _STRING_OPTION_KEYS: Tuple[str, ...] = (
        "company_name",
        "company_subtext",
        "call_to_action",
        "call_to_action_subtext",
        "link",
        "company_font",
        "subtext_font",
        "subtitle_font",
        "outro_transition",
        "text_transition",
        "template_heading_font",
        "template_description_font",
        "template_text_align",
        "template_text_transition",
        "recovery_mode",
        "extension_method",
        "lingering_method",
        "bitrate",
    )

    _COLOR_OPTION_KEYS: Tuple[str, ...] = (
        "subtitle_color",
        "subtitle_bg_color",
        "outro_bg_color",
        "main_text_color",
        "sub_text_color",
        "cta_text_color",
        "cta_subtext_color",
        "cta_bg_color",
        "template_heading_color",
        "template_description_color",
        "template_bg_color",
    )

    _RENDER_OPTION_KEYS: Tuple[str, ...] = (
        *_BOOL_OPTION_KEYS,
        *_INT_OPTION_KEYS,
        *_FLOAT_OPTION_KEYS,
        *_STRING_OPTION_KEYS,
        *_COLOR_OPTION_KEYS,
        "watermark",
        "outro_logo_size",
    )

    _ALLOWED_EXTENSION_METHODS: Set[str] = {"freeze", "loop", "mirror"}
    _ALLOWED_TEMPLATE_TEXT_ALIGN: Set[str] = {"left", "center", "right"}
    _ALLOWED_RECOVERY_MODES: Set[str] = {"progressive", "aggressive", "minimal"}
    _OUTRO_LOGO_SIZE_COMPONENTS: int = 2

    def _collect_render_option_values(self, params: Dict[str, Any]) -> Dict[str, Any]:
        collected: Dict[str, Any] = {}
        for key in self._RENDER_OPTION_KEYS:
            if key in params and params[key] is not None:
                collected[key] = params[key]
        return collected

    def _apply_option_groups(self, data: Dict[str, Any], options: Dict[str, Any]) -> None:
        if not options:
            return

        assigned: Set[str] = set()

        for key in self._BOOL_OPTION_KEYS:
            if key in options:
                data[key] = bool(options[key])
                assigned.add(key)

        for key in self._INT_OPTION_KEYS:
            if key in options:
                data[key] = int(options[key])
                assigned.add(key)

        for key in self._FLOAT_OPTION_KEYS:
            if key in options:
                data[key] = float(options[key])
                assigned.add(key)

        for key in self._STRING_OPTION_KEYS:
            if key in options:
                data[key] = str(options[key])
                assigned.add(key)

        for key in self._COLOR_OPTION_KEYS:
            if key in options:
                data[key] = self._normalize_color(options[key])
                assigned.add(key)

        for key, value in options.items():
            if key not in assigned:
                data[key] = value

    def _validate_render_options(self, options: Dict[str, Any]) -> None:
        extension_method = options.get("extension_method")
        if extension_method is not None:
            normalized_extension = str(extension_method).lower()
            if normalized_extension not in self._ALLOWED_EXTENSION_METHODS:
                raise ValueError("extension_method must be 'freeze', 'loop', or 'mirror'")
            options["extension_method"] = normalized_extension

        template_align = options.get("template_text_align")
        if template_align is not None:
            normalized_align = str(template_align).lower()
            if normalized_align not in self._ALLOWED_TEMPLATE_TEXT_ALIGN:
                raise ValueError("template_text_align must be one of 'left', 'center', or 'right'")
            options["template_text_align"] = normalized_align

        recovery_mode = options.get("recovery_mode")
        if recovery_mode is not None:
            normalized_mode = str(recovery_mode).lower()
            if normalized_mode not in self._ALLOWED_RECOVERY_MODES:
                raise ValueError("recovery_mode must be 'progressive', 'aggressive', or 'minimal'")
            options["recovery_mode"] = normalized_mode

        subtitle_position = options.get("subtitle_position")
        if subtitle_position is not None:
            position_value = int(subtitle_position)
            if position_value < 0 or position_value > 4:
                raise ValueError("subtitle_position must be between 0 and 4")
            options["subtitle_position"] = position_value

        outro_logo_mode = options.get("outro_logo_mode")
        if outro_logo_mode is not None:
            mode_value = int(outro_logo_mode)
            if mode_value not in {0, 1, 2}:
                raise ValueError("outro_logo_mode must be 0, 1, or 2")
            options["outro_logo_mode"] = mode_value

        min_video_length = options.get("min_video_length")
        if min_video_length is not None:
            min_length = int(min_video_length)
            if min_length < 0:
                raise ValueError("min_video_length cannot be negative")
            options["min_video_length"] = min_length

        fallback_vo_length = options.get("fallback_vo_length")
        if fallback_vo_length is not None:
            fallback_length = int(fallback_vo_length)
            if fallback_length < 0:
                raise ValueError("fallback_vo_length cannot be negative")
            options["fallback_vo_length"] = fallback_length

        subtitle_font_size = options.get("subtitle_font_size")
        if subtitle_font_size is not None:
            font_size = int(subtitle_font_size)
            if font_size <= 0:
                raise ValueError("subtitle_font_size must be greater than zero")
            options["subtitle_font_size"] = font_size

        company_font_size = options.get("company_font_size")
        if company_font_size is not None:
            size_value = int(company_font_size)
            if size_value <= 0:
                raise ValueError("company_font_size must be greater than zero")
            options["company_font_size"] = size_value

        subtext_font_size = options.get("subtext_font_size")
        if subtext_font_size is not None:
            size_value = int(subtext_font_size)
            if size_value <= 0:
                raise ValueError("subtext_font_size must be greater than zero")
            options["subtext_font_size"] = size_value

        cta_company_font_size = options.get("cta_company_font_size")
        if cta_company_font_size is not None:
            size_value = int(cta_company_font_size)
            if size_value <= 0:
                raise ValueError("cta_company_font_size must be greater than zero")
            options["cta_company_font_size"] = size_value

        cta_subtext_font_size = options.get("cta_subtext_font_size")
        if cta_subtext_font_size is not None:
            size_value = int(cta_subtext_font_size)
            if size_value <= 0:
                raise ValueError("cta_subtext_font_size must be greater than zero")
            options["cta_subtext_font_size"] = size_value

        subtitle_bg_padding = options.get("subtitle_bg_padding")
        if subtitle_bg_padding is not None:
            padding_value = int(subtitle_bg_padding)
            if padding_value < 0:
                raise ValueError("subtitle_bg_padding cannot be negative")
            options["subtitle_bg_padding"] = padding_value

        subtitle_bg_corner_radius = options.get("subtitle_bg_corner_radius")
        if subtitle_bg_corner_radius is not None:
            radius_value = int(subtitle_bg_corner_radius)
            if radius_value < 0:
                raise ValueError("subtitle_bg_corner_radius cannot be negative")
            options["subtitle_bg_corner_radius"] = radius_value

        subtitle_squeeze_xp = options.get("subtitle_squeeze_xp")
        if subtitle_squeeze_xp is not None:
            squeeze_value = int(subtitle_squeeze_xp)
            if squeeze_value < 0:
                raise ValueError("subtitle_squeeze_xp cannot be negative")
            options["subtitle_squeeze_xp"] = squeeze_value

        subtitle_max_group_size = options.get("subtitle_max_group_size")
        if subtitle_max_group_size is not None:
            group_size = int(subtitle_max_group_size)
            if group_size <= 0:
                raise ValueError("subtitle_max_group_size must be greater than zero")
            options["subtitle_max_group_size"] = group_size

        fps_value = options.get("fps")
        if fps_value is not None:
            fps_int = int(fps_value)
            if fps_int <= 0:
                raise ValueError("fps must be greater than zero")
            options["fps"] = fps_int

        template_heading_font_size = options.get("template_heading_font_size")
        if template_heading_font_size is not None:
            size_value = int(template_heading_font_size)
            if size_value <= 0:
                raise ValueError("template_heading_font_size must be greater than zero")
            options["template_heading_font_size"] = size_value

        template_description_font_size = options.get("template_description_font_size")
        if template_description_font_size is not None:
            size_value = int(template_description_font_size)
            if size_value <= 0:
                raise ValueError("template_description_font_size must be greater than zero")
            options["template_description_font_size"] = size_value

        template_text_spacing = options.get("template_text_spacing")
        if template_text_spacing is not None:
            spacing_value = int(template_text_spacing)
            if spacing_value < 0:
                raise ValueError("template_text_spacing cannot be negative")
            options["template_text_spacing"] = spacing_value

        template_bg_corner_radius = options.get("template_bg_corner_radius")
        if template_bg_corner_radius is not None:
            radius_value = int(template_bg_corner_radius)
            if radius_value < 0:
                raise ValueError("template_bg_corner_radius cannot be negative")
            options["template_bg_corner_radius"] = radius_value

        max_retries = options.get("max_retries")
        if max_retries is not None:
            retries_value = int(max_retries)
            if retries_value < 0:
                raise ValueError("max_retries cannot be negative")
            options["max_retries"] = retries_value

        memory_threshold = options.get("memory_threshold")
        if memory_threshold is not None:
            threshold_value = int(memory_threshold)
            if threshold_value < 0 or threshold_value > 100:
                raise ValueError("memory_threshold must be between 0 and 100")
            options["memory_threshold"] = threshold_value

        subtitle_bg_opacity = options.get("subtitle_bg_opacity")
        if subtitle_bg_opacity is not None:
            opacity_value = float(subtitle_bg_opacity)
            if not 0.0 <= opacity_value <= 1.0:
                warnings.warn(f"subtitle_bg_opacity should be between 0.0 and 1.0, got {opacity_value}")
            options["subtitle_bg_opacity"] = opacity_value

        template_bg_opacity = options.get("template_bg_opacity")
        if template_bg_opacity is not None:
            opacity_value = float(template_bg_opacity)
            if not 0.0 <= opacity_value <= 1.0:
                warnings.warn(f"template_bg_opacity should be between 0.0 and 1.0, got {opacity_value}")
            options["template_bg_opacity"] = opacity_value

        background_opacity = options.get("background_opacity")
        if background_opacity is not None:
            opacity_value = float(background_opacity)
            if not 0.0 <= opacity_value <= 1.0:
                warnings.warn(f"background_opacity should be between 0.0 and 1.0, got {opacity_value}")
            options["background_opacity"] = opacity_value

        outro_duration = options.get("outro_duration")
        if outro_duration is not None:
            duration_value = float(outro_duration)
            if duration_value < 0:
                raise ValueError("outro_duration cannot be negative")
            options["outro_duration"] = duration_value

        transition_duration = options.get("transition_duration")
        if transition_duration is not None:
            duration_value = float(transition_duration)
            if duration_value < 0:
                raise ValueError("transition_duration cannot be negative")
            options["transition_duration"] = duration_value

        text_transition_delay = options.get("text_transition_delay")
        if text_transition_delay is not None:
            delay_value = float(text_transition_delay)
            if delay_value < 0:
                raise ValueError("text_transition_delay cannot be negative")
            options["text_transition_delay"] = delay_value

        text_transition_duration = options.get("text_transition_duration")
        if text_transition_duration is not None:
            duration_value = float(text_transition_duration)
            if duration_value < 0:
                raise ValueError("text_transition_duration cannot be negative")
            options["text_transition_duration"] = duration_value

        template_text_transition_delay = options.get("template_text_transition_delay")
        if template_text_transition_delay is not None:
            delay_value = float(template_text_transition_delay)
            if delay_value < 0:
                raise ValueError("template_text_transition_delay cannot be negative")
            options["template_text_transition_delay"] = delay_value

        template_text_transition_duration = options.get("template_text_transition_duration")
        if template_text_transition_duration is not None:
            duration_value = float(template_text_transition_duration)
            if duration_value < 0:
                raise ValueError("template_text_transition_duration cannot be negative")
            options["template_text_transition_duration"] = duration_value

        subtitle_bridge_threshold = options.get("subtitle_bridge_small_gaps_threshold")
        if subtitle_bridge_threshold is not None:
            threshold_value = float(subtitle_bridge_threshold)
            if threshold_value < 0:
                raise ValueError("subtitle_bridge_small_gaps_threshold cannot be negative")
            options["subtitle_bridge_small_gaps_threshold"] = threshold_value

        scene_threshold = options.get("scene_threshold")
        if scene_threshold is not None:
            threshold_value = float(scene_threshold)
            if threshold_value < 0:
                raise ValueError("scene_threshold cannot be negative")
            options["scene_threshold"] = threshold_value

        scene_min_duration = options.get("scene_min_scene_duration")
        if scene_min_duration is not None:
            duration_value = float(scene_min_duration)
            if duration_value < 0:
                raise ValueError("scene_min_scene_duration cannot be negative")
            options["scene_min_scene_duration"] = duration_value

        scene_min_gap = options.get("scene_min_scene_gap")
        if scene_min_gap is not None:
            gap_value = float(scene_min_gap)
            if gap_value < 0:
                raise ValueError("scene_min_scene_gap cannot be negative")
            options["scene_min_scene_gap"] = gap_value

        lingering_max_window = options.get("lingering_max_window")
        if lingering_max_window is not None:
            window_value = float(lingering_max_window)
            if window_value < 0:
                raise ValueError("lingering_max_window cannot be negative")
            options["lingering_max_window"] = window_value

        audio_lingering_max_window = options.get("audio_lingering_max_window")
        if audio_lingering_max_window is not None:
            window_value = float(audio_lingering_max_window)
            if window_value < 0:
                raise ValueError("audio_lingering_max_window cannot be negative")
            options["audio_lingering_max_window"] = window_value

        blur_strength = options.get("blur_strength")
        if blur_strength is not None:
            blur_value = float(blur_strength)
            if blur_value < 0:
                raise ValueError("blur_strength cannot be negative")
            options["blur_strength"] = blur_value

        lingering_method = options.get("lingering_method")
        if lingering_method is not None:
            normalized_method = str(lingering_method).lower()
            if normalized_method not in {"trim"}:
                warnings.warn(f"Unrecognized lingering_method '{lingering_method}', proceeding without validation of backend support")
            options["lingering_method"] = normalized_method

    def _apply_render_options(self, data: Dict[str, Any], options: Dict[str, Any]) -> None:
        if not options:
            return

        normalized_options = dict(options)
        outro_logo_size_value = normalized_options.pop("outro_logo_size", None)
        watermark_value = normalized_options.pop("watermark", None)

        self._validate_render_options(normalized_options)
        self._apply_option_groups(data, normalized_options)

        if outro_logo_size_value is not None:
            data["outro_logo_size"] = self._normalize_int_sequence(
                outro_logo_size_value,
                self._OUTRO_LOGO_SIZE_COMPONENTS,
                "outro_logo_size",
            )

        if watermark_value is not None:
            watermark_bool = bool(watermark_value)
            data["watermark"] = watermark_bool
            if "include_branding_outro" not in normalized_options:
                data.setdefault("include_branding_outro", watermark_bool)
    
    # Render Creation and Management
    
    def create_render(
        self,
        project_id: str,
        project_type: Optional[str] = None,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        standardize_resolution_enabled: Optional[bool] = None,
        bg_music_volume: Optional[float] = None,
        video_audio_volume: Optional[float] = None,
        voiceover_volume: Optional[float] = None,
        min_video_length: Optional[int] = None,
        fallback_vo_length: Optional[int] = None,
        subtitle_enabled: Optional[bool] = None,
        subtitle_font_size: Optional[int] = None,
        subtitle_font: Optional[str] = None,
        subtitle_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        subtitle_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        subtitle_bg_opacity: Optional[float] = None,
        subtitle_position: Optional[int] = None,
        subtitle_bg_padding: Optional[int] = None,
        subtitle_bg_rounded: Optional[bool] = None,
        subtitle_bg_corner_radius: Optional[int] = None,
        subtitle_squeeze_xp: Optional[int] = None,
        subtitle_max_group_size: Optional[int] = None,
        outro_duration: Optional[float] = None,
        outro_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        outro_logo_size: Optional[Union[List[int], Tuple[int, ...]]] = None,
        outro_logo_mode: Optional[int] = None,
        outro_transition: Optional[str] = None,
        outro_transition_duration: Optional[float] = None,
        company_name: Optional[str] = None,
        company_subtext: Optional[str] = None,
        call_to_action: Optional[str] = None,
        call_to_action_subtext: Optional[str] = None,
        link: Optional[str] = None,
        enable_cta: Optional[bool] = None,
        company_font: Optional[str] = None,
        company_font_size: Optional[int] = None,
        subtext_font: Optional[str] = None,
        subtext_font_size: Optional[int] = None,
        text_spacing: Optional[int] = None,
        logo_text_spacing: Optional[int] = None,
        main_text_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        sub_text_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        cta_text_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        cta_subtext_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        cta_company_font_size: Optional[int] = None,
        cta_subtext_font_size: Optional[int] = None,
        cta_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        text_transition: Optional[str] = None,
        text_transition_delay: Optional[float] = None,
        text_transition_duration: Optional[float] = None,
        template_heading_font_size: Optional[int] = None,
        template_heading_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        template_heading_font: Optional[str] = None,
        template_description_font_size: Optional[int] = None,
        template_description_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        template_description_font: Optional[str] = None,
        template_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        template_bg_opacity: Optional[float] = None,
        template_bg_rounded: Optional[bool] = None,
        template_bg_corner_radius: Optional[int] = None,
        template_text_spacing: Optional[int] = None,
        template_xp: Optional[int] = None,
        template_yp: Optional[int] = None,
        template_text_align: Optional[str] = None,
        template_text_transition: Optional[str] = None,
        template_text_transition_delay: Optional[float] = None,
        template_text_transition_duration: Optional[float] = None,
        color_balance_fix: Optional[bool] = None,
        color_exposure_fix: Optional[bool] = None,
        color_contrast_fix: Optional[bool] = None,
        image_slideshow: Optional[bool] = None,
        extend_short_clips: Optional[bool] = None,
        extension_method: Optional[str] = None,
        max_retries: Optional[int] = None,
        adaptive_complexity: Optional[bool] = None,
        enable_emergency_mode: Optional[bool] = None,
        memory_threshold: Optional[int] = None,
        recovery_mode: Optional[str] = None,
        include_outro: Optional[bool] = None,
        include_branding_outro: Optional[bool] = None,
        watermark: Optional[bool] = None,
        bitrate: Optional[str] = None,
        fps: Optional[int] = None,
        subtitle_bridge_small_gaps_threshold: Optional[float] = None,
        scene_threshold: Optional[float] = None,
        scene_min_scene_duration: Optional[float] = None,
        scene_min_scene_gap: Optional[float] = None,
        lingering_fix_enabled: Optional[bool] = None,
        lingering_method: Optional[str] = None,
        lingering_max_window: Optional[float] = None,
        audio_lingering_fix_enabled: Optional[bool] = None,
        audio_lingering_max_window: Optional[float] = None,
        allow_extend_last_clip: Optional[bool] = None,
        framing_fill_bias: Optional[float] = None,
        add_blurred_background: Optional[bool] = None,
        blur_strength: Optional[float] = None,
        background_opacity: Optional[float] = None,
    ) -> Dict:
        """Create a new render for a project using explicit render option bindings."""
        if not project_id:
            raise ValueError("project_id is required")
        if not isinstance(project_id, str):
            project_id = str(project_id)
            warnings.warn(f"project_id was converted to string: {project_id}")

        self._ensure_legacy_render_supported(project_id, project_type)

        local_params = dict(locals())
        data: Dict[str, Any] = {"project_id": project_id}

        if target_width is not None:
            width = int(target_width)
            if width <= 0:
                raise ValueError("target_width must be greater than zero")
            data["target_width"] = width

        if target_height is not None:
            height = int(target_height)
            if height <= 0:
                raise ValueError("target_height must be greater than zero")
            data["target_height"] = height

        for volume_key in ("bg_music_volume", "video_audio_volume", "voiceover_volume"):
            volume_value = local_params.get(volume_key)
            if volume_value is not None:
                data[volume_key] = self._validate_volume(volume_value)

        option_values = self._collect_render_option_values(local_params)
        self._apply_render_options(data, option_values)

        return self._make_request("POST", f"{self.render_url}/create", json_data=data)
    
    def get_render(
        self, 
        render_id: Optional[str] = None, 
        project_id: Optional[str] = None,
        include_results: bool = True, 
        include_sequence: bool = False,
        include_subtitles: bool = False, 
        generate_download_link: bool = False,
        generate_streamable_link: bool = False, 
        generate_thumbnail_stream_link: bool = False
    ) -> Dict:
        """
        Get details of a render by either render ID or project ID.
        
        Args:
            render_id: ID of the render to retrieve (either this or project_id must be provided)
            project_id: ID of the project to retrieve the render for (either this or render_id must be provided)
            include_results: Whether to include job results
            include_sequence: Whether to include the full sequence data
            include_subtitles: Whether to include subtitles data
            generate_download_link: Whether to generate a temporary download link
            generate_streamable_link: Whether to generate a temporary streamable link
            generate_thumbnail_stream_link: Whether to generate a thumbnail streamable link
            
        Returns:
            Dictionary with render details
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")
            
        params = {
            "include_results": str(include_results).lower(),
            "include_sequence": str(include_sequence).lower(),
            "include_subtitles": str(include_subtitles).lower(),
            "generate_download_link": str(generate_download_link).lower(),
            "generate_streamable_link": str(generate_streamable_link).lower(),
            "generate_thumbnail_stream_link": str(generate_thumbnail_stream_link).lower()
        }
        
        if render_id:
            params["render_id"] = render_id
        if project_id:
            params["project_id"] = project_id
            
        return self._make_request("GET", f"{self.render_url}/get", params=params)
    
    def redo_render(
        self,
        render_id: Optional[str] = None,
        project_id: Optional[str] = None,
        project_type: Optional[str] = None,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        standardize_resolution_enabled: Optional[bool] = None,
        bg_music_volume: Optional[float] = None,
        video_audio_volume: Optional[float] = None,
        voiceover_volume: Optional[float] = None,
        min_video_length: Optional[int] = None,
        fallback_vo_length: Optional[int] = None,
        subtitle_enabled: Optional[bool] = None,
        subtitle_font_size: Optional[int] = None,
        subtitle_font: Optional[str] = None,
        subtitle_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        subtitle_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        subtitle_bg_opacity: Optional[float] = None,
        subtitle_position: Optional[int] = None,
        subtitle_bg_padding: Optional[int] = None,
        subtitle_bg_rounded: Optional[bool] = None,
        subtitle_bg_corner_radius: Optional[int] = None,
        subtitle_squeeze_xp: Optional[int] = None,
        subtitle_max_group_size: Optional[int] = None,
        outro_duration: Optional[float] = None,
        outro_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        outro_logo_size: Optional[Union[List[int], Tuple[int, ...]]] = None,
        outro_logo_mode: Optional[int] = None,
        outro_transition: Optional[str] = None,
        outro_transition_duration: Optional[float] = None,
        company_name: Optional[str] = None,
        company_subtext: Optional[str] = None,
        call_to_action: Optional[str] = None,
        call_to_action_subtext: Optional[str] = None,
        link: Optional[str] = None,
        enable_cta: Optional[bool] = None,
        company_font: Optional[str] = None,
        company_font_size: Optional[int] = None,
        subtext_font: Optional[str] = None,
        subtext_font_size: Optional[int] = None,
        text_spacing: Optional[int] = None,
        logo_text_spacing: Optional[int] = None,
        main_text_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        sub_text_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        cta_text_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        cta_subtext_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        cta_company_font_size: Optional[int] = None,
        cta_subtext_font_size: Optional[int] = None,
        cta_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        text_transition: Optional[str] = None,
        text_transition_delay: Optional[float] = None,
        text_transition_duration: Optional[float] = None,
        template_heading_font_size: Optional[int] = None,
        template_heading_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        template_heading_font: Optional[str] = None,
        template_description_font_size: Optional[int] = None,
        template_description_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        template_description_font: Optional[str] = None,
        template_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        template_bg_opacity: Optional[float] = None,
        template_bg_rounded: Optional[bool] = None,
        template_bg_corner_radius: Optional[int] = None,
        template_text_spacing: Optional[int] = None,
        template_xp: Optional[int] = None,
        template_yp: Optional[int] = None,
        template_text_align: Optional[str] = None,
        template_text_transition: Optional[str] = None,
        template_text_transition_delay: Optional[float] = None,
        template_text_transition_duration: Optional[float] = None,
        color_balance_fix: Optional[bool] = None,
        color_exposure_fix: Optional[bool] = None,
        color_contrast_fix: Optional[bool] = None,
        image_slideshow: Optional[bool] = None,
        extend_short_clips: Optional[bool] = None,
        extension_method: Optional[str] = None,
        max_retries: Optional[int] = None,
        adaptive_complexity: Optional[bool] = None,
        enable_emergency_mode: Optional[bool] = None,
        memory_threshold: Optional[int] = None,
        recovery_mode: Optional[str] = None,
        include_outro: Optional[bool] = None,
        include_branding_outro: Optional[bool] = None,
        watermark: Optional[bool] = None,
        bitrate: Optional[str] = None,
        fps: Optional[int] = None,
        subtitle_bridge_small_gaps_threshold: Optional[float] = None,
        scene_threshold: Optional[float] = None,
        scene_min_scene_duration: Optional[float] = None,
        scene_min_scene_gap: Optional[float] = None,
        lingering_fix_enabled: Optional[bool] = None,
        lingering_method: Optional[str] = None,
        lingering_max_window: Optional[float] = None,
        audio_lingering_fix_enabled: Optional[bool] = None,
        audio_lingering_max_window: Optional[float] = None,
        allow_extend_last_clip: Optional[bool] = None,
        framing_fill_bias: Optional[float] = None,
        add_blurred_background: Optional[bool] = None,
        blur_strength: Optional[float] = None,
        background_opacity: Optional[float] = None,
    ) -> Dict:
        """Redo an existing render with optional overrides."""
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")

        if render_id and not isinstance(render_id, str):
            render_id = str(render_id)
            warnings.warn(f"render_id was converted to string: {render_id}")
        if project_id and not isinstance(project_id, str):
            project_id = str(project_id)
            warnings.warn(f"project_id was converted to string: {project_id}")

        resolved_project_id = project_id
        if project_id:
            self._ensure_legacy_render_supported(project_id, project_type)
        else:
            resolved_project_id = self._resolve_project_id_from_render(render_id)
            self._ensure_legacy_render_supported(resolved_project_id, project_type)
            project_id = resolved_project_id

        local_params = dict(locals())
        data: Dict[str, Any] = {}
        if render_id:
            data["render_id"] = render_id
        if project_id:
            data["project_id"] = project_id

        if target_width is not None:
            width = int(target_width)
            if width <= 0:
                raise ValueError("target_width must be greater than zero")
            data["target_width"] = width

        if target_height is not None:
            height = int(target_height)
            if height <= 0:
                raise ValueError("target_height must be greater than zero")
            data["target_height"] = height

        for volume_key in ("bg_music_volume", "video_audio_volume", "voiceover_volume"):
            volume_value = local_params.get(volume_key)
            if volume_value is not None:
                data[volume_key] = self._validate_volume(volume_value)

        option_values = self._collect_render_option_values(local_params)
        self._apply_render_options(data, option_values)

        return self._make_request("POST", f"{self.render_url}/redo", json_data=data)
    
    def update_render_settings(
        self,
        render_id: Optional[str] = None,
        project_id: Optional[str] = None,
        bg_music_volume: Optional[float] = None,
        video_audio_volume: Optional[float] = None,
        voiceover_volume: Optional[float] = None,
        subtitle_enabled: Optional[bool] = None,
        subtitle_font_size: Optional[int] = None,
        subtitle_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        subtitle_bg_color: Optional[Union[str, List[int], Tuple[int, ...]]] = None,
        subtitle_bg_opacity: Optional[float] = None,
        outro_duration: Optional[float] = None,
        company_name: Optional[str] = None,
        company_subtext: Optional[str] = None,
        call_to_action: Optional[str] = None,
        call_to_action_subtext: Optional[str] = None,
        enable_cta: Optional[bool] = None,
        color_balance_fix: Optional[bool] = None,
        color_exposure_fix: Optional[bool] = None,
        color_contrast_fix: Optional[bool] = None,
        **kwargs
    ) -> Dict:
        """
        Update render settings without regenerating.
        
        Args:
            render_id: ID of the render to update (either this or project_id must be provided)
            project_id: ID of the project whose render to update (either this or render_id must be provided)
            bg_music_volume: New background music volume (0.0 to 1.0)
            video_audio_volume: New video audio volume (0.0 to 1.0)
            voiceover_volume: New voiceover volume (0.0 to 1.0)
            subtitle_enabled: Whether to enable subtitles
            subtitle_font_size: New subtitle text size
            subtitle_color: New subtitle text color (RGB tuple/list or hex string)
            subtitle_bg_color: New subtitle background color (RGB tuple/list or hex string)
            subtitle_bg_opacity: New subtitle background opacity (0.0 to 1.0)
            outro_duration: New duration of the outro in seconds
            company_name: New company name for the outro
            company_subtext: New company tagline for the outro
            call_to_action: New CTA text
            call_to_action_subtext: New CTA subtext
            enable_cta: Whether to show CTA
            color_balance_fix: Whether to apply color balance correction
            color_exposure_fix: Whether to apply exposure correction
            color_contrast_fix: Whether to apply contrast correction
            **kwargs: Additional parameters to update
            
        Returns:
            Dictionary with update confirmation
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")

        project_type_hint = kwargs.pop('project_type', None)

        if render_id and not isinstance(render_id, str):
            render_id = str(render_id)
            warnings.warn(f"render_id was converted to string: {render_id}")
        if project_id and not isinstance(project_id, str):
            project_id = str(project_id)
            warnings.warn(f"project_id was converted to string: {project_id}")

        resolved_project_id = project_id
        if project_id:
            self._ensure_legacy_render_supported(project_id, project_type_hint)
        elif render_id:
            resolved_project_id = self._resolve_project_id_from_render(render_id)
            self._ensure_legacy_render_supported(resolved_project_id, project_type_hint)
            project_id = resolved_project_id
            
        data = {}
        
        if render_id:
            data["render_id"] = render_id
        if project_id:
            data["project_id"] = project_id
            
        # Process specific parameters with validation
        # Volume parameters
        if bg_music_volume is not None:
            data["bg_music_volume"] = self._validate_volume(bg_music_volume)
            
        if video_audio_volume is not None:
            data["video_audio_volume"] = self._validate_volume(video_audio_volume)
            
        if voiceover_volume is not None:
            data["voiceover_volume"] = self._validate_volume(voiceover_volume)
        
        # Boolean parameters
        for param_name, param_value in [
            ("subtitle_enabled", subtitle_enabled),
            ("enable_cta", enable_cta),
            ("color_balance_fix", color_balance_fix),
            ("color_exposure_fix", color_exposure_fix),
            ("color_contrast_fix", color_contrast_fix)
        ]:
            if param_value is not None:
                data[param_name] = bool(param_value)
        
        # Color parameters
        if subtitle_color is not None:
            data["subtitle_color"] = self._normalize_color(subtitle_color)
            
        if subtitle_bg_color is not None:
            data["subtitle_bg_color"] = self._normalize_color(subtitle_bg_color)
        
        # Other numeric parameters
        if subtitle_font_size is not None:
            data["subtitle_font_size"] = int(subtitle_font_size)
            
        if subtitle_bg_opacity is not None:
            if not 0.0 <= subtitle_bg_opacity <= 1.0:
                warnings.warn(f"subtitle_bg_opacity should be between 0.0 and 1.0, got {subtitle_bg_opacity}")
            data["subtitle_bg_opacity"] = float(subtitle_bg_opacity)
            
        if outro_duration is not None:
            if outro_duration < 0:
                raise ValueError("outro_duration cannot be negative")
            data["outro_duration"] = float(outro_duration)
        
        # String parameters
        for param_name, param_value in [
            ("company_name", company_name),
            ("company_subtext", company_subtext),
            ("call_to_action", call_to_action),
            ("call_to_action_subtext", call_to_action_subtext)
        ]:
            if param_value is not None:
                data[param_name] = str(param_value)
        
        # Add any additional settings from kwargs
        for key, value in kwargs.items():
            if key not in ["render_id", "project_id"]:
                data[key] = value
                
        # Make sure at least one setting is being updated
        if len(data) <= 1:  # Only has ID, no actual updates
            raise ValueError("At least one setting must be provided to update")
            
        return self._make_request("PUT", f"{self.render_url}/update", json_data=data)
    
    def update_render(
        self,
        render_id: Optional[str] = None,
        project_id: Optional[str] = None,
        fields_to_update: Optional[List[str]] = None,
        project_type: Optional[str] = None
    ) -> Dict:
        """
        Update a render with the latest sequence data from its source project.
        
        This method pulls the latest data from upstream sources (sequence, brand settings, 
        company details) and updates the render record accordingly.
        
        Args:
            render_id: ID of the render to update (either this or project_id must be provided)
            project_id: ID of the project whose render to update (either this or render_id must be provided)
            fields_to_update: Optional list of specific fields to update from the source data
            
        Returns:
            Dictionary with update confirmation
        """
        if not render_id and not project_id:
            raise ValueError("Either render_id or project_id must be provided")
            
        if render_id and not isinstance(render_id, str):
            render_id = str(render_id)
            warnings.warn(f"render_id was converted to string: {render_id}")
        if project_id and not isinstance(project_id, str):
            project_id = str(project_id)
            warnings.warn(f"project_id was converted to string: {project_id}")

        resolved_project_id = project_id
        if project_id:
            self._ensure_legacy_render_supported(project_id, project_type)
        elif render_id:
            resolved_project_id = self._resolve_project_id_from_render(render_id)
            self._ensure_legacy_render_supported(resolved_project_id, project_type)
            project_id = resolved_project_id

        data = {}
        
        if render_id:
            data["render_id"] = render_id
        if project_id:
            data["project_id"] = project_id
        if fields_to_update:
            if not isinstance(fields_to_update, list):
                raise TypeError("fields_to_update must be a list of strings")
            data["fields_to_update"] = fields_to_update
            
        return self._make_request("PUT", f"{self.render_url}/selfupdate", json_data=data)
    
    def get_render_status(
        self,
        render_id: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> Dict:
        """
        Get the current status of a render job.
        
        This is a convenience method that provides a simplified view of the render status.
        
        Args:
            render_id: ID of the render to check (either this or project_id must be provided)
            project_id: ID of the project whose render to check (either this or render_id must be provided)
            
        Returns:
            Dictionary with render status information including:
            - render_id: The ID of the render
            - project_id: The ID of the associated project
            - status: Current status (PENDING, PROCESSING, COMPLETED, FAILED, or UNKNOWN)
            - created_at: When the render was created
            - updated_at: When the render was last updated
            - is_stale: Whether the render settings have been changed since the last render
        """
        result = self.get_render(render_id, project_id, include_results=True, 
                               include_sequence=False, include_subtitles=False)
        
        # Extract status information for a cleaner response
        status = "UNKNOWN"
        job_result = result.get("job_result", {})
        
        if job_result:
            status = job_result.get("status", "UNKNOWN")
            
        return {
            "render_id": result.get("render_id"),
            "project_id": result.get("project_id"),
            "status": status,
            "created_at": result.get("created_at"),
            "updated_at": result.get("updated_at"),
            "is_stale": result.get("is_stale", False),
            "job_id": result.get("job_id")
        }
    
    def get_render_download_links(
        self,
        render_id: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> Dict:
        """
        Get download and streaming links for a completed render.
        
        This is a convenience method that provides all available download links
        for the rendered video, thumbnail, and subtitles.
        
        Args:
            render_id: ID of the render (either this or project_id must be provided)
            project_id: ID of the project whose render to access (either this or render_id must be provided)
            
        Returns:
            Dictionary with download and streaming URLs:
            - download_url: Direct download link for the rendered video
            - streamable_url: Link for streaming the video
            - thumbnail_streamable_url: Link for the video thumbnail
            - srt_download_url: Link for the SRT subtitle file
            
        Raises:
            Exception: If the render is not yet complete
        """
        result = self.get_render(
            render_id, project_id, 
            include_results=True,
            generate_download_link=True, 
            generate_streamable_link=True, 
            generate_thumbnail_stream_link=True
        )
        
        # Check if render is complete
        job_result = result.get("job_result", {})
        if job_result.get("status") != "COMPLETED":
            raise Exception(f"Render is not yet complete. Current status: {job_result.get('status', 'UNKNOWN')}")
            
        # Extract and return just the links
        links = {
            "render_id": result.get("render_id"),
            "project_id": result.get("project_id"),
            "download_url": result.get("download_url"),
            "download_expires_in": result.get("download_expires_in"),
            "streamable_url": result.get("streamable_url"),
            "streamable_expires_in": result.get("streamable_expires_in"),
            "thumbnail_streamable_url": result.get("thumbnail_streamable_url"),
            "thumbnail_streamable_expires_in": result.get("thumbnail_streamable_expires_in"),
            "srt_download_url": result.get("srt_download_url"),
            "srt_download_expires_in": result.get("srt_download_expires_in")
        }
        
        return links
        
    # Advanced workflows
    
    def create_and_wait_for_render(
        self,
        project_id: str,
        poll_interval: int = 5,
        timeout: int = 3600,
        auto_generate_links: bool = True,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Create a render and wait for it to complete.
        
        This is a convenience workflow that:
        1. Creates a new render
        2. Polls the status until completion or timeout
        3. Returns the final result with download links
        
        Args:
            project_id: ID of the project to render
            poll_interval: How often to check status (in seconds)
            timeout: Maximum time to wait (in seconds)
            auto_generate_links: Whether to automatically generate download links on completion
            **kwargs: Additional parameters for create_render
            
        Returns:
            Dictionary with render details and results
            
        Raises:
            TimeoutError: If the render doesn't complete within the timeout period
            Exception: If the render fails
        """
        # Create the render
        create_kwargs = dict(kwargs)
        if project_type is not None:
            create_kwargs['project_type'] = project_type
        result = self.create_render(project_id=project_id, **create_kwargs)
        render_id = result.get("render", {}).get("render_id")
        
        if not render_id:
            raise ValueError("Failed to get render_id from response")
        
        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < timeout:
            status_result = self.get_render_status(render_id=render_id)
            status = status_result.get("status", "UNKNOWN")
            
            if status == "COMPLETED":
                if auto_generate_links:
                    return self.get_render(
                        render_id=render_id,
                        include_results=True,
                        generate_download_link=True,
                        generate_streamable_link=True,
                        generate_thumbnail_stream_link=True
                    )
                else:
                    return self.get_render(render_id=render_id, include_results=True)
            elif status == "FAILED":
                details = self.get_render(render_id=render_id, include_results=True)
                error_message = details.get("job_result", {}).get("error", "Unknown error")
                raise Exception(f"Render failed: {error_message}")
            
            print(f"Render status: {status}. Waiting {poll_interval} seconds...")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Render did not complete within the timeout of {timeout} seconds")
    
    def update_settings_and_redo(
        self,
        render_id: Optional[str] = None,
        project_id: Optional[str] = None,
        wait_for_completion: bool = False,
        poll_interval: int = 5,
        timeout: int = 3600,
        project_type: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Update render settings and immediately redo the render.
        
        This is a convenience workflow that:
        1. Updates render settings
        2. Redoes the render with updated settings
        3. Optionally waits for completion
        
        Args:
            render_id: ID of the render to update and redo
            project_id: ID of the project whose render to update and redo
            wait_for_completion: Whether to wait for the render to complete
            poll_interval: How often to check status (in seconds) if waiting
            timeout: Maximum time to wait (in seconds) if waiting
            **kwargs: Settings to update
            
        Returns:
            Dictionary with render details and optionally results if waiting
            
        Raises:
            TimeoutError: If waiting and the render doesn't complete within timeout
            Exception: If waiting and the render fails
        """
        # Update settings
        settings_kwargs = dict(kwargs)
        if project_type is not None:
            settings_kwargs['project_type'] = project_type
        self.update_render_settings(render_id=render_id, project_id=project_id, **settings_kwargs)
        
        # Redo render
        redo_kwargs: Dict[str, Any] = {}
        if project_type is not None:
            redo_kwargs['project_type'] = project_type
        result = self.redo_render(render_id=render_id, project_id=project_id, **redo_kwargs)
        new_job_id = result.get("job_id")
        render_id = result.get("render_id")
        
        if wait_for_completion:
            # Poll for completion
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_result = self.get_render_status(render_id=render_id)
                status = status_result.get("status", "UNKNOWN")
                
                if status == "COMPLETED":
                    return self.get_render(
                        render_id=render_id,
                        include_results=True,
                        generate_download_link=True,
                        generate_streamable_link=True,
                        generate_thumbnail_stream_link=True
                    )
                elif status == "FAILED":
                    details = self.get_render(render_id=render_id, include_results=True)
                    error_message = details.get("job_result", {}).get("error", "Unknown error")
                    raise Exception(f"Render failed: {error_message}")
                
                print(f"Render status: {status}. Waiting {poll_interval} seconds...")
                time.sleep(poll_interval)
                
            raise TimeoutError(f"Render did not complete within the timeout of {timeout} seconds")
        
        return result
