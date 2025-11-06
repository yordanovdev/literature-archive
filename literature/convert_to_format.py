"""
Simple script to convert works.json and doc.txt into the proper JSON format using Gemini AI
"""
import json
from google import genai

# Hardcoded API key
GEMINI_API_KEY = "AIzaSyAj0cL_6Sqc79iVBDfg7cPv8WIaxZS_XQ0"


def load_works_json(filepath):
    """Load the works.json file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('works', [])


def load_doc_txt(filepath):
    """Load the doc.txt file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def create_conversion_prompt(works_list, doc_content):
    """Create the prompt for Gemini to convert the data"""
    works_json = json.dumps(works_list, ensure_ascii=False, indent=2)
    
    return f"""
You are given two pieces of information:

1. A JSON list of literary works with titles and authors:
{works_json}

2. A text document containing detailed analysis and information about these works:
{doc_content[:20000]}... (content truncated for brevity, but you have access to the full text)

YOUR TASK:
Convert this into a JSON array with the following format:
[
  {{
    "workName": "Title of the work",
    "text": "Full text content about this work from the document"
  }},
  ...
]

INSTRUCTIONS:
1. For each work in the JSON list, find the corresponding text in the document
2. The document contains sections that start with work titles (like "Димитър Талев - Железният светилник")
3. Extract ALL the text that belongs to each work
4. If a work has no text in the document, set "text" to an empty string ""
5. Match work titles carefully - some may have slight variations
6. Return ONLY the JSON array, no additional text or markdown

IMPORTANT:
- Include ALL works from the JSON list, even if they have no text
- Extract complete text sections for each work
- Preserve all Bulgarian text exactly as written
- Return valid JSON that can be parsed

Here's the FULL document text:
{doc_content}

Now generate the JSON array:
"""


def convert_with_gemini(works_file, doc_file, output_file='literature_data.json'):
    """Main conversion function"""
    print("🚀 Starting conversion process...")
    
    # Load data
    print(f"📖 Loading works from {works_file}...")
    works = load_works_json(works_file)
    print(f"✅ Loaded {len(works)} works")
    
    print(f"📄 Loading document from {doc_file}...")
    doc_content = load_doc_txt(doc_file)
    print(f"✅ Loaded document ({len(doc_content)} characters)")
    
    # Create prompt
    print("💭 Creating conversion prompt...")
    prompt = create_conversion_prompt(works, doc_content)
    
    # Call Gemini API
    print("⏳ Calling Gemini API (this may take a minute)...")
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Extract text from response
        response_text = response.text.strip()
        
    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        return
    
    # Parse response
    print("📝 Processing response...")
    
    # Remove markdown code blocks if present
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.startswith('```'):
        response_text = response_text[3:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    
    response_text = response_text.strip()
    
    # Parse JSON
    try:
        result = json.loads(response_text)
        print(f"✅ Successfully parsed {len(result)} works")
        
        # Save to file
        print(f"💾 Saving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Conversion complete! Output saved to {output_file}")
        print(f"\n📊 Summary:")
        print(f"   Total works: {len(result)}")
        
        # Count works with text
        works_with_text = sum(1 for work in result if work.get('text', '').strip())
        print(f"   Works with text: {works_with_text}")
        print(f"   Works without text: {len(result) - works_with_text}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON response: {e}")
        print(f"\n📄 Raw response (first 500 chars):")
        print(response_text[:500])
        
        # Save raw response for debugging
        with open('gemini_response.txt', 'w', encoding='utf-8') as f:
            f.write(response_text)
        print(f"\n💾 Full response saved to gemini_response.txt for debugging")


def main():
    """Main entry point"""
    import sys
    from pathlib import Path
    
    # Default files
    works_file = 'works.json'
    doc_file = 'sources/doc.txt'
    output_file = 'literature_data.json'
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        works_file = sys.argv[1]
    if len(sys.argv) > 2:
        doc_file = sys.argv[2]
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    
    # Check files exist
    if not Path(works_file).exists():
        print(f"❌ Error: {works_file} not found")
        return
    
    if not Path(doc_file).exists():
        print(f"❌ Error: {doc_file} not found")
        return
    
    print("="*60)
    print("📚 Literature Data Converter")
    print("="*60)
    print(f"Works file: {works_file}")
    print(f"Document file: {doc_file}")
    print(f"Output file: {output_file}")
    print("="*60)
    print()
    
    convert_with_gemini(works_file, doc_file, output_file)


if __name__ == "__main__":
    main()
