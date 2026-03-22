"""
Generic Clinical Case Data Interface

Data-agnostic interface for clinical dizziness presentations.
Works with ANY data source: SynDX synthetic, real EMR, manual entry.

Author: PhD Research Team
Date: 2026-01-10
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TimingPattern(Enum):
    """Symptom timing patterns (TiTrATE framework)"""

    EPISODIC = "episodic"
    CONTINUOUS = "continuous"
    ACUTE = "acute"
    CHRONIC = "chronic"
    VARIABLE = "variable"
    UNKNOWN = "unknown"


class TriggerType(Enum):
    """Symptom triggers"""

    POSITIONAL = "positional"
    SPONTANEOUS = "spontaneous"
    EXERTIONAL = "exertional"
    SITUATIONAL = "situational"
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass
class VitalSigns:
    """Patient vital signs"""

    BP_systolic: Optional[float] = None
    BP_diastolic: Optional[float] = None
    heart_rate: Optional[float] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    respiratory_rate: Optional[float] = None

    def is_complete(self) -> bool:
        """Check if essential vital signs are present"""
        return all(
            [
                self.BP_systolic is not None,
                self.BP_diastolic is not None,
                self.heart_rate is not None,
            ]
        )


@dataclass
class CriticalFlags:
    """Critical red flag symptoms (Gate G1)"""

    diplopia: bool = False
    dysarthria: bool = False
    ataxia: bool = False
    focal_weakness: bool = False
    acute_hearing_loss: bool = False
    severe_headache: bool = False
    altered_consciousness: bool = False
    facial_droop: bool = False
    severe_vertigo: bool = False

    def any_present(self) -> bool:
        """Check if ANY critical flag is present"""
        return any(
            [
                self.diplopia,
                self.dysarthria,
                self.ataxia,
                self.focal_weakness,
                self.acute_hearing_loss,
                self.severe_headache,
                self.altered_consciousness,
                self.facial_droop,
                self.severe_vertigo,
            ]
        )

    def get_detected_flags(self) -> List[str]:
        """Return list of detected critical flags"""
        flags = []
        for field_name, field_value in self.__dict__.items():
            if field_value is True:
                flags.append(field_name)
        return flags


@dataclass
class HINTSExamination:
    """HINTS exam results (Head Impulse, Nystagmus, Test of Skew)"""

    head_impulse: Optional[str] = None
    nystagmus: Optional[str] = None
    test_of_skew: Optional[str] = None

    def is_abnormal(self) -> bool:
        """Check if HINTS suggests central pathology"""
        return (
            self.head_impulse == 'abnormal'
            or self.nystagmus == 'vertical'
            or self.test_of_skew == 'positive'
        )

    def is_complete(self) -> bool:
        """Check if HINTS exam was performed"""
        return all(
            [
                self.head_impulse is not None,
                self.nystagmus is not None,
                self.test_of_skew is not None,
            ]
        )


@dataclass
class PhysicalExamination:
    """Physical examination findings"""

    HINTS: HINTSExamination = field(default_factory=HINTSExamination)
    dix_hallpike: Optional[str] = None
    gait_test: Optional[str] = None
    coordination_test: Optional[str] = None
    romberg: Optional[str] = None


@dataclass
class MedicalHistory:
    """Patient medical history"""

    cardiovascular_history: bool = False
    prior_stroke: bool = False
    prior_tia: bool = False
    diabetes: bool = False
    hypertension: bool = False
    atrial_fibrillation: bool = False
    migraine_history: bool = False
    vestibular_disorder_history: bool = False


@dataclass
class ClinicalCase:
    """
    Generic Clinical Case Data Structure

    Data-agnostic representation of a dizziness presentation.
    Can be populated from ANY source:
    - SynDX synthetic data
    - Real EMR/EHR systems
    - Manual clinical assessment
    - Research databases
    """

    case_id: str
    age: Optional[int] = None
    sex: Optional[str] = None
    vitals: VitalSigns = field(default_factory=VitalSigns)
    onset_hours: Optional[float] = None
    symptom_duration_min: Optional[float] = None
    timing: Optional[TimingPattern] = None
    trigger: Optional[TriggerType] = None
    pattern: Optional[str] = None
    critical_flags: CriticalFlags = field(default_factory=CriticalFlags)
    examination: PhysicalExamination = field(default_factory=PhysicalExamination)
    history: MedicalHistory = field(default_factory=MedicalHistory)
    abcd2_score: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to flat dictionary for SRGL gates"""
        return {
            'case_id': self.case_id,
            'age': self.age,
            'sex': self.sex,
            'BP_systolic': self.vitals.BP_systolic,
            'BP_diastolic': self.vitals.BP_diastolic,
            'heart_rate': self.vitals.heart_rate,
            'temperature': self.vitals.temperature,
            'onset_hours': self.onset_hours,
            'symptom_duration_min': self.symptom_duration_min,
            'timing': self.timing.value if self.timing else None,
            'trigger': self.trigger.value if self.trigger else None,
            'pattern': self.pattern,
            'diplopia': self.critical_flags.diplopia,
            'dysarthria': self.critical_flags.dysarthria,
            'ataxia': self.critical_flags.ataxia,
            'focal_weakness': self.critical_flags.focal_weakness,
            'acute_hearing_loss': self.critical_flags.acute_hearing_loss,
            'severe_headache': self.critical_flags.severe_headache,
            'altered_consciousness': self.critical_flags.altered_consciousness,
            'HINTS_head_impulse': self.examination.HINTS.head_impulse,
            'HINTS_nystagmus': self.examination.HINTS.nystagmus,
            'HINTS_test_of_skew': self.examination.HINTS.test_of_skew,
            'dix_hallpike': self.examination.dix_hallpike,
            'gait_test': self.examination.gait_test,
            'coordination_test': self.examination.coordination_test,
            'cardiovascular_history': self.history.cardiovascular_history,
            'diabetes': self.history.diabetes,
            'hypertension': self.history.hypertension,
            'abcd2_score': self.abcd2_score,
            **self.metadata,
        }

    @classmethod
    def from_syndx(cls, syndx_row: Dict[str, Any]) -> 'ClinicalCase':
        """Create ClinicalCase from SynDX synthetic data row"""
        exam_data = syndx_row.get('examination', {})
        symptoms = syndx_row.get('symptoms', {})
        comorbidities = syndx_row.get('comorbidities', {})

        return cls(
            case_id=syndx_row.get('patient_id', syndx_row.get('case_id', 'UNKNOWN')),
            age=syndx_row.get('age'),
            sex=syndx_row.get('gender', syndx_row.get('sex')),
            vitals=VitalSigns(
                BP_systolic=syndx_row.get('BP_systolic'),
                BP_diastolic=syndx_row.get('BP_diastolic'),
                heart_rate=syndx_row.get('heart_rate'),
            ),
            onset_hours=symptoms.get('duration_hours') if symptoms else None,
            timing=(
                TimingPattern(syndx_row['timing']) if 'timing' in syndx_row else None
            ),
            trigger=(
                TriggerType(syndx_row['trigger']) if 'trigger' in syndx_row else None
            ),
            critical_flags=CriticalFlags(
                diplopia=exam_data.get('neurological_signs', False)
                and syndx_row.get('diagnosis') in ['stroke', 'tia'],
                ataxia=exam_data.get('neurological_signs', False),
                severe_headache=symptoms.get('severity', 0) >= 8 if symptoms else False,
            ),
            history=MedicalHistory(
                cardiovascular_history=(
                    comorbidities.get('cardiovascular', False)
                    if comorbidities
                    else False
                ),
                hypertension=(
                    comorbidities.get('hypertension', False) if comorbidities else False
                ),
                diabetes=(
                    comorbidities.get('diabetes', False) if comorbidities else False
                ),
            ),
            metadata={
                'source': 'SynDX',
                'original_diagnosis': syndx_row.get('diagnosis'),
                'original_urgency': syndx_row.get('urgency'),
            },
        )

    @classmethod
    def from_emr(cls, emr_data: Dict[str, Any]) -> 'ClinicalCase':
        """Create ClinicalCase from real EMR/EHR data"""
        return cls(
            case_id=emr_data.get('mrn', emr_data.get('encounter_id', 'UNKNOWN')),
            age=emr_data.get('age'),
            sex=emr_data.get('sex', emr_data.get('gender')),
            vitals=VitalSigns(
                BP_systolic=emr_data.get('vitals', {}).get('BP_systolic'),
                BP_diastolic=emr_data.get('vitals', {}).get('BP_diastolic'),
                heart_rate=emr_data.get('vitals', {}).get('HR'),
                temperature=emr_data.get('vitals', {}).get('temp'),
                oxygen_saturation=emr_data.get('vitals', {}).get('SpO2'),
            ),
            onset_hours=emr_data.get('chief_complaint', {}).get('onset_hours'),
            timing=cls._parse_timing(emr_data.get('hpi', '')),
            trigger=cls._parse_trigger(emr_data.get('hpi', '')),
            critical_flags=cls._parse_critical_flags(emr_data.get('physical_exam', {})),
            examination=cls._parse_examination(emr_data.get('physical_exam', {})),
            history=cls._parse_history(emr_data.get('problem_list', [])),
            metadata={
                'source': 'EMR',
                'facility': emr_data.get('facility'),
                'encounter_date': emr_data.get('encounter_date'),
            },
        )

    @staticmethod
    def _parse_timing(hpi_text: str) -> Optional[TimingPattern]:
        """Parse timing pattern from clinical text"""
        return None

    @staticmethod
    def _parse_trigger(hpi_text: str) -> Optional[TriggerType]:
        """Parse trigger from clinical text"""
        return None

    @staticmethod
    def _parse_critical_flags(exam_dict: Dict) -> CriticalFlags:
        """Parse critical flags from exam dictionary"""
        return CriticalFlags(
            diplopia=exam_dict.get('diplopia', False),
            dysarthria=exam_dict.get('dysarthria', False),
            ataxia=exam_dict.get('ataxia', False),
            focal_weakness=exam_dict.get('weakness', False),
            altered_consciousness=exam_dict.get('altered_mental_status', False),
        )

    @staticmethod
    def _parse_examination(exam_dict: Dict) -> PhysicalExamination:
        """Parse physical examination from EMR data"""
        hints_data = exam_dict.get('HINTS', {})

        return PhysicalExamination(
            HINTS=HINTSExamination(
                head_impulse=hints_data.get('head_impulse'),
                nystagmus=hints_data.get('nystagmus'),
                test_of_skew=hints_data.get('skew'),
            ),
            dix_hallpike=exam_dict.get('dix_hallpike'),
            gait_test=exam_dict.get('gait'),
            coordination_test=exam_dict.get('coordination'),
        )

    @staticmethod
    def _parse_history(problem_list: List[str]) -> MedicalHistory:
        """Parse medical history from problem list"""
        return MedicalHistory(
            cardiovascular_history=any('CAD' in p or 'CHF' in p for p in problem_list),
            prior_stroke=any('stroke' in p.lower() for p in problem_list),
            prior_tia=any(
                'TIA' in p or 'transient ischemic' in p.lower() for p in problem_list
            ),
            diabetes=any('diabetes' in p.lower() or 'DM' in p for p in problem_list),
            hypertension=any(
                'hypertension' in p.lower() or 'HTN' in p for p in problem_list
            ),
            atrial_fibrillation=any(
                'afib' in p.lower() or 'atrial fib' in p.lower() for p in problem_list
            ),
        )

    def get_data_completeness(self) -> float:
        """Calculate data completeness score (0-1)"""
        essential_fields = [
            self.age is not None,
            self.sex is not None,
            self.vitals.BP_systolic is not None,
            self.vitals.heart_rate is not None,
            self.onset_hours is not None,
            self.timing is not None,
            self.examination.HINTS.is_complete(),
            self.examination.gait_test is not None,
            self.examination.coordination_test is not None,
        ]

        return sum(essential_fields) / len(essential_fields)
