from storylinez import StorylinezClient

# Fill in your credentials and org
API_KEY = "api_xxx"
API_SECRET = "sec_xxx"
BASE_URL = "https://api.storylinezads.com"
ORG_ID = "org_123"
PROJECT_ID = "proj_v2_123"

client = StorylinezClient(API_KEY, API_SECRET, BASE_URL, ORG_ID)

# --- Media: add a user file ---
try:
    resp = client.v2_project.add_media(project_id=PROJECT_ID, file_id="file_abc")
    print("Added media:", resp)
except Exception as e:
    print("Add media error:", e)

# --- Media: add stock asset ---
try:
    resp = client.v2_project.add_media(project_id=PROJECT_ID, stock_id="stk_42", media_type="videos")
    print("Added stock media:", resp)
except Exception as e:
    print("Add stock error:", e)

# --- Media: bulk add ---
try:
    resp = client.v2_project.add_media_bulk(
        project_id=PROJECT_ID,
        file_ids=["file_a", "file_b"],
        items=[{"stock_id": "stk_7", "media_type": "images"}]
    )
    print("Bulk add:", resp)
except Exception as e:
    print("Bulk add error:", e)

# --- Media: list ---
try:
    resp = client.v2_project.list_media(project_id=PROJECT_ID, include_analysis=True, page=1, page_size=10)
    print("List media:", resp)
except Exception as e:
    print("List media error:", e)

# --- Context: add document ---
try:
    resp = client.v2_context.add_document(
        project_id=PROJECT_ID,
        content="Long-form campaign brief...",
        title="Campaign Brief",
        tags=["campaign", "v2"],
        nickname="Brief"
    )
    print("Add document:", resp)
except Exception as e:
    print("Add doc error:", e)

# --- Context: list documents ---
try:
    resp = client.v2_context.list_documents(project_id=PROJECT_ID, page=1, page_size=5, content_chars=500)
    print("List documents:", resp)
except Exception as e:
    print("List docs error:", e)

# --- Context: get document page ---
try:
    DOC_ID = "doc_123"
    resp = client.v2_context.get_document_page(project_id=PROJECT_ID, doc_id=DOC_ID, page=1, page_chars=2000)
    print("Get document page:", resp)
except Exception as e:
    print("Get doc page error:", e)

# --- Context: delete document ---
try:
    DOC_ID = "doc_123"
    resp = client.v2_context.delete_document(project_id=PROJECT_ID, doc_id=DOC_ID)
    print("Delete document:", resp)
except Exception as e:
    print("Delete doc error:", e)

# --- Reference: set ---
try:
    resp = client.v2_context.set_reference(project_id=PROJECT_ID, file_id="file_ref", nickname="Hero")
    print("Set reference:", resp)
except Exception as e:
    print("Set ref error:", e)

# --- Reference: list ---
try:
    resp = client.v2_context.list_references(project_id=PROJECT_ID, page=1, page_size=10)
    print("List references:", resp)
except Exception as e:
    print("List refs error:", e)

# --- Reference: get ---
try:
    REF_ID = "ref_123"
    resp = client.v2_context.get_reference(project_id=PROJECT_ID, ref_id=REF_ID)
    print("Get reference:", resp)
except Exception as e:
    print("Get ref error:", e)

# --- Reference: clear ---
try:
    resp = client.v2_context.clear_reference(project_id=PROJECT_ID)
    print("Clear all references:", resp)
except Exception as e:
    print("Clear refs error:", e)
