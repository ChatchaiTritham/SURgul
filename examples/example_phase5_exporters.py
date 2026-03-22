"""Export example SURgul outputs in packaged formats."""

from pathlib import Path

from surgul.exporters.csv_exporter import CSVExporter
from surgul.exporters.fhir_exporter import FHIRExporter
from surgul.exporters.json_exporter import JSONExporter


def main() -> None:
    output_dir = Path("example_outputs")
    output_dir.mkdir(exist_ok=True)

    payload = {"case_id": "EXPORT-001", "risk": "moderate", "action": "observe"}
    JSONExporter().export(payload, output_dir / "decision.json")
    CSVExporter().export([payload], output_dir / "decision.csv")
    FHIRExporter().export(payload, output_dir / "decision_fhir.json")

    print(f"Wrote example exports to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
