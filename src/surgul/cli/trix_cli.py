"""CLI utilities for the `surgul` package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional

from surgul.exporters.csv_exporter import CSVExporter
from surgul.exporters.fhir_exporter import FHIRExporter
from surgul.exporters.json_exporter import JSONExporter
from surgul.exporters.pdf_exporter import PDFExporter
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator


def validate_command(args: argparse.Namespace) -> int:
    """Run NIST and/or FDA validation commands."""
    metadata = _load_metadata(args.metadata)

    if args.nist:
        nist_report = NISTAIRMFValidator().validate(metadata)
        print(f"NIST compliance score: {nist_report.compliance_score:.1%}")
        if args.output and args.format == "json":
            JSONExporter().export_compliance_report(nist_report, args.output)

    if args.fda:
        fda_report = FDAGMLPValidator().validate(metadata)
        print(f"FDA compliance score: {fda_report.compliance_score:.1%}")
        if args.output and args.format == "json":
            JSONExporter().export_compliance_report(fda_report, args.output)

    return 0


def export_command(args: argparse.Namespace) -> int:
    """Export input JSON to the requested format."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_path = Path(args.output) if args.output else input_path.with_suffix(f".{args.format}")

    if args.format == "json":
        JSONExporter().export(data, output_path)
    elif args.format == "csv":
        CSVExporter().export(data, output_path)
    elif args.format == "fhir":
        FHIRExporter().export(data, output_path)
    elif args.format == "pdf":
        PDFExporter(title="SURgul Export").export(data, output_path)
    else:
        print(f"ERROR: Unsupported export format: {args.format}")
        return 1

    print(f"Exported to: {output_path}")
    return 0


def process_command(args: argparse.Namespace) -> int:
    """Placeholder processing command for package stabilization."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}_processed.json")
    JSONExporter().export(payload, output_path, metadata={"processed": True})
    print(f"Processed payload written to: {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="SURgul CLI")
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="Run compliance validation")
    validate_parser.add_argument("--nist", action="store_true", help="Run NIST AI RMF validation")
    validate_parser.add_argument("--fda", action="store_true", help="Run FDA GMLP validation")
    validate_parser.add_argument("--metadata", type=str, help="Path to system metadata JSON")
    validate_parser.add_argument("--output", type=str, help="Optional output path")
    validate_parser.add_argument("--format", type=str, default="json", help="Output format")

    export_parser = subparsers.add_parser("export", help="Export data")
    export_parser.add_argument("--input", required=True, type=str, help="Input JSON path")
    export_parser.add_argument("--output", type=str, help="Optional output path")
    export_parser.add_argument("--format", required=True, type=str, help="json/csv/fhir/pdf")

    process_parser = subparsers.add_parser("process", help="Process an input payload")
    process_parser.add_argument("--input", required=True, type=str, help="Input JSON path")
    process_parser.add_argument("--output", type=str, help="Optional output path")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return validate_command(args)
    if args.command == "export":
        return export_command(args)
    if args.command == "process":
        return process_command(args)

    parser.print_help()
    return 0


def _load_metadata(metadata_path: Optional[str]) -> Dict[str, Any]:
    """Load metadata from disk or return defaults."""
    if metadata_path:
        path = Path(metadata_path)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {
        "system_name": "SURgul",
        "version": "1.0",
        "intended_use": "Clinical decision support for triage",
        "device_class": "Class II",
        "has_governance_policy": True,
        "has_metrics": True,
        "has_risk_controls": True,
        "has_human_oversight": True,
    }


if __name__ == "__main__":
    raise SystemExit(main())
