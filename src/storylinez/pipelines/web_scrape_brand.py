from typing import Any, Dict, Optional


class PipelineClient:
    """High-level helper for chaining web scraping and brand extraction workflows."""

    def __init__(self, client) -> None:
        """Wrap the shared Storylinez client instance."""
        self.client = client

    def run_web_scraping_and_brand_extraction(
        self,
        website_url: str,
        timeout: int = 60,
        depth: int = 1,
        enable_js: bool = False,
        include_palette: bool = True,
        dynamic_extraction: bool = False,
        deepthink: bool = False,
        overdrive: bool = False,
        web_search: bool = False,
        eco: bool = False,
        polling_interval: int = 10,
    ) -> Dict[str, Any]:
        """Execute the two-stage scraping + brand extraction pipeline and wait for completion."""
        errors: Dict[str, str] = {}
        web_scraping_result: Optional[Dict[str, Any]] = None
        brand_extraction_result: Optional[Dict[str, Any]] = None

        # Step 1: Kick off advanced web scraping
        try:
            web_scraping_job = self.client.tools.create_web_scraper_advanced(
                name="WebScrapingJob",
                website_url=website_url,
                depth=depth,
                enable_js=enable_js,
                deepthink=deepthink,
                overdrive=overdrive,
                web_search=web_search,
                eco=eco,
                timeout=timeout,
            )
            tool_id = web_scraping_job.get("tool", {}).get("tool_id")
            if not tool_id:
                raise RuntimeError("Web scraping did not return tool['tool_id'].")
            web_scraping_result = self.client.tools.wait_for_tool_completion(
                tool_id,
                polling_interval=polling_interval,
            )
        except Exception as exc:  # noqa: BLE001
            errors["web_scraping"] = str(exc)
            web_scraping_result = None

        # Step 2: Kick off brand extraction if scraping produced data
        if web_scraping_result:
            try:
                brand_extraction_job = self.client.utils.extract_brand_settings(
                    website_url=website_url,
                    deepthink=deepthink,
                    overdrive=overdrive,
                    eco=eco,
                    timeout=timeout,
                    include_palette=include_palette,
                    dynamic_extraction=dynamic_extraction,
                    web_search=web_search,
                )
                job_id = brand_extraction_job.get("job_id") or brand_extraction_job.get("id")
                if not job_id:
                    raise RuntimeError("Brand extraction did not return a job ID.")
                brand_extraction_result = self.client.utils.wait_for_job_completion(
                    job_id,
                    polling_interval=polling_interval,
                )
            except Exception as exc:  # noqa: BLE001
                errors["brand_extraction"] = str(exc)
                brand_extraction_result = None
        elif "web_scraping" not in errors:
            errors["web_scraping"] = "Web scraping did not return expected result."
            brand_extraction_result = None

        results: Dict[str, Any] = {
            "web_scraping": web_scraping_result,
            "brand_extraction": brand_extraction_result,
        }
        if errors:
            results["errors"] = errors
        return results
