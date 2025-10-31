# Literature Processing with AI Web Search

This system uses Google's Gemini AI with web search capabilities to automatically gather and structure information about literary works and authors from reliable sources on the internet.

## 🌟 Key Features

- **No Manual Links Required**: Simply provide the work title and author name
- **AI Web Search**: Gemini automatically searches for information from reliable sources
- **Anti-Hallucination**: Explicit instructions to only use verified information
- **Reliable Sources**: AI is instructed to prioritize academic, educational, and reputable literary sources
- **Same Output Format**: Maintains the existing JSON structure for compatibility

## 📋 How It Works

1. **Input**: You provide just the work title and author name in `works.json`
2. **AI Search**: Gemini searches the web for reliable information about:
   - Author biography (birth/death dates, significance, style, legacy)
   - Work details (publication year, genre, themes, motifs, characters)
   - Literary analysis from academic and critical sources
3. **Output**: Structured JSON with all the extracted information in Bulgarian

## 🚀 Usage

### 1. Add Works to `works.json`

Simple format - just title and author name:

```json
{
  "version": "2.0",
  "works": [
    {
      "title": "Под игото",
      "author": {
        "name": "Иван Вазов"
      }
    },
    {
      "title": "Антихрист",
      "author": {
        "name": "Емилиян Станев"
      }
    }
  ]
}
```

### 2. Run the Processing

```bash
cd literature
python main_new.py
```

### 3. Check Results

The AI-generated data will be saved to `results/processed_literature.json` with:
- Author information (name, birth/death years, biographical summary)
- Work analysis (genre, themes, motifs, characters, critical analysis)

## 🎯 What Makes This Better

### Before (with links):
- ❌ Required manual link collection
- ❌ Links could become outdated/broken
- ❌ Limited to the content of those specific links
- ❌ Time-consuming link management

### Now (with AI search):
- ✅ Zero manual link collection
- ✅ Always searches fresh, current information
- ✅ Can access multiple sources automatically
- ✅ AI verifies information from reliable sources
- ✅ Just provide title + author name

## 🛡️ Anti-Hallucination Measures

The system includes explicit instructions to:
1. **Only use verified information** from reliable sources
2. **Search reputable sources**: academic databases, literary journals, educational institutions
3. **Verify facts** from multiple sources when possible
4. **Be transparent** if information cannot be found
5. **Leave fields empty** rather than guessing

## 📊 Output Structure

The output format remains the same as before:

```json
{
  "generated_date": "2025-10-31 14:30:00",
  "works": [
    {
      "work_name": "Под игото",
      "author": {
        "name": "Иван Вазов",
        "year_of_birth": "1850",
        "year_of_death": "1921",
        "information": "Detailed biography in Bulgarian..."
      },
      "analysis": {
        "name": "Под игото",
        "year": "1894",
        "genre": "Роман",
        "themes": [...],
        "motifs": [...],
        "characters": [...],
        "analysis_summary": "Comprehensive analysis..."
      }
    }
  ]
}
```

## 🔧 Configuration

The system uses:
- **Model**: `gemini-2.0-flash-exp` (supports Google Search tool)
- **Search Tool**: `GoogleSearch()` enabled for all queries
- **Output**: JSON with strict schema validation
- **Language**: Bulgarian for all descriptive content

## 📝 Files Overview

- `main_new.py` - Entry point
- `loader_new.py` - Main processing logic
- `gemini_extractor.py` - AI integration with web search
- `prompts.py` - AI instructions with anti-hallucination guidelines
- `schemas.py` - JSON output structure definitions
- `works.json` - Input data (title + author only)
- `results/processed_literature.json` - AI-generated output

## ⚠️ Notes

- Make sure you have a valid Gemini API key configured
- The AI will take longer than before because it searches the web
- Results depend on what information is available online
- All content is in Bulgarian as per configuration
