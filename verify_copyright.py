#!/usr/bin/env python3
"""
Copyright Watermark Verification Script

This script verifies that all Python files in the AEVA project contain
proper copyright watermarks and authorship information.

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import sys
from pathlib import Path
from typing import Tuple, List

# Expected copyright strings
EXPECTED_COPYRIGHT = "Copyright (c) 2024-2026 Liquan Cui"
EXPECTED_AUTHOR = "Liquan Cui"
EXPECTED_PROJECT_ID = "AEVA-2026-LQC-dc68e33"
EXPECTED_GITHUB = "https://github.com/liqcui/AEVA-P"


def verify_file_copyright(filepath: Path) -> Tuple[bool, List[str]]:
    """
    Verify copyright watermark in a single file.

    Returns:
        Tuple of (is_valid, missing_elements)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        missing = []

        if EXPECTED_COPYRIGHT not in content:
            missing.append("Copyright notice")

        if EXPECTED_AUTHOR not in content:
            missing.append("Author name")

        if EXPECTED_PROJECT_ID not in content:
            missing.append("Project ID")

        if EXPECTED_GITHUB not in content:
            missing.append("GitHub URL")

        return len(missing) == 0, missing

    except Exception as e:
        return False, [f"Error reading file: {e}"]


def main():
    """Main verification function."""
    project_root = Path(__file__).parent
    aeva_dir = project_root / 'aeva'

    if not aeva_dir.exists():
        print(f"❌ Error: aeva directory not found at {aeva_dir}")
        sys.exit(1)

    # Find all Python files
    py_files = sorted(aeva_dir.rglob('*.py'))

    print("=" * 70)
    print("AEVA Copyright Watermark Verification")
    print("=" * 70)
    print(f"\nScanning {len(py_files)} Python files...\n")

    valid_files = []
    invalid_files = []

    for py_file in py_files:
        is_valid, missing = verify_file_copyright(py_file)

        rel_path = py_file.relative_to(project_root)

        if is_valid:
            valid_files.append(rel_path)
            print(f"✓ {rel_path}")
        else:
            invalid_files.append((rel_path, missing))
            print(f"✗ {rel_path}")
            for item in missing:
                print(f"  - Missing: {item}")

    # Summary
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70)
    print(f"Total files:   {len(py_files)}")
    print(f"Valid:         {len(valid_files)} ({len(valid_files)/len(py_files)*100:.1f}%)")
    print(f"Invalid:       {len(invalid_files)} ({len(invalid_files)/len(py_files)*100:.1f}%)")

    if invalid_files:
        print("\n⚠️  Files missing copyright information:")
        for filepath, missing in invalid_files:
            print(f"  - {filepath}")
        sys.exit(1)
    else:
        print("\n✅ All files have valid copyright watermarks!")

    # Verify metadata
    print("\n" + "=" * 70)
    print("Project Metadata Verification")
    print("=" * 70)

    try:
        sys.path.insert(0, str(project_root))
        import aeva

        checks = [
            ("Version", aeva.__version__, "2.0.0"),
            ("Author", aeva.__author__, EXPECTED_AUTHOR),
            ("Copyright", aeva.__copyright__, f"Copyright (c) 2024-2026 {EXPECTED_AUTHOR}. All rights reserved."),
            ("Project ID", aeva.__project_id__, EXPECTED_PROJECT_ID),
            ("GitHub", aeva.__github__, EXPECTED_GITHUB),
        ]

        all_match = True
        for name, actual, expected in checks:
            match = actual == expected
            symbol = "✓" if match else "✗"
            print(f"{symbol} {name}: {actual}")
            if not match:
                print(f"  Expected: {expected}")
                all_match = False

        if all_match:
            print("\n✅ All metadata checks passed!")
        else:
            print("\n⚠️  Some metadata checks failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error verifying metadata: {e}")
        sys.exit(1)

    # Final verification
    print("\n" + "=" * 70)
    print("✅ COPYRIGHT VERIFICATION COMPLETE")
    print("=" * 70)
    print(f"\nProject: AEVA v{aeva.__version__}")
    print(f"Author: {aeva.__author__}")
    print(f"Project ID: {aeva.__project_id__}")
    print(f"Files Protected: {len(valid_files)}/{len(py_files)}")
    print("\nAll copyright watermarks are valid and in place.")
    print("This project is protected against plagiarism.")
    print("=" * 70)


if __name__ == '__main__':
    main()
