from typing import Dict, List, Optional, Union

from .base_client import BaseClient


class V2ContextClient(BaseClient):
    """
    Client for Storylinez V2 context endpoints.
    Manage briefs, long-form documents, and reference media exposed under /v2/context.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: str = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._context_documents_url = f"{self.base_url}/v2/context/documents"
        self._context_reference_url = f"{self.base_url}/v2/context/reference"

    # ------------------------------
    # Context: documents (briefs)
    # ------------------------------

    def add_document(
        self,
        project_id: str,
        content: str,
        org_id: Optional[str] = None,
        *,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        tags: Optional[List[str]] = None,
        nickname: Optional[str] = None,
    ) -> Dict:
        """
        Add a text document to the project's context library.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not content:
            raise ValueError("content is required")

        payload: Dict[str, Union[str, List[str]]] = {
            "org_id": org,
            "project_id": project_id,
            "content": content,
        }
        if title is not None:
            payload["title"] = title
        if summary is not None:
            payload["summary"] = summary
        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError("tags must be a list of strings")
            payload["tags"] = [str(t) for t in tags]
        if nickname is not None:
            payload["nickname"] = nickname

        return self._make_request("POST", f"{self._context_documents_url}/add", json_data=payload)

    def list_documents(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        page_size: int = 10,
        content_chars: Optional[int] = None,
    ) -> Dict:
        """
        List document summaries for a V2 project.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1 or page_size > 50:
            raise ValueError("page_size must be within 1..50")

        params: Dict[str, Union[str, int]] = {
            "org_id": org,
            "project_id": project_id,
            "page": page,
            "page_size": page_size,
        }
        if content_chars is not None:
            if content_chars < 100:
                raise ValueError("content_chars must be >= 100 when provided")
            params["content_chars"] = content_chars

        return self._make_request("GET", f"{self._context_documents_url}/list", params=params)

    def get_document_page(
        self,
        project_id: str,
        doc_id: str,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        page_chars: Optional[int] = None,
    ) -> Dict:
        """
        Get a specific page slice of a document.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not doc_id:
            raise ValueError("doc_id is required")

        params: Dict[str, Union[str, int]] = {
            "org_id": org,
            "project_id": project_id,
            "doc_id": doc_id,
            "page": page,
        }
        if page_chars is not None:
            if page_chars < 1000:
                raise ValueError("page_chars must be >= 1000 when provided")
            params["page_chars"] = page_chars

        return self._make_request("GET", f"{self._context_documents_url}/get", params=params)

    def update_document(
        self,
        project_id: str,
        doc_id: str,
        org_id: Optional[str] = None,
        *,
        title: Optional[str] = None,
        content: Optional[str] = None,
        summary: Optional[str] = None,
        tags: Optional[List[str]] = None,
        nickname: Optional[str] = None,
    ) -> Dict:
        """
        Update an existing context document.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not doc_id:
            raise ValueError("doc_id is required")

        payload: Dict[str, Union[str, List[str]]] = {
            "org_id": org,
            "project_id": project_id,
            "doc_id": doc_id,
        }
        if title is not None:
            payload["title"] = title
        if content is not None:
            payload["content"] = content
        if summary is not None:
            payload["summary"] = summary
        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError("tags must be a list of strings")
            payload["tags"] = [str(t) for t in tags]
        if nickname is not None:
            payload["nickname"] = nickname

        return self._make_request("PUT", f"{self._context_documents_url}/update", json_data=payload)

    def delete_document(self, project_id: str, doc_id: str, org_id: Optional[str] = None) -> Dict:
        """
        Delete a document from the context library.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not doc_id:
            raise ValueError("doc_id is required")

        params = {
            "org_id": org,
            "project_id": project_id,
            "doc_id": doc_id,
        }
        return self._make_request("DELETE", f"{self._context_documents_url}/delete", params=params)

    # ------------------------------
    # Context: reference videos
    # ------------------------------

    def set_reference(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        file_id: Optional[str] = None,
        ref_id: Optional[str] = None,
        nickname: Optional[str] = None,
    ) -> Dict:
        """
        Create or update the primary reference video metadata for a project.

        Provide file_id to create. Use ref_id (+ optional new file_id) to update.
        """
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not file_id and not ref_id:
            raise ValueError("Provide file_id to create a reference or ref_id to update")

        payload: Dict[str, Optional[str]] = {
            "org_id": org,
            "project_id": project_id,
        }
        if file_id is not None:
            payload["file_id"] = file_id
        if ref_id is not None:
            payload["ref_id"] = ref_id
        if nickname is not None:
            payload["nickname"] = nickname

        return self._make_request("POST", f"{self._context_reference_url}/set", json_data=payload)

    def get_reference(self, project_id: str, ref_id: str, org_id: Optional[str] = None) -> Dict:
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if not ref_id:
            raise ValueError("ref_id is required")

        params = {
            "org_id": org,
            "project_id": project_id,
            "ref_id": ref_id,
        }
        return self._make_request("GET", f"{self._context_reference_url}/get", params=params)

    def list_references(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict:
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1 or page_size > 50:
            raise ValueError("page_size must be within 1..50")

        params = {
            "org_id": org,
            "project_id": project_id,
            "page": page,
            "page_size": page_size,
        }
        return self._make_request("GET", f"{self._context_reference_url}/list", params=params)

    def clear_reference(
        self,
        project_id: str,
        org_id: Optional[str] = None,
        *,
        ref_id: Optional[str] = None,
    ) -> Dict:
        org = org_id or self.default_org_id
        if not org:
            raise ValueError("Organization ID is required (org_id or default_org_id)")
        if not project_id:
            raise ValueError("project_id is required")

        params = {
            "org_id": org,
            "project_id": project_id,
        }
        if ref_id is not None:
            params["ref_id"] = ref_id

        return self._make_request("DELETE", f"{self._context_reference_url}/clear", params=params)
