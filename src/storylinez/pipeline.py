import time
from typing import Dict, Any
from .utils import UtilsClient

class PipelineClient:
    """
    Client for managing pipelines that combine multiple operations like web scraping and brand extraction.
    """

    def __init__(self, utils_client: UtilsClient):
        """
        Initialize the PipelineClient.

        Args:
            utils_client: An instance of UtilsClient to interact with utility APIs.
        """
        self.utils_client = utils_client

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
        polling_interval: int = 10
    ) -> Dict[str, Any]:
        """
        Perform web scraping and brand extraction in a single pipeline.

        Args:
            website_url: The URL of the website to scrape.
            timeout: Maximum time (in seconds) to wait for each job (default: 60).
            depth: How deep to crawl links during web scraping (default: 1).
            enable_js: Enable JavaScript rendering for web scraping (default: False).
            include_palette: Include color palette in brand extraction (default: True).
            dynamic_extraction: Enable dynamic extraction for brand settings (default: False).
            deepthink: Enable advanced AI reasoning (default: False).
            overdrive: Enable maximum quality and detail (default: False).
            web_search: Enable web search for up-to-date information (default: False).
            eco: Enable eco mode for faster processing (default: False).
            polling_interval: Time (in seconds) between job status checks (default: 10).

        Returns:
            A dictionary containing the combined results of web scraping and brand extraction.

        Raises:
            TimeoutError: If the pipeline does not complete within the timeout period.
            Exception: If any step in the pipeline fails.
        """
        # Step 1: Start web scraping job
        web_scraping_params = {
            "website_url": website_url,
            "timeout": timeout,
            "depth": depth,
            "enable_js": enable_js,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
        }
        web_scraping_job = self.utils_client._make_request("POST", f"{self.utils_client.utils_url}/web-scraping", json=web_scraping_params)
        web_scraping_job_id = web_scraping_job.get("job_id")

        if not web_scraping_job_id:
            raise Exception("Failed to start web scraping job")

        # Step 2: Wait for web scraping to complete
        web_scraping_result = self.utils_client.wait_for_job_completion(
            job_id=web_scraping_job_id,
            timeout_seconds=timeout,
            polling_interval=polling_interval
        )

        # Step 3: Start brand extraction job using web scraping results
        brand_extraction_params = {
            "website_url": website_url,
            "scraped_data": web_scraping_result.get("result"),
            "include_palette": include_palette,
            "dynamic_extraction": dynamic_extraction,
            "deepthink": deepthink,
            "overdrive": overdrive,
            "web_search": web_search,
            "eco": eco,
        }
        brand_extraction_job = self.utils_client._make_request("POST", f"{self.utils_client.utils_url}/brand-extraction", json=brand_extraction_params)
        brand_extraction_job_id = brand_extraction_job.get("job_id")

        if not brand_extraction_job_id:
            raise Exception("Failed to start brand extraction job")

        # Step 4: Wait for brand extraction to complete
        brand_extraction_result = self.utils_client.wait_for_job_completion(
            job_id=brand_extraction_job_id,
            timeout_seconds=timeout,
            polling_interval=polling_interval
        )

        # Step 5: Combine results and return
        return {
            "web_scraping": web_scraping_result.get("result"),
            "brand_extraction": brand_extraction_result.get("result")
        }