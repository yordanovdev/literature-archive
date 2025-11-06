"""
Interactive script to add text content to works from works.json
Opens a text editor for each work to handle large text input
"""
import json
import tempfile
import subprocess
from pathlib import Path


def load_works_json(filepath):
    """Load the works.json file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('works', [])


def save_works_json(filepath, works):
    """Save back to works.json"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data['works'] = works
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved to {filepath}")


def open_editor(initial_text=""):
    """Open text editor for input"""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tf:
        tf.write(initial_text)
        temp_path = tf.name
    
    # Try different editors in order of preference
    editors = ['nano', 'vim', 'vi']
    
    for editor in editors:
        try:
            subprocess.run([editor, temp_path], check=True)
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    # Read the edited content
    with open(temp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean up
    Path(temp_path).unlink()
    
    return content


def add_text_to_works(filepath='works.json'):
    """Interactive function to add text to each work"""
    
    # Load existing data
    print(f"📖 Loading works from {filepath}...")
    works = load_works_json(filepath)
    
    print(f"Found {len(works)} works\n")
    print("="*60)
    print("INSTRUCTIONS:")
    print("- For each work, a text editor will open")
    print("- Paste or type your text")
    print("- Save and exit the editor (Ctrl+X in nano, :wq in vim)")
    print("- Type 'SKIP' to skip a work")
    print("- Type 'QUIT' to save and exit")
    print("="*60)
    print()
    
    for i, work in enumerate(works, 1):
        work_name = work.get('title', 'Unknown')
        current_text = work.get('text', '')
        
        print(f"\n{'='*60}")
        print(f"Work {i}/{len(works)}: {work_name}")
        print(f"{'='*60}")
        
        if current_text and current_text.strip():
            print(f"📝 Current text exists ({len(current_text)} chars)")
            print(f"   First 200 chars: {current_text[:200]}...")
            print()
            choice = input("(E)dit existing / (R)eplace / (S)kip? [E/r/s]: ").strip().lower()
            
            if choice == 's':
                print("⏭️  Skipping...")
                continue
            elif choice == 'q':
                print("\n💾 Saving and exiting...")
                save_works_json(filepath, works)
                return
            elif choice == 'r':
                initial = ""
            else:
                initial = current_text
        else:
            initial = ""
            choice = input(f"Add text for '{work_name}'? (Y/n/quit): ").strip().lower()
            if choice == 'n':
                print("⏭️  Skipping...")
                continue
            elif choice == 'quit':
                print("\n💾 Saving and exiting...")
                save_works_json(filepath, works)
                return
        
        print(f"\n✍️  Opening editor for '{work_name}'...")
        print("Paste your text, then save and exit the editor")
        input("Press Enter to open editor...")
        
        try:
            text = open_editor(initial)
            
            if text.strip():
                work['text'] = text.strip()
                print(f"✅ Added {len(text)} characters")
            else:
                print("⚠️  No text entered")
            
            # Save after each work
            save_works_json(filepath, works)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Skipping this work...")
            continue
    
    print(f"\n{'='*60}")
    print("🎉 All works processed!")
    print(f"{'='*60}")


def main():
    """Main entry point"""
    import sys
    
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'works.json'
    
    print("\n" + "="*60)
    print("📚 Interactive Text Entry for Literature Works")
    print("="*60)
    print(f"File: {filepath}\n")
    
    add_text_to_works(filepath)


if __name__ == "__main__":
    main()
