"""Smoke tests for the canonical packaged SURgul API."""

from surgul import CarePathway, ClinicalCase, SRGL, SRGLAdapter, TRIXPipeline
from surgul.clinical_case import CriticalFlags, TimingPattern, TriggerType, VitalSigns
from surgul.gates_enhanced import Gate_G5_Enhanced, Gate_G6_Enhanced


def test_package_imports_expose_core_api() -> None:
    assert SRGL is not None
    assert SRGLAdapter is not None
    assert TRIXPipeline is not None
    assert CarePathway.HOME_CARE.value == "home_care"


def test_adapter_accepts_clinical_case() -> None:
    case = ClinicalCase(
        case_id="SMOKE-001",
        age=64,
        sex="F",
        vitals=VitalSigns(BP_systolic=150, BP_diastolic=90, heart_rate=88),
        timing=TimingPattern.ACUTE,
        trigger=TriggerType.SPONTANEOUS,
        critical_flags=CriticalFlags(diplopia=True),
        metadata={"source": "smoke"},
    )

    decision = SRGLAdapter().predict(case)

    assert decision.case_id == "SMOKE-001"
    assert decision.risk_tier in {"CRITICAL", "HIGH", "MODERATE", "ABSTAIN"}


def test_pipeline_returns_packaged_recommendation() -> None:
    case = ClinicalCase(
        case_id="SMOKE-002",
        age=52,
        sex="M",
        vitals=VitalSigns(BP_systolic=125, BP_diastolic=80, heart_rate=72),
        timing=TimingPattern.EPISODIC,
        trigger=TriggerType.POSITIONAL,
        symptom_duration_min=0.5,
        metadata={"source": "smoke"},
    )

    recommendation = TRIXPipeline().process(case)

    assert recommendation.case_id == "SMOKE-002"
    assert recommendation.care_pathway in set(CarePathway)
    assert recommendation.total_latency_ms >= 0


def test_enhanced_gates_are_importable_and_callable() -> None:
    patient = {
        "age": 70,
        "onset_hours": 3,
        "pattern": "worsening",
        "timing": "acute",
        "HINTS_head_impulse": "unknown",
        "HINTS_nystagmus": "unknown",
        "cardiovascular_history": True,
    }

    uncertainty_output = Gate_G5_Enhanced()(patient)
    temporal_output = Gate_G6_Enhanced()(patient)

    assert uncertainty_output.gate_name == "G5_Enhanced_Uncertainty"
    assert temporal_output.gate_name == "G6_Enhanced_Temporal"
