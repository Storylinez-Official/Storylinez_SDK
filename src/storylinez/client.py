from .storage import StorageClient
from .company_details import CompanyDetailsClient
from .brand import BrandClient
from .stock import StockClient
from .search import SearchClient
from .project import ProjectClient
from .prompt import PromptClient
from .storyboard import StoryboardClient
from .voiceover import VoiceoverClient
from .sequence import SequenceClient
from .render import RenderClient
from .utils import UtilsClient
from .v2_project import V2ProjectClient
from .v2_context import V2ContextClient
from .v2_effects import V2EffectsClient
from .v2_schema import V2SchemaClient
from .v2_sequence import V2SequenceClient
from .v2_render import V2RenderClient
from .v2_share import V2ShareClient
from .data_collection import DataCollectionClient
from .pipeline_jobs import PipelineJobsClient
from .voice_library import VoiceLibraryClient
from .settings import SettingsClient
from .user import UserClient
from .tools import ToolsClient

class StorylinezClient:
    """
    Main client for Storylinez API.
    Provides unified access to all Storylinez services.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.storylinezads.com", org_id: str = None):
        """
        Initialize the Storylinez client with authentication details.
        
        Args:
            api_key: Your Storylinez API Key
            api_secret: Your Storylinez API Secret
            base_url: Base URL for the API (defaults to production)
            org_id: Default organization ID to use for all API calls (optional)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.org_id = org_id
        
        # Initialize service clients as needed
        self._storage = None
        self._company_details = None
        self._brand = None
        self._stock = None
        self._search = None
        self._project = None
        self._prompt = None
        self._storyboard = None
        self._voiceover = None
        self._sequence = None
        self._render = None
        self._utils = None
        self._settings = None
        self._user = None
        self._tools = None
        self._v2_project = None
        self._v2_context = None
        self._v2_effects = None
        self._v2_schema = None
        self._v2_sequence = None
        self._v2_render = None
        self._v2_share = None
        self._data_collection = None
        self._pipeline_jobs = None
        self._voice_library = None
        # Future service clients will be added here
        
    @property
    def storage(self) -> StorageClient:
        """
        Get the Storage client for file and folder operations.
        
        Returns:
            StorageClient instance
        """
        if self._storage is None:
            self._storage = StorageClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._storage
    
    @property
    def company_details(self) -> CompanyDetailsClient:
        """
        Get the Company Details client for managing company profiles.
        
        Returns:
            CompanyDetailsClient instance
        """
        if self._company_details is None:
            self._company_details = CompanyDetailsClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._company_details
    
    @property
    def brand(self) -> BrandClient:
        """
        Get the Brand client for managing brand presets and styling.
        
        Returns:
            BrandClient instance
        """
        if self._brand is None:
            self._brand = BrandClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._brand
    
    @property
    def stock(self) -> StockClient:
        """
        Get the Stock client for searching and retrieving stock media.
        
        Returns:
            StockClient instance
        """
        if self._stock is None:
            self._stock = StockClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._stock
    
    @property
    def search(self) -> SearchClient:
        """
        Get the Search client for advanced searching across media types.
        
        Returns:
            SearchClient instance
        """
        if self._search is None:
            self._search = SearchClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._search
    
    @property
    def project(self) -> ProjectClient:
        """
        Get the Project client for managing projects and project resources.
        
        Returns:
            ProjectClient instance
        """
        if self._project is None:
            self._project = ProjectClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._project
    
    @property
    def prompt(self) -> PromptClient:
        """
        Get the Prompt client for managing prompts and reference videos.
        
        Returns:
            PromptClient instance
        """
        if self._prompt is None:
            self._prompt = PromptClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._prompt
    
    @property
    def storyboard(self) -> StoryboardClient:
        """
        Get the Storyboard client for creating and managing storyboards.
        
        Returns:
            StoryboardClient instance
        """
        if self._storyboard is None:
            self._storyboard = StoryboardClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._storyboard
    
    @property
    def voiceover(self) -> VoiceoverClient:
        """
        Get the Voiceover client for generating and managing voiceovers.
        
        Returns:
            VoiceoverClient instance
        """
        if self._voiceover is None:
            self._voiceover = VoiceoverClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._voiceover
    
    @property
    def sequence(self) -> SequenceClient:
        """
        Get the Sequence client for creating and managing video sequences.
        
        Returns:
            SequenceClient instance
        """
        if self._sequence is None:
            self._sequence = SequenceClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._sequence
    
    @property
    def render(self) -> RenderClient:
        """
        Get the Render client for creating and managing video renders.
        
        Returns:
            RenderClient instance
        """
        if self._render is None:
            self._render = RenderClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._render
    
    @property
    def utils(self) -> UtilsClient:
        """
        Get the Utils client for accessing utility functions and AI helpers.
        
        Returns:
            UtilsClient instance
        """
        if self._utils is None:
            self._utils = UtilsClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._utils
    
    @property
    def settings(self) -> SettingsClient:
        """
        Get the Settings client for managing user settings and preferences.
        
        Returns:
            SettingsClient instance
        """
        if self._settings is None:
            self._settings = SettingsClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._settings
    
    @property
    def user(self) -> UserClient:
        """
        Get the User client for managing user profiles and subscription information.
        
        Returns:
            UserClient instance
        """
        if self._user is None:
            self._user = UserClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._user
    
    @property
    def tools(self) -> ToolsClient:
        """
        Get the Tools client for creating and managing AI-powered creative tools.
        
        Returns:
            ToolsClient instance
        """
        if self._tools is None:
            self._tools = ToolsClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._tools
    
    @property
    def v2_project(self) -> V2ProjectClient:
        """
        Get the V2 Project client for media catalogue endpoints.

        Returns:
            V2ProjectClient instance
        """
        if self._v2_project is None:
            self._v2_project = V2ProjectClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_project

    @property
    def v2_context(self) -> V2ContextClient:
        """
        Get the V2 Context client for document and reference endpoints.

        Returns:
            V2ContextClient instance
        """
        if self._v2_context is None:
            self._v2_context = V2ContextClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_context

    @property
    def v2_effects(self) -> V2EffectsClient:
        """
        Get the V2 Effects client for catalog and listing endpoints.

        Returns:
            V2EffectsClient instance
        """
        if self._v2_effects is None:
            self._v2_effects = V2EffectsClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_effects

    @property
    def v2_schema(self) -> V2SchemaClient:
        """
        Get the V2 Schema client for sequence and asset schema endpoints.

        Returns:
            V2SchemaClient instance
        """
        if self._v2_schema is None:
            self._v2_schema = V2SchemaClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_schema

    @property
    def v2_sequence(self) -> V2SequenceClient:
        """
        Get the V2 Sequence client for sequence session endpoints.

        Returns:
            V2SequenceClient instance
        """
        if self._v2_sequence is None:
            self._v2_sequence = V2SequenceClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_sequence

    @property
    def v2_render(self) -> V2RenderClient:
        """
        Get the V2 Render client for rendering workflow endpoints.

        Returns:
            V2RenderClient instance
        """
        if self._v2_render is None:
            self._v2_render = V2RenderClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_render

    @property
    def v2_share(self) -> V2ShareClient:
        """
        Get the V2 Share client for creating and managing public share links.

        Returns:
            V2ShareClient instance
        """
        if self._v2_share is None:
            self._v2_share = V2ShareClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._v2_share

    @property
    def data_collection(self) -> DataCollectionClient:
        """
        Get the Data Collection client for collection and extraction jobs.

        Returns:
            DataCollectionClient instance
        """
        if self._data_collection is None:
            self._data_collection = DataCollectionClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._data_collection

    @property
    def pipeline_jobs(self) -> PipelineJobsClient:
        """
        Get the Pipeline Jobs client for V1/V2 pipeline orchestration endpoints.

        Returns:
            PipelineJobsClient instance
        """
        if self._pipeline_jobs is None:
            self._pipeline_jobs = PipelineJobsClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._pipeline_jobs

    @property
    def voice_library(self) -> VoiceLibraryClient:
        """
        Get the Voice Library client for voice catalog, user voices, and TTS jobs.

        Returns:
            VoiceLibraryClient instance
        """
        if self._voice_library is None:
            self._voice_library = VoiceLibraryClient(self.api_key, self.api_secret, self.base_url, self.org_id)
        return self._voice_library
    
    # Additional service properties will be added as they're implemented
