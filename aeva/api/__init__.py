"""
AEVA API Module
REST API for AEVA platform

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.api.server import create_app, start_server

__all__ = [
    "create_app",
    "start_server",
]
