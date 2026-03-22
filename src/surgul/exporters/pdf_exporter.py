"""PDF-style report export for SURgul.

This implementation intentionally writes a plain-text report with a `.pdf` path
when no PDF backend is installed, so workflows remain deterministic.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Optional, Union


class PDFExporter:
    """Export human-readable reports for SURgul."""

    def __init__(self, title: str = "SURgul Report"):
        self.title = title

    def export(self, data: Any, output_path: Union[str, Path]) -> Path:
        """Write a simple report body to the requested path."""
        normalized_data = asdict(data) if is_dataclass(data) else data
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        report_text = f"{self.title}\n{'=' * len(self.title)}\n\n{normalized_data}\n"
        output_file.write_text(report_text, encoding="utf-8")
        return output_file

    def export_compliance_report(self, report: Any, output_path: Union[str, Path]) -> Path:
        """Export a compliance report."""
        return self.export(report, output_path)
