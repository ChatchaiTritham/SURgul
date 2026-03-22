# TRI-X Framework Documentation

**Comprehensive documentation for the TRI-X Clinical Decision Support System**

---

## Quick Links

- **Getting Started**: [Quick Start Guide](#quick-start-guide)
- **Phase 5 Tutorial**: [PHASE5_TUTORIAL.md](PHASE5_TUTORIAL.md) - Step-by-step guide
- **Quick Reference**: [PHASE5_QUICK_REFERENCE.md](PHASE5_QUICK_REFERENCE.md) - Fast lookup
- **Full Documentation**: See sections below

---

## Quick Start Guide

### Installation

```bash
# Clone repository
git clone <repository-url>
cd SURgul

# Install dependencies (Python 3.8+)
pip install -r requirements.txt

# Optional: PDF export support
pip install reportlab
```

### Basic Usage

```python
# Process a clinical case
from surgul.clinical_case import ClinicalCase
from surgul.trix_pipeline import TRIXPipeline

case = ClinicalCase.from_dict({
 'case_id': 'TEST001',
 'age': 65,
 'sex': 'M',
 'BP_systolic': 150
})

pipeline = TRIXPipeline()
recommendation = pipeline.process(case)

print(f"Risk Tier: {recommendation.triage_decision.risk_tier.name}")
print(f"Confidence: {recommendation.triage_decision.confidence:.1%}")
```

### Validate Compliance

```python
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator

validator = NISTAIRMFValidator()
report = validator.validate({"system_name": "TRI-X", "version": "1.0"})

print(f"Compliance: {report.compliance_score:.1%}")
```

### Export Data

```python
from surgul.exporters.json_exporter import JSONExporter

exporter = JSONExporter(pretty=True)
exporter.export_care_recommendation(recommendation, "result.json")
```

---

## Documentation Structure

### Phase-Specific Documentation

| Phase | Document | Description |
|-------|----------|-------------|
| Phase 3 | [PHASE3_README.md](../PHASE3_README.md) | Clinical data interface & pipeline |
| Phase 5 | [PHASE5_README.md](../PHASE5_README.md) | Validators & exporters overview |
| Phase 5 | [PHASE_5_COMPLETION_SUMMARY.md](../PHASE_5_COMPLETION_SUMMARY.md) | Detailed completion summary |

### Tutorials & Guides

| Document | Level | Description |
|----------|-------|-------------|
| [PHASE5_TUTORIAL.md](PHASE5_TUTORIAL.md) | Beginner | Step-by-step tutorial with examples |
| [PHASE5_QUICK_REFERENCE.md](PHASE5_QUICK_REFERENCE.md) | All | Fast lookup for common tasks |

### Additional Documentation

| Document | Description |
|----------|-------------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes |
| [prospective_study_protocol.md](prospective_study_protocol.md) | Clinical validation protocol |

---

## Feature Overview

### Core Components

#### TRI-X Pipeline (Phases 1-4)
- **SRGL**: 6-gate risk assessment framework
- **DRAS-5**: 5-state risk stratification
- **ORASR**: Action plan generation
- **Uncertainty Quantification**: Dempster-Shafer theory

#### Compliance Validation (Phase 5)
- **NIST AI RMF**: 4 functions, 40+ checks
- **FDA GMLP**: 10 principles, 30+ checks
- **Gap Analysis**: Identify missing requirements
- **Export**: Markdown, JSON reports

#### Data Export (Phase 5)
- **JSON**: Machine-readable, preserves structure
- **CSV**: Spreadsheet analysis, flattened
- **FHIR R4**: Healthcare interoperability
- **PDF**: Human-readable reports (optional)

#### Command-Line Interface (Phase 5)
- **validate**: Run compliance checks
- **export**: Convert data formats
- **process**: End-to-end pipeline execution

---

## Examples

### Example Scripts

All examples are in the [examples/](../examples/) directory:

| Script | Description |
|--------|-------------|
| `example_usage.py` | Basic TRI-X pipeline usage |
| `example_enhanced_gates.py` | Phase 4 enhanced gates demo |
| `example_phase5_validators.py` | NIST & FDA validation demo |
| `example_phase5_exporters.py` | Multi-format export demo |
| `example_phase5_tutorial_walkthrough.py` | Interactive tutorial |

### Running Examples

```bash
# Basic usage
python examples/example_usage.py

# Phase 5 validators
python examples/example_phase5_validators.py

# Phase 5 exporters
python examples/example_phase5_exporters.py

# Interactive tutorial
python examples/example_phase5_tutorial_walkthrough.py
```

---

## Testing

### Test Suites

Located in [tests/](../tests/) directory:

| Test File | Coverage |
|-----------|----------|
| `test_validators.py` | NIST & FDA compliance validators |
| `test_exporters.py` | JSON, CSV, FHIR, PDF exporters |

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_validators.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

---

## Use Cases

### Clinical Workflow Integration

```python
# Emergency department integration
from surgul.trix_pipeline import TRIXPipeline
from surgul.exporters.fhir_exporter import FHIRExporter

pipeline = TRIXPipeline()
fhir_exporter = FHIRExporter()

# Process ED patient
recommendation = pipeline.process(ed_patient_case)

# Export to EHR
fhir_exporter.export_care_recommendation(
 recommendation,
 ed_patient_case,
 "ehr_integration.json"
)
```

### Research Study

```python
# Batch processing for research
from surgul.exporters.csv_exporter import CSVExporter

results = []
for case in study_cases:
 rec = pipeline.process(case)
 results.append({
 'case_id': case.case_id,
 'risk_tier': rec.triage_decision.risk_tier.name,
 'confidence': rec.triage_decision.confidence
 })

# Export for analysis
CSVExporter().export(results, "study_results.csv")
```

### Regulatory Submission

```bash
# Generate compliance reports
python -m src.cli.trix_cli validate --nist --fda --output compliance_report.md

# Export supporting documentation
python -m src.cli.trix_cli export --input validation_cases.json --format pdf
```

---

## Architecture

### System Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Clinical Input Data â”‚
â”‚ (ClinicalCase) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
 â”‚
 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ TRI-X Pipeline â”‚
â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ SRGL â”‚â†’ â”‚ DRAS-5 â”‚â†’ â”‚ ORASR â”‚ â”‚
â”‚ â”‚ (6 Gates) â”‚ â”‚(5 States)â”‚ â”‚ (Action) â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
 â”‚
 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Care Recommendation â”‚
â”‚ (Risk Tier + Action Plan) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
 â”‚
 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
 â–¼ â–¼ â–¼
 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”
 â”‚ JSON â”‚ â”‚ FHIR â”‚ â”‚ PDF â”‚
 â”‚ Export â”‚ â”‚ Export â”‚ â”‚ Export â”‚
 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
 â”‚ â”‚ â”‚
 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
 â–¼ â–¼
 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
 â”‚ EHR System â”‚ â”‚ Clinician â”‚
 â”‚ Integration â”‚ â”‚ Review â”‚
 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Phase 5 Architecture

```
Phase 5: Validators & Exporters
â”œâ”€â”€ Validators
â”‚ â”œâ”€â”€ NIST AI RMF
â”‚ â”‚ â”œâ”€â”€ GOVERN (10 checks)
â”‚ â”‚ â”œâ”€â”€ MAP (10 checks)
â”‚ â”‚ â”œâ”€â”€ MEASURE (12 checks)
â”‚ â”‚ â””â”€â”€ MANAGE (10 checks)
â”‚ â””â”€â”€ FDA GMLP
â”‚ â”œâ”€â”€ P1-P10 (30+ checks)
â”‚ â””â”€â”€ Pre-submission actions
â”œâ”€â”€ Exporters
â”‚ â”œâ”€â”€ JSON (structured data)
â”‚ â”œâ”€â”€ CSV (tabular data)
â”‚ â”œâ”€â”€ FHIR R4 (healthcare standard)
â”‚ â””â”€â”€ PDF (human reports)
â””â”€â”€ CLI
 â”œâ”€â”€ validate (compliance)
 â”œâ”€â”€ export (formats)
 â””â”€â”€ process (pipeline)
```

---

## API Reference

### Validators

#### NISTAIRMFValidator

```python
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator

validator = NISTAIRMFValidator()
report = validator.validate(metadata)

# Report properties
report.compliance_score # float (0-1)
report.regulatory_ready # bool
report.certification_readiness # str
report.total_checks # int
report.checks_passed # int
report.all_checks # List[ComplianceCheck]
report.critical_deficiencies # List[str]
report.recommendations # List[str]
```

#### FDAGMLPValidator

```python
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator

validator = FDAGMLPValidator()
report = validator.validate(metadata)

# Report properties
report.compliance_score # float (0-1)
report.regulatory_ready # bool
report.submission_readiness # str
report.device_classification # str
report.pre_submission_actions # List[str]
```

### Exporters

#### JSONExporter

```python
from surgul.exporters.json_exporter import JSONExporter

exporter = JSONExporter(pretty=True)

exporter.export_clinical_case(case, path)
exporter.export_triage_decision(decision, path)
exporter.export_care_recommendation(recommendation, path)
exporter.export_compliance_report(report, path)
exporter.export_batch(items, path)
```

#### CSVExporter

```python
from surgul.exporters.csv_exporter import CSVExporter

exporter = CSVExporter(flatten_nested=True, delimiter=',')

exporter.export_clinical_cases(cases, path)
exporter.export_triage_decisions(decisions, path)
exporter.export_compliance_summary(reports, path)
exporter.export(data, path, columns=None)
```

#### FHIRExporter

```python
from surgul.exporters.fhir_exporter import FHIRExporter

exporter = FHIRExporter(system_url="http://example.org")

exporter.export_clinical_case_bundle(case, path)
exporter.export_triage_decision(decision, case, path)
exporter.export_care_recommendation(recommendation, case, path)
```

#### PDFExporter

```python
from surgul.exporters.pdf_exporter import PDFExporter

exporter = PDFExporter(title="Report", page_size="Letter")

exporter.export_clinical_case(case, path)
exporter.export_triage_decision(decision, case, path)
exporter.export_care_recommendation(recommendation, case, path)
exporter.export_compliance_report(report, path)
```

---

## Common Workflows

### Workflow 1: Clinical Case Processing

```python
# 1. Create case
case = ClinicalCase.from_dict(patient_data)

# 2. Process through TRI-X
pipeline = TRIXPipeline()
recommendation = pipeline.process(case)

# 3. Export for EHR
FHIRExporter().export_care_recommendation(
 recommendation, case, "ehr.json"
)

# 4. Generate clinician report
PDFExporter().export_care_recommendation(
 recommendation, case, "clinician_report.pdf"
)
```

### Workflow 2: Compliance Tracking

```python
# 1. Define system metadata
metadata = {...} # See templates

# 2. Run validations
nist_report = NISTAIRMFValidator().validate(metadata)
fda_report = FDAGMLPValidator().validate(metadata)

# 3. Export reports
NISTAIRMFValidator().export_markdown_report(nist_report, "nist.md")
FDAGMLPValidator().export_markdown_report(fda_report, "fda.md")

# 4. Track over time
# (Save scores, identify trends)
```

### Workflow 3: Research Study

```python
# 1. Batch process cases
results = [pipeline.process(case) for case in study_cases]

# 2. Extract metrics
metrics = [{
 'case_id': case.case_id,
 'risk_tier': rec.triage_decision.risk_tier.name,
 'confidence': rec.triage_decision.confidence
} for case, rec in zip(study_cases, results)]

# 3. Export for analysis
CSVExporter().export(metrics, "study_results.csv")

# 4. Generate summary report
# (Statistics, visualizations)
```

---

## FAQ

### Q: What's the difference between NIST AI RMF and FDA GMLP?

**A:** NIST AI RMF focuses on AI risk management and trustworthiness (applicable to all AI systems), while FDA GMLP focuses on medical device quality and clinical validation (specific to healthcare ML).

### Q: Which export format should I use?

**A:**
- **JSON**: APIs, data storage, preserves structure
- **CSV**: Spreadsheet analysis, statistical tools
- **FHIR**: EHR integration, healthcare interoperability
- **PDF**: Clinical documentation, human review

### Q: Do I need external validation to be compliant?

**A:** Yes, external validation on independent datasets is critical for both NIST and FDA compliance, especially for clinical deployment.

### Q: Can I use Phase 5 without the full TRI-X pipeline?

**A:** Yes! Validators and exporters can be used independently with any system metadata or data structures.

### Q: How do I improve my compliance score?

**A:** Provide comprehensive metadata covering governance, risk assessment, validation, monitoring, and transparency. See metadata templates in [PHASE5_QUICK_REFERENCE.md](PHASE5_QUICK_REFERENCE.md).

---

## Support

### Getting Help

1. **Read the Tutorial**: [PHASE5_TUTORIAL.md](PHASE5_TUTORIAL.md)
2. **Check Quick Reference**: [PHASE5_QUICK_REFERENCE.md](PHASE5_QUICK_REFERENCE.md)
3. **Review Examples**: [examples/](../examples/)
4. **Run Tests**: See if similar functionality works in tests

### Reporting Issues

When reporting issues, include:
- Python version
- Full error message
- Minimal code to reproduce
- Expected vs actual behavior

---

## Roadmap

### Current Status (Phase 5)
âœ… NIST AI RMF validator
âœ… FDA GMLP validator
âœ… Multi-format export (JSON, CSV, FHIR, PDF)
âœ… Command-line interface
âœ… Comprehensive testing

### Future Phases
- **Phase 6**: Jupyter notebooks & interactive tools
- **Phase 7**: PyPI package & Docker deployment
- **Phase 8**: External clinical validation study

---

## Citation

If you use the TRI-X framework in your research, please cite:

```
TRI-X Framework: A Three-Layer Risk-Integrated Expert System
for Acute Dizziness Triage
PhD Research Project, 2026
Phase 5: Regulatory Compliance Validators & Multi-Format Exporters
```

---

## License

Academic research project - See main repository for license details.

---

## Contributors

- PhD Research Team
- Clinical Advisory Board
- Software Engineering Team

---

**Documentation Last Updated:** 2026-01-10
**Framework Version:** 1.0
**Phase:** 5 Complete

---

*For additional support, please refer to the specific documentation files listed above.*

