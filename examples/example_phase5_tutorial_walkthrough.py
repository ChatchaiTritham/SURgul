"""Compact walkthrough for the packaged SURgul Phase 5 workflow."""

from pathlib import Path

from surgul.clinical_case import ClinicalCase, TimingPattern, TriggerType, VitalSigns
from surgul.exporters.json_exporter import JSONExporter
from surgul.trix_pipeline import TRIXPipeline
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator


def main() -> None:
    case = ClinicalCase(
        case_id="TUTORIAL-001",
        age=58,
        sex="F",
        vitals=VitalSigns(BP_systolic=132, BP_diastolic=82, heart_rate=74),
        timing=TimingPattern.EPISODIC,
        trigger=TriggerType.POSITIONAL,
        symptom_duration_min=0.5,
        metadata={"source": "tutorial"},
    )

    recommendation = TRIXPipeline().process(case)
    report = NISTAIRMFValidator().validate(
        {
            "has_governance_policy": True,
            "intended_use": "Clinical triage support",
            "has_metrics": True,
            "has_risk_controls": True,
        }
    )

    output_path = Path("tutorial_output.json")
    JSONExporter().export(
        {
            "recommendation": recommendation,
            "nist_report": report,
        },
        output_path,
    )

    print(f"Care pathway: {recommendation.care_pathway.value}")
    print(f"NIST compliance: {report.compliance_score:.1%}")
    print(f"Saved walkthrough output to {output_path.resolve()}")


if __name__ == "__main__":
    main()
