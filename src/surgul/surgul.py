"""
SURgul: Safety-first Universal Risk Governance Logic

Pronounced: "SUR-gul" | เซอร์เกิล

Main system implementation integrating all six gates with conservative merging.

Author: PhD Research Team
Date: 2026-01-09
"""

import time
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

from surgul.gates import (
    Gate_G1_CriticalFlags,
    Gate_G2_ModerateRisk,
    Gate_G3_DataQuality,
    Gate_G4_TiTrATE,
    Gate_G5_Uncertainty,
    Gate_G6_Temporal,
    GateOutput,
    RiskTier,
)
from surgul.merging import ConservativeMerging, MergedDecision


@dataclass
class TriageDecision:
    """Final triage decision with full audit trail"""

    case_id: str
    risk_tier: str
    action: str
    explanation: str

    gate_outputs: Dict[str, Dict]
    enforcement_actions: List[str]
    confidence: float

    decision_time_ms: float
    timestamp: str
    theorems_validated: Dict[str, bool]


class SURgul:
    """
    SURgul: Safety-first Universal Risk Governance Logic

    Pronounced: "SUR-gul" | เซอร์เกิล

    Six-gate parallel architecture:
    - G1: Critical Red Flags (binary safety gate)
    - G2: Moderate Risk Factors (evidence-weighted)
    - G3: Data Quality (completeness check)
    - G4: TiTrATE Pattern Matching (guideline-based)
    - G5: Uncertainty Quantification (epistemic + aleatoric)
    - G6: Temporal Constraints (time-dependent urgency)

    Merging: Conservative max-aggregation with abstention priority

    Safety Guarantees (Proven):
    - Theorem 1: Monotonicity
    - Theorem 2: Abstention Priority
    - Theorem 3: Critical Flag Safety (100% sensitivity)
    - Theorem 4: Soundness (no unsafe discharge)
    - Theorem 5: Completeness (all cases handled)
    - Theorem 6: Auditability (full explainability)
    """

    def __init__(self, merging_strategy: str = 'conservative'):
        """
        Initialize SURgul system

        Args:
            merging_strategy: 'conservative' (default), 'average', or 'weighted'
        """
        self.gates = [
            Gate_G1_CriticalFlags(),
            Gate_G2_ModerateRisk(),
            Gate_G3_DataQuality(),
            Gate_G4_TiTrATE(),
            Gate_G5_Uncertainty(),
            Gate_G6_Temporal(),
        ]

        if merging_strategy == 'conservative':
            self.merger = ConservativeMerging()
        elif merging_strategy == 'average':
            from surgul.merging import AverageMerging

            self.merger = AverageMerging()
        elif merging_strategy == 'weighted':
            from surgul.merging import WeightedMerging

            self.merger = WeightedMerging()
        else:
            raise ValueError(f"Unknown merging strategy: {merging_strategy}")

        self.merging_strategy = merging_strategy

    def predict(self, patient_data: Dict) -> TriageDecision:
        """
        Make triage decision for patient

        Args:
            patient_data: Dictionary with patient information

        Returns:
            TriageDecision with risk tier, action, and full explanation

        Complexity: O(1) constant time (parallel gates + constant merging)
        """
        start_time = time.perf_counter()

        case_id = patient_data.get('case_id', 'UNKNOWN')

        gate_outputs: List[GateOutput] = []
        for gate in self.gates:
            output = gate(patient_data)
            gate_outputs.append(output)

        merged = self.merger.merge(gate_outputs)

        theorems_validated = (
            self.merger.validate_theorems(gate_outputs, merged)
            if isinstance(self.merger, ConservativeMerging)
            else {}
        )

        decision_time_ms = (time.perf_counter() - start_time) * 1000

        from datetime import datetime

        timestamp = datetime.now().isoformat()

        decision = TriageDecision(
            case_id=case_id,
            risk_tier=merged.final_tier.name,
            action=merged.final_action,
            explanation=merged.explanation,
            gate_outputs={
                name: {
                    'tier': output.tier.name,
                    'confidence': output.confidence,
                    'explanation': output.explanation,
                    'enforcement': output.enforcement,
                }
                for name, output in merged.gate_outputs.items()
            },
            enforcement_actions=merged.enforcement_actions,
            confidence=merged.confidence,
            decision_time_ms=round(decision_time_ms, 2),
            timestamp=timestamp,
            theorems_validated=theorems_validated,
        )

        return decision

    def predict_batch(self, patient_data_list: List[Dict]) -> List[TriageDecision]:
        """
        Make triage decisions for multiple patients

        Args:
            patient_data_list: List of patient data dictionaries

        Returns:
            List of TriageDecision objects
        """
        return [self.predict(data) for data in patient_data_list]

    def explain(self, patient_data: Dict, verbose: bool = True) -> str:
        """
        Generate detailed explanation for a case

        Args:
            patient_data: Patient information
            verbose: Include gate-by-gate breakdown

        Returns:
            Human-readable explanation string
        """
        decision = self.predict(patient_data)

        explanation_parts = [
            "=" * 80,
            "SURGUL TRIAGE DECISION REPORT",
            "=" * 80,
            f"Case ID: {decision.case_id}",
            f"Timestamp: {decision.timestamp}",
            f"Decision Time: {decision.decision_time_ms:.2f} ms",
            "",
            f"FINAL DECISION: {decision.action}",
            f"Risk Tier: {decision.risk_tier}",
            f"Confidence: {decision.confidence:.2%}",
            "",
            "=" * 80,
            "DETAILED EXPLANATION",
            "=" * 80,
            decision.explanation,
        ]

        if verbose:
            explanation_parts.extend(
                [
                    "",
                    "=" * 80,
                    "GATE-BY-GATE BREAKDOWN",
                    "=" * 80,
                ]
            )

            for gate_name, gate_output in sorted(decision.gate_outputs.items()):
                explanation_parts.extend(
                    [
                        f"\n{gate_name}:",
                        f" Tier: {gate_output['tier']}",
                        f" Confidence: {gate_output['confidence']:.2%}",
                        f" Explanation: {gate_output['explanation']}",
                        f" Enforcement: {', '.join(gate_output['enforcement']) if gate_output['enforcement'] else 'None'}",
                    ]
                )

        if decision.theorems_validated:
            explanation_parts.extend(
                [
                    "",
                    "=" * 80,
                    "THEOREM VALIDATION",
                    "=" * 80,
                ]
            )
            for theorem, valid in decision.theorems_validated.items():
                status = "✓ PASS" if valid else "✗ FAIL"
                explanation_parts.append(f"{theorem}: {status}")

        explanation_parts.append("=" * 80)

        return '\n'.join(explanation_parts)

    def to_dict(self, decision: TriageDecision) -> Dict:
        """Convert decision to dictionary for serialization"""
        return asdict(decision)

    def get_statistics(self, decisions: List[TriageDecision]) -> Dict:
        """
        Calculate statistics over multiple decisions

        Args:
            decisions: List of TriageDecision objects

        Returns:
            Dictionary with statistics
        """
        import numpy as np

        if not decisions:
            return {}

        decision_times = [d.decision_time_ms for d in decisions]
        confidences = [d.confidence for d in decisions]

        risk_distribution = {}
        action_distribution = {}
        abstention_count = 0

        for d in decisions:
            risk_distribution[d.risk_tier] = risk_distribution.get(d.risk_tier, 0) + 1
            action_distribution[d.action] = action_distribution.get(d.action, 0) + 1
            if d.risk_tier == 'ABSTAIN':
                abstention_count += 1

        return {
            'total_cases': len(decisions),
            'decision_time': {
                'mean_ms': np.mean(decision_times),
                'median_ms': np.median(decision_times),
                'p95_ms': np.percentile(decision_times, 95),
                'p99_ms': np.percentile(decision_times, 99),
            },
            'confidence': {
                'mean': np.mean(confidences),
                'median': np.median(confidences),
                'std': np.std(confidences),
            },
            'risk_distribution': risk_distribution,
            'action_distribution': action_distribution,
            'abstention_rate': abstention_count / len(decisions),
        }


def quick_predict(patient_data: Dict, verbose: bool = False) -> str:
    """
    Quick prediction with human-readable output

    Args:
        patient_data: Patient information dictionary
        verbose: Show detailed explanation

    Returns:
        String with decision summary
    """
    surgul = SURgul()
    decision = surgul.predict(patient_data)

    if verbose:
        return surgul.explain(patient_data, verbose=True)
    else:
        return f"Risk: {decision.risk_tier} | Action: {decision.action} | Time: {decision.decision_time_ms:.1f}ms"


if __name__ == '__main__':
    print("SURgul System Demo\n")

    print("Example 1: Posterior Stroke")
    stroke_patient = {
        'case_id': 'DEMO_001',
        'age': 68,
        'sex': 'M',
        'BP_systolic': 152,
        'BP_diastolic': 88,
        'heart_rate': 76,
        'onset_hours': 6,
        'symptom_duration_min': 180,
        'timing': 'continuous',
        'pattern': 'worsening',
        'trigger': 'none',
        'diplopia': True,
        'ataxia': True,
        'HINTS_head_impulse': 'abnormal',
        'HINTS_nystagmus': 'vertical',
        'HINTS_test_of_skew': 'positive',
        'gait_test': 'impaired',
        'coordination_test': 'impaired',
        'hypertension': True,
        'cardiovascular_history': True,
        'abcd2_score': 5,
    }

    surgul = SURgul()
    print(surgul.explain(stroke_patient, verbose=False))

    print("\n" + "=" * 80 + "\n")

    print("Example 2: BPPV (Benign)")
    bppv_patient = {
        'case_id': 'DEMO_002',
        'age': 52,
        'sex': 'F',
        'BP_systolic': 128,
        'BP_diastolic': 78,
        'heart_rate': 72,
        'onset_hours': 48,
        'symptom_duration_min': 0.5,
        'timing': 'episodic',
        'pattern': 'stable',
        'trigger': 'positional',
        'diplopia': False,
        'ataxia': False,
        'HINTS_head_impulse': 'normal',
        'HINTS_nystagmus': 'torsional',
        'HINTS_test_of_skew': 'negative',
        'gait_test': 'normal',
        'coordination_test': 'normal',
        'dix_hallpike': 'positive',
        'hypertension': False,
        'cardiovascular_history': False,
    }

    print(quick_predict(bppv_patient, verbose=False))
    print(f"\nFull explanation:\n{surgul.explain(bppv_patient, verbose=True)}")
