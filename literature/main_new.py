"""
Main entry point for literature processing with AI web search
"""
from loader_new import LiteratureLoader


def main():
    """Process literature works: use AI with web search to extract and save results"""
    literature = LiteratureLoader('works.json')
    literature.load()
    literature.process_works_with_gemini()
    literature.save_to_json()


if __name__ == "__main__":
    main()
