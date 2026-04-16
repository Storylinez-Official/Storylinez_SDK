from typing import Dict, List, Optional

from .base_client import BaseClient


class VoiceLibraryClient(BaseClient):
    """Client for /voice-library endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._voice_library_url = f"{self.base_url}/voice-library"

    # ------------------------------
    # System voices
    # ------------------------------

    def list_voices(
        self,
        *,
        query: Optional[str] = None,
        category: Optional[str] = None,
        gender: Optional[str] = None,
        accent: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
        include_audio_url: bool = True,
    ) -> Dict:
        """List system voices with optional filters."""
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be within 1..100")

        params = {
            "page": page,
            "limit": limit,
            "include_audio_url": str(bool(include_audio_url)).lower(),
        }
        if query is not None:
            params["query"] = query
        if category is not None:
            params["category"] = category
        if gender is not None:
            params["gender"] = gender
        if accent is not None:
            params["accent"] = accent

        return self._make_request("GET", f"{self._voice_library_url}/voices", params=params)

    def get_voice(self, voice_id: str, *, include_audio_url: bool = True) -> Dict:
        """Get one system voice by voice_id."""
        if not voice_id:
            raise ValueError("voice_id is required")

        params = {
            "include_audio_url": str(bool(include_audio_url)).lower(),
        }
        return self._make_request("GET", f"{self._voice_library_url}/voices/{voice_id}", params=params)

    def list_categories(self) -> Dict:
        """List system voice categories."""
        return self._make_request("GET", f"{self._voice_library_url}/categories")

    # ------------------------------
    # User voices
    # ------------------------------

    def create_upload_link(self, filename: str, file_size: int, org_id: Optional[str] = None) -> Dict:
        """Create upload link for a user voice sample."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not filename:
            raise ValueError("filename is required")
        if file_size <= 0:
            raise ValueError("file_size must be > 0")

        params = {
            "org_id": org,
            "filename": filename,
            "file_size": file_size,
        }
        return self._make_request("GET", f"{self._voice_library_url}/user-voices/upload/create_link", params=params)

    def create_user_voice(
        self,
        name: str,
        upload_id: str,
        duration: float,
        org_id: Optional[str] = None,
        *,
        description: Optional[str] = None,
        gender: Optional[str] = None,
        accent: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict:
        """Create a user voice sample from an uploaded audio file."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not name:
            raise ValueError("name is required")
        if not upload_id:
            raise ValueError("upload_id is required")

        payload = {
            "org_id": org,
            "name": name,
            "upload_id": upload_id,
            "duration": duration,
        }
        if description is not None:
            payload["description"] = description
        if gender is not None:
            payload["gender"] = gender
        if accent is not None:
            payload["accent"] = accent
        if tags is not None:
            payload["tags"] = tags

        return self._make_request("POST", f"{self._voice_library_url}/user-voices", json_data=payload)

    def get_user_voice_job(self, job_id: str) -> Dict:
        """Get user voice preprocess job status."""
        if not job_id:
            raise ValueError("job_id is required")
        return self._make_request("GET", f"{self._voice_library_url}/user-voices/jobs/{job_id}")

    def list_user_voices(
        self,
        org_id: Optional[str] = None,
        *,
        search: Optional[str] = None,
        gender: Optional[str] = None,
        accent: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        limit: int = 50,
    ) -> Dict:
        """List user voices for an organization."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be within 1..100")

        params = {
            "org_id": org,
            "page": page,
            "limit": limit,
        }
        if search is not None:
            params["search"] = search
        if gender is not None:
            params["gender"] = gender
        if accent is not None:
            params["accent"] = accent
        if tags:
            params["tags"] = ",".join([str(tag) for tag in tags])

        return self._make_request("GET", f"{self._voice_library_url}/user-voices", params=params)

    def get_user_voice(self, voice_id: str) -> Dict:
        """Get one user voice by voice_id."""
        if not voice_id:
            raise ValueError("voice_id is required")
        return self._make_request("GET", f"{self._voice_library_url}/user-voices/{voice_id}")

    def update_user_voice(
        self,
        voice_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        gender: Optional[str] = None,
        accent: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict:
        """Update user voice metadata."""
        if not voice_id:
            raise ValueError("voice_id is required")

        payload: Dict = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if gender is not None:
            payload["gender"] = gender
        if accent is not None:
            payload["accent"] = accent
        if tags is not None:
            payload["tags"] = tags

        if not payload:
            raise ValueError("At least one field must be provided for update_user_voice")

        return self._make_request("PUT", f"{self._voice_library_url}/user-voices/{voice_id}", json_data=payload)

    def delete_user_voice(self, voice_id: str) -> Dict:
        """Delete a user voice sample."""
        if not voice_id:
            raise ValueError("voice_id is required")
        return self._make_request("DELETE", f"{self._voice_library_url}/user-voices/{voice_id}")

    # ------------------------------
    # TTS generation
    # ------------------------------

    def generate_tts(
        self,
        text: str,
        org_id: Optional[str] = None,
        *,
        voice_id: Optional[str] = None,
        voice_source: Optional[str] = None,
        voice_s3_key: Optional[str] = None,
        exaggeration: Optional[float] = None,
        cfg_weight: Optional[float] = None,
        temperature: Optional[float] = None,
    ) -> Dict:
        """Start single-speaker TTS generation."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not text:
            raise ValueError("text is required")

        payload = {
            "org_id": org,
            "text": text,
        }
        if voice_id is not None:
            payload["voice_id"] = voice_id
        if voice_source is not None:
            payload["voice_source"] = voice_source
        if voice_s3_key is not None:
            payload["voice_s3_key"] = voice_s3_key
        if exaggeration is not None:
            payload["exaggeration"] = exaggeration
        if cfg_weight is not None:
            payload["cfg_weight"] = cfg_weight
        if temperature is not None:
            payload["temperature"] = temperature

        return self._make_request("POST", f"{self._voice_library_url}/generate", json_data=payload)

    def generate_tts_multi_speaker(
        self,
        segments: List[Dict],
        voices: Dict,
        org_id: Optional[str] = None,
        *,
        exaggeration: Optional[float] = None,
        cfg_weight: Optional[float] = None,
        temperature: Optional[float] = None,
        add_silence_between_speakers: bool = True,
        silence_duration: Optional[float] = None,
    ) -> Dict:
        """Start multi-speaker TTS generation."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not segments:
            raise ValueError("segments is required")
        if not voices:
            raise ValueError("voices is required")

        payload = {
            "org_id": org,
            "segments": segments,
            "voices": voices,
            "add_silence_between_speakers": bool(add_silence_between_speakers),
        }
        if exaggeration is not None:
            payload["exaggeration"] = exaggeration
        if cfg_weight is not None:
            payload["cfg_weight"] = cfg_weight
        if temperature is not None:
            payload["temperature"] = temperature
        if silence_duration is not None:
            payload["silence_duration"] = silence_duration

        return self._make_request("POST", f"{self._voice_library_url}/generate/multi-speaker", json_data=payload)

    def get_tts_job(self, job_id: str, *, poll: bool = True) -> Dict:
        """Get one TTS job status."""
        if not job_id:
            raise ValueError("job_id is required")

        params = {
            "poll": str(bool(poll)).lower(),
        }
        return self._make_request("GET", f"{self._voice_library_url}/jobs/{job_id}", params=params)

    def list_tts_jobs(
        self,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> Dict:
        """List TTS jobs for an organization."""
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1 or limit > 50:
            raise ValueError("limit must be within 1..50")

        params = {
            "org_id": org,
            "page": page,
            "limit": limit,
        }
        if status is not None:
            params["status"] = status

        return self._make_request("GET", f"{self._voice_library_url}/jobs", params=params)
