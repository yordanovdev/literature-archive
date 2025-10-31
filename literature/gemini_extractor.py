"""
Gemini AI integration for extracting structured information
"""
from google import genai
from schemas import AuthorInfo, WorkInfo
from prompts import get_author_extraction_prompt, get_work_extraction_prompt


class GeminiExtractor:
    """Handles all Gemini API interactions for literature analysis"""
    
    def __init__(self, model="gemini-2.5-flash"):
        """
        Initialize the Gemini extractor.
        
        Args:
            model: The Gemini model to use (default: gemini-2.0-flash-exp with search support)
        """
        self.model = model
        self.client = None
    
    def _get_client(self):
        """Get or create Gemini client (lazy initialization)"""
        if self.client is None:
            print(f"    DEBUG: Creating Gemini client...")
            self.client = genai.Client(api_key="YOUR_API_KEY")
        return self.client
    
    def extract_author_info(self, author_name):
        """
        Extract structured author information using Google Gemini API with web search.
        
        Args:
            author_name: The name of the author to research
            
        Returns:
            Dictionary with author information (name, year_of_birth, year_of_death, information)
        """
        prompt = get_author_extraction_prompt(author_name)
        
        print(f"    DEBUG: Client created, sending request to Gemini with search enabled...")
        client = self._get_client()
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": AuthorInfo,
            },
        )
        print(f"    DEBUG: Received response from Gemini")
        
        # Use instantiated object
        author_info: AuthorInfo = response.parsed
        # Convert to dictionary for compatibility with existing code
        return {
            "name": author_info.name,
            "year_of_birth": author_info.year_of_birth,
            "year_of_death": author_info.year_of_death,
            "information": author_info.information
        }
    
    def extract_work_info(self, work_name, author_name, document_context=""):
        """
        Extract structured literary work information using Google Gemini API with document context.
        
        Args:
            work_name: The name of the literary work
            author_name: The name of the author
            document_context: Relevant excerpts from source documents (optional)
            
        Returns:
            Dictionary with work information (name, year, motifs, themes, characters, analysis_summary)
        """
        prompt = get_work_extraction_prompt(work_name, author_name, document_context)
        
        print(f"    DEBUG: Client created, sending request to Gemini with search enabled...")
        client = self._get_client()
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": WorkInfo,
            },
        )
        print(f"    DEBUG: Received response from Gemini")
        
        # Use instantiated object
        work_info: WorkInfo = response.parsed
        # Convert to dictionary for compatibility with existing code
        return {
            "name": work_info.name,
            "year": work_info.year,
            "genre": work_info.genre,
            "motifs": [{"motif_name": m.motif_name, "info": m.info} for m in work_info.motifs],
            "themes": [{"theme_name": t.theme_name, "info": t.info} for t in work_info.themes],
            "characters": [{"name": c.name, "info": c.info} for c in work_info.characters],
            "analysis_summary": work_info.analysis_summary
        }
