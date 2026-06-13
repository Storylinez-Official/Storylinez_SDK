"""Centralized validation and configuration helpers for the Storylinez SDK."""

from typing import Dict, List, Optional

# Engine configurations - matches SERVER config.config
# Only two engines are supported: bolt (fast) and weave (multi-step)
ALLOWED_ENGINES = [
    'bolt',   # Fast, direct, single LLM call (DEFAULT)
    'weave'   # Multi-step, threaded pipeline
]

DEFAULT_ENGINE = 'bolt'

# Model alias configurations - matches server-side public alias allowlists.
# These are Storylinez branded model aliases that map to underlying LLM models.
ALLOWED_MODELS = {
    # V1 creative-gen endpoints (prompt/storyboard/sequence)
    'narrative_v1': [
        'storylinez-1-reasoning-fast',
        'storylinez-1-reasoning',
        'storylinez-1-reasoning-high',
        'storylinez-1-quasar',
        'storylinez-1-lumina',
        'storylinez-1-nebula',
        'storylinez-1-nebula-fast',
        'storylinez-1-muse',
        'storylinez-1-muse-pro',
    ],
    # V2 agent/sequence endpoints (session-based)
    'narrative_v2': [
        'storylinez-1-reasoning-fast',
        'storylinez-1-reasoning',
        'storylinez-1-reasoning-high',
        'storylinez-1-quasar',
        'storylinez-1-lumina',
        'storylinez-1-nebula',
        'storylinez-1-nebula-fast',
        'storylinez-1-muse',
        'storylinez-1-muse-pro',
        'auto'
    ],
    # Backward-compat convenience: treat legacy 'narrative' as union.
    'narrative': [
        'storylinez-1-reasoning-fast',
        'storylinez-1-reasoning',
        'storylinez-1-reasoning-high',
        'storylinez-1-quasar',
        'storylinez-1-lumina',
        'storylinez-1-nebula',
        'storylinez-1-nebula-fast',
        'storylinez-1-muse',
        'storylinez-1-muse-pro',
        'auto'
    ],
    'analysis': [
        'storylinez-1-reasoning-fast',
        'storylinez-1-reasoning',
        'storylinez-1-quasar',
        'auto'
    ]
}

# Media format configurations - mirrors server-side validation for uploads and prompts
ALLOWED_MEDIA_FORMATS: Dict[str, List[str]] = {
    'VIDEO': [
        'mp4', 'mov', 'mkv', 'webm', 'm4v', 'flv', 'wmv', 'mpg', 'mpeg', 'ts', 'm2ts',
        '3gp', 'asf'
    ],
    'AUDIO': [
        'mp3', 'wav', 'ogg', 'flac', 'm4a', 'opus', 'wma', 'ac3', 'aiff', 'mp2', 'au'
    ],
    'IMAGE': [
        'jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff', 'tif'
    ]
}


def get_allowed_engines() -> List[str]:
    """
    Get list of allowed engine names.
    
    Returns:
        List of allowed engine names
    """
    return ALLOWED_ENGINES.copy()


def get_default_engine() -> str:
    """
    Get default engine name.
    
    Returns:
        Default engine name
    """
    return DEFAULT_ENGINE


def is_valid_engine(engine: str) -> bool:
    """
    Check if engine name is valid.
    
    Args:
        engine: Engine name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(engine, str):
        return False
    return engine.strip().lower() in ALLOWED_ENGINES


def normalize_engine(engine: Optional[str]) -> str:
    """
    Normalize engine name to lowercase or return default.
    
    Args:
        engine: Optional engine name
        
    Returns:
        Normalized engine name or default
        
    Raises:
        ValueError: If engine is invalid
    """
    if engine is None:
        return DEFAULT_ENGINE
    
    if not isinstance(engine, str):
        raise ValueError(f"engine must be a string, allowed engines: {ALLOWED_ENGINES}")
    
    normalized = engine.strip().lower()
    if normalized not in ALLOWED_ENGINES:
        raise ValueError(f"Invalid engine '{engine}', allowed engines: {ALLOWED_ENGINES}")
    
    return normalized


def get_allowed_models(domain: str = 'narrative_v1') -> List[str]:
    """
    Get list of allowed model aliases for a domain.
    
    Args:
        domain: Domain name ('narrative_v1', 'narrative_v2', 'narrative', or 'analysis')
        
    Returns:
        List of allowed model aliases for the domain
    """
    domain_key = (domain or 'narrative_v1').lower()
    return ALLOWED_MODELS.get(domain_key, ALLOWED_MODELS['narrative_v1']).copy()


def is_valid_model(model: str, domain: str = 'narrative_v1') -> bool:
    """
    Check if model alias is valid for a domain.
    
    Args:
        model: Model alias to validate
        domain: Domain name ('narrative_v1', 'narrative_v2', 'narrative', or 'analysis')
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(model, str):
        return False
    
    domain_key = (domain or 'narrative_v1').lower()
    allowed = ALLOWED_MODELS.get(domain_key, ALLOWED_MODELS['narrative_v1'])
    return model.strip().lower() in [m.lower() for m in allowed]


def normalize_model(model: Optional[str], domain: str = 'narrative_v1') -> Optional[str]:
    """
    Normalize model alias to lowercase format.
    
    Args:
        model: Optional model alias
        domain: Domain name ('narrative_v1', 'narrative_v2', 'narrative', or 'analysis')
        
    Returns:
        Normalized model alias or None
        
    Raises:
        ValueError: If model is invalid
    """
    if model is None:
        return None
    
    if not isinstance(model, str):
        raise ValueError(f"model must be a string, allowed models for {domain}: {get_allowed_models(domain)}")
    
    normalized = model.strip().lower()
    
    # 'auto' is always valid
    if normalized == 'auto':
        return 'auto'
    
    # Find case-insensitive match
    domain_key = (domain or 'narrative_v1').lower()
    allowed = ALLOWED_MODELS.get(domain_key, ALLOWED_MODELS['narrative_v1'])
    for allowed_model in allowed:
        if allowed_model.lower() == normalized:
            return allowed_model.lower()
    
    raise ValueError(f"Invalid model '{model}' for domain '{domain}', allowed models: {allowed}")


def validate_eco_model_conflict(eco: bool, model: Optional[str], domain: str = 'narrative_v1') -> None:
    """
    Validate that eco mode is not used with custom models.
    
    Args:
        eco: Whether eco mode is enabled
        model: Optional model override
        domain: Domain of the model aliases for error messaging
        
    Raises:
        ValueError: If eco mode is enabled with a custom model
    """
    if eco and model and model != 'auto':
        domain_key = (domain or 'narrative_v1').lower()
        raise ValueError(
            f"eco mode cannot be used with custom models. "
            f"Either disable eco or remove model override. "
            f"Allowed models for {domain_key} domain: {get_allowed_models(domain_key)}"
        )


def get_allowed_media_formats() -> Dict[str, List[str]]:
    """Return a copy of the allowed media format mapping."""
    return {media_type: extensions.copy() for media_type, extensions in ALLOWED_MEDIA_FORMATS.items()}


def get_allowed_media_extensions(media_type: str) -> List[str]:
    """Return allowed extensions for a specific media type."""
    if not isinstance(media_type, str):
        raise ValueError("media_type must be a string")
    normalized = media_type.strip().upper()
    if normalized not in ALLOWED_MEDIA_FORMATS:
        allowed_types = ", ".join(sorted(ALLOWED_MEDIA_FORMATS))
        raise ValueError(f"Unknown media type '{media_type}'. Allowed types: {allowed_types}")
    return ALLOWED_MEDIA_FORMATS[normalized].copy()


def get_all_media_extensions() -> List[str]:
    """Return a flattened list of all supported media extensions."""
    extensions: List[str] = []
    for group in ALLOWED_MEDIA_FORMATS.values():
        extensions.extend(group)
    return sorted(set(extensions))


def validate_media_extension(filename: str, media_type: Optional[str] = None) -> str:
    """Validate filename extension optionally constrained by media type."""
    if not isinstance(filename, str) or not filename:
        raise ValueError("filename must be a non-empty string")

    extension = filename.strip().lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if not extension:
        raise ValueError(f"Filename '{filename}' has no extension")

    if media_type:
        allowed = get_allowed_media_extensions(media_type)
        if extension not in allowed:
            raise ValueError(
                f"File extension '{extension}' is not supported for {media_type.upper()}. "
                f"Valid extensions are: {', '.join(allowed)}"
            )
    else:
        allowed = get_all_media_extensions()
        if extension not in allowed:
            raise ValueError(
                f"File extension '{extension}' is not supported. "
                f"Valid extensions are: {', '.join(allowed)}"
            )

    return extension
