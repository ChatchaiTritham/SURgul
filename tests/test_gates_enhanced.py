"""Tests for enhanced SURgul gates."""

from surgul.gates import RiskTier
from surgul.gates_enhanced import Gate_G5_Enhanced, Gate_G6_Enhanced


def test_g5_enhanced_abstains_on_high_uncertainty() -> None:
    patient = {
        "age": None,
        "timing": "variable",
        "pattern": "variable",
        "HINTS_head_impulse": "unknown",
        "HINTS_nystagmus": "unknown",
    }

    output = Gate_G5_Enhanced()(patient)

    assert output.tier == RiskTier.ABSTAIN
    assert "ABSTENTION" in output.explanation
    assert "FORCE[human_review]" in output.enforcement


def test_g5_enhanced_returns_safe_for_clear_case() -> None:
    patient = {
        "age": 45,
        "sex": "F",
        "BP_systolic": 120,
        "heart_rate": 72,
        "onset_hours": 72,
        "timing": "episodic",
        "trigger": "positional",
        "pattern": "stable",
        "HINTS_head_impulse": "normal",
        "HINTS_nystagmus": "horizontal",
        "HINTS_test_of_skew": "negative",
        "gait_test": "normal",
        "coordination_test": "normal",
        "dix_hallpike": "positive",
    }

    output = Gate_G5_Enhanced()(patient)

    assert output.tier in {RiskTier.SAFE, RiskTier.LOW}
    assert output.confidence >= 0.6


def test_g6_enhanced_marks_hyperacute_case_time_critical() -> None:
    patient = {
        "age": 70,
        "onset_hours": 2.5,
        "pattern": "worsening",
        "cardiovascular_history": True,
        "hypertension": True,
    }

    output = Gate_G6_Enhanced()(patient)

    assert output.tier in {RiskTier.MODERATE, RiskTier.HIGH}
    assert any("TIME_CRITICAL" in item or "EXPEDITE" in item for item in output.enforcement)


def test_g6_enhanced_treats_chronic_stable_case_as_low_risk() -> None:
    patient = {"age": 52, "onset_hours": 240, "pattern": "stable"}

    output = Gate_G6_Enhanced()(patient)

    assert output.tier in {RiskTier.SAFE, RiskTier.LOW}
    assert output.confidence >= 0.5
