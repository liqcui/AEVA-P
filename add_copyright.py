#!/usr/bin/env python3
"""
Script to add copyright headers to all Python files in the AEVA project.

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import os
import sys
from pathlib import Path

COPYRIGHT_HEADER = '''"""
{original_docstring}
Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""'''

SIMPLE_COPYRIGHT = '''# Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
# Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
# Project ID: AEVA-2026-LQC-dc68e33
'''

def has_copyright(content):
    """Check if file already has copyright notice."""
    return 'Copyright (c) 2024-2026 Liquan Cui' in content or 'AEVA-2026-LQC-dc68e33' in content

def extract_docstring(content):
    """Extract the first docstring from file content."""
    lines = content.split('\n')
    if not lines:
        return None, content

    # Check for triple-quoted docstring
    if lines[0].strip().startswith('"""') or lines[0].strip().startswith("'''"):
        quote = '"""' if '"""' in lines[0] else "'''"

        # Single-line docstring
        if lines[0].count(quote) == 2:
            docstring = lines[0].strip().replace(quote, '')
            remaining = '\n'.join(lines[1:])
            return docstring, remaining

        # Multi-line docstring
        for i in range(1, len(lines)):
            if quote in lines[i]:
                docstring_lines = lines[1:i]
                docstring = '\n'.join(docstring_lines).strip()
                remaining = '\n'.join(lines[i+1:])
                return docstring, remaining

    return None, content

def add_copyright_to_file(filepath):
    """Add copyright header to a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has copyright
        if has_copyright(content):
            print(f"✓ Already has copyright: {filepath}")
            return False

        # Extract docstring
        docstring, remaining_content = extract_docstring(content)

        # Build new content
        if docstring:
            # Has docstring - merge with copyright
            new_docstring = f'''"""
{docstring}

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""'''
            new_content = new_docstring + '\n' + remaining_content
        else:
            # No docstring - add simple copyright comment at top
            new_content = SIMPLE_COPYRIGHT + '\n' + content

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ Added copyright: {filepath}")
        return True

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all Python files."""
    project_root = Path(__file__).parent
    aeva_dir = project_root / 'aeva'

    if not aeva_dir.exists():
        print(f"Error: aeva directory not found at {aeva_dir}")
        sys.exit(1)

    # Find all Python files
    py_files = list(aeva_dir.rglob('*.py'))

    print(f"Found {len(py_files)} Python files in aeva/")
    print("=" * 60)

    modified = 0
    skipped = 0

    for py_file in sorted(py_files):
        if add_copyright_to_file(py_file):
            modified += 1
        else:
            skipped += 1

    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Modified: {modified}")
    print(f"  Skipped:  {skipped}")
    print(f"  Total:    {len(py_files)}")
    print("\n✓ Copyright watermarking complete!")

if __name__ == '__main__':
    main()
