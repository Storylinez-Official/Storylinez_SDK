import os
from dotenv import load_dotenv

from storylinez import StorylinezClient
from storylinez.pipelines import PipelineClient


load_dotenv()

API_KEY = os.environ.get("STORYLINEZ_API_KEY", "api_your_key_here")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_secret_here")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")


def main() -> None:
    """Demonstrate chaining the scraping and brand extraction pipeline."""
    client = StorylinezClient(api_key=API_KEY, api_secret=API_SECRET, org_id=ORG_ID)
    pipeline_client = PipelineClient(client)

    website_url = "https://example.com"

    try:
        results = pipeline_client.run_web_scraping_and_brand_extraction(
            website_url=website_url,
            timeout=120,
            depth=2,
            enable_js=True,
            include_palette=True,
            dynamic_extraction=True,
            deepthink=False,
            overdrive=False,
            web_search=True,
            eco=False,
            polling_interval=15,
        )
    except Exception as exc:
        print(f"Pipeline failed: {exc}")
        return

    print("\n=== Web Scraping Summary ===")
    if results.get("web_scraping"):
        page_count = len(results["web_scraping"].get("pages", []))
        print(f"Fetched {page_count} page(s) from {website_url}")
    else:
        print("No web scraping data returned")

    print("\n=== Brand Extraction Summary ===")
    brand_data = results.get("brand_extraction", {})
    if brand_data:
        palette = brand_data.get("brand_colors", {}).get("palette", [])
        print(f"Brand name: {brand_data.get('brand_name', 'unknown')}")
        if palette:
            swatches = ", ".join(color.get("hex") for color in palette[:5] if color.get("hex"))
            print(f"Palette preview: {swatches}")
    else:
        print("No brand extraction data returned")

    if results.get("errors"):
        print("\nErrors:")
        for stage, message in results["errors"].items():
            print(f"- {stage}: {message}")


if __name__ == "__main__":
    main()