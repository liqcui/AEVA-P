#!/usr/bin/env python3
"""
Script to update copyright headers to Open Source with Attribution format.

Copyright (c) 2024-2026 AEVA Development Team
Open Source with Attribution Required
Traceable Watermark ID: AEVA-2026-LQC-dc68e33
"""

import os
import sys
from pathlib import Path

OLD_COPYRIGHT = "Copyright (c) 2024-2026 Liquan Cui"
NEW_COPYRIGHT = "Copyright (c) 2024-2026 AEVA Development Team"

OLD_AUTHOR = "Author: Liquan Cui"
NEW_AUTHOR = "Open Source with Attribution Required"

def update_file_copyright(filepath):
    """Update copyright header in a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already updated
        if "AEVA Development Team" in content and "Open Source with Attribution" in content:
            print(f"✓ Already updated: {filepath}")
            return False

        # Update copyright statements
        new_content = content.replace(OLD_COPYRIGHT, NEW_COPYRIGHT)
        new_content = new_content.replace(OLD_AUTHOR, NEW_AUTHOR)

        # Remove specific name references in copyright blocks
        new_content = new_content.replace(
            "This software is the proprietary work of Liquan Cui.",
            "If you use this code, you must notify the original author and provide attribution."
        )
        new_content = new_content.replace(
            "Unauthorized copying, modification, distribution, or use of this software,\nvia any medium, is strictly prohibited without explicit permission.",
            "You must keep the traceable watermark (AEVA-2026-LQC-dc68e33) intact in all derivatives."
        )

        # Only write if content changed
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Updated: {filepath}")
            return True
        else:
            print(f"- No changes: {filepath}")
            return False

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

    for py_file in sorted(py_files):
        if update_file_copyright(py_file):
            modified += 1

    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Modified: {modified}")
    print(f"  Total:    {len(py_files)}")
    print("\n✓ Copyright update complete!")

if __name__ == '__main__':
    main()
