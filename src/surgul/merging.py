"""
Conservative Merging Algorithm for SURgul

Implements the theoretically-proven conservative merging strategy:
1. Abstention Priority: If any gate abstains → ABSTAIN
2. Conservative Escalation: Take maximum risk tier
3. Enforcement Composition: Union of all enforcement actions

Author: PhD Research Team
Date: 2026-01-09
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

from surgul.gates import GateOutput, RiskTier


@dataclass
class MergedDecision:
    """Final merged decision from all gates"""

    final_tier: RiskTier
    final_action: str
    explanation: str
    gate_outputs: Dict[str, GateOutput]
    enforcement_actions: List[str]
    confidence: float


class ConservativeMerging:
    """
    Conservative Merging Algorithm

    Theorem 1 (Monotonicity): ∀d∈D, ∀i: Gᵢ(d) ⊑ Φᵣ(d)
    Theorem 2 (Abstention Priority): (∃i: Gᵢ(d)=⊥) ⟹ Φᵣ(d)=⊥
    Theorem 3 (Critical Flag Safety): has_critical_flag(d) ⟹ Φᵣ(d)≥4
    Theorem 4 (Soundness): No unsafe discharge
    """

    def __init__(self):
        """Initialize merging algorithm"""
        pass

    def merge(self, gate_outputs: List[GateOutput]) -> MergedDecision:
        """
        Merge gate outputs using conservative strategy

        Algorithm:
        1. Check for abstention (highest priority)
        2. Take maximum risk tier
        3. Union all enforcement actions
        4. Generate explanation

        Args:
            gate_outputs: List of GateOutput from each gate

        Returns:
            MergedDecision with final tier and action
        """
        gate_dict = {g.gate_name: g for g in gate_outputs}

        abstaining_gates = [g for g in gate_outputs if g.tier == RiskTier.ABSTAIN]
        if abstaining_gates:
            return self._merge_abstention(gate_dict, abstaining_gates)

        risk_values = [g.tier.value for g in gate_outputs]
        max_risk = max(risk_values)
        final_tier = RiskTier(max_risk)

        all_enforcement = []
        for g in gate_outputs:
            all_enforcement.extend(g.enforcement)
        unique_enforcement = list(set(all_enforcement))

        final_action = self._determine_action(final_tier, unique_enforcement)

        explanation = self._generate_explanation(final_tier, gate_outputs, final_action)

        confidences = [g.confidence for g in gate_outputs if g.tier != RiskTier.ABSTAIN]
        overall_confidence = min(confidences) if confidences else 0.0

        return MergedDecision(
            final_tier=final_tier,
            final_action=final_action,
            explanation=explanation,
            gate_outputs=gate_dict,
            enforcement_actions=unique_enforcement,
            confidence=overall_confidence,
        )

    def _merge_abstention(
        self, gate_dict: Dict[str, GateOutput], abstaining_gates: List[GateOutput]
    ) -> MergedDecision:
        """Handle abstention case (Theorem 2)"""

        reasons = [g.explanation for g in abstaining_gates]
        explanation = (
            f"ABSTENTION triggered by {len(abstaining_gates)} gate(s): "
            f"{', '.join([g.gate_name for g in abstaining_gates])}. "
            f"Reasons: {' | '.join(reasons[:2])}. "
            f"Decision deferred to human expert."
        )

        return MergedDecision(
            final_tier=RiskTier.ABSTAIN,
            final_action='HUMAN_REVIEW',
            explanation=explanation,
            gate_outputs=gate_dict,
            enforcement_actions=['FORCE[human_review]', 'BLOCK[discharge]'],
            confidence=0.0,
        )

    def _determine_action(self, tier: RiskTier, enforcement: List[str]) -> str:
        """
        Determine final action based on risk tier and enforcement

        Action hierarchy:
        1. FORCE[emergency] → "EMERGENCY"
        2. FORCE[human_review] → "HUMAN_REVIEW"
        3. BLOCK[discharge] → "OBSERVE" or "EMERGENCY"
        4. Otherwise → based on risk tier
        """
        if any('FORCE[emergency]' in e for e in enforcement):
            return 'EMERGENCY'

        if any('FORCE[human_review]' in e for e in enforcement):
            return 'HUMAN_REVIEW'

        discharge_blocked = any('BLOCK[discharge]' in e for e in enforcement)

        if tier == RiskTier.CRITICAL:
            return 'EMERGENCY'
        elif tier == RiskTier.HIGH:
            return 'EMERGENCY'
        elif tier == RiskTier.MODERATE:
            return 'OBSERVE'
        elif tier == RiskTier.LOW:
            if discharge_blocked:
                return 'OBSERVE'
            return 'DISCHARGE_WITH_PRECAUTIONS'
        elif tier == RiskTier.SAFE:
            if discharge_blocked:
                return 'OBSERVE'
            if any('PERMIT[discharge]' in e for e in enforcement):
                return 'DISCHARGE'
            return 'DISCHARGE_WITH_PRECAUTIONS'
        else:
            return 'HUMAN_REVIEW'

    def _generate_explanation(
        self, final_tier: RiskTier, gate_outputs: List[GateOutput], final_action: str
    ) -> str:
        """Generate human-readable explanation"""

        max_tier = final_tier
        determining_gates = [
            g for g in gate_outputs if g.tier == max_tier and g.tier != RiskTier.ABSTAIN
        ]

        if not determining_gates:
            determining_gates = gate_outputs

        parts = []

        parts.append(f"Final Risk Tier: {final_tier.name} (Level {final_tier.value})")
        parts.append(f"Recommended Action: {final_action}")
        parts.append("")
        parts.append("Decision Rationale:")

        for gate in determining_gates:
            parts.append(f" • {gate.gate_name}: {gate.explanation}")

        enforcement = [g.enforcement for g in gate_outputs if g.enforcement]
        if enforcement:
            flat_enforcement = [e for sublist in enforcement for e in sublist]
            parts.append("")
            parts.append(f"Enforcement: {', '.join(set(flat_enforcement))}")

        parts.append("")
        parts.append("Gate Summary:")
        for gate in sorted(gate_outputs, key=lambda g: g.gate_name):
            if gate.tier != final_tier:
                parts.append(
                    f" • {gate.gate_name}: {gate.tier.name} "
                    f"(confidence: {gate.confidence:.2f})"
                )

        return '\n'.join(parts)

    def validate_theorems(
        self, gate_outputs: List[GateOutput], decision: MergedDecision
    ) -> Dict[str, bool]:
        """
        Validate that decision satisfies safety theorems

        Returns:
            Dictionary of theorem names → validation results
        """
        validations = {}

        if decision.final_tier != RiskTier.ABSTAIN:
            monotonic = all(
                g.tier.value <= decision.final_tier.value or g.tier == RiskTier.ABSTAIN
                for g in gate_outputs
            )
        else:
            monotonic = True
        validations['Theorem1_Monotonicity'] = monotonic

        has_abstention = any(g.tier == RiskTier.ABSTAIN for g in gate_outputs)
        if has_abstention:
            abstention_priority = decision.final_tier == RiskTier.ABSTAIN
        else:
            abstention_priority = True
        validations['Theorem2_AbstentionPriority'] = abstention_priority

        g1_output = next((g for g in gate_outputs if 'G1' in g.gate_name), None)
        if g1_output and g1_output.tier == RiskTier.CRITICAL:
            critical_safety = (
                decision.final_tier == RiskTier.CRITICAL
                or decision.final_tier == RiskTier.ABSTAIN
            ) and (
                'FORCE[emergency]' in decision.enforcement_actions
                or decision.final_action == 'HUMAN_REVIEW'
            )
        else:
            critical_safety = True
        validations['Theorem3_CriticalFlagSafety'] = critical_safety

        if decision.final_action in ['DISCHARGE', 'DISCHARGE_WITH_PRECAUTIONS']:
            soundness = g1_output.tier != RiskTier.CRITICAL and not any(
                'BLOCK[discharge]' in e for e in decision.enforcement_actions
            )
        else:
            soundness = True
        validations['Theorem4_Soundness'] = soundness

        completeness = (
            decision.final_tier is not None and decision.final_action is not None
        )
        validations['Theorem5_Completeness'] = completeness

        auditability = len(decision.explanation) > 0 and len(decision.gate_outputs) > 0
        validations['Theorem6_Auditability'] = auditability

        return validations


class AverageMerging:
    """
    Average Merging (Baseline for comparison)

    WARNING: This violates safety theorems! Used only for ablation study.
    Takes average of gate risk tiers instead of max.
    """

    def merge(self, gate_outputs: List[GateOutput]) -> MergedDecision:
        """Merge by averaging (UNSAFE!)"""
        non_abstaining = [g for g in gate_outputs if g.tier != RiskTier.ABSTAIN]

        if not non_abstaining:
            return ConservativeMerging()._merge_abstention(
                {g.gate_name: g for g in gate_outputs}, gate_outputs
            )

        avg_risk = sum(g.tier.value for g in non_abstaining) / len(non_abstaining)
        final_tier = RiskTier(round(avg_risk))

        all_enforcement = []
        for g in gate_outputs:
            all_enforcement.extend(g.enforcement)

        final_action = ConservativeMerging()._determine_action(
            final_tier, all_enforcement
        )

        return MergedDecision(
            final_tier=final_tier,
            final_action=final_action,
            explanation=f"Average merging (UNSAFE): avg_risk={avg_risk:.2f} → tier={final_tier.name}",
            gate_outputs={g.gate_name: g for g in gate_outputs},
            enforcement_actions=list(set(all_enforcement)),
            confidence=sum(g.confidence for g in non_abstaining) / len(non_abstaining),
        )


class WeightedMerging:
    """
    Learned Weighted Merging (Baseline for comparison)

    Assigns learned weights to gates. Performance depends on training data.
    """

    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize with gate weights

        Default weights: G1=2.0, G2=1.0, G3=1.5, G4=0.8, G5=1.5, G6=0.5
        """
        self.weights = weights or {
            'G1_CriticalFlags': 2.0,
            'G2_ModerateRisk': 1.0,
            'G3_DataQuality': 1.5,
            'G4_TiTrATE': 0.8,
            'G5_Uncertainty': 1.5,
            'G6_Temporal': 0.5,
        }

    def merge(self, gate_outputs: List[GateOutput]) -> MergedDecision:
        """Merge using learned weights"""
        non_abstaining = [g for g in gate_outputs if g.tier != RiskTier.ABSTAIN]

        if not non_abstaining:
            return ConservativeMerging()._merge_abstention(
                {g.gate_name: g for g in gate_outputs}, gate_outputs
            )

        weighted_sum = sum(
            g.tier.value * self.weights.get(g.gate_name, 1.0) for g in non_abstaining
        )
        weight_total = sum(self.weights.get(g.gate_name, 1.0) for g in non_abstaining)
        avg_risk = weighted_sum / weight_total

        final_tier = RiskTier(round(avg_risk))

        all_enforcement = []
        for g in gate_outputs:
            all_enforcement.extend(g.enforcement)

        final_action = ConservativeMerging()._determine_action(
            final_tier, all_enforcement
        )

        return MergedDecision(
            final_tier=final_tier,
            final_action=final_action,
            explanation=f"Weighted merging: weighted_avg={avg_risk:.2f} → tier={final_tier.name}",
            gate_outputs={g.gate_name: g for g in gate_outputs},
            enforcement_actions=list(set(all_enforcement)),
            confidence=sum(g.confidence for g in non_abstaining) / len(non_abstaining),
        )
