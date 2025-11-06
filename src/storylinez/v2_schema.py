from typing import Dict, Optional, Any, Union, Iterable

from .base_client import BaseClient


ParamValue = Union[str, int, float, bool]


class V2SchemaClient(BaseClient):
    """SDK helper for Storylinez V2 schema endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
    ) -> None:
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._schema_base_url = f"{self.base_url}/v2/schema"

    def get_sequence_schema(
        self,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        *,
        include_examples: Optional[bool] = None,
        extra_params: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, Any]:
        """Fetch the upstream JSON schema describing V2 sequences."""
        params = self._build_params(
            org_id,
            project_id,
            include_examples=include_examples,
            extra=extra_params,
        )
        return self._make_request("GET", f"{self._schema_base_url}/sequence", params=params)

    def get_asset_schema(
        self,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        *,
        asset_type: Optional[str] = None,
        extra_params: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, Any]:
        """Fetch the upstream JSON schema describing V2 assets."""
        params = self._build_params(
            org_id,
            project_id,
            asset_type=asset_type,
            extra=extra_params,
        )
        return self._make_request("GET", f"{self._schema_base_url}/assets", params=params)

    def get_all_schemas(
        self,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
        *,
        include_examples: Optional[bool] = None,
        asset_types: Optional[Iterable[str]] = None,
        sequence_extra_params: Optional[Dict[str, ParamValue]] = None,
        asset_extra_params: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, Any]:
        """Fetch sequence and asset schemas in a single call for quick bootstrapping."""
        sequence_schema = self.get_sequence_schema(
            org_id=org_id,
            project_id=project_id,
            include_examples=include_examples,
            extra_params=sequence_extra_params,
        )

        asset_payloads: Dict[str, Any] = {}
        if asset_types:
            for asset in asset_types:
                asset_payloads[str(asset)] = self.get_asset_schema(
                    org_id=org_id,
                    project_id=project_id,
                    asset_type=asset,
                    extra_params=asset_extra_params,
                )
        else:
            asset_payloads["default"] = self.get_asset_schema(
                org_id=org_id,
                project_id=project_id,
                extra_params=asset_extra_params,
            )

        return {
            "sequence_schema": sequence_schema,
            "asset_schemas": asset_payloads,
        }

    def _build_params(
        self,
        org_id: Optional[str],
        project_id: Optional[str],
        *,
        include_examples: Optional[bool] = None,
        asset_type: Optional[str] = None,
        extra: Optional[Dict[str, ParamValue]] = None,
    ) -> Dict[str, str]:
        params: Dict[str, str] = {}
        org = org_id or self.default_org_id
        if org:
            params["org_id"] = str(org)
        if project_id:
            params["project_id"] = str(project_id)
        if include_examples is not None:
            params["include_examples"] = str(include_examples).lower()
        if asset_type:
            params["asset_type"] = str(asset_type)
        if extra:
            for key, value in extra.items():
                if value is None:
                    continue
                if isinstance(value, bool):
                    params[key] = str(value).lower()
                else:
                    params[key] = str(value)
        return params
