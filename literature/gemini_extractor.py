"""
Gemini AI integration for extracting structured information
"""
import json
from google import genai
from google.genai import types
from schemas import AUTHOR_SCHEMA, WORK_SCHEMA
from prompts import get_author_extraction_prompt, get_work_extraction_prompt


class GeminiExtractor:
    """Handles all Gemini API interactions for literature analysis"""
    
    def __init__(self, model="gemini-2.0-flash-exp"):
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
            self.client = genai.Client(api_key="YOUR_API_KEY_HERE")
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
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AUTHOR_SCHEMA,
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )
        print(f"    DEBUG: Received response from Gemini")
        
        return json.loads(response.text)
    
    def extract_work_info(self, work_name, author_name):
        """
        Extract structured literary work information using Google Gemini API with web search.
        
        Args:
            work_name: The name of the literary work
            author_name: The name of the author
            
        Returns:
            Dictionary with work information (name, year, motifs, themes, characters, analysis_summary)
        """
        prompt = get_work_extraction_prompt(work_name, author_name)
        
        print(f"    DEBUG: Client created, sending request to Gemini with search enabled...")
        client = self._get_client()
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=WORK_SCHEMA,
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )
        print(f"    DEBUG: Received response from Gemini")
        
        return json.loads(response.text)
