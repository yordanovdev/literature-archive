"""
Literature Loader - Main class for loading and processing literature data with AI web search
"""
import json
import os
import time
from gemini_extractor import GeminiExtractor


class LiteratureLoader:
    """Main class for loading and processing literature data using Gemini with web search"""
    
    def __init__(self, source):
        """
        Initialize the loader.
        
        Args:
            source: Path to the JSON file containing works data
        """
        self.source = source
        self.content = ""
        self.works = []
        self.gemini = GeminiExtractor()
        self.author_cache = {}  # Cache for author information {author_name: author_info}
        self.processed_works_cache = {}  # Cache for already processed works {work_title: work_data}
        self.output_file = "results/processed_literature.json"
        
        with open(self.source, 'r', encoding='utf-8') as file:
            self.content = file.read()
        
        # Load existing processed works if available
        self._load_existing_processed_works()
    
    def _load_existing_processed_works(self):
        """Load existing processed works from the output file to avoid re-processing."""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'works' in data:
                        for work in data['works']:
                            work_name = work.get('work_name')
                            if work_name:
                                self.processed_works_cache[work_name] = work
                                # Also cache author info if available
                                if 'author' in work and 'name' in work['author']:
                                    author_name = work['author']['name']
                                    if author_name not in self.author_cache:
                                        self.author_cache[author_name] = work['author']
                        print(f"📦 Loaded {len(self.processed_works_cache)} previously processed works from cache")
                        print(f"📦 Loaded {len(self.author_cache)} authors from cache")
            except Exception as e:
                print(f"⚠️  Could not load existing processed works: {e}")

    def load(self):
        """
        Load works from the source JSON file.
        
        Returns:
            self for method chaining
        """
        print(f"\n📚 Loading works from: {self.source}")
        json_data = json.loads(self.content)
        if 'works' in json_data:
            self.works = json_data['works']
        print(f"✓ Loaded {len(self.works)} work(s)")
        
        return self
    
    def process_works_with_gemini(self):
        """
        Process all works using Gemini with web search to extract structured information.
        The AI will search the web for reliable information about each work and author.
        Skips works that are already processed and saves progress after each work.
        Updates the works list with extracted data.
        
        Returns:
            The processed works list
        """
        print("\n🤖 Starting Gemini AI extraction with web search...")
        print(f"Processing {len(self.works)} work(s)\n")
        
        processed_count = 0
        skipped_count = 0
        
        for idx, work in enumerate(self.works, 1):
            work_title = work.get("title", "Unknown Work")
            author_name = work.get("author", {}).get("name", "Unknown Author")
            
            print(f"[{idx}/{len(self.works)}] Processing: {work_title} by {author_name}")
            
            # Check if this work is already processed
            if work_title in self.processed_works_cache:
                print(f"  ⏭️  Skipping - already processed")
                # Use cached data
                cached_work = self.processed_works_cache[work_title]
                if "author" in cached_work:
                    if "author" not in work:
                        work["author"] = {}
                    work["author"]["extracted_info"] = cached_work["author"]
                if "analysis" in cached_work:
                    work["extracted_analysis"] = cached_work["analysis"]
                skipped_count += 1
                print()
                continue
            
            # Extract author information using web search
            author_extracted = False
            try:
                # Check if we already have this author's info cached
                if author_name in self.author_cache:
                    print(f"  📦 Using cached author information: {author_name}")
                    author_info = self.author_cache[author_name]
                else:
                    print(f"  🔍 Searching for author information: {author_name}")
                    print(f"  DEBUG: Calling Gemini API with search for author...")
                    author_info = self.gemini.extract_author_info(author_name)
                    print(f"  DEBUG: Gemini response received for author")
                    # Cache the author info for future use
                    self.author_cache[author_name] = author_info
                
                # Initialize author dict if it doesn't exist
                if "author" not in work:
                    work["author"] = {}
                work["author"]["extracted_info"] = author_info
                print(f"  ✓ Author: {author_info.get('name', 'Unknown')}")
                author_extracted = True
            except Exception as e:
                print(f"  ✗ Error extracting author info: {e}")
                import traceback
                print(f"  DEBUG: {traceback.format_exc()}")
            
            # Extract work information using web search
            work_extracted = False
            try:
                print(f"  🔍 Searching for work analysis: {work_title}")
                print(f"  DEBUG: Calling Gemini API with search for work analysis...")
                work_info = self.gemini.extract_work_info(work_title, author_name)
                print(f"  DEBUG: Gemini response received for work")
                work["extracted_analysis"] = work_info
                print(f"  ✓ Extracted {len(work_info.get('themes', []))} themes, "
                      f"{len(work_info.get('motifs', []))} motifs, "
                      f"{len(work_info.get('characters', []))} characters")
                work_extracted = True
            except Exception as e:
                print(f"  ✗ Error extracting work info: {e}")
                import traceback
                print(f"  DEBUG: {traceback.format_exc()}")
            
            # If we successfully extracted data, save it immediately as backup
            if author_extracted or work_extracted:
                processed_count += 1
                try:
                    print(f"  💾 Saving progress...")
                    self._save_backup()
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not save backup: {e}")
            
            print()  # Blank line between works
        
        print("✓ Finished Gemini AI extraction")
        print(f"📊 Statistics:")
        print(f"   - Newly processed: {processed_count}")
        print(f"   - Skipped (already done): {skipped_count}")
        print(f"   - Unique authors cached: {len(self.author_cache)}")
        return self.works
    
    def _save_backup(self):
        """Save current progress as backup (internal method)."""
        # Extract only the Gemini-generated data
        processed_works = []
        for work in self.works:
            work_data = {}
            
            # Add work title if available
            if "title" in work:
                work_data["work_name"] = work["title"]
            
            # Add only the extracted author info from Gemini
            if "author" in work and "extracted_info" in work["author"]:
                work_data["author"] = work["author"]["extracted_info"]
            
            # Add only the extracted analysis from Gemini
            if "extracted_analysis" in work:
                work_data["analysis"] = work["extracted_analysis"]
            
            # Only add if it has some processed data
            if "author" in work_data or "analysis" in work_data:
                processed_works.append(work_data)
        
        # Prepare the data structure with only Gemini-generated content
        output_data = {
            "generated_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "works": processed_works
        }
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write to JSON file with proper formatting
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    def save_to_json(self, output_file="results/processed_literature.json"):
        """
        Save the processed works data (only Gemini-generated content) to a JSON file.
        
        Args:
            output_file: Path to the output JSON file (default: results/processed_literature.json)
            
        Returns:
            Path to the saved file
        """
        print(f"\n💾 Saving final processed data...")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"  Created directory: {output_dir}")
        
        # Extract only the Gemini-generated data
        print(f"  Extracting Gemini-generated content...")
        processed_works = []
        for work in self.works:
            work_data = {}
            
            # Add work title if available
            if "title" in work:
                work_data["work_name"] = work["title"]
            
            # Add only the extracted author info from Gemini
            if "author" in work and "extracted_info" in work["author"]:
                work_data["author"] = work["author"]["extracted_info"]
            
            # Add only the extracted analysis from Gemini
            if "extracted_analysis" in work:
                work_data["analysis"] = work["extracted_analysis"]
            
            processed_works.append(work_data)
        
        # Prepare the data structure with only Gemini-generated content
        output_data = {
            "generated_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "works": processed_works
        }
        
        print(f"  Writing to file: {output_file}")
        # Write to JSON file with proper formatting
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully saved processed data to: {output_file}")
        print(f"  Total works processed: {len(processed_works)}")
        
        return output_file
