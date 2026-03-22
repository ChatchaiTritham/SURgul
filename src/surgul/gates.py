"""
SURgul Gate Implementations

Six parallel gates for safety-first clinical triage:
- G1: Critical Red Flags
- G2: Moderate Risk Factors
- G3: Data Quality
- G4: Pattern Matching (TiTrATE)
- G5: Uncertainty Quantification
- G6: Temporal Constraints

Author: PhD Research Team
Date: 2026-01-09
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np


class RiskTier(Enum):
    """Risk tier levels"""

    SAFE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4
    ABSTAIN = -1


@dataclass
class GateOutput:
    """Output from a single gate"""

    tier: RiskTier
    confidence: float
    explanation: str
    enforcement: List[str]
    gate_name: str


class Gate_G1_CriticalFlags:
    """
    G1: Critical Red Flags Detection

    Purpose: Detect life-threatening conditions requiring immediate emergency care
    Logic: Binary gate - ANY critical flag → EMERGENCY
    Enforcement: FORCE[emergency], BLOCK[discharge]

    Critical flags (evidence-based):
    - Diplopia (double vision) - posterior circulation indicator
    - Dysarthria (slurred speech) - brainstem involvement
    - Ataxia (coordination problems) - cerebellar dysfunction
    - Focal weakness - stroke indicator
    - Acute hearing loss - vertebral artery dissection
    - Severe headache - SAH/hemorrhage indicator
    - Altered consciousness - critical sign
    """

    CRITICAL_FLAGS = [
        'diplopia',
        'dysarthria',
        'ataxia',
        'focal_weakness',
        'acute_hearing_loss',
        'severe_headache',
        'altered_consciousness',
    ]

    def __call__(self, patient_data: Dict) -> GateOutput:
        """Evaluate critical red flags"""
        detected_flags = [
            flag for flag in self.CRITICAL_FLAGS if patient_data.get(flag, False)
        ]

        if detected_flags:
            return GateOutput(
                tier=RiskTier.CRITICAL,
                confidence=1.0,
                explanation=f"Critical red flags detected: {', '.join(detected_flags)}. "
                f"Requires immediate emergency evaluation.",
                enforcement=['FORCE[emergency]', 'BLOCK[discharge]'],
                gate_name='G1_CriticalFlags',
            )
        else:
            return GateOutput(
                tier=RiskTier.SAFE,
                confidence=1.0,
                explanation="No critical red flags detected.",
                enforcement=[],
                gate_name='G1_CriticalFlags',
            )


class Gate_G2_ModerateRisk:
    """
    G2: Moderate Risk Factor Assessment

    Purpose: Evaluate cumulative moderate risk factors
    Logic: Evidence-weighted scoring, threshold at ≥2 points
    Enforcement: BLOCK[discharge] if risk ≥ MODERATE

    Risk factors (ABCD², TiTrATE):
    - Age >60 + comorbidities (DM/HTN): +1
    - Cardiovascular history: +2 (highest weight)
    - Symptom duration >60 min: +1
    - ABCD² score ≥4: +2
    """

    def __call__(self, patient_data: Dict) -> GateOutput:
        """Evaluate moderate risk factors"""
        score = 0
        factors = []

        age = patient_data.get('age') or 0
        has_dm = patient_data.get('diabetes', False)
        has_htn = patient_data.get('hypertension', False)

        if age > 60 and (has_dm or has_htn):
            score += 1
            factors.append(f"Age {age} with {'DM' if has_dm else 'HTN'}")

        if patient_data.get('cardiovascular_history', False):
            score += 2
            factors.append("Cardiovascular history (+2)")

        duration = patient_data.get('symptom_duration_min') or 0
        if duration > 60:
            score += 1
            factors.append(f"Duration {duration:.0f} min (>60)")

        abcd2 = patient_data.get('abcd2_score', 0)
        if abcd2 and abcd2 >= 4:
            score += 2
            factors.append(f"ABCD² score {abcd2} (≥4, +2)")

        if score >= 2:
            tier = RiskTier.MODERATE
            enforcement = ['BLOCK[discharge]']
            explanation = f"Moderate risk (score={score}): {', '.join(factors)}"
        elif score == 1:
            tier = RiskTier.LOW
            enforcement = []
            explanation = f"Low risk (score={score}): {', '.join(factors)}"
        else:
            tier = RiskTier.SAFE
            enforcement = []
            explanation = "No moderate risk factors identified."

        return GateOutput(
            tier=tier,
            confidence=0.9,
            explanation=explanation,
            enforcement=enforcement,
            gate_name='G2_ModerateRisk',
        )


class Gate_G3_DataQuality:
    """
    G3: Data Completeness Check

    Purpose: Ensure sufficient data quality for safe decision-making
    Logic: Abstain if <70% essential fields present
    Enforcement: TRIGGER[abstention], FORCE[human_review]

    Essential fields:
    - Demographics: age, sex
    - Vital signs: BP, HR
    - Symptoms: onset, duration, pattern
    - Exam: HINTS, gait, coordination

    Rationale: Incomplete data → uncertain assessment → defer to human
    """

    ESSENTIAL_FIELDS = [
        'age',
        'sex',
        'BP_systolic',
        'BP_diastolic',
        'heart_rate',
        'onset_hours',
        'symptom_duration_min',
        'timing',
        'HINTS_head_impulse',
        'HINTS_nystagmus',
        'HINTS_test_of_skew',
        'gait_test',
        'coordination_test',
    ]

    def __call__(self, patient_data: Dict) -> GateOutput:
        """Evaluate data completeness"""
        missing = [
            f
            for f in self.ESSENTIAL_FIELDS
            if f not in patient_data or patient_data[f] is None or patient_data[f] == ''
        ]
        completeness = 1 - len(missing) / len(self.ESSENTIAL_FIELDS)

        if completeness < 0.7:
            return GateOutput(
                tier=RiskTier.ABSTAIN,
                confidence=0.0,
                explanation=f"Insufficient data ({completeness:.1%} complete). "
                f"Missing: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}. "
                f"Requires human review.",
                enforcement=[
                    'TRIGGER[abstention]',
                    'FORCE[human_review]',
                    'BLOCK[discharge]',
                ],
                gate_name='G3_DataQuality',
            )
        elif completeness < 0.9:
            return GateOutput(
                tier=RiskTier.LOW,
                confidence=0.7,
                explanation=f"Data {completeness:.1%} complete (safety margin applied). "
                f"Some fields missing but core assessment possible.",
                enforcement=[],
                gate_name='G3_DataQuality',
            )
        else:
            return GateOutput(
                tier=RiskTier.SAFE,
                confidence=1.0,
                explanation=f"Data {completeness:.1%} complete (excellent).",
                enforcement=[],
                gate_name='G3_DataQuality',
            )


class Gate_G4_TiTrATE:
    """
    G4: Pattern Matching (TiTrATE Framework)

    Purpose: Match clinical presentation to known benign/dangerous patterns
    Logic: Rule-based pattern recognition from TiTrATE guidelines
    Enforcement: PERMIT[discharge] if clear benign pattern

    Patterns:
    - BPPV: episodic, <60s, positional, Dix-Hallpike+
    - Vestibular neuritis: continuous, horizontal nystagmus
    - Anxiety: variable, situational trigger
    - Stroke: continuous, central nystagmus, HINTS+
    """

    def __call__(self, patient_data: Dict) -> GateOutput:
        """Match clinical pattern"""
        timing = patient_data.get('timing') or ''
        duration = patient_data.get('symptom_duration_min') or 0
        trigger = patient_data.get('trigger') or ''
        dix_hallpike = patient_data.get('dix_hallpike') or ''
        hints_nystagmus = patient_data.get('HINTS_nystagmus') or ''
        hints_abnormal = (
            patient_data.get('HINTS_head_impulse') == 'abnormal'
            or hints_nystagmus == 'vertical'
            or patient_data.get('HINTS_test_of_skew') == 'positive'
        )

        if (
            timing == 'episodic'
            and duration < 60
            and trigger == 'positional'
            and dix_hallpike == 'positive'
        ):
            return GateOutput(
                tier=RiskTier.SAFE,
                confidence=0.95,
                explanation="Matches BPPV pattern: episodic <60s, positional trigger, Dix-Hallpike+. "
                "Classic benign presentation.",
                enforcement=['PERMIT[discharge]'],
                gate_name='G4_TiTrATE',
            )

        if (
            timing == 'continuous'
            and hints_nystagmus == 'horizontal'
            and not hints_abnormal
        ):
            return GateOutput(
                tier=RiskTier.SAFE,
                confidence=0.85,
                explanation="Matches vestibular neuritis: continuous, horizontal nystagmus, "
                "normal HINTS. Peripheral vestibular disorder.",
                enforcement=['PERMIT[observe]'],
                gate_name='G4_TiTrATE',
            )

        if hints_abnormal or hints_nystagmus == 'vertical':
            return GateOutput(
                tier=RiskTier.MODERATE,
                confidence=0.90,
                explanation="Does NOT match benign pattern. HINTS exam suggests central pathology. "
                "Requires further evaluation.",
                enforcement=['BLOCK[discharge]'],
                gate_name='G4_TiTrATE',
            )

        return GateOutput(
            tier=RiskTier.LOW,
            confidence=0.60,
            explanation="No clear benign or dangerous pattern identified. "
            "Default to cautious assessment.",
            enforcement=[],
            gate_name='G4_TiTrATE',
        )


class Gate_G5_Uncertainty:
    """
    G5: Uncertainty Quantification

    Purpose: Assess epistemic and aleatoric uncertainty
    Logic: Conservative composition of multiple uncertainty sources
    Enforcement: TRIGGER[abstention] if uncertainty ≥ 0.8

    Uncertainty sources:
    1. Epistemic: model/knowledge uncertainty (HINTS ambiguity, missing guidelines)
    2. Aleatoric: data noise (vital sign variability, symptom inconsistency)
    3. Data quality: completeness and consistency

    Thresholds (conservative):
    - μ < 0.3: LOW uncertainty → SAFE
    - 0.3 ≤ μ < 0.6: MODERATE uncertainty → LOW risk
    - 0.6 ≤ μ < 0.8: HIGH uncertainty → MODERATE risk
    - μ ≥ 0.8: VERY HIGH uncertainty → ABSTAIN
    """

    def __call__(self, patient_data: Dict) -> GateOutput:
        """Quantify uncertainty"""
        uncertainties = []

        hints_head_impulse = patient_data.get('HINTS_head_impulse', 'unknown')
        hints_nystagmus = patient_data.get('HINTS_nystagmus', 'unknown')

        if hints_head_impulse == 'unknown' or hints_nystagmus == 'unknown':
            epistemic = 0.9
            uncertainties.append("HINTS exam incomplete (0.9)")
        elif hints_head_impulse == 'normal' and hints_nystagmus == 'none':
            epistemic = 0.2
        elif hints_head_impulse == 'abnormal' or hints_nystagmus == 'vertical':
            epistemic = 0.1
        else:
            epistemic = 0.5

        timing = patient_data.get('timing', 'variable')
        pattern = patient_data.get('pattern', 'variable')

        if timing == 'variable' or pattern == 'variable':
            aleatoric = 0.6
            uncertainties.append("Symptoms variable/inconsistent (0.6)")
        else:
            aleatoric = 0.3

        age = patient_data.get('age')
        bp = patient_data.get('BP_systolic')
        onset = patient_data.get('onset_hours')

        data_missing = sum([age is None, bp is None, onset is None])
        data_uncertainty = 0.3 * data_missing
        if data_uncertainty > 0:
            uncertainties.append(
                f"Missing {data_missing} key fields ({data_uncertainty:.1f})"
            )

        mu = max(epistemic, aleatoric, data_uncertainty)

        if mu >= 0.8:
            tier = RiskTier.ABSTAIN
            explanation = (
                f"Very high uncertainty (μ={mu:.2f}): {'; '.join(uncertainties)}. "
                f"Insufficient confidence for safe decision. Requires human review."
            )
            enforcement = ['TRIGGER[abstention]', 'FORCE[human_review]']
        elif mu >= 0.6:
            tier = RiskTier.MODERATE
            explanation = (
                f"High uncertainty (μ={mu:.2f}): {'; '.join(uncertainties)}. "
                f"Conservative escalation due to uncertainty."
            )
            enforcement = ['BLOCK[discharge]']
        elif mu >= 0.3:
            tier = RiskTier.LOW
            explanation = f"Moderate uncertainty (μ={mu:.2f}). Some ambiguity present."
            enforcement = []
        else:
            tier = RiskTier.SAFE
            explanation = f"Low uncertainty (μ={mu:.2f}). Clear assessment possible."
            enforcement = []

        return GateOutput(
            tier=tier,
            confidence=1 - mu,
            explanation=explanation,
            enforcement=enforcement,
            gate_name='G5_Uncertainty',
        )


class Gate_G6_Temporal:
    """
    G6: Temporal Constraints

    Purpose: Assess time-dependent urgency
    Logic: Disease-specific time windows
    Enforcement: TIME_WINDOW specification for urgent cases

    Time windows:
    - Onset <3h + high risk → tPA window (stroke)
    - Onset <24h + worsening → MODERATE risk
    - Onset >7 days + stable → LOW risk

    Rationale: "Time is brain" for stroke, but chronic stable = lower urgency
    """

    def __call__(self, patient_data: Dict) -> GateOutput:
        """Evaluate temporal factors"""
        onset_hours = patient_data.get('onset_hours')
        if onset_hours is None:
            onset_hours = 999
        pattern = patient_data.get('pattern') or 'stable'
        age = patient_data.get('age') or 50

        if onset_hours < 3 and age > 50:
            return GateOutput(
                tier=RiskTier.MODERATE,
                confidence=0.85,
                explanation=f"Onset {onset_hours:.1f}h ago (<3h). "
                f"Within tPA window if stroke. Time-sensitive evaluation required.",
                enforcement=['TIME_WINDOW[3h]', 'EXPEDITE[imaging]'],
                gate_name='G6_Temporal',
            )

        if onset_hours < 24 and pattern == 'worsening':
            return GateOutput(
                tier=RiskTier.LOW,
                confidence=0.80,
                explanation=f"Onset {onset_hours:.1f}h ago, worsening pattern. "
                f"Acute presentation requires evaluation.",
                enforcement=[],
                gate_name='G6_Temporal',
            )

        if onset_hours > 168:
            return GateOutput(
                tier=RiskTier.SAFE,
                confidence=0.75,
                explanation=f"Onset {onset_hours/24:.1f} days ago, chronic presentation. "
                f"Lower urgency for stable chronic symptoms.",
                enforcement=[],
                gate_name='G6_Temporal',
            )

        return GateOutput(
            tier=RiskTier.SAFE,
            confidence=0.70,
            explanation=f"Onset {onset_hours:.1f}h ago. Standard timeline.",
            enforcement=[],
            gate_name='G6_Temporal',
        )


ALL_GATES = [
    Gate_G1_CriticalFlags,
    Gate_G2_ModerateRisk,
    Gate_G3_DataQuality,
    Gate_G4_TiTrATE,
    Gate_G5_Uncertainty,
    Gate_G6_Temporal,
]
