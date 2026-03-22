"""Run the packaged SURgul validator examples."""

from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator


def main() -> None:
    metadata = {
        "has_governance_policy": True,
        "intended_use": "Clinical decision support for triage",
        "has_metrics": True,
        "has_risk_controls": True,
        "has_human_oversight": True,
        "device_class": "Class II",
    }

    nist_report = NISTAIRMFValidator().validate(metadata)
    fda_report = FDAGMLPValidator().validate(metadata)

    print(f"NIST compliance: {nist_report.compliance_score:.1%}")
    print(f"FDA compliance: {fda_report.compliance_score:.1%}")


if __name__ == "__main__":
    main()
