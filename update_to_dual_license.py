#!/usr/bin/env python3
"""
Update copyright headers to Dual License format.
"""

import os
from pathlib import Path

def update_file(filepath):
    """Update copyright header in a Python file to dual license."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has dual license
        if "Dual License" in content or ("Commercial" in content and "permission" in content.lower()):
            print(f"✓ Already dual license: {filepath}")
            return False

        # Replace old copyright patterns
        replacements = [
            # Update open source attribution to dual license
            (
                "Open Source with Attribution Required",
                "Dual License: Free for Personal/Academic, Commercial Requires Permission"
            ),
            (
                "Open Source with Attribution",
                "Dual License"
            ),
            # Update instructions
            (
                "If you use this code, you must notify the original author and provide attribution.",
                "If you use this code, you must:\n1. Notify the original author\n2. Provide attribution in your project\n3. Keep this watermark intact\n4. For commercial use: Obtain written permission"
            ),
            (
                "You must keep the traceable watermark (AEVA-2026-LQC-dc68e33) intact in all derivatives.",
                "For commercial use: Requires explicit permission from the author."
            ),
        ]

        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)

        # Update "All rights reserved" where missing
        if "All rights reserved" not in new_content and "Copyright (c) 2024-2026 AEVA Development Team" in new_content:
            new_content = new_content.replace(
                "Copyright (c) 2024-2026 AEVA Development Team.",
                "Copyright (c) 2024-2026 AEVA Development Team. All rights reserved."
            )
            new_content = new_content.replace(
                "Copyright (c) 2024-2026 AEVA Development Team\n",
                "Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.\n"
            )

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Updated: {filepath}")
            return True
        else:
            print(f"- No changes: {filepath}")
            return False

    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")
        return False

def main():
    """Main function."""
    project_root = Path(__file__).parent
    aeva_dir = project_root / 'aeva'

    py_files = list(aeva_dir.rglob('*.py'))

    print(f"Found {len(py_files)} Python files")
    print("=" * 60)

    modified = 0
    for py_file in sorted(py_files):
        if update_file(py_file):
            modified += 1

    print("=" * 60)
    print(f"\nModified: {modified}/{len(py_files)}")
    print("\n✓ Update complete!")

if __name__ == '__main__':
    main()
