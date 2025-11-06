"""
Simplified prompts for literature extraction using provided text
"""

def get_extraction_prompt(work_name: str, text_content: str) -> str:
    """
    Generate prompt for extracting literary work information from provided text.
    
    Args:
        work_name: The name of the literary work
        text_content: The text content about the work
        
    Returns:
        String prompt for Gemini
    """
    return f"""
You are analyzing the literary work: "{work_name}"

You have been provided with text content about this work. Extract and analyze the following information based ONLY on the provided text:

=== TEXT CONTENT ===
{text_content}
=== END OF TEXT CONTENT ===

IMPORTANT INSTRUCTIONS:
1. Extract information ONLY from the provided text above
2. Do not use external knowledge or web search
3. If information is not present in the text, leave fields empty or null
4. Be thorough and detailed in your analysis
5. All responses should be in BULGARIAN language

Please extract and return the following in JSON format:

{{
  "name": "Name of the work",
  "year": "Year of publication (if mentioned, as string)",
  "genre": "Literary genre (e.g., Роман, Повест, Разказ, Стихотворение, Драма, etc.)",
  "motifs": [
    {{
      "motif_name": "Name of motif",
      "info": "Detailed explanation of the motif"
    }}
  ],
  "themes": [
    {{
      "theme_name": "Name of theme",
      "info": "Detailed explanation of the theme based on the text"
    }}
  ],
  "characters": [
    {{
      "name": "Character name",
      "info": "Important character analysis including: physical description, personality, social status, relationships, development, motivations, role in plot, symbolic significance, key actions, values, speech patterns, impact on story"
    }}
  ],
  "analysis_summary": "Comprehensive analysis including: composition, literary significance, style, narrative techniques, historical context mentioned in text, critical interpretations, and overall impact"
}}

IMPORTANT: 
- Extract ALL characters mentioned in the text (main, secondary, minor)
- Identify ALL themes and motifs discussed
- Provide detailed analysis for each element
- Use Bulgarian language for all text fields
- The analysis_summary should be comprehensive and cover all aspects
- Return ONLY valid JSON, no additional text or markdown
"""


def get_author_research_prompt(author_name: str, work_name: str) -> str:
    """
    Generate prompt for researching author information using web search.
    
    Args:
        author_name: The name of the author to research
        work_name: The name of the work (for context)
        
    Returns:
        String prompt for Gemini with grounding
    """
    return f"""
Research the author "{author_name}" who wrote "{work_name}".

Use Google Search to find the most important information about this author and return a JSON with the following structure:

{{
  "name": "Full name of the author",
  "year_of_birth": "Year of birth as string (e.g., \"1962\")",
  "year_of_death": "Year of death as string (e.g., \"1979\") or null if still alive",
  "information": "Small biography in Bulgarian covering: birth place, education, key life events, literary significance and contributions, major works and achievements, writing style and themes, historical/cultural context, critical reception and legacy. Shouldn't be so long to bore the reader."
}}

IMPORTANT:
- Use web search to find accurate factual information
- Years should be strings (e.g., "1962", not numbers)
- The information field should be comprehensive and detailed in Bulgarian
- Cover all aspects: biography, literary contributions, style, themes, historical context, legacy
- Write in a formal, encyclopedic style
- Return ONLY valid JSON, no additional text or markdown
"""