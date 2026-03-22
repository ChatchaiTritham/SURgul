"""Adapter utilities for using SURgul with structured clinical cases."""

from __future__ import annotations

from typing import Dict, List, Union

from surgul.clinical_case import ClinicalCase
from surgul.srgl import SRGL, TriageDecision


class SRGLAdapter:
    """Adapt `ClinicalCase` objects to the dict-based SRGL interface."""

    def __init__(self, merging_strategy: str = "conservative"):
        self.srgl = SRGL(merging_strategy=merging_strategy)

    def predict(self, clinical_case: Union[ClinicalCase, Dict]) -> TriageDecision:
        """Generate a triage decision for a clinical case or raw dictionary."""
        if isinstance(clinical_case, ClinicalCase):
            patient_data = clinical_case.to_dict()
        elif isinstance(clinical_case, dict):
            patient_data = clinical_case
        else:
            raise TypeError(f"Expected ClinicalCase or dict, got {type(clinical_case)!r}")
        return self.srgl.predict(patient_data)

    def predict_batch(self, clinical_cases: List[Union[ClinicalCase, Dict]]) -> List[TriageDecision]:
        """Generate decisions for multiple cases."""
        return [self.predict(clinical_case) for clinical_case in clinical_cases]

    def explain(self, clinical_case: Union[ClinicalCase, Dict], verbose: bool = True) -> str:
        """Generate a textual explanation for a case."""
        if isinstance(clinical_case, ClinicalCase):
            patient_data = clinical_case.to_dict()
        else:
            patient_data = clinical_case
        return self.srgl.explain(patient_data, verbose=verbose)

    def to_dict(self, decision: TriageDecision) -> Dict:
        """Serialize a decision to a dictionary."""
        return self.srgl.to_dict(decision)

    def get_statistics(self, decisions: List[TriageDecision]) -> Dict:
        """Compute aggregate decision statistics."""
        return self.srgl.get_statistics(decisions)


def quick_predict_case(clinical_case: Union[ClinicalCase, Dict], verbose: bool = False) -> str:
    """Convenience helper for quick prediction output."""
    adapter = SRGLAdapter()
    decision = adapter.predict(clinical_case)
    if verbose:
        return adapter.explain(clinical_case, verbose=True)
    return (
        f"Risk: {decision.risk_tier} | Action: {decision.action} | "
        f"Time: {decision.decision_time_ms:.1f}ms"
    )


def predict_from_syndx_row(syndx_row: Dict) -> TriageDecision:
    """Build a `ClinicalCase` from SynDX-like input and predict."""
    return SRGLAdapter().predict(ClinicalCase.from_syndx(syndx_row))


def predict_from_emr(emr_record: Dict) -> TriageDecision:
    """Build a `ClinicalCase` from EMR-like input and predict."""
    return SRGLAdapter().predict(ClinicalCase.from_emr(emr_record))
