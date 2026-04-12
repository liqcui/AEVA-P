"""
AEVA CLI Usage Examples
Demonstrates how to use AEVA via CLI and programmatically

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission
Watermark: AEVA-2026-LQC-dc68e33
GitHub: https://github.com/liqcui/AEVA-P
"""

import subprocess
import sys
from pathlib import Path


def run_cli_command(command: str, description: str = ""):
    """Execute AEVA CLI command and display output"""
    print(f"\n{'='*60}")
    if description:
        print(f"📋 {description}")
    print(f"💻 Command: {command}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"⚠️ Warnings:\n{result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False


def main():
    """Demonstrate AEVA CLI usage"""

    print("""
╔════════════════════════════════════════════════════════════╗
║           AEVA CLI Usage Examples                          ║
║   Copyright © 2024-2026 AEVA Development Team              ║
║   Watermark: AEVA-2026-LQC-dc68e33                         ║
╚════════════════════════════════════════════════════════════╝
""")

    # Example 1: Display system information
    run_cli_command(
        "aeva info",
        "Display AEVA system information and installed dependencies"
    )

    # Example 2: Display help
    run_cli_command(
        "aeva --help",
        "Show all available commands"
    )

    # Example 3: Display evaluation help
    run_cli_command(
        "aeva evaluate --help",
        "Show model evaluation options"
    )

    # Example 4: Initialize a new project
    project_name = "demo_project"
    run_cli_command(
        f"aeva init {project_name} --template basic",
        f"Initialize a new AEVA project: {project_name}"
    )

    # Example 5: Data profiling (if sample data exists)
    sample_data = Path("example_datasets/sample_data.csv")
    if sample_data.exists():
        run_cli_command(
            f"aeva data profile {sample_data} --output profile_report.html",
            "Generate data profiling report"
        )

    # Example 6: Model evaluation (if sample model exists)
    sample_model = Path("models/sample_classifier.pkl")
    if sample_model.exists() and sample_data.exists():
        run_cli_command(
            f"aeva evaluate model {sample_model} {sample_data} "
            "--metrics accuracy --metrics f1 --format json",
            "Evaluate sample model"
        )

    # Example 7: Launch dashboard (commented out - interactive)
    print(f"\n{'='*60}")
    print("📋 Launch interactive dashboard (run separately)")
    print(f"{'='*60}\n")
    print("To launch the web dashboard, run:")
    print("  aeva dashboard")
    print("\nThen open: http://localhost:8501")

    # Example 8: Launch API server (commented out - interactive)
    print(f"\n{'='*60}")
    print("📋 Launch API server (run separately)")
    print(f"{'='*60}\n")
    print("To launch the API server, run:")
    print("  aeva server")
    print("\nThen access:")
    print("  API: http://localhost:8000")
    print("  Docs: http://localhost:8000/docs")

    # Programmatic usage example
    print(f"\n{'='*60}")
    print("📋 Programmatic Usage Example")
    print(f"{'='*60}\n")

    print("""
You can also use AEVA programmatically in Python:

```python
from aeva.cli_enhanced import cli

# Run CLI programmatically
cli(['--help'])

# Or import AEVA modules directly
from aeva import AEVA
from aeva.core.pipeline import Pipeline

aeva = AEVA()
result = aeva.run(pipeline, algorithm)
```
""")

    print(f"\n{'='*60}")
    print("✅ Examples complete!")
    print(f"{'='*60}\n")

    print("📖 For more information, see:")
    print("  - docs/CLI_USAGE.md - Complete CLI reference")
    print("  - docs/CLI_VS_WEB.md - CLI vs Web comparison")
    print("  - examples/ - More code examples")


if __name__ == "__main__":
    main()
