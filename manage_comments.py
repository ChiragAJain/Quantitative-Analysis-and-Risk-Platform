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
        content = f.read()
    
    # Remove single-line comments but preserve strings
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip empty lines and lines that are only comments
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            if stripped:  # Keep structure but remove comment content
                cleaned_lines.append('')
            else:
                cleaned_lines.append(line)
            continue
        
        # Remove inline comments but preserve strings
        in_string = False
        string_char = None
        cleaned_line = ""
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if not in_string and char in ['"', "'"]:
                # Check for triple quotes
                if i + 2 < len(line) and line[i:i+3] in ['"""', "'''"]:
                    # Handle docstrings - remove them entirely
                    if line[i:i+3] == '"""' or line[i:i+3] == "'''":
                        # Skip to end of docstring or line
                        end_quote = line.find(line[i:i+3], i+3)
                        if end_quote != -1:
                            i = end_quote + 3
                            continue
                        else:
                            # Docstring continues to next line, skip rest of line
                            break
                else:
                    # Regular string
                    in_string = True
                    string_char = char
                    cleaned_line += char
            elif in_string and char == string_char:
                # End of string
                in_string = False
                string_char = None
                cleaned_line += char
            elif not in_string and char == '#':
                # Comment found, remove rest of line
                break
            else:
                cleaned_line += char
            
            i += 1
        
        cleaned_lines.append(cleaned_line.rstrip())
    
    # Write cleaned content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
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

files_to_process = [
    'dashboard.py',
    'stock_analyzer.py',
    'start_render.py'
]

print("🧹 Removing comments for clean commit...")
backup_files(files_to_process)

for file_path in files_to_process:
    remove_comments_from_file(file_path)

print("✅ Comments removed! Files ready for commit.")