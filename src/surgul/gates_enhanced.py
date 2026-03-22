"""Enhanced uncertainty and temporal gates for the packaged SURgul API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from surgul.gates import GateOutput, RiskTier


@dataclass
class UncertaintyBreakdown:
    """Detailed uncertainty summary for Gate G5."""

    total_uncertainty: float
    epistemic: float
    aleatoric: float
    data_quality: float
    clinical_ambiguity: float
    temporal_evolution: float
    sources: List[str]
    confidence_interval: Tuple[float, float]
    abstention_recommended: bool


@dataclass
class TemporalProfile:
    """Detailed temporal summary for Gate G6."""

    onset_hours: float
    symptom_progression: str
    time_window_risk: str
    urgency_score: float
    monitoring_interval_hours: Optional[float]
    intervention_window: Optional[str]
    temporal_risk_tier: int


class Gate_G5_Enhanced:
    """Enhanced uncertainty gate with source-level breakdown."""

    ABSTENTION_THRESHOLD = 0.8
    HIGH_UNCERTAINTY_THRESHOLD = 0.6
    MODERATE_UNCERTAINTY_THRESHOLD = 0.3

    def __call__(self, patient_data: Dict) -> GateOutput:
        breakdown = self._compute_uncertainty_breakdown(patient_data)
        uncertainty = breakdown.total_uncertainty

        if uncertainty >= self.ABSTENTION_THRESHOLD:
            return GateOutput(
                tier=RiskTier.ABSTAIN,
                confidence=0.0,
                explanation=self._build_abstention_explanation(breakdown),
                enforcement=[
                    "TRIGGER[abstention]",
                    "FORCE[human_review]",
                    "BLOCK[autonomous_discharge]",
                ],
                gate_name="G5_Enhanced_Uncertainty",
            )

        if uncertainty >= self.HIGH_UNCERTAINTY_THRESHOLD:
            tier = RiskTier.MODERATE
            explanation = (
                f"High uncertainty (mu={uncertainty:.2f}). "
                f"Sources: {'; '.join(breakdown.sources[:2]) or 'multiple factors'}."
            )
            enforcement = ["BLOCK[discharge]", "REQUIRE[specialist_review]"]
        elif uncertainty >= self.MODERATE_UNCERTAINTY_THRESHOLD:
            tier = RiskTier.LOW
            explanation = (
                f"Moderate uncertainty (mu={uncertainty:.2f}). "
                "Additional data may improve confidence."
            )
            enforcement = ["RECOMMEND[additional_data]"]
        else:
            tier = RiskTier.SAFE
            explanation = (
                f"Low uncertainty (mu={uncertainty:.2f}, "
                f"CI=[{breakdown.confidence_interval[0]:.2f}, {breakdown.confidence_interval[1]:.2f}])."
            )
            enforcement = []

        return GateOutput(
            tier=tier,
            confidence=max(0.0, 1 - uncertainty),
            explanation=explanation,
            enforcement=enforcement,
            gate_name="G5_Enhanced_Uncertainty",
        )

    def _compute_uncertainty_breakdown(self, patient_data: Dict) -> UncertaintyBreakdown:
        epistemic = self._compute_epistemic_uncertainty(patient_data)
        aleatoric = self._compute_aleatoric_uncertainty(patient_data)
        data_quality = self._compute_data_quality_uncertainty(patient_data)
        clinical_ambiguity = self._compute_clinical_ambiguity(patient_data)
        temporal_evolution = self._compute_temporal_uncertainty(patient_data)
        total_uncertainty = max(
            epistemic,
            aleatoric,
            data_quality,
            clinical_ambiguity,
            temporal_evolution,
        )

        sources = []
        if epistemic > 0.5:
            sources.append(f"knowledge uncertainty {epistemic:.2f}")
        if aleatoric > 0.5:
            sources.append(f"data variability {aleatoric:.2f}")
        if data_quality > 0.5:
            sources.append(f"data incompleteness {data_quality:.2f}")
        if clinical_ambiguity > 0.5:
            sources.append(f"clinical ambiguity {clinical_ambiguity:.2f}")
        if temporal_evolution > 0.5:
            sources.append(f"temporal uncertainty {temporal_evolution:.2f}")

        return UncertaintyBreakdown(
            total_uncertainty=total_uncertainty,
            epistemic=epistemic,
            aleatoric=aleatoric,
            data_quality=data_quality,
            clinical_ambiguity=clinical_ambiguity,
            temporal_evolution=temporal_evolution,
            sources=sources,
            confidence_interval=(max(0.0, total_uncertainty - 0.1), min(1.0, total_uncertainty + 0.1)),
            abstention_recommended=total_uncertainty >= self.ABSTENTION_THRESHOLD,
        )

    def _compute_epistemic_uncertainty(self, patient_data: Dict) -> float:
        hints_fields = [
            patient_data.get("HINTS_head_impulse"),
            patient_data.get("HINTS_nystagmus"),
            patient_data.get("HINTS_test_of_skew"),
        ]
        if any(value in {None, "unknown"} for value in hints_fields):
            return 0.9
        if patient_data.get("HINTS_head_impulse") == "abnormal" or patient_data.get("HINTS_nystagmus") == "vertical":
            return 0.1
        if patient_data.get("HINTS_head_impulse") == "normal" and patient_data.get("HINTS_nystagmus") in {"none", "horizontal", "torsional"}:
            return 0.2
        return 0.5

    def _compute_aleatoric_uncertainty(self, patient_data: Dict) -> float:
        flags = [
            patient_data.get("timing") in {None, "unknown", "variable"},
            patient_data.get("pattern") in {None, "unknown", "variable", "fluctuating"},
            patient_data.get("trigger") in {None, "unknown"},
        ]
        return min(0.3 * sum(flags), 0.9)

    def _compute_data_quality_uncertainty(self, patient_data: Dict) -> float:
        required_fields = [
            "age",
            "sex",
            "BP_systolic",
            "heart_rate",
            "onset_hours",
            "timing",
            "HINTS_head_impulse",
            "HINTS_nystagmus",
            "gait_test",
            "coordination_test",
        ]
        missing = sum(
            patient_data.get(field) in {None, "", "unknown"} for field in required_fields
        )
        completeness = 1 - (missing / len(required_fields))
        if completeness < 0.6:
            return 0.9
        if completeness < 0.8:
            return 0.6
        return 0.3 * (1 - completeness)

    def _compute_clinical_ambiguity(self, patient_data: Dict) -> float:
        has_central = any(
            [
                patient_data.get("diplopia", False),
                patient_data.get("dysarthria", False),
                patient_data.get("ataxia", False),
                patient_data.get("HINTS_nystagmus") == "vertical",
            ]
        )
        has_peripheral = any(
            [
                patient_data.get("timing") == "episodic",
                patient_data.get("trigger") == "positional",
                patient_data.get("dix_hallpike") == "positive",
                patient_data.get("HINTS_nystagmus") in {"horizontal", "torsional"},
            ]
        )
        if has_central and has_peripheral:
            return 0.7
        if has_central or has_peripheral:
            return 0.2
        return 0.6

    def _compute_temporal_uncertainty(self, patient_data: Dict) -> float:
        pattern = patient_data.get("pattern", "unknown")
        onset_hours = patient_data.get("onset_hours")
        if pattern in {"variable", "fluctuating"}:
            return 0.7
        if pattern == "worsening":
            return 0.5
        if onset_hours is None:
            return 0.6
        if onset_hours < 6:
            return 0.4
        if onset_hours > 168 and pattern == "stable":
            return 0.1
        return 0.3

    def _build_abstention_explanation(self, breakdown: UncertaintyBreakdown) -> str:
        sources = "; ".join(breakdown.sources) or "multiple sources"
        return (
            f"ABSTENTION TRIGGERED: Very high uncertainty (mu={breakdown.total_uncertainty:.2f}, "
            f"CI=[{breakdown.confidence_interval[0]:.2f}, {breakdown.confidence_interval[1]:.2f}]). "
            f"Sources: {sources}. Mandatory human review required."
        )


class Gate_G6_Enhanced:
    """Enhanced temporal gate with explicit monitoring and intervention windows."""

    TPA_WINDOW = 4.5
    HYPERACUTE_THRESHOLD = 6
    ACUTE_THRESHOLD = 24
    SUBACUTE_THRESHOLD = 72
    CHRONIC_THRESHOLD = 168

    def __call__(self, patient_data: Dict) -> GateOutput:
        profile = self._compute_temporal_profile(patient_data)
        return GateOutput(
            tier=self._determine_temporal_risk_tier(profile),
            confidence=self._compute_temporal_confidence(profile, patient_data),
            explanation=self._build_temporal_explanation(profile),
            enforcement=self._build_temporal_enforcement(profile),
            gate_name="G6_Enhanced_Temporal",
        )

    def _compute_temporal_profile(self, patient_data: Dict) -> TemporalProfile:
        onset_hours = patient_data.get("onset_hours")
        if onset_hours is None:
            onset_hours = 999.0
        pattern = patient_data.get("pattern", "unknown")

        if onset_hours < self.HYPERACUTE_THRESHOLD:
            time_window_risk = "hyperacute"
            urgency = 0.9
        elif onset_hours < self.ACUTE_THRESHOLD:
            time_window_risk = "acute"
            urgency = 0.7
        elif onset_hours < self.SUBACUTE_THRESHOLD:
            time_window_risk = "subacute"
            urgency = 0.5
        elif onset_hours < self.CHRONIC_THRESHOLD:
            time_window_risk = "early_chronic"
            urgency = 0.3
        else:
            time_window_risk = "chronic"
            urgency = 0.2

        if pattern == "worsening":
            urgency = min(1.0, urgency + 0.2)
        elif pattern == "improving":
            urgency = max(0.1, urgency - 0.1)

        intervention_window = self._determine_intervention_window(onset_hours, patient_data)
        monitoring_interval = self._determine_monitoring_interval(onset_hours, pattern, urgency)

        if urgency >= 0.8:
            temporal_risk_tier = 3
        elif urgency >= 0.6:
            temporal_risk_tier = 2
        elif urgency >= 0.4:
            temporal_risk_tier = 1
        else:
            temporal_risk_tier = 0

        return TemporalProfile(
            onset_hours=onset_hours,
            symptom_progression=pattern,
            time_window_risk=time_window_risk,
            urgency_score=urgency,
            monitoring_interval_hours=monitoring_interval,
            intervention_window=intervention_window,
            temporal_risk_tier=temporal_risk_tier,
        )

    def _determine_intervention_window(self, onset_hours: float, patient_data: Dict) -> Optional[str]:
        high_risk_context = any(
            [
                patient_data.get("cardiovascular_history", False),
                patient_data.get("hypertension", False),
                patient_data.get("diabetes", False),
                (patient_data.get("age") or 0) > 60,
            ]
        )
        if onset_hours < self.TPA_WINDOW and high_risk_context:
            return f"tPA_window_{self.TPA_WINDOW - onset_hours:.1f}h_remaining"
        if self.TPA_WINDOW <= onset_hours < 24 and high_risk_context:
            return "thrombectomy_window"
        return None

    def _determine_monitoring_interval(self, onset_hours: float, pattern: str, urgency: float) -> Optional[float]:
        if pattern == "worsening":
            if onset_hours < 6:
                return 1.0
            if onset_hours < 24:
                return 4.0
            return 12.0
        if urgency >= 0.7:
            return 2.0
        if urgency >= 0.5:
            return 6.0
        if urgency >= 0.3:
            return 24.0
        return None

    def _determine_temporal_risk_tier(self, profile: TemporalProfile) -> RiskTier:
        return {
            0: RiskTier.SAFE,
            1: RiskTier.LOW,
            2: RiskTier.MODERATE,
            3: RiskTier.HIGH,
        }[profile.temporal_risk_tier]

    def _compute_temporal_confidence(self, profile: TemporalProfile, patient_data: Dict) -> float:
        onset_documented = patient_data.get("onset_hours") is not None
        pattern_documented = patient_data.get("pattern") not in {None, "unknown", "variable"}
        if onset_documented and pattern_documented:
            return 0.9
        if onset_documented:
            return 0.75
        if pattern_documented:
            return 0.6
        return 0.5

    def _build_temporal_explanation(self, profile: TemporalProfile) -> str:
        parts = [
            f"Temporal assessment: {profile.time_window_risk.upper()} phase",
            f"(onset {profile.onset_hours:.1f}h ago)",
            f"urgency score {profile.urgency_score:.2f}",
        ]
        if profile.symptom_progression != "unknown":
            parts.append(f"symptoms {profile.symptom_progression}")
        if profile.intervention_window:
            parts.append(f"within {profile.intervention_window}")
        if profile.monitoring_interval_hours:
            parts.append(f"monitoring every {profile.monitoring_interval_hours:.0f}h")
        return ". ".join(parts) + "."

    def _build_temporal_enforcement(self, profile: TemporalProfile) -> List[str]:
        enforcement: List[str] = []
        if profile.intervention_window:
            if "tPA" in profile.intervention_window:
                enforcement.extend(
                    [
                        "TIME_CRITICAL[tPA_window]",
                        "EXPEDITE[imaging]",
                        "ACTIVATE[stroke_protocol]",
                    ]
                )
            elif "thrombectomy" in profile.intervention_window:
                enforcement.extend(
                    ["TIME_WINDOW[thrombectomy]", "EXPEDITE[vascular_imaging]"]
                )
        if profile.monitoring_interval_hours and profile.monitoring_interval_hours <= 4:
            enforcement.append(f"REQUIRE[monitoring_q{profile.monitoring_interval_hours:.0f}h]")
        if profile.symptom_progression == "worsening":
            enforcement.extend(["BLOCK[discharge]", "REQUIRE[admission_or_observation]"])
        return enforcement


__all__ = [
    "Gate_G5_Enhanced",
    "Gate_G6_Enhanced",
    "TemporalProfile",
    "UncertaintyBreakdown",
]
