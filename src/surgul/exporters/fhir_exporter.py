"""FHIR-like export utilities for SURgul."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union


class FHIRExporter:
    """Export SURgul outputs into a lightweight FHIR-style bundle."""

    def export(
        self,
        resource_data: Any,
        output_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Build and optionally save a FHIR-like bundle."""
        normalized_data = asdict(resource_data) if is_dataclass(resource_data) else resource_data
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [
                {
                    "resource": {
                        "resourceType": "Observation",
                        "status": "final",
                        "valueString": json.dumps(normalized_data, default=str),
                    }
                }
            ],
        }
        if output_path is not None:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
        return bundle
