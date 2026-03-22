"""CSV export utilities for SURgul."""

from __future__ import annotations

import csv
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union


class CSVExporter:
    """Export flat records to CSV."""

    def export_records(
        self,
        records: Iterable[Dict[str, Any]],
        output_path: Union[str, Path],
    ) -> Path:
        """Write iterable records to CSV."""
        rows = list(records)
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not rows:
            output_file.write_text("", encoding="utf-8")
            return output_file

        field_names = sorted({key for row in rows for key in row.keys()})
        with output_file.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(rows)
        return output_file

    def export(self, data: Any, output_path: Union[str, Path]) -> Path:
        """Export a record or list of records to CSV."""
        normalized_records = self._normalize_to_records(data)
        return self.export_records(normalized_records, output_path)

    def _normalize_to_records(self, data: Any) -> List[Dict[str, Any]]:
        """Normalize arbitrary data to a list of dictionaries."""
        if is_dataclass(data):
            return [asdict(data)]
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            normalized_rows: List[Dict[str, Any]] = []
            for item in data:
                if is_dataclass(item):
                    normalized_rows.append(asdict(item))
                elif isinstance(item, dict):
                    normalized_rows.append(item)
                else:
                    normalized_rows.append({"value": str(item)})
            return normalized_rows
        return [{"value": str(data)}]
