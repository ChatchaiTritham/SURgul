# SURgul: Safety-first Universal Risk Governance Logic

**Pronounced:** "SUR-gul" | à¹€à¸‹à¸­à¸£à¹Œà¹€à¸à¸´à¸¥

[![DOI](https://img.shields.io/badge/DOI-pending-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/paper-under%20review-red)]()

**A formally verified, safety-first AI system for clinical triage with provable safety guarantees and selective prediction.**



---

## ðŸš¨ Important Research Disclaimer

**This is PhD research codeâ€”NOT production medical software.**

- âš ï¸ **Not FDA/à¸­à¸¢.-approved**: SURgul has not undergone regulatory approval for clinical use
- âš ï¸ **Research prototype**: Designed for academic validation and reproducibility
- âš ï¸ **Synthetic data only**: Current implementation uses synthetic cases (not validated on real patients)
- âš ï¸ **Requires clinical validation**: Prospective studies with real EHR data are pending
- âœ… **Use for**: Research, algorithm development, safety analysis, and academic publications
- âŒ **Do NOT use for**: Real patient care, clinical decision-making, or production deployment

If you plan to use this system clinically, you **must**:
1. Obtain appropriate ethical approval and regulatory clearance
2. Conduct prospective validation studies
3. Integrate with human clinical oversight
4. Follow your jurisdiction's AI/ML medical device regulations

---

## What is SURgul?

**Think of it as:** Safety constraints + Multiple expert opinions â†’ Provably safe clinical decisions

**SURgul** (*Safety-first Universal Risk Governance Logic*) is a novel AI safety architecture for clinical triage that:

- ðŸ›¡ï¸ **Guarantees safety** through formal verification (6 mathematical safety theorems)
- ðŸŽ¯ **Achieves high accuracy** with 95.3% sensitivity and 94.7% specificity
- ðŸ¤” **Knows when to abstain** using uncertainty quantification (R* tier)
- âš¡ **Runs in constant time** O(1) complexity for real-time deployment
- ðŸ” **Provides full explainability** with audit trails for every decision
- ðŸ¥ **Designed for dizziness/vertigo triage** but generalizable to other conditions

### The Core Innovation

Traditional AI triage systems make single predictionsâ€”**SURgul** uses **6 parallel safety gates** that vote conservatively:

```
Patient Data â†’ [G1: Critical Flags ] â†’
 [G2: Moderate Risk ] â†’ Conservative â†’ Final Risk Tier
 [G3: Data Quality ] â†’ Merging â†’ (R1-R5 or R*)
 [G4: Clinical Logic ] â†’ + Explanation
 [G5: Uncertainty ] â†’
 [G6: Temporal Risk ] â†’
```

**Key Principle:** When in doubt, escalate or abstain. Better to over-triage than miss critical cases.

---

## Key Features

### ðŸ”’ Formal Safety Guarantees

- **Theorem 1 (No False Discharge)**: P(discharge | critical condition) â‰¤ Îµ with Îµ â†’ 0
- **Theorem 2 (Conservative Bias)**: T_merged âŠ‘ min(T_i) on risk lattice
- **Theorem 3 (Abstention Correctness)**: High uncertainty â†’ R* tier (deferred to human)
- **Theorem 4 (Monotonicity)**: More severe symptoms â†’ higher or equal risk tier
- **Theorem 5 (Data Quality Gate)**: Missing critical data â†’ R* (safe abstention)
- **Theorem 6 (Temporal Consistency)**: Symptom duration considered in risk assessment

### ðŸŽ¯ Performance Metrics (Synthetic Test Set, n=200)

| Metric | Value | 95% CI |
|--------|-------|--------|
| **Sensitivity** (Critical cases) | 95.3% | [92.1%, 97.8%] |
| **Specificity** (Safe discharge) | 94.7% | [91.3%, 97.2%] |
| **False Negative Rate** | 4.7% | [2.2%, 7.9%] |
| **Unsafe Discharge Rate** | 3.1% | [1.5%, 5.8%] |
| **Abstention Rate** | 12.4% | [9.7%, 15.6%] |
| **Mean Decision Time** | 1.23 ms | [1.18, 1.29] |

**Remember:** These metrics are from **synthetic data only**. Real-world performance requires prospective validation.

### ðŸ—ï¸ System Architecture

**SURgul** operates in **3 phases**:

#### Phase 1: Parallel Gate Evaluation (O(1))
- **G1 - Critical Flags Gate**: Binary safety screen for life-threatening red flags
- **G2 - Moderate Risk Gate**: Evidence-weighted scoring of moderate risk indicators
- **G3 - Data Quality Gate** â­ *Novel*: Completeness and reliability assessment
- **G4 - TiTrATE Logic Gate**: Validated clinical decision rules (Timing, Triggers, Targeted Exam)
- **G5 - Uncertainty Quantification Gate** â­ *Novel*: Monte Carlo dropout for confidence estimation
- **G6 - Temporal Risk Gate** â­ *Novel*: Time-dependent symptom evolution analysis

#### Phase 2: Conservative Merging (O(1))
- Abstention-first priority: R* overrides all predictions
- Most conservative tier selection: min(T_i) on risk lattice (R*, âŠ‘)
- Formal verification of safety theorems at merge time

#### Phase 3: Explainability & Audit Trail (O(1))
- Gate-by-gate reasoning extraction
- Highlighted critical features triggering each gate
- Full decision audit log with timestamps

---

## Installation

### Option 1: pip (Recommended for most users)

```bash
# Clone the repository
git clone https://github.com/ChatchaiTritham/SURgul.git
cd SURgul

# Create virtual environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install SURgul package
pip install -e .
```

### Option 2: Conda

```bash
# Create conda environment
conda create -n srgl python=3.8
conda activate srgl

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Option 3: Docker (For reproducibility)

```bash
# Build Docker image
docker build -t surgul:latest .

# Run container
docker run -it -p 8888:8888 surgul:latest
```

---

## Quick Start

### Basic Usage

```python
from surgul.surgul import SURgul
from surgul.data_generator import SyntheticDataGenerator

# Initialize SURgul system
surgul = SURgul(merging_strategy='conservative')

# Example patient data
patient_data = {
 'patient_id': 'P001',
 'age': 67,
 'sex': 'M',
 'symptoms': ['vertigo', 'nausea', 'imbalance'],
 'red_flags': ['sudden_onset', 'severe_headache'],
 'risk_factors': ['hypertension', 'diabetes'],
 'vital_signs': {
 'blood_pressure_systolic': 165,
 'blood_pressure_diastolic': 95,
 'heart_rate': 88,
 'temperature': 36.8
 },
 'timestamp': '2024-01-15T10:30:00'
}

# Get triage decision
decision = surgul.predict(patient_data)

print(f"Risk Tier: {decision.final_tier.value if decision.final_tier else 'R* (Abstain)'}")
print(f"Confidence: {decision.confidence:.3f}")
print(f"Decision Time: {decision.processing_time_ms:.2f} ms")

# Get detailed explanation
explanation = surgul.explain(patient_data, verbose=True)
print(explanation)
```

### Output Example:

```
Risk Tier: 1 (Critical - Immediate Care)
Confidence: 0.947
Decision Time: 1.21 ms

=== SURgul DECISION EXPLANATION ===

GATE OUTPUTS:
 G1 (Critical Flags): R1 | Confidence: 0.95 | ENFORCED
 âš  Detected critical red flags: sudden_onset, severe_headache

 G2 (Moderate Risk): R2 | Confidence: 0.82
 â€¢ Risk score: 7.3/10
 â€¢ Key factors: hypertension + vertigo

 G3 (Data Quality): R2 | Confidence: 0.91
 âœ“ Completeness: 95% (19/20 critical fields present)

 G4 (TiTrATE Logic): R1 | Confidence: 0.88
 â€¢ Timing: Sudden onset (<1 hour)
 â€¢ Triggers: Headache + vertigo
 â€¢ Targeted: Central pattern detected

 G5 (Uncertainty): R2 | Confidence: 0.75
 â€¢ Epistemic uncertainty: 0.23
 â€¢ Aleatoric uncertainty: 0.12

 G6 (Temporal Risk): R1 | Confidence: 0.79
 â€¢ Symptom evolution: Acute onset pattern
 â€¢ Time-dependent risk: Escalating

FINAL DECISION:
 Tier: R1 (Critical)
 Reasoning: G1 enforcement due to critical red flags
 Recommendation: Immediate emergency care

SAFETY VERIFICATION:
 âœ“ Theorem 1: No false discharge guarantee satisfied
 âœ“ Theorem 2: Conservative merging applied
 âœ“ All safety constraints verified
```

---

## Reproducing the Paper Results

Follow these steps to reproduce all analyses, figures, and tables from the manuscript:

### Step 1: Generate Synthetic Datasets

```bash
jupyter lab notebooks/01_data_generation.ipynb
```

This creates:
- `data/synthetic_train.json` (600 cases)
- `data/synthetic_test.json` (200 cases)
- `figures/dataset_distribution.png`
- `figures/demographics.png`
- `figures/clinical_features.png`

### Step 2: Run Statistical Analysis

```bash
jupyter lab notebooks/02_statistical_analysis.ipynb
```

Outputs:
- `results/safety_metrics_summary.csv`
- `results/predictions_conservative.csv`
- `results/final_summary.csv`
- `figures/confusion_matrix.png`
- `figures/reliability_diagram.png`
- `figures/decision_time_analysis.png`

### Step 3: Generate Publication Figures

```bash
jupyter lab notebooks/03_visualization.ipynb
```

Creates all 6 main manuscript figures:
- `figures/figure1_architecture.png`
- `figures/figure2_ablation.png`
- `figures/figure3_calibration.png`
- `figures/figure4_roc.png`
- `figures/figure5_decision_time.png`
- `figures/figure6_tradeoff.png`

### Step 4: Run Ablation Study

```bash
jupyter lab notebooks/04_ablation_study.ipynb
```

Generates:
- `results/ablation_study_summary.csv`
- `results/gate_contributions.csv`
- `results/merging_comparison.csv`
- `figures/ablation_study_comprehensive.png`
- `figures/gate_contributions.png`

**Total runtime:** ~15-20 minutes on standard laptop

---

## Repository Structure

```
SURgul/
â”œâ”€â”€ src/
â”‚ â”œâ”€â”€ __init__.py # Package initialization
â”‚ â”œâ”€â”€ data_generator.py # Synthetic data generation (SynDX-based)
â”‚ â”œâ”€â”€ gates.py # All 6 gate implementations
â”‚ â”œâ”€â”€ merging.py # Conservative merging algorithm
â”‚ â”œâ”€â”€ surgul.py # Main SURgul system
â”‚ â”œâ”€â”€ evaluation.py # Safety metrics & statistical tests
â”‚ â””â”€â”€ visualization.py # Publication-quality figure generation
â”‚
â”œâ”€â”€ notebooks/
â”‚ â”œâ”€â”€ 01_data_generation.ipynb # Dataset creation & analysis
â”‚ â”œâ”€â”€ 02_statistical_analysis.ipynb # Comprehensive evaluation
â”‚ â”œâ”€â”€ 03_visualization.ipynb # Figure generation
â”‚ â””â”€â”€ 04_ablation_study.ipynb # Gate contribution analysis
â”‚
â”œâ”€â”€ data/ # Generated datasets (JSON)
â”œâ”€â”€ results/ # Statistical outputs (CSV)
â”œâ”€â”€ figures/ # Publication figures (PNG, 300 DPI)
â”œâ”€â”€ tests/ # Unit tests (pytest)
â”œâ”€â”€ docs/ # Additional documentation
â”‚
â”œâ”€â”€ requirements.txt # Python dependencies
â”œâ”€â”€ setup.py # Package installation
â”œâ”€â”€ README.md # This file
â”œâ”€â”€ LICENSE # MIT License
â””â”€â”€ .gitignore # Git ignore rules
```

---

## Performance & Complexity

| Operation | Complexity | Time (ms) |
|-----------|------------|-----------|
| Single prediction | O(1) | 1.23 Â± 0.05 |
| Gate evaluation (parallel) | O(1) | 0.87 Â± 0.03 |
| Conservative merging | O(1) | 0.24 Â± 0.02 |
| Explanation generation | O(1) | 0.12 Â± 0.01 |

**Scalability:** SURgul maintains constant-time complexity regardless of:
- Number of patients in database
- Historical data volume
- Model ensemble size

This makes it suitable for real-time emergency department deployment.

---

## The Reality Check: Limitations

**Be aware of these constraints:**

### Current Limitations
1. **Synthetic data only**: Not validated on real patient EHR data
2. **Single condition focus**: Designed for dizziness/vertigo triage only
3. **No prospective validation**: Requires clinical trials before deployment
4. **Fixed gate architecture**: Manual feature engineering (not end-to-end learned)
5. **Language-specific**: Clinical rules based on English medical terminology
6. **Missing integration**: No FHIR/HL7 connectors yet (planned)

### Known Issues
- G5 (Uncertainty) gate requires GPU for faster inference (CPU: 15-20ms per case)
- Abstention rate may be too high for emergency settings (12.4% vs. target <10%)
- Calibration degradation when deployed on different patient populations
- No mechanism for continuous learning from clinical feedback

### What This Is Good For âœ… / Not Good For âŒ

| Use Case | Status | Notes |
|----------|--------|-------|
| âœ… Algorithm research | Safe | Primary purpose |
| âœ… Safety analysis | Safe | Formal verification testbed |
| âœ… Academic publications | Safe | Full reproducibility |
| âœ… Dataset augmentation | Safe | Synthetic data generation |
| âœ… Teaching AI safety | Safe | Educational demonstrations |
| âŒ Real patient triage | **UNSAFE** | Requires validation + approval |
| âŒ Clinical trials | **UNSAFE** | Need ethical review first |
| âŒ Production deployment | **UNSAFE** | Not FDA/à¸­à¸¢.-cleared |
| âŒ Automated diagnosis | **UNSAFE** | Human oversight required |
| âš ï¸ Retrospective studies | Conditional | With IRB approval only |

---

## Citation

If you use SURgul in your research, please cite our paper:

```bibtex
@article{surgul2024,
 title={{SURgul}: Safety-first Universal Risk Governance Logic for Clinical Triage AI},
 author={Chatchai Tritham and [Co-authors]},
 journal={Under Review},
 year={2024},
 note={Code available at: https://github.com/ChatchaiTritham/SURgul}
}
```

---

## What's Next? Clinical Validation Roadmap

### Phase 1: Retrospective Validation (Months 1-6)
- Partner with emergency departments for de-identified EHR data
- IRB approval for retrospective chart review
- Test SURgul on real historical cases (n=1000+)
- Calibration and fine-tuning with clinical feedback

### Phase 2: Prospective Observational Study (Months 7-12)
- Deploy SURgul as decision support tool (non-binding recommendations)
- Clinicians make final decisions independently
- Collect ground truth outcomes (MRI/CT, 30-day follow-up)
- Measure concordance between SURgul and expert opinion

### Phase 3: Randomized Controlled Trial (Months 13-24)
- Multi-site RCT comparing SURgul-assisted vs. standard triage
- Primary outcome: Missed critical diagnoses rate
- Secondary outcomes: Door-to-disposition time, overtriage rate
- Health economics analysis (cost-effectiveness)

### Phase 4: Regulatory Approval (Months 25-36)
- FDA 510(k) clearance (US) or Thai FDA (à¸­à¸¢.) Class II approval
- CE Mark certification (Europe)
- Post-market surveillance system implementation

**Current status:** Seeking hospital partnerships for Phase 1 (Contact us!)

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
flake8 src/ tests/
black src/ tests/

# Type checking
mypy src/
```

### Areas We Need Help With
- ðŸ”¬ Clinical validation studies
- ðŸŒ Multi-language support (Thai, Spanish, etc.)
- ðŸ”Œ EHR integration (FHIR, HL7)
- ðŸ“Š Additional visualization tools
- ðŸ› Bug reports and testing
- ðŸ“š Documentation improvements

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Important:** While the code is open-source, clinical deployment requires:
1. Proper regulatory approval in your jurisdiction
2. Institutional review board (IRB) approval
3. Professional liability insurance
4. Adherence to local medical device regulations

---

## Acknowledgments

- Clinical validation framework based on [TiTrATE](https://doi.org/10.1136/emermed-2015-205356)
- Synthetic data methodology inspired by [SynDX](https://github.com/ChatchaiTritham/SynDX)
- Formal verification approach adapted from safety-critical systems literature
- Dataset generation follows clinical distributions from multiple published studies
- Name pronunciation inspired by user-friendly branding (SUR-gul = "surgical" precision)

---

**Last Updated:** 2024-01-09
**Version:** 1.0.0-research
**Status:** ðŸš§ Research prototype - Not for clinical use

---

<p align="center">
 <strong>Built with safety first. Every decision auditable. Every patient protected.</strong>
</p>

