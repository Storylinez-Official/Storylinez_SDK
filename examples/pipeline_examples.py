from storylinez.pipeline import PipelineClient
from storylinez.utils import UtilsClient

# Initialize the UtilsClient and PipelineClient
utils_client = UtilsClient(utils_url="https://api.example.com")
pipeline_client = PipelineClient(utils_client=utils_client)

# Example input data
website_url = "https://example.com"

# Run the pipeline
try:
    result = pipeline_client.run_web_scraping_and_brand_extraction(
        website_url=website_url,
        timeout=120,  # Optional: Adjust timeout as needed
        depth=2,      # Optional: Adjust scraping depth
        enable_js=True,  # Optional: Enable JavaScript rendering
        include_palette=True,  # Optional: Include color palette in brand extraction
        dynamic_extraction=False  # Optional: Disable dynamic extraction
    )
    print("Pipeline result:", result)
except Exception as e:
    print("An error occurred:", str(e))