"""
AEVA API Module
REST API for AEVA platform
"""

from aeva.api.server import create_app, start_server

__all__ = [
    "create_app",
    "start_server",
]
