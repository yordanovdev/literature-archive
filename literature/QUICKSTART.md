# Quick Start Guide

## Adding a New Work to the Database

### Step 1: Run the add_work.py script

```bash
cd literature
python3 add_work.py
```

### Step 2: Follow the prompts

The script will ask you for:

#### 1. Work Information
```
Work Title: Под игото
Author Name: Иван Вазов
```

> **Note**: Genre is automatically extracted by Gemini AI during processing, so you don't need to specify it manually.

#### 2. Author Content
When prompted, you can paste large blocks of text about the author. Example:

```
Do you want to add author content? (y/n): y

📝 Author Content:
(Paste your content below. Press Ctrl+D on Unix/Mac or Ctrl+Z then Enter on Windows when done)
------------------------------------------------------------
Иван Минчов Вазов е роден на 27 юни 1850 г. в Сопот. Завършва 
училище в родния си град, след което учи в Пловдив при Ботьо Петков 
и Найден Геров. Работи като учител в Сопот и Варна.

Първите си стихотворения публикува във вестник "Знание" през 1870 г...
(press Ctrl+D here)
------------------------------------------------------------
✓ Captured 245 characters
```

#### 3. Author Links (Optional)
```
🔗 Author Links (optional)
------------------------------------------------------------
Enter author link (or press Enter to skip): https://bglit.com/ivan-vazov
  ✓ Added link
Enter author link (or press Enter to skip): [press Enter to skip]
```

#### 4. Analysis Content
Similar to author content - paste your analysis text:

```
Do you want to add analysis content? (y/n): y

📝 Analysis Content:
------------------------------------------------------------
"Под игото" е исторически роман, който разказва за живота на 
българите в навечерието на Априлското въстание през 1876 г...
(press Ctrl+D)
------------------------------------------------------------
✓ Captured 512 characters
```

#### 5. Analysis Links (Optional)
```
🔗 Analysis Links (optional)
------------------------------------------------------------
Enter analysis link (or press Enter to skip): [press Enter]
```

### Step 3: Confirm and Save

The script will show you a summary:

```
============================================================
📋 Summary of New Work Entry
============================================================
Title:              Под игото
Author:             Иван Вазов
Author Content:     245 characters
Author Links:       1
Analysis Content:   512 characters
Analysis Links:     0
============================================================

Add this work to works.json? (y/n): y

📂 Loading works.json...

💾 Saving...
  💾 Backup created: works.json.backup
  ✓ Saved to works.json

============================================================
✅ Success! Added 'Под игото' to works.json
   Total works: 17
============================================================
```

## Processing Works with Gemini AI

Once you've added works to `works.json`, process them with:

```bash
python3 main_new.py
```

### What Happens:

1. **Load Phase**: Reads all works from works.json
2. **Content Processing**: 
   - Adds content from `content` fields
   - Scrapes content from any `links`
   - Combines both sources
3. **Gemini Extraction** (only if content exists):
   - Extracts author biographical info
   - Extracts work analysis (themes, motifs, characters)
4. **Save**: Exports to `results/processed_literature.json`

### Example Output:

```
📚 Loading works from: works.json
✓ Loaded 17 work(s)

🌐 Starting to process content from links and content fields...

  📖 Под игото - Author
     ✓ Added 245 characters from content field
     Scraping 1 author link(s)...
     [1/1] https://bglit.com/ivan-vazov
     ✓ Scraped 3421 characters

  📝 Под игото - Analysis
     ✓ Added 512 characters from content field

✓ Finished scraping: 1/1 links successful

🤖 Starting Gemini AI extraction...
Processing 17 work(s)

[1/17] Processing: Под игото
  DEBUG: Author text length: 3666 chars
  DEBUG: Analysis text length: 512 chars
  🧑 Extracting author information...
  ✓ Author: Иван Вазов
  📊 Extracting work analysis...
  ✓ Extracted 5 themes, 8 motifs, 12 characters

[2/17] Processing: Железният светилник
  DEBUG: Author text length: 0 chars
  DEBUG: Analysis text length: 0 chars
  ⚠️  Skipping - no content available (no links or content field provided)

...

✓ Finished Gemini AI extraction

💾 Saving processed data...
✓ Successfully saved processed data to: results/processed_literature.json
  Total works processed: 17
```

## Tips

### ✅ Best Practices

1. **Use Content Field for Manual Input**: If you have text ready, paste it into the content field rather than using links
2. **Combine Both**: You can use both content and links - they'll be combined
3. **Skip Empty Works**: Works without any content won't waste Gemini API calls
4. **Backup Created**: The script automatically creates `works.json.backup` before saving

### ⚠️ Common Issues

**Issue**: "Ctrl+D doesn't work"
- **Solution**: On Windows, use `Ctrl+Z` then press Enter

**Issue**: "Script can't find works.json"
- **Solution**: Make sure you're in the `literature/` directory when running the script

**Issue**: "Gemini API errors"
- **Solution**: Make sure you have content (either in content field or links). Empty works are now automatically skipped!

## File Structure

After adding a work, your `works.json` will look like:

```json
{
  "version": "1.0",
  "works": [
    {
      "title": "Под игото",
      "author": {
        "name": "Иван Вазов",
        "links": ["https://bglit.com/ivan-vazov"],
        "content": "Иван Минчов Вазов е роден..."
      },
      "analysis": {
        "links": [],
        "content": "\"Под игото\" е исторически роман..."
      }
    }
  ]
}
```

> **Note**: The `genre` field is not stored in `works.json`. Instead, Gemini AI automatically extracts it during processing based on the analysis text.

The processed output in `results/processed_literature.json` will contain extracted data:

```json
{
  "generated_date": "2025-10-30 14:23:45",
  "works": [
    {
      "work_name": "Под игото",
      "author": {
        "name": "Иван Минчов Вазов",
        "year_of_birth": 1850,
        "year_of_death": 1921,
        "information": "Български поет и писател..."
      },
      "analysis": {
        "name": "Под игото",
        "year": 1894,
        "genre": "Роман",
        "themes": ["Национално освобождение", "Героизъм", ...],
        "motifs": ["Поробеността", "Свободата", ...],
        "characters": [...],
        "summary": "..."
      }
    }
  ]
}
```
