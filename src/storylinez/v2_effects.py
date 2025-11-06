from typing import Dict, Optional, Any, Union

from .base_client import BaseClient


ParamValue = Union[str, int, float, bool]


class V2EffectsClient(BaseClient):
    """SDK helper for Storylinez V2 effects endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ) -> None:
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._effects_base_url = f"{self.base_url}/v2/effects"

    def get_catalog(
        self,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        *,
        asset_type: Optional[str] = None,
        search: Optional[str] = None,
        extra_params: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, Any]:
        """Return the upstream effects catalog grouped by compatibility."""
        params = self._build_params(org_id, project_id, asset_type=asset_type, search=search, extra=extra_params)
        return self._make_request("GET", f"{self._effects_base_url}/catalog", params=params)

    def list_effects(
        self,
        asset_type: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        *,
        search: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        extra_params: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, Any]:
        """List effect presets filtered by asset type and optional search."""
        if not asset_type:
            raise ValueError("asset_type is required")

        params = self._build_params(
            org_id,
            project_id,
            asset_type=asset_type,
            search=search,
            page=page,
            page_size=page_size,
            extra=extra_params,
        )
        return self._make_request("GET", f"{self._effects_base_url}/list", params=params)

    def find_effect(
        self,
        effect_id: str,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        *,
        asset_type: Optional[str] = None,
        search: Optional[str] = None,
        extra_params: Optional[Dict[str, ParamValue]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Locate a single effect definition within the catalog or list results."""
        if not effect_id:
            raise ValueError("effect_id is required")

        target_id = str(effect_id)
        catalog_payload = self.get_catalog(
            org_id=org_id,
            project_id=project_id,
            asset_type=asset_type,
            search=search,
            extra_params=extra_params,
        )
        effect = self._extract_effect_from_payload(catalog_payload, target_id)
        if effect is not None:
            return effect

        if asset_type:
            listing_payload = self.list_effects(
                asset_type=asset_type,
                org_id=org_id,
                project_id=project_id,
                search=search,
                extra_params=extra_params,
            )
            return self._extract_effect_from_payload(listing_payload, target_id)
        return None

    def _build_params(
        self,
        org_id: Optional[str],
        project_id: Optional[str],
        *,
        asset_type: Optional[str] = None,
        search: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        extra: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, str]:
        params: Dict[str, str] = {}
        org = org_id or self.default_org_id
        if org:
            params["org_id"] = str(org)
        if project_id:
            params["project_id"] = str(project_id)
        if asset_type:
            params["asset_type"] = str(asset_type)
        if search:
            params["search"] = search
        if page is not None:
            params["page"] = str(page)
        if page_size is not None:
            params["page_size"] = str(page_size)
        if extra:
            for key, value in extra.items():
                if value is None:
                    continue
                if isinstance(value, bool):
                    params[key] = str(value).lower()
                else:
                    params[key] = str(value)
        return params

    @staticmethod
    def _extract_effect_from_payload(payload: Any, effect_id: str) -> Optional[Dict[str, Any]]:
        for candidate in V2EffectsClient._iter_effect_candidates(payload):
            candidate_id = str(candidate.get("effect_id") or candidate.get("id") or "")
            if candidate_id == effect_id:
                return candidate
        return None

    @staticmethod
    def _iter_effect_candidates(payload: Any):
        if isinstance(payload, dict):
            if any(key in payload for key in ("effect_id", "id")) and "name" in payload:
                yield payload
            for value in payload.values():
                yield from V2EffectsClient._iter_effect_candidates(value)
        elif isinstance(payload, list):
            for item in payload:
                yield from V2EffectsClient._iter_effect_candidates(item)
