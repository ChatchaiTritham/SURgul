"""
CLI Module (Phase 5)
=====================

Command-line interface tools for TRI-X framework.
Provides commands for validation, export, and processing.

Author: PhD Research Team
Date: 2026-01-10
Phase: 5
"""

from .trix_cli import export_command, main, process_command, validate_command

__all__ = ['main', 'validate_command', 'export_command', 'process_command']
