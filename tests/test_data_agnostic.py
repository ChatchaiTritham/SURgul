"""Integration tests for package-level SURgul data interfaces."""

from surgul.clinical_case import ClinicalCase, CriticalFlags, TimingPattern, TriggerType, VitalSigns
from surgul.srgl import quick_predict
from surgul.srgl_adapter import SRGLAdapter
from surgul.trix_pipeline import CarePathway, TRIXPipeline


def test_clinical_case_from_syndx_preserves_source_metadata() -> None:
    case = ClinicalCase.from_syndx(
        {
            "patient_id": "SYN-001",
            "age": 67,
            "gender": "M",
            "timing": "acute",
            "trigger": "spontaneous",
            "diagnosis": "stroke",
            "comorbidities": {"cardiovascular": True},
            "examination": {"neurological_signs": True},
        }
    )

    assert case.case_id == "SYN-001"
    assert case.metadata["source"] == "SynDX"


def test_srgl_adapter_accepts_dict_and_clinical_case() -> None:
    adapter = SRGLAdapter()
    patient_dict = {"case_id": "DICT-001", "age": 65, "diplopia": True}
    case = ClinicalCase(
        case_id="CASE-001",
        age=65,
        sex="F",
        critical_flags=CriticalFlags(diplopia=True),
    )

    dict_decision = adapter.predict(patient_dict)
    case_decision = adapter.predict(case)

    assert dict_decision.risk_tier in {"CRITICAL", "HIGH", "MODERATE", "ABSTAIN"}
    assert case_decision.risk_tier in {"CRITICAL", "HIGH", "MODERATE", "ABSTAIN"}


def test_trix_pipeline_routes_low_risk_case() -> None:
    case = ClinicalCase(
        case_id="PIPE-001",
        age=48,
        sex="F",
        vitals=VitalSigns(BP_systolic=122, BP_diastolic=78, heart_rate=70),
        timing=TimingPattern.EPISODIC,
        trigger=TriggerType.POSITIONAL,
        symptom_duration_min=0.5,
        metadata={"source": "manual"},
    )

    recommendation = TRIXPipeline().process(case)

    assert recommendation.care_pathway in set(CarePathway)
    assert recommendation.total_latency_ms >= 0


def test_quick_predict_returns_summary_string() -> None:
    summary = quick_predict({"case_id": "FAST-001", "age": 60, "diplopia": False}, verbose=False)

    assert "Risk:" in summary
    assert "Action:" in summary
