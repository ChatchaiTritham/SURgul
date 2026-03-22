# Phase 5 Tutorial: Validators & Exporters

**A Step-by-Step Guide to Regulatory Compliance and Data Export**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Tutorial 1: Compliance Validation](#tutorial-1-compliance-validation)
4. [Tutorial 2: Data Export](#tutorial-2-data-export)
5. [Tutorial 3: Command-Line Interface](#tutorial-3-command-line-interface)
6. [Tutorial 4: End-to-End Workflow](#tutorial-4-end-to-end-workflow)
7. [Common Patterns & Best Practices](#common-patterns--best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Introduction

### What is Phase 5?

Phase 5 adds two critical capabilities to the TRI-X framework:

1. **Compliance Validation**: Automated checking against NIST AI RMF and FDA GMLP standards
2. **Multi-Format Export**: Converting TRI-X data to JSON, CSV, FHIR R4, and PDF formats

### Who Should Use This Tutorial?

- **Researchers**: Validating AI systems for clinical research
- **Developers**: Integrating TRI-X into healthcare systems
- **Regulatory Teams**: Preparing documentation for FDA submission
- **Clinical Teams**: Exporting data for EHR integration

### Prerequisites

- Python 3.8 or higher
- TRI-X framework installed (Phases 1-4)
- Basic understanding of Python programming
- Familiarity with clinical decision support concepts

### Learning Outcomes

By the end of this tutorial, you'll be able to:
- âœ… Run compliance validation against NIST AI RMF and FDA GMLP
- âœ… Export clinical data to multiple formats
- âœ… Use the TRI-X CLI for automated workflows
- âœ… Integrate Phase 5 into your applications
- âœ… Troubleshoot common issues

---

## Getting Started

### Installation

Phase 5 is included with the TRI-X framework. No additional installation is required for core functionality.

**Optional: PDF Export Support**
```bash
pip install reportlab
```

### Verify Installation

```python
# Test imports
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
from surgul.exporters.json_exporter import JSONExporter
from surgul.exporters.csv_exporter import CSVExporter
from surgul.exporters.fhir_exporter import FHIRExporter

print("âœ… Phase 5 components imported successfully!")
```

### Directory Structure

```
SURgul/
â”œâ”€â”€ src/
â”‚ â”œâ”€â”€ validators/
â”‚ â”‚ â”œâ”€â”€ nist_ai_rmf_validator.py
â”‚ â”‚ â””â”€â”€ fda_gmlp_validator.py
â”‚ â”œâ”€â”€ exporters/
â”‚ â”‚ â”œâ”€â”€ json_exporter.py
â”‚ â”‚ â”œâ”€â”€ csv_exporter.py
â”‚ â”‚ â”œâ”€â”€ fhir_exporter.py
â”‚ â”‚ â””â”€â”€ pdf_exporter.py
â”‚ â””â”€â”€ cli/
â”‚ â””â”€â”€ trix_cli.py
â”œâ”€â”€ examples/
â”‚ â”œâ”€â”€ example_phase5_validators.py
â”‚ â””â”€â”€ example_phase5_exporters.py
â””â”€â”€ tests/
 â”œâ”€â”€ test_validators.py
 â””â”€â”€ test_exporters.py
```

---

## Tutorial 1: Compliance Validation

### 1.1 Understanding Compliance Validation

Compliance validation assesses whether your AI system meets regulatory standards:

- **NIST AI RMF**: Focus on AI risk management, governance, and trustworthiness
- **FDA GMLP**: Focus on medical device quality, validation, and clinical safety

### 1.2 NIST AI RMF Validation (Basic)

Let's start with a simple NIST validation:

```python
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator

# Step 1: Create validator
validator = NISTAIRMFValidator()

# Step 2: Define minimal system metadata
metadata = {
 "system_name": "My AI System",
 "version": "1.0",
}

# Step 3: Run validation
report = validator.validate(metadata)

# Step 4: View results
print(f"Compliance Score: {report.compliance_score:.1%}")
print(f"Regulatory Ready: {report.regulatory_ready}")
print(f"Status: {report.certification_readiness}")
```

**Expected Output:**
```
Compliance Score: 15.0%
Regulatory Ready: False
Status: NOT_READY
```

**Why so low?** We only provided minimal information. Let's improve!

### 1.3 NIST AI RMF Validation (Comprehensive)

Now let's provide comprehensive metadata:

```python
metadata = {
 "system_name": "TRI-X Framework",
 "version": "1.0",
 "intended_use": "Clinical decision support for acute dizziness triage",
 "algorithm_type": "Rule-based expert system",

 # Governance
 "governance": {
 "accountability": "Defined - Principal Investigator responsible",
 "risk_management_process": "Implemented - Systematic SRGL gates",
 "documentation": "Complete - Phase 1-5 documentation",
 "stakeholder_engagement": "Clinical experts consulted"
 },

 # Risk Assessment
 "risk_assessment": {
 "conducted": True,
 "harms_identified": [
 "Misclassification of high-risk patients",
 "Delayed treatment due to false negatives"
 ],
 "mitigation_strategies": [
 "Conservative MAX-based merging",
 "Human oversight requirement",
 "Confidence thresholds (0.7)",
 "Abstention mechanism (>= 0.8 uncertainty)"
 ]
 },

 # Validation
 "validation": {
 "internal_validation": True,
 "external_validation": False, # Gap!
 "performance_metrics": {
 "accuracy": 0.92,
 "sensitivity": 0.95,
 "specificity": 0.88
 }
 },

 # Transparency
 "transparency": {
 "documentation_available": True,
 "explainability": True,
 "source_code_available": True
 }
}

# Run validation
report = validator.validate(metadata)

# Detailed results
print(f"\nCompliance Score: {report.compliance_score:.1%}")
print(f"Status: {report.certification_readiness}")
print(f"\nChecks: {report.checks_passed}/{report.total_checks} passed")

# Show function breakdown
print(f"\nðŸ“‹ Function Breakdown:")
for func in ['GOVERN', 'MAP', 'MEASURE', 'MANAGE']:
 func_checks = [c for c in report.all_checks if c.function == func]
 passed = sum(1 for c in func_checks if c.status == 'PASS')
 total = len(func_checks)
 print(f" {func}: {passed}/{total} ({passed/total*100:.0f}%)")
```

**Expected Output:**
```
Compliance Score: 68.5%
Status: NEEDS_WORK

Checks: 29/42 passed

ðŸ“‹ Function Breakdown:
 GOVERN: 9/10 (90%)
 MAP: 7/10 (70%)
 MEASURE: 6/12 (50%)
 MANAGE: 7/10 (70%)
```

**Much better!** But we still need external validation.

### 1.4 Viewing Critical Deficiencies

```python
# Show what's missing
if report.critical_deficiencies:
 print("\nâš  Critical Deficiencies:")
 for i, deficiency in enumerate(report.critical_deficiencies, 1):
 print(f" {i}. {deficiency}")

# Show recommendations
if report.recommendations:
 print("\nðŸ’¡ Top Recommendations:")
 for i, rec in enumerate(report.recommendations[:3], 1):
 print(f" {i}. {rec}")
```

**Output:**
```
âš  Critical Deficiencies:
 1. No external validation on real clinical data
 2. No continuous monitoring system implemented
 3. Limited demographic bias assessment

ðŸ’¡ Top Recommendations:
 1. Conduct external validation study on independent dataset
 2. Implement continuous performance monitoring system
 3. Perform comprehensive demographic bias assessment
```

### 1.5 Exporting NIST Reports

```python
from pathlib import Path

# Export to Markdown (human-readable)
output_dir = Path("compliance_reports")
output_dir.mkdir(exist_ok=True)

validator.export_markdown_report(report, output_dir / "nist_report.md")
print(f"âœ… Markdown report: compliance_reports/nist_report.md")

# Export to JSON (machine-readable)
from surgul.exporters.json_exporter import JSONExporter
json_exporter = JSONExporter()
json_exporter.export_compliance_report(report, output_dir / "nist_report.json")
print(f"âœ… JSON report: compliance_reports/nist_report.json")
```

### 1.6 FDA GMLP Validation

FDA GMLP validation follows a similar pattern:

```python
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator

# Create validator
fda_validator = FDAGMLPValidator()

# Define metadata
metadata = {
 "system_name": "TRI-X Framework",
 "version": "1.0",
 "intended_use": "Clinical decision support for acute dizziness triage",
 "device_class": "Class II",

 # P1: Multi-Disciplinary Expertise
 "development_team": {
 "clinical_experts": True,
 "data_scientists": True,
 "software_engineers": True,
 "regulatory_specialists": False # Gap!
 },

 # P2: Good Software Engineering
 "software_engineering": {
 "version_control": True,
 "code_review": True,
 "automated_testing": True,
 "ci_cd_pipeline": True,
 "documentation": True
 },

 # P3: Clinical Data
 "clinical_data": {
 "representative_population": True,
 "sample_size_adequate": True,
 "data_quality_assessed": True,
 "clinical_workflow_considered": True
 },

 # P4: Independent Validation
 "validation": {
 "independent_test_set": True,
 "external_validation": False, # Gap!
 "hold_out_set": True
 },

 # P6: Model Design
 "model_design": {
 "algorithm_justified": True,
 "interpretability": True,
 "uncertainty_quantification": True,
 "safety_mechanisms": [
 "Abstention when uncertain",
 "Conservative MAX merging",
 "Human oversight required"
 ]
 },

 # P10: Transparency
 "transparency": {
 "documentation": True,
 "explainability": True,
 "intended_use_statement": True,
 "limitations_documented": True
 }
}

# Run validation
fda_report = fda_validator.validate(metadata)

# View results
print(f"\nFDA GMLP Compliance: {fda_report.compliance_score:.1%}")
print(f"Submission Status: {fda_report.submission_readiness}")
print(f"Device Class: {fda_report.device_classification}")

# Principle breakdown
print(f"\nðŸ“‹ GMLP Principles:")
for i in range(1, 11):
 principle = f"P{i}"
 p_checks = [c for c in fda_report.all_checks if c.principle == principle]
 if p_checks:
 passed = sum(1 for c in p_checks if c.status == 'PASS')
 total = len(p_checks)
 name = p_checks[0].principle_name
 status = "âœ…" if passed == total else "âš ï¸"
 print(f" {status} {principle}: {passed}/{total} - {name}")
```

**Output:**
```
FDA GMLP Compliance: 62.0%
Submission Status: NEEDS_WORK
Device Class: Class II

ðŸ“‹ GMLP Principles:
 âœ… P1: 3/3 - Multi-Disciplinary Expertise
 âœ… P2: 5/5 - Good Software Engineering
 âœ… P3: 4/4 - Clinical Study Participants
 âš ï¸ P4: 1/2 - Independent Data Sets
 âœ… P5: 2/2 - Reference Standards
 âœ… P6: 4/4 - Model Design
 âœ… P7: 3/3 - Data Quality
 âš ï¸ P8: 1/3 - Performance Monitoring
 âš ï¸ P9: 2/3 - Quality Culture
 âœ… P10: 4/4 - Transparency
```

### 1.7 Pre-Submission Actions

```python
# View pre-submission actions
if fda_report.pre_submission_actions:
 print("\nðŸ“‹ Pre-Submission Actions:")
 for i, action in enumerate(fda_report.pre_submission_actions, 1):
 print(f" {i}. {action}")
```

**Output:**
```
ðŸ“‹ Pre-Submission Actions:
 1. Conduct external validation study on independent clinical dataset
 2. Implement continuous performance monitoring system
 3. Add regulatory specialist to development team
 4. Document post-market surveillance plan
 5. Complete demographic subgroup analysis
```

### 1.8 Comparing Both Frameworks

```python
# Run both validations
nist_report = validator.validate(metadata)
fda_report = fda_validator.validate(metadata)

# Compare
print(f"\nðŸ“Š Compliance Comparison:")
print(f" NIST AI RMF: {nist_report.compliance_score:.1%} - {nist_report.certification_readiness}")
print(f" FDA GMLP: {fda_report.compliance_score:.1%} - {fda_report.submission_readiness}")

# Common gaps
print(f"\nðŸŽ¯ Common Critical Gaps:")
nist_gaps = set(nist_report.critical_deficiencies)
fda_gaps = set(fda_report.critical_deficiencies)
common = nist_gaps & fda_gaps

if common:
 for i, gap in enumerate(common, 1):
 print(f" {i}. {gap}")
else:
 print(" (Review individual reports for framework-specific gaps)")
```

---

## Tutorial 2: Data Export

### 2.1 Understanding Export Formats

Each format serves a different purpose:

| Format | Best For | Preserves Structure | Machine Readable | Human Readable |
|--------|----------|---------------------|------------------|----------------|
| JSON | APIs, storage | âœ… Yes | âœ… Yes | âš ï¸ Partial |
| CSV | Spreadsheets | âŒ Flattened | âœ… Yes | âœ… Yes |
| FHIR | EHR integration | âœ… Yes | âœ… Yes | âŒ No |
| PDF | Clinical reports | âŒ No | âŒ No | âœ… Yes |

### 2.2 JSON Export (Basic)

```python
from surgul.clinical_case import ClinicalCase
from surgul.exporters.json_exporter import JSONExporter
from pathlib import Path

# Create output directory
output_dir = Path("exports_tutorial/json")
output_dir.mkdir(parents=True, exist_ok=True)

# Create sample clinical case
case = ClinicalCase.from_dict({
 'case_id': 'TUTORIAL_001',
 'age': 65,
 'sex': 'M',
 'BP_systolic': 150,
 'heart_rate': 88,
 'onset_hours': 4,
 'diplopia': True,
 'dysarthria': True
})

# Export to JSON
json_exporter = JSONExporter(pretty=True)
json_exporter.export_clinical_case(case, output_dir / "case.json")
print(f"âœ… Exported: {output_dir / 'case.json'}")
```

**Output File (`case.json`):**
```json
{
 "format": "clinical_case",
 "version": "1.0",
 "timestamp": "2026-01-10T14:30:00",
 "data": {
 "case_id": "TUTORIAL_001",
 "age": 65,
 "sex": "M",
 "vitals": {
 "BP_systolic": 150,
 "heart_rate": 88
 },
 "critical_flags": {
 "diplopia": true,
 "dysarthria": true
 },
 "onset_hours": 4
 }
}
```

### 2.3 JSON Export (Batch)

```python
# Create multiple cases
cases = [
 ClinicalCase.from_dict({'case_id': f'CASE_{i}', 'age': 60+i, 'sex': 'M' if i%2==0 else 'F'})
 for i in range(1, 6)
]

# Batch export
json_exporter.export_batch(cases, output_dir / "cases_batch.json")
print(f"âœ… Exported {len(cases)} cases to batch file")
```

### 2.4 Processing and Exporting Results

```python
from surgul.trix_pipeline import TRIXPipeline

# Process case through TRI-X
pipeline = TRIXPipeline()
recommendation = pipeline.process(case)

# Export triage decision
json_exporter.export_triage_decision(
 recommendation.triage_decision,
 output_dir / "triage_decision.json"
)

# Export complete care recommendation
json_exporter.export_care_recommendation(
 recommendation,
 output_dir / "care_recommendation.json"
)

print(f"âœ… Results exported:")
print(f" - Triage decision: {output_dir / 'triage_decision.json'}")
print(f" - Care recommendation: {output_dir / 'care_recommendation.json'}")
```

### 2.5 CSV Export

CSV is ideal for spreadsheet analysis:

```python
from surgul.exporters.csv_exporter import CSVExporter

output_dir = Path("exports_tutorial/csv")
output_dir.mkdir(parents=True, exist_ok=True)

# Create CSV exporter with auto-flattening
csv_exporter = CSVExporter(flatten_nested=True)

# Export cases
csv_exporter.export_clinical_cases(cases, output_dir / "cases.csv")
print(f"âœ… Exported to: {output_dir / 'cases.csv'}")
```

**Output File (`cases.csv`):**
```csv
case_id,age,sex,vitals.BP_systolic,vitals.heart_rate,critical_flags.diplopia,critical_flags.dysarthria
CASE_1,61,F,,,False,False
CASE_2,62,M,,,False,False
CASE_3,63,F,,,False,False
```

### 2.6 CSV Export (Custom Columns)

```python
# Export only specific columns
custom_columns = ['case_id', 'age', 'sex', 'vitals.BP_systolic', 'vitals.heart_rate']

csv_exporter.export(cases, output_dir / "cases_summary.csv", columns=custom_columns)
print(f"âœ… Custom column export complete")
```

### 2.7 CSV Export (Triage Decisions)

```python
# Process multiple cases and export decisions
decisions = []
for case in cases:
 rec = pipeline.process(case)
 decisions.append({
 'case_id': case.case_id,
 'risk_tier': rec.triage_decision.risk_tier.name,
 'confidence': rec.triage_decision.confidence,
 'action_state': rec.action_state.name,
 'timestamp': rec.triage_decision.timestamp
 })

csv_exporter.export(decisions, output_dir / "triage_decisions.csv")
print(f"âœ… Triage decisions: {output_dir / 'triage_decisions.csv'}")
```

### 2.8 FHIR Export (Healthcare Standard)

FHIR (Fast Healthcare Interoperability Resources) is the standard for EHR integration:

```python
from surgul.exporters.fhir_exporter import FHIRExporter

output_dir = Path("exports_tutorial/fhir")
output_dir.mkdir(parents=True, exist_ok=True)

# Create FHIR exporter
fhir_exporter = FHIRExporter(system_url="http://trix.tutorial.example")

# Export clinical case as FHIR Bundle
bundle = fhir_exporter.export_clinical_case_bundle(
 case,
 output_dir / "case_bundle.json"
)

print(f"âœ… FHIR Bundle created:")
print(f" Resources: {len(bundle['entry'])}")
print(f" Types: {', '.join(set(e['resource']['resourceType'] for e in bundle['entry']))}")
```

**Output:**
```
âœ… FHIR Bundle created:
 Resources: 7
 Types: Patient, Observation, Condition
```

### 2.9 FHIR DiagnosticReport

```python
# Export triage decision as DiagnosticReport
diagnostic_report = fhir_exporter.export_triage_decision(
 recommendation.triage_decision,
 case,
 output_dir / "diagnostic_report.json"
)

print(f"âœ… DiagnosticReport created:")
print(f" Status: {diagnostic_report['status']}")
print(f" Code: {diagnostic_report['code']['coding'][0]['display']}")
```

### 2.10 FHIR ClinicalImpression

```python
# Export care recommendation as ClinicalImpression
clinical_impression = fhir_exporter.export_care_recommendation(
 recommendation,
 case,
 output_dir / "clinical_impression.json"
)

print(f"âœ… ClinicalImpression created:")
print(f" Status: {clinical_impression['status']}")
print(f" Summary: {clinical_impression.get('summary', 'N/A')[:60]}...")
```

### 2.11 PDF Export (Human Reports)

**Note:** Requires `reportlab` library.

```python
try:
 from surgul.exporters.pdf_exporter import PDFExporter

 output_dir = Path("exports_tutorial/pdf")
 output_dir.mkdir(parents=True, exist_ok=True)

 # Create PDF exporter
 pdf_exporter = PDFExporter(title="TRI-X Clinical Report")

 # Export clinical case
 pdf_exporter.export_clinical_case(case, output_dir / "clinical_case.pdf")

 # Export triage decision
 pdf_exporter.export_triage_decision(
 recommendation.triage_decision,
 case,
 output_dir / "triage_decision.pdf"
 )

 # Export care recommendation
 pdf_exporter.export_care_recommendation(
 recommendation,
 case,
 output_dir / "care_recommendation.pdf"
 )

 print(f"âœ… PDF reports generated in: {output_dir}")

except ImportError:
 print("âš ï¸ PDF export not available. Install reportlab: pip install reportlab")
```

---

## Tutorial 3: Command-Line Interface

The TRI-X CLI provides convenient command-line access to Phase 5 functionality.

### 3.1 CLI Help

```bash
python -m src.cli.trix_cli --help
```

**Output:**
```
TRI-X Framework CLI

Commands:
 validate Run compliance validation
 export Export data to various formats
 process Process clinical case through TRI-X pipeline

Use 'trix_cli <command> --help' for command-specific help.
```

### 3.2 Validate Command

```bash
# NIST validation
python -m src.cli.trix_cli validate --nist --output nist_report.md

# FDA validation
python -m src.cli.trix_cli validate --fda --output fda_report.md

# Both validations
python -m src.cli.trix_cli validate --nist --fda --format markdown

# With custom metadata
python -m src.cli.trix_cli validate --nist --metadata custom_metadata.json --output report.md
```

### 3.3 Export Command

```bash
# Export to FHIR
python -m src.cli.trix_cli export --input case.json --format fhir --output case_fhir.json

# Export to CSV
python -m src.cli.trix_cli export --input cases.json --format csv --output cases.csv

# Export to PDF
python -m src.cli.trix_cli export --input case.json --format pdf --output report.pdf
```

### 3.4 Process Command

```bash
# Process and export to JSON
python -m src.cli.trix_cli process --input case.json --output result.json

# Process and export to FHIR
python -m src.cli.trix_cli process --input case.json --format fhir --output result_fhir.json

# Process and create PDF report
python -m src.cli.trix_cli process --input case.json --format pdf --output clinical_report.pdf
```

### 3.5 Example Workflow

```bash
# 1. Create input case (case.json)
echo '{
 "case_id": "ED_12345",
 "age": 68,
 "sex": "M",
 "BP_systolic": 165,
 "heart_rate": 92,
 "onset_hours": 2,
 "diplopia": true,
 "dysarthria": true,
 "ataxia": true
}' > case.json

# 2. Process through TRI-X
python -m src.cli.trix_cli process --input case.json --output result.json

# 3. Export to FHIR for EHR integration
python -m src.cli.trix_cli export --input result.json --format fhir --output ehr_bundle.json

# 4. Generate PDF for clinician
python -m src.cli.trix_cli export --input result.json --format pdf --output clinician_report.pdf

# 5. Validate TRI-X compliance
python -m src.cli.trix_cli validate --nist --fda --output compliance_report.md
```

---

## Tutorial 4: End-to-End Workflow

Let's combine everything into a complete workflow.

### 4.1 Scenario: Emergency Department Integration

**Goal**: Process ED patients, export to EHR, and track compliance.

```python
from pathlib import Path
from surgul.clinical_case import ClinicalCase
from surgul.trix_pipeline import TRIXPipeline
from surgul.exporters.json_exporter import JSONExporter
from surgul.exporters.fhir_exporter import FHIRExporter
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator

# Setup
output_dir = Path("ed_integration")
output_dir.mkdir(exist_ok=True)

# Step 1: Receive patient data from ED system
ed_patients = [
 {
 'case_id': 'ED_001',
 'age': 72,
 'sex': 'M',
 'BP_systolic': 180,
 'heart_rate': 95,
 'onset_hours': 3,
 'diplopia': True,
 'dysarthria': True,
 'ataxia': True
 },
 {
 'case_id': 'ED_002',
 'age': 52,
 'sex': 'F',
 'BP_systolic': 125,
 'heart_rate': 70,
 'onset_hours': 48,
 'timing': 'episodic',
 'trigger': 'positional'
 }
]

print("ðŸ“¥ Received 2 patients from ED system")

# Step 2: Process through TRI-X
pipeline = TRIXPipeline()
results = []

for patient_data in ed_patients:
 case = ClinicalCase.from_dict(patient_data)
 recommendation = pipeline.process(case)
 results.append({
 'case': case,
 'recommendation': recommendation
 })

 print(f" âœ“ {case.case_id}: {recommendation.triage_decision.risk_tier.name}")

# Step 3: Export to FHIR for EHR integration
fhir_exporter = FHIRExporter(system_url="http://hospital.example.org/trix")

for result in results:
 case_id = result['case'].case_id

 # Create FHIR bundle
 bundle_path = output_dir / f"{case_id}_bundle.json"
 fhir_exporter.export_clinical_case_bundle(result['case'], bundle_path)

 # Create diagnostic report
 report_path = output_dir / f"{case_id}_report.json"
 fhir_exporter.export_triage_decision(
 result['recommendation'].triage_decision,
 result['case'],
 report_path
 )

 print(f" âœ“ {case_id}: FHIR resources exported")

# Step 4: Archive results as JSON
json_exporter = JSONExporter(pretty=True)
archive_data = [{
 'case_id': r['case'].case_id,
 'risk_tier': r['recommendation'].triage_decision.risk_tier.name,
 'confidence': r['recommendation'].triage_decision.confidence,
 'action_state': r['recommendation'].action_state.name,
 'recommendations': [rec.recommendation for rec in r['recommendation'].recommendations]
} for r in results]

json_exporter.export_batch(archive_data, output_dir / "daily_archive.json")
print(f"\nðŸ’¾ Daily archive saved: {output_dir / 'daily_archive.json'}")

# Step 5: Compliance check (weekly)
print(f"\nðŸ“Š Running weekly compliance check...")
validator = NISTAIRMFValidator()

metadata = {
 "system_name": "TRI-X ED Integration",
 "version": "1.0",
 "validation": {"internal_validation": True},
 "governance": {"documentation": "Complete"},
 "transparency": {"explainability": True}
}

report = validator.validate(metadata)
print(f" Compliance: {report.compliance_score:.1%}")
print(f" Status: {report.certification_readiness}")

# Export compliance report
validator.export_markdown_report(report, output_dir / "weekly_compliance.md")
print(f" âœ“ Report: {output_dir / 'weekly_compliance.md'}")

print(f"\nâœ… ED integration workflow complete!")
print(f"ðŸ“ All files in: {output_dir}/")
```

### 4.2 Scenario: Research Study Data Export

**Goal**: Export research data for analysis and publication.

```python
from surgul.exporters.csv_exporter import CSVExporter
from surgul.exporters.pdf_exporter import PDFExporter

# Setup
study_dir = Path("research_study")
study_dir.mkdir(exist_ok=True)

# Simulate processing 100 cases
print("ðŸ”¬ Processing research study cases...")
study_results = []

for i in range(1, 101):
 # Simulate case data
 case_data = {
 'case_id': f'STUDY_{i:03d}',
 'age': 50 + (i % 40),
 'sex': 'M' if i % 2 == 0 else 'F'
 }

 case = ClinicalCase.from_dict(case_data)
 recommendation = pipeline.process(case)

 study_results.append({
 'case_id': case.case_id,
 'age': case.age,
 'sex': case.sex,
 'risk_tier': recommendation.triage_decision.risk_tier.name,
 'confidence': recommendation.triage_decision.confidence,
 'processing_time_ms': 10.5 # Placeholder
 })

print(f" âœ“ Processed {len(study_results)} cases")

# Export to CSV for statistical analysis
csv_exporter = CSVExporter()
csv_exporter.export(study_results, study_dir / "study_results.csv")
print(f" âœ“ CSV export: {study_dir / 'study_results.csv'}")

# Calculate summary statistics
from collections import Counter
risk_distribution = Counter(r['risk_tier'] for r in study_results)
avg_confidence = sum(r['confidence'] for r in study_results) / len(study_results)

print(f"\nðŸ“ˆ Study Summary:")
print(f" Total Cases: {len(study_results)}")
print(f" Risk Distribution:")
for tier, count in risk_distribution.most_common():
 print(f" {tier}: {count} ({count/len(study_results)*100:.1f}%)")
print(f" Average Confidence: {avg_confidence:.2f}")

# Export summary to JSON
summary = {
 'study_id': 'TRI-X-VALIDATION-2026',
 'total_cases': len(study_results),
 'risk_distribution': dict(risk_distribution),
 'average_confidence': avg_confidence
}

json_exporter.export(summary, study_dir / "study_summary.json")
print(f" âœ“ Summary: {study_dir / 'study_summary.json'}")

print(f"\nâœ… Research study export complete!")
```

---

## Common Patterns & Best Practices

### Pattern 1: Batch Processing with Progress Tracking

```python
from tqdm import tqdm # pip install tqdm

def process_batch_with_progress(cases, output_dir):
 """Process cases with progress bar"""
 pipeline = TRIXPipeline()
 results = []

 for case in tqdm(cases, desc="Processing cases"):
 try:
 recommendation = pipeline.process(case)
 results.append({
 'case': case,
 'recommendation': recommendation,
 'status': 'success'
 })
 except Exception as e:
 results.append({
 'case': case,
 'error': str(e),
 'status': 'error'
 })

 return results
```

### Pattern 2: Error Handling in Exports

```python
def safe_export(exporter, data, output_path, format_name="data"):
 """Export with error handling"""
 try:
 exporter.export(data, output_path)
 print(f"âœ… {format_name} exported: {output_path}")
 return True
 except Exception as e:
 print(f"âŒ {format_name} export failed: {e}")
 return False
```

### Pattern 3: Multi-Format Export

```python
def export_all_formats(case, recommendation, base_path):
 """Export to all available formats"""
 base_path = Path(base_path)
 results = {}

 # JSON
 json_exporter = JSONExporter(pretty=True)
 results['json'] = safe_export(
 json_exporter,
 recommendation,
 base_path.with_suffix('.json'),
 'JSON'
 )

 # CSV (flatten recommendation)
 csv_exporter = CSVExporter(flatten_nested=True)
 csv_data = [{
 'case_id': case.case_id,
 'risk_tier': recommendation.triage_decision.risk_tier.name,
 'confidence': recommendation.triage_decision.confidence
 }]
 results['csv'] = safe_export(
 csv_exporter,
 csv_data,
 base_path.with_suffix('.csv'),
 'CSV'
 )

 # FHIR
 fhir_exporter = FHIRExporter()
 try:
 fhir_exporter.export_care_recommendation(
 recommendation,
 case,
 base_path.with_name(f"{base_path.stem}_fhir.json")
 )
 results['fhir'] = True
 print(f"âœ… FHIR exported")
 except Exception as e:
 results['fhir'] = False
 print(f"âŒ FHIR export failed: {e}")

 # PDF (optional)
 try:
 from surgul.exporters.pdf_exporter import PDFExporter
 pdf_exporter = PDFExporter()
 pdf_exporter.export_care_recommendation(
 recommendation,
 case,
 base_path.with_suffix('.pdf')
 )
 results['pdf'] = True
 print(f"âœ… PDF exported")
 except ImportError:
 results['pdf'] = False
 print("âš ï¸ PDF export skipped (reportlab not installed)")
 except Exception as e:
 results['pdf'] = False
 print(f"âŒ PDF export failed: {e}")

 return results
```

### Pattern 4: Compliance Tracking Over Time

```python
from datetime import datetime

def track_compliance_over_time(metadata, output_dir):
 """Track compliance scores over time"""
 output_dir = Path(output_dir)
 output_dir.mkdir(exist_ok=True)

 # Run validations
 nist_validator = NISTAIRMFValidator()
 nist_report = nist_validator.validate(metadata)

 from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
 fda_validator = FDAGMLPValidator()
 fda_report = fda_validator.validate(metadata)

 # Create tracking record
 record = {
 'timestamp': datetime.now().isoformat(),
 'system_name': metadata.get('system_name', 'Unknown'),
 'version': metadata.get('version', 'Unknown'),
 'nist_score': nist_report.compliance_score,
 'nist_status': nist_report.certification_readiness,
 'fda_score': fda_report.compliance_score,
 'fda_status': fda_report.submission_readiness
 }

 # Append to tracking file
 tracking_file = output_dir / "compliance_tracking.json"

 if tracking_file.exists():
 import json
 with open(tracking_file, 'r') as f:
 tracking_data = json.load(f)
 else:
 tracking_data = {'records': []}

 tracking_data['records'].append(record)

 with open(tracking_file, 'w') as f:
 json.dump(tracking_data, f, indent=2)

 print(f"âœ… Compliance tracking updated: {tracking_file}")
 return record
```

### Pattern 5: Validation Before Export

```python
def validate_before_export(case, recommendation, export_func, *args, **kwargs):
 """Validate data before exporting"""

 # Check case has required fields
 if not case.case_id:
 raise ValueError("Case missing case_id")

 # Check recommendation is complete
 if not recommendation.triage_decision:
 raise ValueError("Recommendation missing triage_decision")

 # Check confidence threshold
 if recommendation.triage_decision.confidence < 0.5:
 print(f"âš ï¸ Warning: Low confidence ({recommendation.triage_decision.confidence:.2f})")

 # Proceed with export
 return export_func(*args, **kwargs)
```

---

## Troubleshooting

### Issue 1: Import Errors

**Problem:**
```python
ImportError: cannot import name 'NISTAIRMFValidator'
```

**Solution:**
```python
# Ensure you're in the correct directory
import sys
import os

# Or use module import
python -m src.validators.nist_ai_rmf_validator
```

### Issue 2: PDF Export Not Available

**Problem:**
```
ImportError: No module named 'reportlab'
```

**Solution:**
```bash
pip install reportlab
```

Or handle gracefully:
```python
try:
 from surgul.exporters.pdf_exporter import PDFExporter
 PDF_AVAILABLE = True
except ImportError:
 PDF_AVAILABLE = False
 print("âš ï¸ PDF export disabled. Install reportlab to enable.")
```

### Issue 3: Low Compliance Scores

**Problem:**
```
Compliance Score: 15.0%
Status: NOT_READY
```

**Solution:**
Provide comprehensive metadata. See [Tutorial 1.3](#13-nist-ai-rmf-validation-comprehensive) for examples.

### Issue 4: FHIR Validation Errors

**Problem:**
FHIR resources fail validation against FHIR spec.

**Solution:**
- Ensure all required fields are present
- Use standard coding systems (LOINC, SNOMED CT)
- Validate against FHIR validator: https://validator.fhir.org/

### Issue 5: CSV Nested Structure Lost

**Problem:**
Nested data structures are flattened in CSV.

**Solution:**
```python
# Use flatten_nested=True and dot notation
csv_exporter = CSVExporter(flatten_nested=True)

# Nested data becomes: vitals.BP_systolic, vitals.heart_rate, etc.
```

### Issue 6: Large File Performance

**Problem:**
Exporting large batches is slow.

**Solution:**
```python
# Use batch export with chunking
def export_large_batch(cases, output_path, chunk_size=1000):
 json_exporter = JSONExporter()

 for i in range(0, len(cases), chunk_size):
 chunk = cases[i:i+chunk_size]
 chunk_path = output_path.with_name(f"{output_path.stem}_{i//chunk_size}{output_path.suffix}")
 json_exporter.export_batch(chunk, chunk_path)
 print(f" âœ“ Chunk {i//chunk_size}: {len(chunk)} cases")
```

### Issue 7: CLI Command Not Found

**Problem:**
```bash
python -m src.cli.trix_cli: No module named src.cli.trix_cli
```

**Solution:**
```bash
# Ensure you're in the project root directory
cd /path/to/SURgul

# Verify CLI file exists
ls src/cli/trix_cli.py

# Run with full path
python -m src.cli.trix_cli --help
```

---

## Next Steps

### Congratulations!

You've completed the Phase 5 tutorial. You now know how to:
- âœ… Validate AI systems against NIST AI RMF and FDA GMLP
- âœ… Export clinical data to JSON, CSV, FHIR, and PDF
- âœ… Use the TRI-X CLI for automated workflows
- âœ… Implement end-to-end integration patterns

### Continue Learning

1. **Run Example Scripts**
 ```bash
 python examples/example_phase5_validators.py
 python examples/example_phase5_exporters.py
 ```

2. **Explore Test Suite**
 ```bash
 pytest tests/test_validators.py -v
 pytest tests/test_exporters.py -v
 ```

3. **Read Full Documentation**
 - [PHASE5_README.md](../PHASE5_README.md)
 - [PHASE_5_COMPLETION_SUMMARY.md](../PHASE_5_COMPLETION_SUMMARY.md)

4. **Integrate into Your Workflow**
 - Customize metadata for your system
 - Set up automated compliance tracking
 - Integrate FHIR export with your EHR

### Getting Help

- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory
- **Tests**: See `tests/` directory for usage examples
- **Issues**: Report bugs or request features in your issue tracker

### Advanced Topics

For advanced usage, consider:
- Custom validators for other regulatory frameworks
- Custom exporters for proprietary formats
- Integration with CI/CD pipelines for continuous compliance tracking
- Real-time monitoring dashboards using exported data

---

## Appendix: Quick Reference

### Validator Quick Reference

```python
# NIST AI RMF
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator
validator = NISTAIRMFValidator()
report = validator.validate(metadata)

# FDA GMLP
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
validator = FDAGMLPValidator()
report = validator.validate(metadata)
```

### Exporter Quick Reference

```python
# JSON
from surgul.exporters.json_exporter import JSONExporter
exporter = JSONExporter(pretty=True)
exporter.export_clinical_case(case, "output.json")

# CSV
from surgul.exporters.csv_exporter import CSVExporter
exporter = CSVExporter(flatten_nested=True)
exporter.export_clinical_cases(cases, "output.csv")

# FHIR
from surgul.exporters.fhir_exporter import FHIRExporter
exporter = FHIRExporter()
bundle = exporter.export_clinical_case_bundle(case, "bundle.json")

# PDF
from surgul.exporters.pdf_exporter import PDFExporter
exporter = PDFExporter()
exporter.export_clinical_case(case, "report.pdf")
```

### CLI Quick Reference

```bash
# Validate
python -m src.cli.trix_cli validate --nist --output report.md

# Export
python -m src.cli.trix_cli export --input case.json --format fhir

# Process
python -m src.cli.trix_cli process --input case.json --output result.json
```

---

**Tutorial Complete!** ðŸŽ‰

*Last Updated: 2026-01-10*
*Version: 1.0*


