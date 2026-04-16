from typing import Dict, List, Optional

from .base_client import BaseClient


class TrendingAdsClient(BaseClient):
    """Client for /trending_ads endpoints.

    These endpoints require Bearer token authentication. Set auth_token on the client
    or pass auth_token per method call.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.storylinezads.com",
        default_org_id: Optional[str] = None,
        auth_token: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, base_url, default_org_id)
        self._trending_ads_url = f"{self.base_url}/trending_ads"
        self.auth_token = auth_token

    def set_auth_token(self, auth_token: str) -> None:
        """Set default Bearer token used for token-authenticated calls."""
        self.auth_token = auth_token

    def _auth_headers(self, auth_token: Optional[str]) -> Dict[str, str]:
        token = auth_token or self.auth_token
        if not token:
            raise ValueError("auth_token is required for trending_ads endpoints")
        return {
            "Authorization": f"Bearer {token}",
        }

    # ------------------------------
    # Discovery
    # ------------------------------

    def search(self, payload: Dict, *, auth_token: Optional[str] = None) -> Dict:
        """Search trending ads with advanced filters and sorting."""
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dictionary")
        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/search",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def get_by_id(self, ad_id: str, *, auth_token: Optional[str] = None) -> Dict:
        """Get one ad by ad_id."""
        if not ad_id:
            raise ValueError("ad_id is required")
        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/get_by_id",
            params={"ad_id": ad_id},
            headers=self._auth_headers(auth_token),
        )

    def list(
        self,
        *,
        category: Optional[str] = None,
        sort_by: str = "smart_default",
        sort_order: int = -1,
        min_average_rating: float = 0,
        min_total_ratings: int = 0,
        page: int = 1,
        limit: int = 20,
        auto_track_views: bool = True,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """List trending ads with optional filtering and sorting."""
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1 or limit > 50:
            raise ValueError("limit must be within 1..50")

        params = {
            "sort_by": sort_by,
            "sort_order": sort_order,
            "min_average_rating": min_average_rating,
            "min_total_ratings": min_total_ratings,
            "page": page,
            "limit": limit,
            "auto_track_views": str(bool(auto_track_views)).lower(),
        }
        if category is not None:
            params["category"] = category

        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/list",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    # ------------------------------
    # Ratings
    # ------------------------------

    def rate(
        self,
        ad_id: str,
        overall_score: int,
        *,
        category_ratings: Optional[Dict[str, int]] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Create or update rating for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        if overall_score < 1 or overall_score > 5:
            raise ValueError("overall_score must be between 1 and 5")

        payload = {
            "ad_id": ad_id,
            "overall_score": overall_score,
        }
        if category_ratings is not None:
            payload["category_ratings"] = category_ratings

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/rate",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def rating_stats(self, ad_id: str, *, auth_token: Optional[str] = None) -> Dict:
        """Get aggregate rating stats for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/rating_stats",
            params={"ad_id": ad_id},
            headers=self._auth_headers(auth_token),
        )

    # ------------------------------
    # Comments
    # ------------------------------

    def add_comment(
        self,
        ad_id: str,
        comment: str,
        *,
        parent_comment_id: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Create a comment or reply."""
        if not ad_id:
            raise ValueError("ad_id is required")
        if not comment:
            raise ValueError("comment is required")

        payload = {
            "ad_id": ad_id,
            "comment": comment,
        }
        if parent_comment_id is not None:
            payload["parent_comment_id"] = parent_comment_id

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/comment",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def list_comments(
        self,
        ad_id: str,
        *,
        parent_comment_id: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """List comments for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1 or limit > 50:
            raise ValueError("limit must be within 1..50")

        params = {
            "ad_id": ad_id,
            "page": page,
            "limit": limit,
        }
        if parent_comment_id is not None:
            params["parent_comment_id"] = parent_comment_id

        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/comments",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    def edit_comment(self, comment_id: str, comment: str, *, auth_token: Optional[str] = None) -> Dict:
        """Edit one of the current user's comments."""
        if not comment_id:
            raise ValueError("comment_id is required")
        if not comment:
            raise ValueError("comment is required")

        payload = {
            "comment_id": comment_id,
            "comment": comment,
        }
        return self._make_request(
            "PUT",
            f"{self._trending_ads_url}/comment/edit",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def delete_comment(self, comment_id: str, *, auth_token: Optional[str] = None) -> Dict:
        """Delete one of the current user's comments."""
        if not comment_id:
            raise ValueError("comment_id is required")
        return self._make_request(
            "DELETE",
            f"{self._trending_ads_url}/comment/delete",
            params={"comment_id": comment_id},
            headers=self._auth_headers(auth_token),
        )

    def react_comment(
        self,
        comment_id: str,
        reaction: str,
        *,
        action: str = "add",
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Add or remove a reaction on a comment."""
        if not comment_id:
            raise ValueError("comment_id is required")
        if not reaction:
            raise ValueError("reaction is required")
        if action not in ("add", "remove"):
            raise ValueError("action must be 'add' or 'remove'")

        payload = {
            "comment_id": comment_id,
            "reaction": reaction,
            "action": action,
        }
        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/comment/react",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    # ------------------------------
    # Polls and feedback
    # ------------------------------

    def list_polls(
        self,
        ad_id: str,
        *,
        page: int = 1,
        polls_per_page: int = 50,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """List active polls for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")

        params = {
            "ad_id": ad_id,
            "page": page,
            "polls_per_page": polls_per_page,
        }
        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/polls",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    def respond_poll(
        self,
        ad_id: str,
        poll_id: str,
        *,
        selected_option: Optional[int] = None,
        response: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Respond to a poll by option index or option text."""
        if not ad_id:
            raise ValueError("ad_id is required")
        if not poll_id:
            raise ValueError("poll_id is required")
        if selected_option is None and response is None:
            raise ValueError("selected_option or response is required")

        payload = {
            "ad_id": ad_id,
            "poll_id": poll_id,
        }
        if selected_option is not None:
            payload["selected_option"] = selected_option
        if response is not None:
            payload["response"] = response

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/poll/respond",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def add_feedback(
        self,
        ad_id: str,
        *,
        what_worked: Optional[str] = None,
        what_didnt_work: Optional[str] = None,
        suggestions: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Submit structured feedback for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        if not any([what_worked, what_didnt_work, suggestions]):
            raise ValueError("At least one feedback field is required")

        payload = {
            "ad_id": ad_id,
        }
        if what_worked is not None:
            payload["what_worked"] = what_worked
        if what_didnt_work is not None:
            payload["what_didnt_work"] = what_didnt_work
        if suggestions is not None:
            payload["suggestions"] = suggestions

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/feedback",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def list_feedback(
        self,
        ad_id: str,
        *,
        feedback_type: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """List structured feedback for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")

        params = {
            "ad_id": ad_id,
            "page": page,
            "limit": limit,
        }
        if feedback_type is not None:
            params["type"] = feedback_type

        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/feedback",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    # ------------------------------
    # Highlights
    # ------------------------------

    def add_highlight(
        self,
        ad_id: str,
        start_time: float,
        end_time: float,
        *,
        annotation: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Add a timeline highlight for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        if end_time <= start_time:
            raise ValueError("end_time must be greater than start_time")

        payload = {
            "ad_id": ad_id,
            "start_time": start_time,
            "end_time": end_time,
        }
        if annotation is not None:
            payload["annotation"] = annotation

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/highlight",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def list_highlights(
        self,
        ad_id: str,
        *,
        user_only: bool = False,
        page: int = 1,
        limit: int = 50,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """List highlights for an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")

        params = {
            "ad_id": ad_id,
            "user_only": str(bool(user_only)).lower(),
            "page": page,
            "limit": limit,
        }
        return self._make_request(
            "GET",
            f"{self._trending_ads_url}/highlights",
            params=params,
            headers=self._auth_headers(auth_token),
        )

    # ------------------------------
    # Views and saves
    # ------------------------------

    def track_view(
        self,
        *,
        ad_id: Optional[str] = None,
        unique_id: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Dict:
        """Track a view event for an ad."""
        if not ad_id and not unique_id:
            raise ValueError("ad_id or unique_id is required")

        payload: Dict[str, str] = {}
        if ad_id is not None:
            payload["ad_id"] = ad_id
        if unique_id is not None:
            payload["unique_id"] = unique_id

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/track_view",
            json_data=payload,
            headers=self._auth_headers(auth_token),
        )

    def get_viewed_ads(self, ad_ids: List[str], *, auth_token: Optional[str] = None) -> Dict:
        """Get viewed-state map for supplied ad IDs."""
        if not isinstance(ad_ids, list):
            raise ValueError("ad_ids must be a list")

        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/viewed_ads",
            json_data={"ad_ids": ad_ids},
            headers=self._auth_headers(auth_token),
        )

    def save_ad(self, ad_id: str, *, auth_token: Optional[str] = None) -> Dict:
        """Save an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/save",
            json_data={"ad_id": ad_id},
            headers=self._auth_headers(auth_token),
        )

    def unsave_ad(self, ad_id: str, *, auth_token: Optional[str] = None) -> Dict:
        """Unsave an ad."""
        if not ad_id:
            raise ValueError("ad_id is required")
        return self._make_request(
            "POST",
            f"{self._trending_ads_url}/unsave",
            json_data={"ad_id": ad_id},
            headers=self._auth_headers(auth_token),
        )
