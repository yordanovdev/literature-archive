"""
Main entry point for literature processing with AI web search and document-based analysis
"""
from loader_new import LiteratureLoader
import sys


def main():
    """
    Process literature works: use AI with web search and document context to extract and save results.
    
    Usage:
        python main_new.py                              # Use web search only
        python main_new.py document.txt                 # Use document + web search
    """
    # Check if document path is provided
    if len(sys.argv) >= 2:
        doc_path = sys.argv[1]
        print(f"🎯 Mode: Document-based analysis with web search supplement")
        print(f"   Document: {doc_path}")
        literature = LiteratureLoader('works.json', doc_path=doc_path)
    else:
        print(f"🌐 Mode: Web search only")
        print(f"   Tip: To use document-based analysis, run:")
        print(f"        python main_new.py <document.txt>")
        literature = LiteratureLoader('works.json')
    
    literature.load()
    literature.process_works_with_gemini()
    literature.save_to_json()


if __name__ == "__main__":
    main()
