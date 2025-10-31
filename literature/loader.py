import json
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from google import genai
from google.genai import types

api_key = "AIzaSyCawQtMobmFWgMbTpj3yJhQBqgkIMhLzGU"

class LiteratureLoader:
    def __init__(self, source):
        self.source = source
        self.content = "",
        self.works = []
        with open(self.source, 'r', encoding='utf-8') as file:
            self.content = file.read()

    def load(self):
        print(f"\n📚 Loading works from: {self.source}")
        json_data = json.loads(self.content)
        if 'works' in json_data:
            self.works = json_data['works']
        print(f"✓ Loaded {len(self.works)} work(s)")
        
        return self
    
    def get_link_contents(self):
        print("\n🌐 Starting to scrape content from links...")
        total_links = 0
        successful_scrapes = 0
        for work in self.works:
            work_name = work.get('name', 'Unknown')
            if 'author' in work:
                if 'links' in work['author']:
                    author_links = len(work['author']['links'])
                    total_links += author_links
                    print(f"\n  📖 {work_name} - Author")
                    print(f"     Scraping {author_links} author link(s)...")
                    work["author"]["text"] = ""
                    for i, link in enumerate(work['author']['links'], 1):
                        print(f"     [{i}/{author_links}] {link}")
                        scraped_content = self.scrape_link(link)
                        if scraped_content:
                            work['author']['text'] += scraped_content
                            print(f"     ✓ Scraped {len(scraped_content)} characters")
                            successful_scrapes += 1
                        else:
                            print(f"     ✗ No content scraped")
            if 'analysis' in work:
                work["analysis"]["text"] = ""
                if 'links' in work['analysis']:
                    analysis_links = len(work['analysis']['links'])
                    total_links += analysis_links
                    print(f"\n  📝 {work_name} - Analysis")
                    print(f"     Scraping {analysis_links} analysis link(s)...")
                    for i, link in enumerate(work['analysis']['links'], 1):
                        print(f"     [{i}/{analysis_links}] {link}")
                        scraped_content = self.scrape_link(link)
                        if scraped_content:
                            work['analysis']['text'] += scraped_content
                            print(f"     ✓ Scraped {len(scraped_content)} characters")
                            successful_scrapes += 1
                        else:
                            print(f"     ✗ No content scraped")
        print(f"\n✓ Finished scraping: {successful_scrapes}/{total_links} links successful")


    def scrape_link(self, link):
        """
        Scrapes content from a link, handling both static and client-side rendered pages.
        First tries with requests, falls back to Playwright if needed.
        """
        try:
            text_requests = self._scrape_with_requests(link)
            text = self._scrape_with_playwright(link)

            if text_requests and len(text_requests) > len(text):
                return text_requests    

            return text if text else ""
        except Exception as e:
            print(f"     ⚠️  Failed to scrape (continuing anyway): {str(e)[:100]}")
            return ""

    def _scrape_with_requests(self, link):
        """Try scraping with requests first (faster for static pages)"""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }

        try:
            response = requests.get(link, timeout=10, headers=headers)
            response.raise_for_status() 

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator="\n")
            clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

            return clean_text

        except requests.RequestException as e:
            print(f"Requests failed for {link}: {e}")
            return None

    def _scrape_with_playwright(self, link):
        """Scrape using Playwright for client-side rendered content"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Set a shorter timeout and try multiple times if needed
                try:
                    # Navigate to the page with reduced timeout
                    page.goto(link, wait_until="domcontentloaded", timeout=15000)
                    
                    # Wait a bit for JavaScript to execute
                    time.sleep(1)
                except Exception as goto_error:
                    print(f"     ⚠️  Navigation timeout/error: {str(goto_error)[:80]}")
                    browser.close()
                    return None
                
                # Get the full page content after JavaScript execution
                content = page.content()
                
                browser.close()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                text = soup.get_text(separator="\n")
                clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                
                return clean_text
                
        except Exception as e:
            print(f"Playwright failed for {link}: {e}")
            return None
    
    def extract_author_info_with_gemini(self, author_text, analysis_text):
        """
        Extracts structured author information using Google Gemini API.
        
        Args:
            author_text: Text content about the author
            analysis_text: Additional analysis text that might contain author info
            
        Returns:
            Dictionary with author information (name, year_of_birth, year_of_death, information)
        """
        # Define schema for author information
        author_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "year_of_birth": {"type": "string"},
                "year_of_death": {"type": "string"},
                "information": {"type": "string"}
            },
            "required": ["name", "information"]
        }
        
        # Create the prompt
        prompt = f"""
Based on the following texts about an author, extract and structure the key biographical information:

Author Text:
{author_text}

Analysis Text (may contain additional author context):
{analysis_text}

Please extract:
- name: The full name of the author
- year_of_birth: The year the author was born (if available, otherwise use empty string)
- year_of_death: The year the author died (if available, otherwise use empty string or "present" if still alive)
- information: A concise summary of key biographical information, literary significance, and important facts about the author

Provide the information in JSON format and please use bulgarian language only for the information.
"""
        
        # Call Gemini API
        print(f"    DEBUG: Creating Gemini client...")
        client = genai.Client()
        print(f"    DEBUG: Client created, sending request to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=author_schema,
            ),
        )
        print(f"    DEBUG: Received response from Gemini")
        
        # Return parsed JSON
        return json.loads(response.text)
    
    def extract_work_info_with_gemini(self, work_name, analysis_text):
        """
        Extracts structured literary work information using Google Gemini API.
        
        Args:
            work_name: The name of the literary work
            analysis_text: Text analysis of the work
            
        Returns:
            Dictionary with work information (name, year, motifs, themes, characters, analysis_summary)
        """
        # Define schema for work information
        work_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "year": {"type": "string"},
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
        
        # Create the prompt
        prompt = f"""
Analyze the following literary work and extract structured information:

Work Title: {work_name}

Analysis Text:
{analysis_text}

Please extract and structure the following information:
- name: The title of the literary work
- year: The year of publication (if available, otherwise use empty string)
- motifs: A list of literary motifs in the work. Each motif should have:
  - motif_name: The name of the motif
  - info: A brief explanation of how this motif appears and its significance in the work
- themes: A list of major themes in the work. Each theme should have:
  - theme_name: The name of the theme
  - info: An explanation of how this theme is explored in the work
- characters: A list of main characters. Each character should have:
  - name: The character's name
  - info: Key information about the character, their role, development, and significance
- analysis_summary: A comprehensive summary of the analysis, including the work's significance, style, impact, and key critical insights

Provide the information in JSON format in bulgarian only.
"""
        
        # Call Gemini API
        print(f"    DEBUG: Creating Gemini client...")
        client = genai.Client()
        print(f"    DEBUG: Client created, sending request to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=work_schema,
            ),
        )
        print(f"    DEBUG: Received response from Gemini")
        
        # Return parsed JSON
        return json.loads(response.text)
    
    def process_works_with_gemini(self):
        """
        Process all works using Gemini to extract structured information.
        Updates the works list with extracted data.
        """
        print("\n🤖 Starting Gemini AI extraction...")
        print(f"Processing {len(self.works)} work(s)\n")
        
        for idx, work in enumerate(self.works, 1):
            authors_text = work.get("author", {}).get("text", "")
            analysis_text = work.get("analysis", {}).get("text", "")
            work_name = work.get("name", "Unknown Work")
            
            print(f"[{idx}/{len(self.works)}] Processing: {work_name}")
            print(f"  DEBUG: Author text length: {len(authors_text)} chars")
            print(f"  DEBUG: Analysis text length: {len(analysis_text)} chars")
            
            # Extract author information
            if authors_text or analysis_text:
                print(f"  DEBUG: Condition met for author extraction (has text)")
                try:
                    print(f"  🧑 Extracting author information...")
                    print(f"  DEBUG: Calling Gemini API for author...")
                    author_info = self.extract_author_info_with_gemini(authors_text, analysis_text)
                    print(f"  DEBUG: Gemini response received for author")
                    work["author"]["extracted_info"] = author_info
                    print(f"  ✓ Author: {author_info.get('name', 'Unknown')}")
                except Exception as e:
                    print(f"  ✗ Error extracting author info: {e}")
                    import traceback
                    print(f"  DEBUG: {traceback.format_exc()}")
            else:
                print(f"  ⚠️  Skipping author extraction - no text available")
            
            # Extract work information
            if analysis_text:
                print(f"  DEBUG: Condition met for work analysis extraction")
                try:
                    print(f"  📊 Extracting work analysis...")
                    print(f"  DEBUG: Calling Gemini API for work analysis...")
                    work_info = self.extract_work_info_with_gemini(work_name, analysis_text)
                    print(f"  DEBUG: Gemini response received for work")
                    work["extracted_analysis"] = work_info
                    print(f"  ✓ Extracted {len(work_info.get('themes', []))} themes, "
                          f"{len(work_info.get('motifs', []))} motifs, "
                          f"{len(work_info.get('characters', []))} characters")
                except Exception as e:
                    print(f"  ✗ Error extracting work info: {e}")
                    import traceback
                    print(f"  DEBUG: {traceback.format_exc()}")
            else:
                print(f"  ⚠️  Skipping work analysis - no analysis text available")
            
            print()  # Blank line between works
        
        print("✓ Finished Gemini AI extraction")
        return self.works
    
    def save_to_json(self, output_file="results/processed_literature.json"):
        """
        Saves the processed works data (including extracted author and analysis info) to a JSON file.
        
        Args:
            output_file: Path to the output JSON file (default: results/processed_literature.json)
        """
        import os
        
        print(f"\n💾 Saving processed data...")
        
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
            
            # Add work name if available
            if "name" in work:
                work_data["work_name"] = work["name"]
            
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



    


