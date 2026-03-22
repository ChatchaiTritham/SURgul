"""NIST AI RMF validator for SURgul."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class ComplianceLevel(Enum):
    """Compliance assessment levels."""

    FULL = "full"
    PARTIAL = "partial"
    MISSING = "missing"
    NOT_APPLICABLE = "n/a"


@dataclass
class ComplianceCheck:
    """Single compliance check result."""

    requirement_id: str
    function: str
    category: str
    description: str
    level: ComplianceLevel
    evidence: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class NISTComplianceReport:
    """Summary NIST AI RMF compliance report."""

    system_name: str
    version: str
    validation_timestamp: str
    total_checks: int
    checks_passed: int
    checks_failed: int
    compliance_score: float
    regulatory_ready: bool
    certification_readiness: str
    critical_deficiencies: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    all_checks: List[ComplianceCheck] = field(default_factory=list)


class NISTAIRMFValidator:
    """Perform a lightweight NIST AI RMF-style validation."""

    def __init__(self, system_name: str = "SURgul", version: str = "1.0"):
        self.system_name = system_name
        self.version = version

    def validate(
        self,
        system_metadata: Dict,
        documentation_paths: Optional[Dict[str, str]] = None,
    ) -> NISTComplianceReport:
        """Validate supplied metadata against a compact checklist."""
        checks = [
            self._check("GOVERN-1.1", "GOVERN", "Policies", "Governance policy", bool(system_metadata.get("has_governance_policy"))),
            self._check("MAP-1.1", "MAP", "Context", "Intended use documented", bool(system_metadata.get("intended_use"))),
            self._check("MEASURE-1.1", "MEASURE", "Monitoring", "Performance metrics available", bool(system_metadata.get("has_metrics"))),
            self._check("MANAGE-1.1", "MANAGE", "Mitigation", "Risk controls documented", bool(system_metadata.get("has_risk_controls"))),
        ]
        checks_passed = sum(1 for check in checks if check.level == ComplianceLevel.FULL)
        checks_failed = sum(1 for check in checks if check.level == ComplianceLevel.MISSING)
        compliance_score = checks_passed / len(checks) if checks else 0.0
        critical_deficiencies = [check.description for check in checks if check.level == ComplianceLevel.MISSING]
        recommendations = [
            recommendation
            for check in checks
            for recommendation in check.recommendations
        ]
        return NISTComplianceReport(
            system_name=self.system_name,
            version=self.version,
            validation_timestamp=datetime.now().isoformat(),
            total_checks=len(checks),
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            compliance_score=compliance_score,
            regulatory_ready=compliance_score >= 0.75 and not critical_deficiencies,
            certification_readiness=("ready" if compliance_score >= 0.75 else "needs_improvement"),
            critical_deficiencies=critical_deficiencies,
            recommendations=recommendations,
            all_checks=checks,
        )

    def export_markdown_report(self, report: NISTComplianceReport, output_path: Path) -> Path:
        """Export a simple markdown report."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "\n".join(
                [
                    f"# {report.system_name} NIST AI RMF Report",
                    f"- Version: {report.version}",
                    f"- Compliance score: {report.compliance_score:.1%}",
                    f"- Regulatory ready: {report.regulatory_ready}",
                ]
            ),
            encoding="utf-8",
        )
        return output_path

    def _check(
        self,
        requirement_id: str,
        function: str,
        category: str,
        description: str,
        passed: bool,
    ) -> ComplianceCheck:
        """Build a simple compliance check."""
        level = ComplianceLevel.FULL if passed else ComplianceLevel.MISSING
        return ComplianceCheck(
            requirement_id=requirement_id,
            function=function,
            category=category,
            description=description,
            level=level,
            evidence=["Metadata flag present"] if passed else [],
            gaps=[] if passed else [f"Missing requirement: {description}"],
            recommendations=[] if passed else [f"Document and implement: {description}"],
        )
