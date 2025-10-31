"""
Prompts for Gemini AI extraction with web search
"""

def get_author_extraction_prompt(author_name):
    """
    Generate prompt for extracting author information using web search.
    
    Args:
        author_name: The name of the author to research
        
    Returns:
        String prompt for Gemini
    """
    return f"""
You have access to Google Search. Use it to find accurate and reliable information about the author: {author_name}

IMPORTANT INSTRUCTIONS:
1. DO NOT HALLUCINATE - Only provide information you find from reliable sources
2. Search for information from reputable literary websites, encyclopedias, academic sources, and official biographical resources
3. Verify facts from multiple sources when possible
4. If you cannot find certain information (like birth/death years), leave those fields as empty strings
5. Focus on gathering factual, well-documented information

Please search and extract:
- name: The full name of the author (verify the exact spelling)
- year_of_birth: The year the author was born (search for verified biographical data)
- year_of_death: The year the author died (or empty string if still alive)
- information: A comprehensive summary in BULGARIAN language including:
  * Key biographical facts
  * Literary significance and contributions
  * Major works and achievements
  * Writing style and themes
  * Historical and cultural context
  * Critical reception and legacy

Search reliable sources such as:
- Literary encyclopedias and databases
- Academic literary journals
- Official author websites and biographical resources
- Reputable cultural and educational institutions
- Verified historical records

Provide the information in JSON format. Use Bulgarian language ONLY for the 'information' field.
"""


def get_work_extraction_prompt(work_name, author_name):
    """
    Generate prompt for extracting literary work information using web search.
    
    Args:
        work_name: The name of the literary work
        author_name: The name of the author
        
    Returns:
        String prompt for Gemini
    """
    return f"""
You have access to Google Search. Use it to find accurate and reliable information about the literary work: "{work_name}" by {author_name}

IMPORTANT INSTRUCTIONS:
1. DO NOT HALLUCINATE - Only provide information you find from reliable sources
2. Search for literary analysis from reputable sources: academic papers, literary journals, educational websites, book reviews from established critics
3. Verify information from multiple reliable sources
4. If you cannot find certain information, provide what you can verify and be transparent about limitations
5. Focus on well-documented literary analysis and criticism

Please search and extract the following information:
- name: The exact title of the literary work
- year: The year of publication (search for verified publication data)
- genre: The literary genre (e.g., Роман, Повест, Разказ, Стихотворение, Драма, Комедия, Елегия, Ода, etc.)
  Search for how literary critics and scholars classify this work
- motifs: Search for literary analysis discussing the motifs in the work. Each motif should have:
  - motif_name: The name of the motif (in Bulgarian)
  - info: A detailed explanation based on literary criticism and analysis
- themes: Search for academic and critical analysis of the major themes. Each theme should have:
  - theme_name: The name of the theme (in Bulgarian)
  - info: A thorough explanation based on scholarly sources
- characters: Search for character analysis from reliable sources. Include ALL characters (main, secondary, and supporting).
  For EACH character provide:
  - name: The character's full name or designation
  - info: Comprehensive character analysis in Bulgarian including:
    * Physical description and appearance
    * Personality traits and psychological profile
    * Social status, occupation, and background
    * Relationships with other characters
    * Character development and transformation throughout the work
    * Motivations, goals, and internal conflicts
    * Role and function in the plot
    * Symbolic significance or archetypal qualities
    * Key actions and decisions
    * Character's worldview, values, and beliefs
    * Speech patterns or distinctive characteristics
    * Impact on other characters and the story
    * Critical interpretations of the character
  
  IMPORTANT: Include ALL characters that appear in the work:
  - Main protagonists and antagonists
  - Secondary characters with significant roles
  - Minor characters that contribute to the plot or themes
  - Collective characters or groups if applicable
  - Symbolic or allegorical characters
  
  Ensure each character entry is detailed and provides deep literary analysis.
- analysis_summary: A detailed summary synthesizing information from multiple reliable sources, including:
  * Plot overview and structure
  * Literary significance and impact
  * Critical reception and interpretation
  * Style and narrative techniques
  * Historical and cultural context
  * The work's place in the author's oeuvre and literary canon

Search reliable sources such as:
- Academic literary databases and journals
- Literary criticism and analysis websites
- Educational institutions and literature departments
- Established literary critics and scholars
- Reputable book review publications
- Literary encyclopedias and reference works

Provide all information in JSON format. All fields should be in Bulgarian language.
"""
