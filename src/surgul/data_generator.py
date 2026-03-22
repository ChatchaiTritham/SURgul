"""Structured synthetic case generation for SURgul."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import numpy as np


class RiskTier(Enum):
    """Risk tier labels for generated cases."""

    SAFE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4


class Diagnosis(Enum):
    """Synthetic diagnosis labels."""

    POSTERIOR_STROKE = "Posterior circulation stroke"
    TIA = "Transient ischemic attack"
    BPPV = "Benign paroxysmal positional vertigo"
    VESTIBULAR_NEURITIS = "Vestibular neuritis"
    ANXIETY = "Anxiety-related dizziness"


@dataclass
class PatientCase:
    """Synthetic patient case record."""

    case_id: str
    diagnosis: str
    risk_tier: int
    age: int
    sex: str
    BP_systolic: float
    BP_diastolic: float
    heart_rate: float
    onset_hours: float
    symptom_duration_min: float
    timing: str
    pattern: str
    trigger: str
    diplopia: bool
    ataxia: bool
    hypertension: bool
    cardiovascular_history: bool
    HINTS_head_impulse: str
    HINTS_nystagmus: str
    HINTS_test_of_skew: str
    gait_test: str
    coordination_test: str
    abcd2_score: Optional[int]


class SyntheticDataGenerator:
    """Generate simple, structured synthetic clinical cases."""

    DIAGNOSIS_RISK_MAP = {
        Diagnosis.POSTERIOR_STROKE: RiskTier.CRITICAL,
        Diagnosis.TIA: RiskTier.HIGH,
        Diagnosis.BPPV: RiskTier.SAFE,
        Diagnosis.VESTIBULAR_NEURITIS: RiskTier.SAFE,
        Diagnosis.ANXIETY: RiskTier.LOW,
    }

    def __init__(self, random_seed: int = 42):
        self.random = np.random.RandomState(random_seed)

    def generate_dataset(
        self,
        n_cases: int = 100,
        risk_distribution: Optional[List[float]] = None,
    ) -> List[PatientCase]:
        """Generate a list of synthetic patient cases."""
        distribution = risk_distribution or [0.35, 0.20, 0.15, 0.15, 0.15]
        risk_tiers = [RiskTier.SAFE, RiskTier.LOW, RiskTier.MODERATE, RiskTier.HIGH, RiskTier.CRITICAL]
        case_counts = [int(n_cases * probability) for probability in distribution]
        case_counts[0] += n_cases - sum(case_counts)

        generated_cases: List[PatientCase] = []
        case_index = 0
        for risk_tier, case_count in zip(risk_tiers, case_counts):
            for _ in range(case_count):
                generated_cases.append(self._generate_single_case(f"SYNTH_{case_index:06d}", risk_tier))
                case_index += 1
        self.random.shuffle(generated_cases)
        return generated_cases

    def _generate_single_case(self, case_id: str, target_risk: RiskTier) -> PatientCase:
        """Generate one synthetic case matching a target risk tier."""
        if target_risk == RiskTier.CRITICAL:
            diagnosis = Diagnosis.POSTERIOR_STROKE
            return PatientCase(
                case_id=case_id,
                diagnosis=diagnosis.value,
                risk_tier=target_risk.value,
                age=int(self.random.normal(70, 8)),
                sex="M",
                BP_systolic=float(self.random.normal(155, 15)),
                BP_diastolic=float(self.random.normal(90, 10)),
                heart_rate=float(self.random.normal(88, 10)),
                onset_hours=float(abs(self.random.normal(4, 2))),
                symptom_duration_min=float(abs(self.random.normal(180, 45))),
                timing="continuous",
                pattern="worsening",
                trigger="none",
                diplopia=True,
                ataxia=True,
                hypertension=True,
                cardiovascular_history=True,
                HINTS_head_impulse="abnormal",
                HINTS_nystagmus="vertical",
                HINTS_test_of_skew="positive",
                gait_test="impaired",
                coordination_test="impaired",
                abcd2_score=5,
            )

        if target_risk == RiskTier.HIGH:
            diagnosis = Diagnosis.TIA
            return PatientCase(
                case_id=case_id,
                diagnosis=diagnosis.value,
                risk_tier=target_risk.value,
                age=int(self.random.normal(67, 9)),
                sex="F",
                BP_systolic=float(self.random.normal(145, 12)),
                BP_diastolic=float(self.random.normal(85, 8)),
                heart_rate=float(self.random.normal(82, 9)),
                onset_hours=float(abs(self.random.normal(10, 4))),
                symptom_duration_min=float(abs(self.random.normal(40, 15))),
                timing="episodic",
                pattern="improving",
                trigger="none",
                diplopia=False,
                ataxia=True,
                hypertension=True,
                cardiovascular_history=True,
                HINTS_head_impulse="normal",
                HINTS_nystagmus="horizontal",
                HINTS_test_of_skew="negative",
                gait_test="impaired",
                coordination_test="normal",
                abcd2_score=4,
            )

        if target_risk == RiskTier.LOW:
            diagnosis = Diagnosis.ANXIETY
            return PatientCase(
                case_id=case_id,
                diagnosis=diagnosis.value,
                risk_tier=target_risk.value,
                age=int(self.random.normal(35, 10)),
                sex="F",
                BP_systolic=float(self.random.normal(122, 10)),
                BP_diastolic=float(self.random.normal(76, 7)),
                heart_rate=float(self.random.normal(78, 8)),
                onset_hours=float(abs(self.random.normal(24, 8))),
                symptom_duration_min=float(abs(self.random.normal(20, 10))),
                timing="variable",
                pattern="variable",
                trigger="situational",
                diplopia=False,
                ataxia=False,
                hypertension=False,
                cardiovascular_history=False,
                HINTS_head_impulse="normal",
                HINTS_nystagmus="none",
                HINTS_test_of_skew="negative",
                gait_test="normal",
                coordination_test="normal",
                abcd2_score=0,
            )

        diagnosis = Diagnosis.BPPV if target_risk == RiskTier.SAFE else Diagnosis.VESTIBULAR_NEURITIS
        return PatientCase(
            case_id=case_id,
            diagnosis=diagnosis.value,
            risk_tier=target_risk.value,
            age=int(self.random.normal(50, 12)),
            sex="F",
            BP_systolic=float(self.random.normal(126, 11)),
            BP_diastolic=float(self.random.normal(78, 7)),
            heart_rate=float(self.random.normal(74, 8)),
            onset_hours=float(abs(self.random.normal(36, 12))),
            symptom_duration_min=float(abs(self.random.normal(15, 8))),
            timing="episodic" if diagnosis == Diagnosis.BPPV else "continuous",
            pattern="stable",
            trigger="positional" if diagnosis == Diagnosis.BPPV else "none",
            diplopia=False,
            ataxia=False,
            hypertension=False,
            cardiovascular_history=False,
            HINTS_head_impulse="normal",
            HINTS_nystagmus="torsional" if diagnosis == Diagnosis.BPPV else "horizontal",
            HINTS_test_of_skew="negative",
            gait_test="normal",
            coordination_test="normal",
            abcd2_score=0,
        )
