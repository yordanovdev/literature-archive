# Literature Processing System

A modular system for scraping, processing, and extracting structured information from literary works using AI.

## 📁 Project Structure

```
literature/
├── main_new.py           # Main entry point
├── loader_new.py         # Core loader class
├── scraper.py            # Web scraping functionality
├── gemini_extractor.py   # Gemini AI integration
├── prompts.py            # AI prompts for extraction
├── schemas.py            # JSON schemas for API responses
├── add_work.py           # Interactive script to add works
├── works.json            # Input data (works to process)
└── results/              # Output directory for processed data
    └── processed_literature.json
```

## 🔧 Module Overview

### `main_new.py`
Entry point for the application. Orchestrates the entire processing pipeline.

### `loader_new.py`
Main `LiteratureLoader` class that coordinates:
- Loading works from JSON
- Processing content from both links and manual content fields
- Extracting information with AI (only when content is available)
- Saving processed results

### `scraper.py`
`WebScraper` class that handles:
- Web scraping using Playwright
- Fallback to requests for static pages
- Error handling and timeout management
- Content cleaning and extraction

### `gemini_extractor.py`
`GeminiExtractor` class that manages:
- Gemini API client initialization
- Author information extraction
- Literary work analysis extraction
- JSON response parsing

### `prompts.py`
Contains prompt templates for:
- `get_author_extraction_prompt()` - Extract author biographical data
- `get_work_extraction_prompt()` - Extract work analysis (themes, motifs, characters)

### `add_work.py`
Interactive script to add new works to `works.json`:
- Prompts for work title and author
- Accepts multiline content input for author and analysis
- Supports adding links (optional)
- Creates automatic backups
- Genre is automatically extracted by Gemini AI during processing

### `schemas.py`
JSON schemas defining the structure for:
- `AUTHOR_SCHEMA` - Author information structure
- `WORK_SCHEMA` - Literary work analysis structure

## 🚀 Usage

### Adding New Works

Use the interactive script to add works to your database:

```bash
cd literature
python3 add_work.py
```

The script will prompt you for:
1. Work title and genre
2. Author name
3. Author content (paste large blocks of text)
4. Author links (optional)
5. Analysis content (paste large blocks of text)
6. Analysis links (optional)

**Tips:**
- You can paste entire documents when prompted for content
- Press `Ctrl+D` (Unix/Mac) or `Ctrl+Z` then Enter (Windows) to finish pasting
- The script creates a backup before saving
- Content field is preferred over links for better control

### Processing Works

Run the full pipeline to process all works:

```bash
python3 main_new.py
```

**Note:** The Gemini API will only be called for works that have content (either from the `content` field or scraped from `links`). Works without any content will be skipped, saving API costs.

## 📊 Data Flow

1. **Load** → Read works from `works.json`
2. **Process Content** → Combine content from both `content` fields and scraped `links`
3. **Extract** → Use Gemini AI to extract structured information (only if content exists)
4. **Save** → Export processed data to JSON

## 📝 works.json Structure

Each work entry supports both manual content and links:

```json
{
  "title": "Work Title",
  "author": {
    "name": "Author Name",
    "links": ["https://example.com/author"],
    "content": "Paste large blocks of text here..."
  },
  "analysis": {
    "links": ["https://example.com/analysis"],
    "content": "Analysis text can be pasted here..."
  }
}
```

**Note**: The `genre` field is not stored in the input JSON. Instead, it is automatically extracted by Gemini AI during the analysis phase and included in the processed output.

**Content Priority:**
1. Content from `content` field is added first
2. Then content scraped from `links` is appended
3. Both sources are combined for Gemini processing

## 🔑 Environment Setup

Make sure to set your Gemini API key:

```bash
export GOOGLE_API_KEY="your-api-key-here"
# or
export GEMINI_API_KEY="your-api-key-here"
```

## � Output Format

The processed JSON includes:
- **Author**: name, birth/death years, biographical information
- **Work Analysis**: name, year, genre (auto-extracted), themes, motifs, characters, summary

## 🛠️ Dependencies

- `google-genai` - Gemini API client
- `playwright` - Web scraping
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
