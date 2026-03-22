"""Tests for SURgul export helpers."""

import json
from pathlib import Path

from surgul.exporters.csv_exporter import CSVExporter
from surgul.exporters.fhir_exporter import FHIRExporter
from surgul.exporters.json_exporter import JSONExporter


def test_json_exporter_writes_metadata_and_data(tmp_path: Path) -> None:
    exporter = JSONExporter(pretty=True)
    payload = {"case_id": "CASE-001", "risk": "high"}

    output_path = tmp_path / "case.json"
    json_string = exporter.export(payload, output_path=output_path, metadata={"source": "test"})

    parsed = json.loads(json_string)
    assert output_path.exists()
    assert parsed["metadata"]["source"] == "test"
    assert parsed["data"]["case_id"] == "CASE-001"


def test_csv_exporter_writes_records(tmp_path: Path) -> None:
    exporter = CSVExporter()
    output_path = exporter.export(
        [{"case_id": "CASE-001", "risk": "high"}, {"case_id": "CASE-002", "risk": "low"}],
        tmp_path / "cases.csv",
    )

    content = output_path.read_text(encoding="utf-8")
    assert output_path.exists()
    assert "case_id" in content
    assert "CASE-002" in content


def test_fhir_exporter_builds_bundle_and_writes_file(tmp_path: Path) -> None:
    exporter = FHIRExporter()
    output_path = tmp_path / "bundle.json"

    bundle = exporter.export({"case_id": "CASE-003", "decision": "urgent"}, output_path=output_path)

    assert output_path.exists()
    assert bundle["resourceType"] == "Bundle"
    assert bundle["entry"][0]["resource"]["resourceType"] == "Observation"
