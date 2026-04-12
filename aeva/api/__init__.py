"""
AEVA API Module
REST API for AEVA platform

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.api.server import create_app, start_server

__all__ = [
    "create_app",
    "start_server",
]
