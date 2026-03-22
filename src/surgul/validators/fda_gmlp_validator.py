"""FDA GMLP validator for SURgul."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class FDAGMLPReport:
    """Summary FDA GMLP compliance report."""

    system_name: str
    version: str
    validation_timestamp: str
    device_classification: str
    total_checks: int
    checks_passed: int
    checks_failed: int
    compliance_score: float
    regulatory_ready: bool
    submission_readiness: str
    critical_deficiencies: List[str] = field(default_factory=list)
    pre_submission_actions: List[str] = field(default_factory=list)


class FDAGMLPValidator:
    """Perform a lightweight FDA GMLP validation."""

    def __init__(self, system_name: str = "SURgul", version: str = "1.0"):
        self.system_name = system_name
        self.version = version

    def validate(
        self,
        system_metadata: Dict,
        documentation_paths: Optional[Dict[str, str]] = None,
    ) -> FDAGMLPReport:
        """Validate supplied metadata against a compact GMLP checklist."""
        checks = {
            "intended_use": bool(system_metadata.get("intended_use")),
            "risk_management": bool(system_metadata.get("has_risk_controls")),
            "performance_monitoring": bool(system_metadata.get("has_metrics")),
            "human_oversight": bool(system_metadata.get("has_human_oversight", True)),
        }
        checks_passed = sum(1 for passed in checks.values() if passed)
        checks_failed = sum(1 for passed in checks.values() if not passed)
        compliance_score = checks_passed / len(checks) if checks else 0.0
        critical_deficiencies = [name for name, passed in checks.items() if not passed]
        pre_submission_actions = [f"Address {name.replace('_', ' ')}" for name in critical_deficiencies]
        return FDAGMLPReport(
            system_name=self.system_name,
            version=self.version,
            validation_timestamp=datetime.now().isoformat(),
            device_classification=system_metadata.get("device_class", "Unknown"),
            total_checks=len(checks),
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            compliance_score=compliance_score,
            regulatory_ready=compliance_score >= 0.75 and not critical_deficiencies,
            submission_readiness=("ready" if compliance_score >= 0.75 else "needs_improvement"),
            critical_deficiencies=critical_deficiencies,
            pre_submission_actions=pre_submission_actions,
        )

    def export_markdown_report(self, report: FDAGMLPReport, output_path: Path) -> Path:
        """Export a simple markdown report."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "\n".join(
                [
                    f"# {report.system_name} FDA GMLP Report",
                    f"- Version: {report.version}",
                    f"- Compliance score: {report.compliance_score:.1%}",
                    f"- Regulatory ready: {report.regulatory_ready}",
                ]
            ),
            encoding="utf-8",
        )
        return output_path
