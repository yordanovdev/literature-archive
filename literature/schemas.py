"""
JSON Schemas for Gemini API responses
"""

# Schema for author information extraction
AUTHOR_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "year_of_birth": {"type": "string"},
        "year_of_death": {"type": "string"},
        "information": {"type": "string"}
    },
    "required": ["name", "information"]
}

# Schema for literary work information extraction
WORK_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "year": {"type": "string"},
        "genre": {"type": "string"},
        "motifs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "motif_name": {"type": "string"},
                    "info": {"type": "string"}
                },
                "required": ["motif_name", "info"]
            }
        },
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme_name": {"type": "string"},
                    "info": {"type": "string"}
                },
                "required": ["theme_name", "info"]
            }
        },
        "characters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "info": {"type": "string"}
                },
                "required": ["name", "info"]
            }
        },
        "analysis_summary": {"type": "string"}
    },
    "required": ["name", "analysis_summary"]
}
