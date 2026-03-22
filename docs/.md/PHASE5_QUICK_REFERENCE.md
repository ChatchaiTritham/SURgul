# Phase 5 Quick Reference Guide

**Fast lookup for common Phase 5 tasks**

---

## Validators

### NIST AI RMF Validator

```python
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator

# Basic usage
validator = NISTAIRMFValidator()
report = validator.validate(metadata)

# View results
print(f"Score: {report.compliance_score:.1%}")
print(f"Status: {report.certification_readiness}")

# Export report
validator.export_markdown_report(report, "nist_report.md")
```

**Key Metadata Fields:**
- `system_name`, `version`, `intended_use`
- `governance` - accountability, risk management, documentation
- `risk_assessment` - conducted, harms_identified, mitigation_strategies
- `validation` - internal_validation, external_validation, performance_metrics
- `transparency` - documentation_available, explainability, source_code_available
- `monitoring` - continuous_monitoring, performance_tracking, alert_system

### FDA GMLP Validator

```python
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator

# Basic usage
validator = FDAGMLPValidator()
report = validator.validate(metadata)

# View results
print(f"Score: {report.compliance_score:.1%}")
print(f"Status: {report.submission_readiness}")

# Export report
validator.export_markdown_report(report, "fda_report.md")
```

**Key Metadata Fields:**
- `system_name`, `version`, `intended_use`, `device_class`
- `development_team` - clinical_experts, data_scientists, software_engineers
- `software_engineering` - version_control, code_review, automated_testing
- `clinical_data` - representative_population, sample_size_adequate
- `validation` - independent_test_set, external_validation
- `model_design` - algorithm_justified, interpretability, uncertainty_quantification
- `transparency` - documentation, explainability, intended_use_statement

---

## Exporters

### JSON Exporter

```python
from surgul.exporters.json_exporter import JSONExporter

exporter = JSONExporter(pretty=True)

# Export clinical case
exporter.export_clinical_case(case, "case.json")

# Export triage decision
exporter.export_triage_decision(triage_decision, "decision.json")

# Export care recommendation
exporter.export_care_recommendation(recommendation, "recommendation.json")

# Export compliance report
exporter.export_compliance_report(report, "compliance.json")

# Batch export
exporter.export_batch(cases, "batch.json")
```

### CSV Exporter

```python
from surgul.exporters.csv_exporter import CSVExporter

# With auto-flattening
exporter = CSVExporter(flatten_nested=True)

# Export clinical cases
exporter.export_clinical_cases(cases, "cases.csv")

# Export triage decisions
exporter.export_triage_decisions(decisions, "decisions.csv")

# Export with custom columns
exporter.export(data, "output.csv", columns=['case_id', 'age', 'sex'])

# Export compliance summary
exporter.export_compliance_summary([report1, report2], "compliance.csv")
```

### FHIR Exporter

```python
from surgul.exporters.fhir_exporter import FHIRExporter

exporter = FHIRExporter(system_url="http://example.org")

# Export clinical case as Bundle
bundle = exporter.export_clinical_case_bundle(case, "bundle.json")

# Export triage decision as DiagnosticReport
report = exporter.export_triage_decision(decision, case, "report.json")

# Export care recommendation as ClinicalImpression
impression = exporter.export_care_recommendation(recommendation, case, "impression.json")

# Export individual resources
patient = exporter._create_patient(case)
observation = exporter._create_observation(...)
condition = exporter._create_condition(...)
```

### PDF Exporter

```python
from surgul.exporters.pdf_exporter import PDFExporter

exporter = PDFExporter(title="Clinical Report", page_size="Letter")

# Export clinical case
exporter.export_clinical_case(case, "case.pdf")

# Export triage decision
exporter.export_triage_decision(decision, case, "decision.pdf")

# Export care recommendation
exporter.export_care_recommendation(recommendation, case, "recommendation.pdf")

# Export compliance report
exporter.export_compliance_report(report, "compliance.pdf")
```

---

## CLI Commands

### Validate

```bash
# NIST validation
python -m src.cli.trix_cli validate --nist --output report.md

# FDA validation
python -m src.cli.trix_cli validate --fda --output report.md

# Both validators
python -m src.cli.trix_cli validate --nist --fda --format markdown

# With custom metadata
python -m src.cli.trix_cli validate --nist --metadata metadata.json --output report.md

# JSON output
python -m src.cli.trix_cli validate --nist --format json --output report.json
```

### Export

```bash
# Export to JSON
python -m src.cli.trix_cli export --input case.json --format json --output output.json

# Export to CSV
python -m src.cli.trix_cli export --input cases.json --format csv --output output.csv

# Export to FHIR
python -m src.cli.trix_cli export --input case.json --format fhir --output bundle.json

# Export to PDF
python -m src.cli.trix_cli export --input case.json --format pdf --output report.pdf
```

### Process

```bash
# Process and export to JSON (default)
python -m src.cli.trix_cli process --input case.json --output result.json

# Process and export to FHIR
python -m src.cli.trix_cli process --input case.json --format fhir --output result_fhir.json

# Process and create PDF report
python -m src.cli.trix_cli process --input case.json --format pdf --output report.pdf
```

---

## Common Patterns

### Multi-Format Export

```python
def export_all_formats(case, recommendation, base_name):
 from pathlib import Path
 base = Path(base_name)

 # JSON
 JSONExporter().export_care_recommendation(recommendation, f"{base}.json")

 # CSV
 CSVExporter().export([{
 'case_id': case.case_id,
 'risk_tier': recommendation.triage_decision.risk_tier.name,
 'confidence': recommendation.triage_decision.confidence
 }], f"{base}.csv")

 # FHIR
 FHIRExporter().export_care_recommendation(recommendation, case, f"{base}_fhir.json")

 # PDF (optional)
 try:
 PDFExporter().export_care_recommendation(recommendation, case, f"{base}.pdf")
 except ImportError:
 pass
```

### Batch Processing

```python
def process_batch(cases):
 pipeline = TRIXPipeline()
 results = []

 for case in cases:
 try:
 rec = pipeline.process(case)
 results.append({'case': case, 'recommendation': rec, 'status': 'success'})
 except Exception as e:
 results.append({'case': case, 'error': str(e), 'status': 'error'})

 return results
```

### Compliance Tracking

```python
def track_compliance(metadata, output_dir):
 from datetime import datetime
 import json

 # Run validations
 nist_report = NISTAIRMFValidator().validate(metadata)
 fda_report = FDAGMLPValidator().validate(metadata)

 # Create tracking record
 record = {
 'timestamp': datetime.now().isoformat(),
 'nist_score': nist_report.compliance_score,
 'fda_score': fda_report.compliance_score,
 'nist_status': nist_report.certification_readiness,
 'fda_status': fda_report.submission_readiness
 }

 # Append to tracking file
 tracking_file = Path(output_dir) / "compliance_history.json"
 if tracking_file.exists():
 with open(tracking_file) as f:
 data = json.load(f)
 else:
 data = {'records': []}

 data['records'].append(record)

 with open(tracking_file, 'w') as f:
 json.dump(data, f, indent=2)

 return record
```

---

## Data Structures

### Clinical Case (from_dict)

```python
case = ClinicalCase.from_dict({
 'case_id': 'TEST001',
 'age': 65,
 'sex': 'M',
 'BP_systolic': 150,
 'BP_diastolic': 90,
 'heart_rate': 88,
 'respiratory_rate': 16,
 'temperature': 37.0,
 'onset_hours': 4,
 'timing': 'acute',
 'pattern': 'worsening',
 'trigger': 'spontaneous',
 'diplopia': True,
 'dysarthria': True,
 'ataxia': True,
 'HINTS_head_impulse': 'abnormal',
 'HINTS_nystagmus': 'vertical',
 'HINTS_test_of_skew': 'positive',
 'gait_test': 'impaired',
 'coordination_test': 'impaired',
 'hypertension': True,
 'diabetes': True,
 'cardiovascular_history': True
})
```

### NIST Metadata Template

```python
nist_metadata = {
 "system_name": "Your System Name",
 "version": "1.0",
 "intended_use": "Clinical decision support for...",
 "algorithm_type": "Rule-based / ML / Hybrid",

 "governance": {
 "accountability": "Defined - [Role] responsible",
 "risk_management_process": "Implemented - [Process name]",
 "documentation": "Complete - [Documentation location]",
 "stakeholder_engagement": "Clinical experts consulted"
 },

 "risk_assessment": {
 "conducted": True,
 "harms_identified": ["Harm 1", "Harm 2"],
 "mitigation_strategies": ["Strategy 1", "Strategy 2"]
 },

 "bias_assessment": {
 "conducted": True,
 "demographic_analysis": True,
 "fairness_metrics": ["Metric 1", "Metric 2"]
 },

 "validation": {
 "internal_validation": True,
 "external_validation": False,
 "cross_validation": True,
 "performance_metrics": {
 "accuracy": 0.92,
 "sensitivity": 0.95,
 "specificity": 0.88
 }
 },

 "monitoring": {
 "continuous_monitoring": True,
 "performance_tracking": True,
 "alert_system": True
 },

 "transparency": {
 "documentation_available": True,
 "explainability": True,
 "source_code_available": True
 },

 "security": {
 "access_control": True,
 "data_encryption": True,
 "audit_logging": True
 }
}
```

### FDA Metadata Template

```python
fda_metadata = {
 "system_name": "Your System Name",
 "version": "1.0",
 "intended_use": "Clinical decision support for...",
 "device_class": "Class II",

 "development_team": {
 "clinical_experts": True,
 "data_scientists": True,
 "software_engineers": True,
 "regulatory_specialists": False
 },

 "software_engineering": {
 "version_control": True,
 "code_review": True,
 "automated_testing": True,
 "ci_cd_pipeline": True,
 "documentation": True,
 "coding_standards": True
 },

 "clinical_data": {
 "representative_population": True,
 "sample_size_adequate": True,
 "data_quality_assessed": True,
 "clinical_workflow_considered": True,
 "label_quality": True
 },

 "validation": {
 "independent_test_set": True,
 "external_validation": False,
 "hold_out_set": True,
 "performance_metrics": {
 "sensitivity": 0.95,
 "specificity": 0.88,
 "ppv": 0.89,
 "npv": 0.94
 }
 },

 "reference_standards": {
 "clinical_guidelines": ["Guideline 1", "Guideline 2"],
 "gold_standard": "Expert clinical diagnosis"
 },

 "model_design": {
 "algorithm_justified": True,
 "interpretability": True,
 "uncertainty_quantification": True,
 "safety_mechanisms": ["Mechanism 1", "Mechanism 2"]
 },

 "data_quality": {
 "preprocessing_documented": True,
 "missing_data_handled": True,
 "outlier_detection": True,
 "data_versioning": True
 },

 "monitoring": {
 "performance_monitoring": True,
 "continuous_monitoring": False,
 "drift_detection": False,
 "retraining_plan": False
 },

 "quality_culture": {
 "sop_documented": True,
 "training_programs": False,
 "quality_metrics": True
 },

 "transparency": {
 "documentation": True,
 "explainability": True,
 "intended_use_statement": True,
 "limitations_documented": True
 }
}
```

---

## Status Codes

### NIST Certification Readiness
- `READY` - Ready for certification
- `NEAR_READY` - Minor gaps, mostly compliant
- `NEEDS_WORK` - Significant gaps, needs improvement
- `NOT_READY` - Major deficiencies, substantial work needed

### FDA Submission Readiness
- `READY` - Ready for FDA submission
- `NEEDS_WORK` - Gaps present, address before submission
- `NOT_READY` - Major deficiencies, not ready for submission

---

## File Extensions

| Format | Extension | Description |
|--------|-----------|-------------|
| JSON | `.json` | Machine-readable, preserves structure |
| CSV | `.csv` | Spreadsheet, flattened structure |
| FHIR | `.json` | Healthcare standard, FHIR R4 compliant |
| PDF | `.pdf` | Human-readable reports |
| Markdown | `.md` | Human-readable documentation |

---

## Troubleshooting

### Import Error
```python
# Add project to path
import sys
import os
```

### PDF Not Available
```bash
pip install reportlab
```

### Low Compliance Score
Add comprehensive metadata - see templates above.

### FHIR Validation Fails
Ensure all required FHIR fields are present. Validate at https://validator.fhir.org/

---

## Resources

- **Tutorial**: [PHASE5_TUTORIAL.md](PHASE5_TUTORIAL.md)
- **Full Documentation**: [PHASE5_README.md](../PHASE5_README.md)
- **Completion Summary**: [PHASE_5_COMPLETION_SUMMARY.md](../PHASE_5_COMPLETION_SUMMARY.md)
- **Examples**: [examples/](../examples/)
- **Tests**: [tests/](../tests/)

---

**Quick Reference Version 1.0**
*Last Updated: 2026-01-10*


