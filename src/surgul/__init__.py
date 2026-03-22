"""
SURgul: Safety-first Universal Risk Governance Logic

Pronounced: "SUR-gul" | เซอร์เกิล

A comprehensive clinical triage system integrating six gates with conservative merging.
Provides parallel gate architecture for safety-first clinical decision support.

Authors: PhD Research Team
Institution: Naresuan University
"""

from surgul.constants import FRAMEWORK_NAME, PACKAGE_VERSION

__version__ = PACKAGE_VERSION
__author__ = "PhD Research Team"
__email__ = "chatchait66@nu.ac.th"

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
from surgul.gates_enhanced import (
    Gate_G5_Enhanced,
    Gate_G6_Enhanced,
    TemporalProfile,
    UncertaintyBreakdown,
)
from surgul.clinical_case import (
    ClinicalCase,
    CriticalFlags,
    HINTSExamination,
    MedicalHistory,
    PhysicalExamination,
    TimingPattern,
    TriggerType,
    VitalSigns,
)
from surgul.srgl import SRGL, TriageDecision, quick_predict
from surgul.srgl_adapter import SRGLAdapter, quick_predict_case
from surgul.surgul import SURgul
from surgul.trix_pipeline import CarePathway, CareRecommendation, TRIXPipeline
from surgul.visualization import (
    VisualizationConfig,
    plot_abstention_tradeoff,
    plot_calibration_curve,
    plot_decision_time_distribution,
    plot_gate_tier_distribution,
)
from surgul.visualization_pro import (
    PublicationFigureConfig,
    PublicationFigureGenerator,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "Gate_G1_CriticalFlags",
    "Gate_G2_ModerateRisk",
    "Gate_G3_DataQuality",
    "Gate_G4_TiTrATE",
    "Gate_G5_Uncertainty",
    "Gate_G6_Temporal",
    "GateOutput",
    "RiskTier",
    "ConservativeMerging",
    "MergedDecision",
    "SRGL",
    "SURgul",
    "TriageDecision",
    "quick_predict",
    "SRGLAdapter",
    "quick_predict_case",
    "TRIXPipeline",
    "CarePathway",
    "CareRecommendation",
    "Gate_G5_Enhanced",
    "Gate_G6_Enhanced",
    "UncertaintyBreakdown",
    "TemporalProfile",
    "ClinicalCase",
    "CriticalFlags",
    "HINTSExamination",
    "MedicalHistory",
    "PhysicalExamination",
    "TimingPattern",
    "TriggerType",
    "VitalSigns",
    "FRAMEWORK_NAME",
    "VisualizationConfig",
    "plot_abstention_tradeoff",
    "plot_calibration_curve",
    "plot_decision_time_distribution",
    "plot_gate_tier_distribution",
    "PublicationFigureConfig",
    "PublicationFigureGenerator",
]
