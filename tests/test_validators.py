"""Tests for SURgul compliance validators."""

from pathlib import Path

from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator


def test_nist_validator_scores_complete_metadata_higher() -> None:
    validator = NISTAIRMFValidator(system_name="SURgul", version="1.0")

    minimal = validator.validate({})
    complete = validator.validate(
        {
            "has_governance_policy": True,
            "intended_use": "Clinical triage support",
            "has_metrics": True,
            "has_risk_controls": True,
        }
    )

    assert minimal.compliance_score == 0.0
    assert complete.compliance_score == 1.0
    assert complete.regulatory_ready is True
    assert minimal.checks_failed > complete.checks_failed


def test_nist_validator_exports_markdown_report(tmp_path: Path) -> None:
    validator = NISTAIRMFValidator()
    report = validator.validate({"has_governance_policy": True, "intended_use": "CDSS"})

    output_path = validator.export_markdown_report(report, tmp_path / "nist_report.md")

    assert output_path.exists()
    assert "Compliance score" in output_path.read_text(encoding="utf-8")


def test_fda_validator_identifies_missing_controls() -> None:
    validator = FDAGMLPValidator(system_name="SURgul", version="1.0")

    report = validator.validate(
        {
            "intended_use": "Clinical decision support",
            "device_class": "Class II",
            "has_risk_controls": False,
            "has_metrics": False,
            "has_human_oversight": True,
        }
    )

    assert report.device_classification == "Class II"
    assert report.compliance_score < 1.0
    assert "risk_management" in report.critical_deficiencies
    assert any("risk management" in action.lower() for action in report.pre_submission_actions)


def test_fda_validator_exports_markdown_report(tmp_path: Path) -> None:
    validator = FDAGMLPValidator()
    report = validator.validate(
        {
            "intended_use": "Clinical decision support",
            "device_class": "Class II",
            "has_risk_controls": True,
            "has_metrics": True,
            "has_human_oversight": True,
        }
    )

    output_path = validator.export_markdown_report(report, tmp_path / "fda_report.md")

    assert output_path.exists()
    assert "FDA GMLP Report" in output_path.read_text(encoding="utf-8")
