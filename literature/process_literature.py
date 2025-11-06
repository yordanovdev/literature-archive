"""
Simple literature processor that extracts information from provided text using AI
"""
import json
from typing import List, Dict, Optional
from google import genai
from prompts import get_extraction_prompt, get_author_research_prompt
from schemas import AuthorInfo, WorkInfo

# Hardcoded API key
GEMINI_API_KEY = ""


class LiteratureProcessor:
    """Process literature works using provided text data"""
    
    def __init__(self, input_file: str):
        """
        Initialize processor with input JSON file
        
        Args:
            input_file: Path to JSON file with format:
                [
                    {"workName": "Title", "text": "content..."},
                    ...
                ]
        """
        self.input_file = input_file
        self.works_data: List[Dict] = []
        self.results: List[Dict] = []
    
    def research_author(self, author_name: str, work_name: str) -> Optional[Dict]:
        """
        Research author information using Gemini with Google Search.
        
        Args:
            author_name: Name of the author
            work_name: Name of the work (for context)
            
        Returns:
            Dictionary with author information or None if failed
        """
        print(f"   🔎 Researching author: {author_name}")
        
        try:
            prompt = get_author_research_prompt(author_name, work_name)
            
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": AuthorInfo,
                }
            )
            
            # Parse JSON response
            author_info = json.loads(response.text)
            print(f"   ✅ Author info retrieved")
            return author_info
            
        except Exception as e:
            print(f"   ⚠️  Could not research author: {e}")
            return {
                "name": author_name,
                "year_of_birth": None,
                "year_of_death": None,
                "information": None
            }
    
    def load(self):
        """Load works data from JSON file"""
        print(f"📖 Loading works from {self.input_file}...")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if it's the works.json format with version and works array
        if isinstance(data, dict) and 'works' in data:
            self.works_data = data['works']
            print(f"✅ Loaded {len(self.works_data)} works from works.json format")
        # Otherwise assume it's already an array
        elif isinstance(data, list):
            self.works_data = data
            print(f"✅ Loaded {len(self.works_data)} works")
        else:
            raise ValueError("Invalid JSON format - expected array or {works: [...]}")
    
    def process_work(self, work: Dict) -> Dict:
        """
        Extract information from a single work using AI
        
        Args:
            work: Dictionary with 'title'/'workName' and 'text' keys
            
        Returns:
            Processed work data with extracted information
        """
        # Support both 'title' (works.json) and 'workName' (literature_data.json)
        work_name = work.get('title') or work.get('workName', 'Unknown')
        text = work.get('text', '')
        author_name = work.get('author', {}).get('name') if isinstance(work.get('author'), dict) else work.get('author', 'Unknown')
        
        print(f"\n🔍 Processing: {work_name}")
        
        if not text or text.strip() == "":
            print(f"⚠️  No text content for '{work_name}', skipping...")
            return {
                "work_name": work_name,
                "author": None,
                "analysis": {
                    "name": work_name,
                    "year": None,
                    "genre": None,
                    "motifs": [],
                    "themes": [],
                    "characters": [],
                    "analysis_summary": ""
                },
                "error": "No text content provided"
            }
        
        try:
            # Step 1: Research author using Google Search
            author_info = self.research_author(author_name, work_name)
            
            # Step 2: Analyze the work text
            prompt = get_extraction_prompt(work_name, text)
            
            print(f"   🤖 Analyzing work with AI...")
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": WorkInfo
                }
            )
            
            # Parse JSON response
            analysis = json.loads(response.text)
            
            # Build final structure matching the required format
            result = {
                "work_name": work_name,
                "author": author_info,
                "analysis": analysis
            }
            
            print(f"   ✅ Successfully processed '{work_name}'")
            return result
            
        except json.JSONDecodeError as e:
            print(f"   ❌ Failed to parse AI response for '{work_name}': {e}")
            return {
                "work_name": work_name,
                "author": None,
                "analysis": {
                    "name": work_name,
                    "year": None,
                    "genre": None,
                    "motifs": [],
                    "themes": [],
                    "characters": [],
                    "analysis_summary": ""
                },
                "error": f"JSON parsing error: {str(e)}"
            }
        except Exception as e:
            print(f"   ❌ Error processing '{work_name}': {e}")
            return {
                "work_name": work_name,
                "author": None,
                "analysis": {
                    "name": work_name,
                    "year": None,
                    "genre": None,
                    "motifs": [],
                    "themes": [],
                    "characters": [],
                    "analysis_summary": ""
                },
                "error": str(e)
            }
    
    def process_all(self, output_file: str = 'results/processed_literature.json'):
        """Process all works and save after each one, skipping already processed works"""
        from pathlib import Path
        Path('results').mkdir(exist_ok=True)
        
        # Load existing results if file exists
        existing_works = set()
        if Path(output_file).exists():
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_results = json.load(f)
                    self.results = existing_results
                    existing_works = {work.get('work_name') for work in existing_results}
                print(f"📂 Loaded {len(existing_works)} existing works from {output_file}")
            except Exception as e:
                print(f"⚠️  Could not load existing results: {e}")
        
        print("\n" + "="*60)
        print("🚀 Starting literature processing")
        print("="*60)
        
        skipped = 0
        processed = 0
        
        for i, work in enumerate(self.works_data, 1):
            work_name = work.get('title') or work.get('workName', 'Unknown')
            
            # Skip if already processed
            if work_name in existing_works:
                print(f"\n[{i}/{len(self.works_data)}] ⏭️  Skipping '{work_name}' (already processed)")
                skipped += 1
                continue
            
            print(f"\n[{i}/{len(self.works_data)}]", end=" ")
            result = self.process_work(work)
            self.results.append(result)
            processed += 1
            
            # Save after each work
            print(f"   💾 Saving progress...")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"   ✅ Progress saved ({len(self.results)} total works)")
        
        print("\n" + "="*60)
        print(f"✅ Processing complete!")
        print(f"   Processed: {processed} new works")
        print(f"   Skipped: {skipped} existing works")
        print(f"   Total: {len(self.results)} works in output")
        print("="*60)
    
    def save_results(self, output_file: str = 'results/processed_literature.json'):
        """Save processed results to JSON file"""
        from pathlib import Path
        Path('results').mkdir(exist_ok=True)
        
        print(f"\n💾 Saving results to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Results saved successfully!")


def main():
    """Main entry point"""
    import sys
    from pathlib import Path
    
    # Get input file from command line or use default
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'works.json'
    
    if not Path(input_file).exists():
        print(f"❌ Error: Input file '{input_file}' not found")
        print(f"\nUsage: python process_literature.py <input_file.json>")
        print(f"\nInput JSON format can be:")
        print("""1. works.json format:
{
  "version": "2.0",
  "works": [
    {"title": "Work Title", "text": "content...", "author": {...}},
    ...
  ]
}

2. Simple array format:
[
  {"workName": "Work Title", "text": "content..."},
  ...
]""")
        return
    
    processor = LiteratureProcessor(input_file)
    processor.load()
    processor.process_all()
    # No need to call save_results separately anymore - it saves after each work
    
    print(f"\n📄 Final results saved to: results/processed_literature.json")


if __name__ == "__main__":
    main()
