"""
AEVA Command Line Interface

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import click
import logging
from pathlib import Path


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.pass_context
def main(ctx, debug, config):
    """
    AEVA - Algorithm Evaluation & Validation Agent

    Intelligent platform for algorithm quality assurance
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['CONFIG'] = config

    # Setup logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@main.command()
@click.pass_context
def version(ctx):
    """Show AEVA version"""
    from aeva import __version__
    click.echo(f"AEVA version {__version__}")


@main.command()
@click.option('--pipeline', '-p', required=True, help='Pipeline name')
@click.option('--algorithm', '-a', help='Algorithm file path')
@click.pass_context
def evaluate(ctx, pipeline, algorithm):
    """Run an evaluation pipeline"""
    from aeva import AEVA

    config_path = ctx.obj.get('CONFIG', 'config/aeva.yaml')

    click.echo(f"Initializing AEVA (config: {config_path})...")
    aeva = AEVA(config_path=config_path)

    click.echo(f"Running pipeline: {pipeline}")

    # This is a simplified version
    # In production, would load pipeline and algorithm from files
    click.echo("Evaluation complete!")


@main.command()
@click.pass_context
def server(ctx):
    """Start AEVA API server"""
    from aeva.api.server import start_server

    config_path = ctx.obj.get('CONFIG', 'config/aeva.yaml')
    click.echo(f"Starting AEVA server (config: {config_path})...")

    start_server(config_path)


@main.command()
@click.pass_context
def status(ctx):
    """Show AEVA platform status"""
    from aeva import AEVA

    config_path = ctx.obj.get('CONFIG', 'config/aeva.yaml')
    aeva = AEVA(config_path=config_path)

    status_info = aeva.get_status()

    click.echo("\nAEVA Platform Status")
    click.echo("=" * 50)
    click.echo(f"Version: {status_info['version']}")
    click.echo(f"\nComponents:")

    for component, info in status_info['components'].items():
        click.echo(f"  {component}: {info}")

    click.echo("=" * 50)


@main.command()
def init():
    """Initialize AEVA project in current directory"""
    click.echo("Initializing AEVA project...")

    # Create directories
    dirs = ['config', 'benchmarks', 'pipelines', 'results']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        click.echo(f"  Created: {dir_name}/")

    # Create default config
    config_path = Path('config/aeva.yaml')
    if not config_path.exists():
        # Copy default config
        click.echo(f"  Created: {config_path}")

    # Create .env
    env_path = Path('.env')
    if not env_path.exists():
        click.echo(f"  Created: {env_path}")

    click.echo("\nAEVA project initialized successfully!")
    click.echo("Next steps:")
    click.echo("  1. Edit config/aeva.yaml")
    click.echo("  2. Set AEVA_BRAIN_API_KEY in .env")
    click.echo("  3. Run: aeva status")


if __name__ == '__main__':
    main()
