"""
Focused unit tests for SURgul pure/deterministic logic.

Targets the real rule-based safety logic that needs no training, network,
or large datasets:
  - surgul.gates: the six deterministic gates + RiskTier/GateOutput
  - surgul.merging: ConservativeMerging (max-tier escalation, abstention
    priority, theorem validation)
  - surgul.evaluation: SafetyMetrics on tiny hand-made arrays

Import style matches the repo: modules live under src/ and are importable
as ``surgul.*`` (pytest.ini sets ``pythonpath = src``). A defensive
sys.path insert is added so the file also runs when invoked directly.
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import numpy as np
import pytest

from surgul.gates import (
    RiskTier,
    GateOutput,
    Gate_G1_CriticalFlags,
    Gate_G2_ModerateRisk,
    Gate_G3_DataQuality,
    Gate_G4_TiTrATE,
)
from surgul.merging import ConservativeMerging
from surgul.evaluation import SafetyMetrics


# --------------------------------------------------------------------------
# G1: Critical red flags -> CRITICAL with emergency/block enforcement
# --------------------------------------------------------------------------
def test_g1_critical_flag_forces_emergency():
    g1 = Gate_G1_CriticalFlags()
    out = g1({"diplopia": True})
    assert isinstance(out, GateOutput)
    assert out.tier == RiskTier.CRITICAL
    assert out.confidence == 1.0
    assert "FORCE[emergency]" in out.enforcement
    assert "BLOCK[discharge]" in out.enforcement


def test_g1_no_flags_is_safe_with_no_enforcement():
    g1 = Gate_G1_CriticalFlags()
    out = g1({"diplopia": False, "ataxia": False})
    assert out.tier == RiskTier.SAFE
    assert out.enforcement == []


# --------------------------------------------------------------------------
# G2: evidence-weighted scoring with documented thresholds
#   cardiovascular_history = +2  -> score>=2 -> MODERATE + BLOCK[discharge]
#   single age+comorbidity factor = +1 -> score==1 -> LOW
# --------------------------------------------------------------------------
def test_g2_cardiovascular_history_reaches_moderate():
    g2 = Gate_G2_ModerateRisk()
    out = g2({"cardiovascular_history": True})
    assert out.tier == RiskTier.MODERATE
    assert "BLOCK[discharge]" in out.enforcement


def test_g2_single_factor_is_low_risk():
    g2 = Gate_G2_ModerateRisk()
    # age>60 with HTN = +1 only -> score==1 -> LOW
    out = g2({"age": 70, "hypertension": True})
    assert out.tier == RiskTier.LOW
    assert out.enforcement == []


# --------------------------------------------------------------------------
# G3: data completeness threshold (abstain below 70% essential fields)
# --------------------------------------------------------------------------
def test_g3_empty_data_abstains():
    g3 = Gate_G3_DataQuality()
    out = g3({})  # 0% complete -> ABSTAIN
    assert out.tier == RiskTier.ABSTAIN
    assert "TRIGGER[abstention]" in out.enforcement
    assert "FORCE[human_review]" in out.enforcement


def test_g3_full_data_is_safe():
    g3 = Gate_G3_DataQuality()
    full = {f: 1 for f in Gate_G3_DataQuality.ESSENTIAL_FIELDS}
    out = g3(full)
    assert out.tier == RiskTier.SAFE
    assert out.confidence == 1.0


# --------------------------------------------------------------------------
# G4: TiTrATE pattern matching - classic BPPV -> SAFE + PERMIT[discharge]
# --------------------------------------------------------------------------
def test_g4_bppv_pattern_permits_discharge():
    g4 = Gate_G4_TiTrATE()
    out = g4(
        {
            "timing": "episodic",
            "symptom_duration_min": 30,
            "trigger": "positional",
            "dix_hallpike": "positive",
        }
    )
    assert out.tier == RiskTier.SAFE
    assert "PERMIT[discharge]" in out.enforcement


# --------------------------------------------------------------------------
# ConservativeMerging: max-tier escalation + abstention priority (Theorem 2)
# --------------------------------------------------------------------------
def _mk(tier, name, enforcement=None, conf=0.9):
    return GateOutput(
        tier=tier,
        confidence=conf,
        explanation=f"{name} says {tier.name}",
        enforcement=enforcement or [],
        gate_name=name,
    )


def test_merge_takes_maximum_risk_tier():
    merger = ConservativeMerging()
    gates = [
        _mk(RiskTier.SAFE, "G1_CriticalFlags"),
        _mk(RiskTier.LOW, "G2_ModerateRisk"),
        _mk(RiskTier.HIGH, "G4_TiTrATE"),
    ]
    decision = merger.merge(gates)
    # Conservative escalation -> highest tier wins
    assert decision.final_tier == RiskTier.HIGH
    assert decision.final_action == "EMERGENCY"
    # confidence is the minimum across non-abstaining gates
    assert decision.confidence == pytest.approx(0.9)


def test_merge_abstention_has_priority_over_higher_risk():
    merger = ConservativeMerging()
    gates = [
        _mk(RiskTier.CRITICAL, "G1_CriticalFlags", ["FORCE[emergency]"]),
        _mk(RiskTier.ABSTAIN, "G3_DataQuality", ["TRIGGER[abstention]"]),
    ]
    decision = merger.merge(gates)
    # Theorem 2: any abstention -> overall ABSTAIN, defer to human
    assert decision.final_tier == RiskTier.ABSTAIN
    assert decision.final_action == "HUMAN_REVIEW"
    validations = merger.validate_theorems(gates, decision)
    assert validations["Theorem2_AbstentionPriority"] is True
    assert validations["Theorem1_Monotonicity"] is True


# --------------------------------------------------------------------------
# SafetyMetrics: hand-made arrays with a known confusion structure
# --------------------------------------------------------------------------
def test_safety_metrics_perfect_critical_sensitivity():
    # tiers 0..4; critical_threshold=3 means {3,4} are "critical"
    y_true = np.array([0, 1, 3, 4])
    y_pred = np.array([0, 1, 3, 4])  # perfect
    m = SafetyMetrics(y_true, y_pred)
    sens = m.sensitivity_critical(critical_threshold=3)
    assert sens["n_critical"] == 2
    assert sens["sensitivity"] == pytest.approx(1.0)
    assert sens["false_negatives"] == 0


def test_safety_metrics_abstention_counts_as_safe_catch():
    # A critical case predicted as abstention (-1) must NOT count as a miss:
    # sensitivity_critical treats abstention as a safe catch.
    y_true = np.array([4, 0])
    y_pred = np.array([-1, 0])  # abstain on the critical one
    m = SafetyMetrics(y_true, y_pred)
    sens = m.sensitivity_critical(critical_threshold=3)
    assert sens["sensitivity"] == pytest.approx(1.0)
    rate = m.abstention_rate()
    assert rate["n_abstentions"] == 1
    assert rate["abstention_rate"] == pytest.approx(0.5)
    assert rate["coverage"] == pytest.approx(0.5)
