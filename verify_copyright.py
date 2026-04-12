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
EXPECTED_COPYRIGHT = "Copyright (c) 2024-2026 AEVA Development Team"
EXPECTED_LICENSE_KEYWORD = "Dual License"  # Or "License:"
EXPECTED_WATERMARK = "AEVA-2026-LQC-dc68e33"
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

        if EXPECTED_LICENSE_KEYWORD not in content and "License:" not in content:
            missing.append("License information")

        if EXPECTED_WATERMARK not in content:
            missing.append("Watermark ID")

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
            ("Author", aeva.__author__, "AEVA Development Team"),
            ("Copyright", aeva.__copyright__, "Copyright (c) 2024-2026 AEVA Development Team. All rights reserved."),
            ("License", aeva.__license__, "Dual License: Free for Personal/Academic, Commercial Requires Permission"),
            ("Watermark", aeva.__watermark__, EXPECTED_WATERMARK),
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
    print(f"Watermark ID: {aeva.__watermark__}")
    print(f"License: {aeva.__license__}")
    print(f"Files Protected: {len(valid_files)}/{len(py_files)}")
    print("\nAll copyright watermarks and license requirements are valid.")
    print("This project uses dual licensing:")
    print("  - FREE for personal and academic use")
    print("  - Commercial use requires permission (liquan_cui@126.com)")
    print("=" * 70)


if __name__ == '__main__':
    main()
