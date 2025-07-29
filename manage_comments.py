#!/usr/bin/env python3
"""
Script to manage comments in Python files for repository commits
"""

import os
import re
import shutil
from pathlib import Path

def backup_files(files_to_process):
    """Create backup copies of files"""
    backup_dir = Path("backup_with_comments")
    backup_dir.mkdir(exist_ok=True)
    
    for file_path in files_to_process:
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_dir / file_path)
            print(f"✅ Backed up: {file_path}")

def remove_comments_from_file(file_path):
    """Remove comments from a Python file"""
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    in_multiline_string = False
    string_delimiter = None
    
    for line in lines:
        original_line = line
        cleaned_line = ""
        i = 0
        
        while i < len(line):
            char = line[i]
            
            # Handle string literals
            if not in_multiline_string and char in ['"', "'"]:
                # Check for triple quotes
                if i + 2 < len(line) and line[i:i+3] in ['"""', "'''"]:
                    if line[i:i+3] == '"""' or line[i:i+3] == "'''":
                        in_multiline_string = True
                        string_delimiter = line[i:i+3]
                        cleaned_line += line[i:i+3]
                        i += 3
                        continue
                else:
                    # Regular string
                    string_delimiter = char
                    cleaned_line += char
                    i += 1
                    # Find the end of the string
                    while i < len(line):
                        cleaned_line += line[i]
                        if line[i] == string_delimiter and (i == 0 or line[i-1] != '\\'):
                            break
                        i += 1
                    i += 1
                    continue
            
            elif in_multiline_string:
                cleaned_line += char
                if i + 2 < len(line) and line[i:i+3] == string_delimiter:
                    cleaned_line += line[i+1:i+3]
                    in_multiline_string = False
                    string_delimiter = None
                    i += 3
                    continue
                i += 1
                continue
            
            # Handle comments
            elif char == '#' and not in_multiline_string:
                # Skip the rest of the line (it's a comment)
                break
            
            else:
                cleaned_line += char
                i += 1
        
        # Keep the line if it has content after removing comments
        cleaned_line = cleaned_line.rstrip()
        if cleaned_line or original_line.strip() == "":
            cleaned_lines.append(cleaned_line + '\n' if cleaned_line else '\n')
    
    # Write cleaned content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"🧹 Removed comments from: {file_path}")

def restore_files_from_backup():
    """Restore files from backup"""
    backup_dir = Path("backup_with_comments")
    
    if not backup_dir.exists():
        print("❌ No backup directory found!")
        return
    
    for backup_file in backup_dir.iterdir():
        if backup_file.is_file():
            original_path = backup_file.name
            shutil.copy2(backup_file, original_path)
            print(f"🔄 Restored: {original_path}")
    
    # Clean up backup directory
    shutil.rmtree(backup_dir)
    print("✅ Backup directory cleaned up")

def main():
    """Main function"""
    files_to_process = [
        'dashboard.py',
        'stock_analyzer.py',
        'start_render.py',
        'run_dashboard.py',
        'deploy.py'
    ]
    
    print("📝 Comment Management Tool")
    print("=" * 40)
    print("1. Remove comments and commit")
    print("2. Restore comments from backup")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        print("\n🔄 Removing comments for commit...")
        backup_files(files_to_process)
        
        for file_path in files_to_process:
            remove_comments_from_file(file_path)
        
        print("\n✅ Comments removed! You can now commit to repository.")
        print("💡 Run this script again with option 2 to restore comments.")
        
    elif choice == '2':
        print("\n🔄 Restoring comments from backup...")
        restore_files_from_backup()
        print("✅ Comments restored!")
        
    elif choice == '3':
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()