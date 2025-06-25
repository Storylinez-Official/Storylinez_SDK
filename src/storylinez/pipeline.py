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

    def run_web_scraping_and_brand_extraction(self, website_url: str, **kwargs) -> Dict[str, Any]:
        """
        Perform web scraping and brand extraction in a single pipeline.

        Args:
            website_url: The URL of the website to scrape.
            **kwargs: Additional parameters for web scraping and brand extraction.

        Returns:
            A dictionary containing the combined results of web scraping and brand extraction.

        Raises:
            TimeoutError: If the pipeline does not complete within the timeout period.
            Exception: If any step in the pipeline fails.
        """
        # Step 1: Start web scraping job
        web_scraping_params = {
            "website_url": website_url,
            "timeout": kwargs.get("timeout", 60),
            "depth": kwargs.get("depth", 1),
            "enable_js": kwargs.get("enable_js", False),
        }
        web_scraping_job = self.utils_client._make_request("POST", f"{self.utils_client.utils_url}/web-scraping", json=web_scraping_params)
        web_scraping_job_id = web_scraping_job.get("job_id")

        if not web_scraping_job_id:
            raise Exception("Failed to start web scraping job")

        # Step 2: Wait for web scraping to complete
        web_scraping_result = self.utils_client.wait_for_job_completion(
            job_id=web_scraping_job_id,
            timeout_seconds=kwargs.get("timeout", 60),
            polling_interval=kwargs.get("polling_interval", 2)
        )

        # Step 3: Start brand extraction job using web scraping results
        brand_extraction_params = {
            "website_url": website_url,
            "scraped_data": web_scraping_result.get("result"),
            "include_palette": kwargs.get("include_palette", True),
            "dynamic_extraction": kwargs.get("dynamic_extraction", False),
        }
        brand_extraction_job = self.utils_client._make_request("POST", f"{self.utils_client.utils_url}/brand-extraction", json=brand_extraction_params)
        brand_extraction_job_id = brand_extraction_job.get("job_id")

        if not brand_extraction_job_id:
            raise Exception("Failed to start brand extraction job")

        # Step 4: Wait for brand extraction to complete
        brand_extraction_result = self.utils_client.wait_for_job_completion(
            job_id=brand_extraction_job_id,
            timeout_seconds=kwargs.get("timeout", 60),
            polling_interval=kwargs.get("polling_interval", 2)
        )

        # Step 5: Combine results and return
        return {
            "web_scraping": web_scraping_result.get("result"),
            "brand_extraction": brand_extraction_result.get("result")
        }