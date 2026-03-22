"""JSON export utilities for SURgul."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class JSONExporter:
    """Export Python objects to JSON."""

    def __init__(self, pretty: bool = True, indent: int = 2):
        self.pretty = pretty
        self.indent = indent if pretty else None

    def export(
        self,
        data: Any,
        output_path: Optional[Union[str, Path]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Serialize data to JSON and optionally write it to disk."""
        export_package = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "exporter": "SURgul JSONExporter v1.0",
                "format_version": "1.0",
                **(metadata or {}),
            },
            "data": self._serialize(data),
        }
        json_string = json.dumps(
            export_package,
            indent=self.indent,
            ensure_ascii=False,
            default=str,
        )
        if output_path is not None:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json_string, encoding="utf-8")
        return json_string

    def export_batch(
        self,
        data_list: List[Any],
        output_path: Optional[Union[str, Path]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Serialize multiple records to JSON."""
        return self.export(
            data=[self._serialize(item) for item in data_list],
            output_path=output_path,
            metadata={"record_count": len(data_list), **(metadata or {})},
        )

    def export_compliance_report(
        self,
        report: Any,
        output_path: Optional[Union[str, Path]] = None,
    ) -> str:
        """Serialize a compliance report."""
        return self.export(report, output_path=output_path, metadata={"data_type": "compliance_report"})

    def _serialize(self, value: Any) -> Any:
        """Convert a Python object into JSON-compatible structures."""
        if value is None:
            return None
        if is_dataclass(value):
            return self._serialize(asdict(value))
        if isinstance(value, Enum):
            return {"name": value.name, "value": value.value}
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {key: self._serialize(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._serialize(item) for item in value]
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)
