"""Basic end-to-end package usage example for SURgul."""

from surgul.clinical_case import ClinicalCase, CriticalFlags, TimingPattern, TriggerType, VitalSigns
from surgul.trix_pipeline import TRIXPipeline


def main() -> None:
    case = ClinicalCase(
        case_id="EXAMPLE-001",
        age=68,
        sex="M",
        vitals=VitalSigns(BP_systolic=158, BP_diastolic=92, heart_rate=86),
        timing=TimingPattern.ACUTE,
        trigger=TriggerType.SPONTANEOUS,
        critical_flags=CriticalFlags(diplopia=True),
        metadata={"source": "example"},
    )

    recommendation = TRIXPipeline().process(case)
    print(f"Case: {recommendation.case_id}")
    print(f"Pathway: {recommendation.care_pathway.value}")
    print(f"Action: {recommendation.action}")
    print(f"Latency: {recommendation.total_latency_ms:.2f} ms")


if __name__ == "__main__":
    main()
