#!/usr/bin/env python3
"""
Interactive script to add works to works.json
Prompts user for work details and content, then updates the JSON file.
"""
import json
import os
import sys


def print_header():
    """Print a nice header for the script"""
    print("\n" + "="*60)
    print("   📚 Add Work to SchoolArchive Literature Database")
    print("="*60 + "\n")


def get_multiline_input(prompt):
    """
    Get multiline input from user.
    User can paste large blocks of text and end with Ctrl+D (Unix) or Ctrl+Z (Windows).
    """
    print(prompt)
    print("(Paste your content below. Press Ctrl+D on Unix/Mac or Ctrl+Z then Enter on Windows when done)")
    print("-" * 60)
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    print("-" * 60)
    content = "\n".join(lines).strip()
    print(f"✓ Captured {len(content)} characters\n")
    return content


def get_input(prompt, required=True, default=""):
    """Get single line input from user"""
    while True:
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        elif not required:
            return default
        else:
            print("  ⚠️  This field is required. Please enter a value.")


def load_works_json(filepath="works.json"):
    """Load the existing works.json file"""
    if not os.path.exists(filepath):
        print(f"⚠️  Warning: {filepath} not found. Creating new file.")
        return {"version": "1.0", "works": []}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error reading {filepath}: {e}")
        sys.exit(1)


def save_works_json(data, filepath="works.json"):
    """Save the updated works data to JSON file"""
    # Create backup
    if os.path.exists(filepath):
        backup_path = filepath + ".backup"
        with open(filepath, 'r', encoding='utf-8') as f:
            backup_data = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_data)
        print(f"  💾 Backup created: {backup_path}")
    
    # Save the new data
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Saved to {filepath}")


def main():
    """Main function to run the interactive script"""
    print_header()
    
    # Get work details
    print("📖 Work Information")
    print("-" * 60)
    title = get_input("Work Title", required=True)
    author_name = get_input("Author Name", required=True)
    print()
    
    # Get author content
    print("👤 Author Content")
    print("-" * 60)
    author_content_choice = get_input("Do you want to add author content? (y/n)", required=False, default="n")
    author_content = ""
    if author_content_choice.lower() in ['y', 'yes']:
        author_content = get_multiline_input("\n📝 Author Content:")
    
    # Get author links
    print("🔗 Author Links (optional)")
    print("-" * 60)
    author_links = []
    while True:
        link = get_input("Enter author link (or press Enter to skip)", required=False)
        if not link:
            break
        author_links.append(link)
        print(f"  ✓ Added link")
    print()
    
    # Get analysis content
    print("📊 Analysis Content")
    print("-" * 60)
    analysis_content_choice = get_input("Do you want to add analysis content? (y/n)", required=False, default="n")
    analysis_content = ""
    if analysis_content_choice.lower() in ['y', 'yes']:
        analysis_content = get_multiline_input("\n📝 Analysis Content:")
    
    # Get analysis links
    print("🔗 Analysis Links (optional)")
    print("-" * 60)
    analysis_links = []
    while True:
        link = get_input("Enter analysis link (or press Enter to skip)", required=False)
        if not link:
            break
        analysis_links.append(link)
        print(f"  ✓ Added link")
    print()
    
    # Create the work entry
    work_entry = {
        "title": title,
        "author": {
            "name": author_name,
            "links": author_links,
            "content": author_content
        },
        "analysis": {
            "links": analysis_links,
            "content": analysis_content
        }
    }
    
    # Show summary
    print("\n" + "="*60)
    print("📋 Summary of New Work Entry")
    print("="*60)
    print(f"Title:              {title}")
    print(f"Author:             {author_name}")
    print(f"Author Content:     {len(author_content)} characters")
    print(f"Author Links:       {len(author_links)}")
    print(f"Analysis Content:   {len(analysis_content)} characters")
    print(f"Analysis Links:     {len(analysis_links)}")
    print("="*60 + "\n")
    
    # Confirm
    confirm = get_input("Add this work to works.json? (y/n)", required=False, default="y")
    if confirm.lower() not in ['y', 'yes']:
        print("❌ Cancelled. No changes made.")
        return
    
    # Load existing works
    print("\n📂 Loading works.json...")
    works_data = load_works_json()
    
    # Add new work
    works_data["works"].append(work_entry)
    
    # Save
    print("\n💾 Saving...")
    save_works_json(works_data)
    
    print("\n" + "="*60)
    print(f"✅ Success! Added '{title}' to works.json")
    print(f"   Total works: {len(works_data['works'])}")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
