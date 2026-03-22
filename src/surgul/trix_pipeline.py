"""Simplified end-to-end pipeline for the packaged SURgul implementation."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from surgul.clinical_case import ClinicalCase
from surgul.srgl import TriageDecision
from surgul.srgl_adapter import SRGLAdapter


class CarePathway(Enum):
    """High-level care routing outputs."""

    HOME_CARE = "home_care"
    OUTPATIENT_SPECIALIST = "outpatient_specialist"
    URGENT_EVALUATION = "urgent_evaluation"
    EMERGENCY_DEPARTMENT = "emergency_department"
    HUMAN_REVIEW = "human_review"


@dataclass
class CareRecommendation:
    """Final package-level care recommendation."""

    case_id: str
    srgl_decision: TriageDecision
    care_pathway: CarePathway
    action: str
    timeline: str
    referral: str
    safety_net_instructions: List[str] = field(default_factory=list)
    total_latency_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


PATHWAY_SPECS: Dict[CarePathway, Dict[str, Any]] = {
    CarePathway.HOME_CARE: {
        "action": "Safe discharge with self-care instructions",
        "timeline": "1-4 weeks",
        "referral": "Primary care follow-up",
        "safety_net_instructions": ["Return if symptoms worsen", "Seek care for new neurologic symptoms"],
    },
    CarePathway.OUTPATIENT_SPECIALIST: {
        "action": "Outpatient specialist referral",
        "timeline": "3-7 days",
        "referral": "ENT or Neurology",
        "safety_net_instructions": ["Return for symptom worsening"],
    },
    CarePathway.URGENT_EVALUATION: {
        "action": "Urgent specialist evaluation",
        "timeline": "24-72 hours",
        "referral": "Urgent Neurology",
        "safety_net_instructions": ["Do not delay imaging", "Escalate immediately if deficits appear"],
    },
    CarePathway.EMERGENCY_DEPARTMENT: {
        "action": "Emergency department transfer",
        "timeline": "Immediate",
        "referral": "Emergency Department",
        "safety_net_instructions": ["Activate emergency protocol"],
    },
    CarePathway.HUMAN_REVIEW: {
        "action": "Mandatory human review",
        "timeline": "Immediate",
        "referral": "Clinician review",
        "safety_net_instructions": ["Collect missing information", "Default to conservative escalation"],
    },
}


class TRIXPipeline:
    """Minimal packaged pipeline using SRGLAdapter as the core engine."""

    def __init__(self, merging_strategy: str = "conservative"):
        self.srgl_adapter = SRGLAdapter(merging_strategy=merging_strategy)

    def process(self, clinical_case: ClinicalCase) -> CareRecommendation:
        """Process a clinical case into a care recommendation."""
        start_time = time.perf_counter()
        triage_decision = self.srgl_adapter.predict(clinical_case)
        care_pathway = self._map_risk_to_pathway(triage_decision.risk_tier)
        pathway_specification = PATHWAY_SPECS[care_pathway]
        total_latency_ms = (time.perf_counter() - start_time) * 1000
        return CareRecommendation(
            case_id=triage_decision.case_id,
            srgl_decision=triage_decision,
            care_pathway=care_pathway,
            action=pathway_specification["action"],
            timeline=pathway_specification["timeline"],
            referral=pathway_specification["referral"],
            safety_net_instructions=pathway_specification["safety_net_instructions"],
            total_latency_ms=round(total_latency_ms, 2),
            metadata={"source": clinical_case.metadata.get("source", "unknown")},
        )

    def _map_risk_to_pathway(self, risk_tier: str) -> CarePathway:
        """Map an SRGL risk tier to a care pathway."""
        normalized_risk_tier = risk_tier.upper()
        if normalized_risk_tier == "SAFE":
            return CarePathway.HOME_CARE
        if normalized_risk_tier == "LOW":
            return CarePathway.OUTPATIENT_SPECIALIST
        if normalized_risk_tier in {"MODERATE", "HIGH"}:
            return CarePathway.URGENT_EVALUATION
        if normalized_risk_tier == "CRITICAL":
            return CarePathway.EMERGENCY_DEPARTMENT
        return CarePathway.HUMAN_REVIEW
