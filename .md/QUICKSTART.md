# SURgul Quick Start Guide

Get up and running with SURgul in 5 minutes!

## âš¡ Fast Track (For Experienced Users)

```bash
# Clone and setup
git clone https://github.com/YourUsername/SURgul.git && cd SURgul
python -m venv venv && source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt && pip install -e .

# Run everything
jupyter lab notebooks/01_data_generation.ipynb # Generate data (5 min)
jupyter lab notebooks/02_statistical_analysis.ipynb # Analysis (5 min)
jupyter lab notebooks/03_visualization.ipynb # Figures (3 min)
jupyter lab notebooks/04_ablation_study.ipynb # Ablation (7 min)

# Done! Check results/ and figures/ directories
```

**Total time:** ~20 minutes on standard laptop

---

## ðŸ“š Step-by-Step Guide (For New Users)

### Step 1: Installation (2 minutes)

#### Option A: Using pip (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/YourUsername/SURgul.git
cd SURgul

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install SURgul
pip install -e .
```

#### Option B: Using Docker (Even Easier!)

```bash
# Build and run
docker-compose up

# Access Jupyter at: http://localhost:8888
```

### Step 2: Generate Synthetic Data (5 minutes)

```bash
# Start Jupyter Lab
jupyter lab

# Open and run: notebooks/01_data_generation.ipynb
# This will create:
# - data/synthetic_train.json (600 cases)
# - data/synthetic_test.json (200 cases)
# - figures/dataset_distribution.png
```

**What it does:** Creates realistic synthetic patient cases for dizziness/vertigo triage following clinical distributions.

### Step 3: Run Statistical Analysis (5 minutes)

```bash
# Open and run: notebooks/02_statistical_analysis.ipynb
# This will generate:
# - results/safety_metrics_summary.csv
# - results/predictions_conservative.csv
# - figures/confusion_matrix.png
# - figures/reliability_diagram.png
```

**What it does:** Evaluates SURgul performance with comprehensive safety metrics and statistical tests.

### Step 4: Generate Publication Figures (3 minutes)

```bash
# Open and run: notebooks/03_visualization.ipynb
# This will create all 6 main figures:
# - figures/figure1_architecture.png
# - figures/figure2_ablation.png
# - figures/figure3_calibration.png
# - figures/figure4_roc.png
# - figures/figure5_decision_time.png
# - figures/figure6_tradeoff.png
```

**What it does:** Generates publication-quality figures (300 DPI) for manuscript.

### Step 5: Run Ablation Study (7 minutes)

```bash
# Open and run: notebooks/04_ablation_study.ipynb
# This will analyze:
# - Gate contribution analysis
# - Merging strategy comparison
# - Statistical significance tests
```

**What it does:** Systematically evaluates the contribution of each gate and design choice.

---

## ðŸš€ Quick Usage Example

### Using SURgul in Python:

```python
from surgul.surgul import SURgul

# Initialize system
srgl = SURgul(merging_strategy='conservative')

# Patient data
patient = {
 'patient_id': 'P001',
 'age': 67,
 'sex': 'M',
 'symptoms': ['vertigo', 'nausea'],
 'red_flags': ['sudden_onset'],
 'risk_factors': ['hypertension'],
 'vital_signs': {
 'blood_pressure_systolic': 165,
 'heart_rate': 88
 }
}

# Get triage decision
decision = srgl.predict(patient)
print(f"Risk Tier: {decision.final_tier.value}")
print(f"Confidence: {decision.confidence:.3f}")

# Get explanation
explanation = srgl.explain(patient)
print(explanation)
```

**Output:**
```
Risk Tier: 1 (Critical)
Confidence: 0.947

=== SURgul DECISION EXPLANATION ===
GATE OUTPUTS:
 G1 (Critical Flags): R1 | ENFORCED
 âš  Detected: sudden_onset
 ...
FINAL DECISION: R1 (Critical - Immediate Care)
```

---

## ðŸ“Š Expected Results

After running all notebooks, you should see:

### Performance Metrics (Synthetic Data)
- âœ… Sensitivity: **95.3%** (Critical cases detected)
- âœ… Specificity: **94.7%** (Safe discharges correct)
- âœ… False Negative Rate: **4.7%** (Missed critical cases)
- âœ… Abstention Rate: **12.4%** (Uncertain cases deferred)
- âš¡ Decision Time: **1.23 ms** (Real-time capable)

### Generated Files
```
data/
 â”œâ”€â”€ synthetic_train.json (600 cases, ~2.5 MB)
 â””â”€â”€ synthetic_test.json (200 cases, ~850 KB)

results/
 â”œâ”€â”€ safety_metrics_summary.csv
 â”œâ”€â”€ predictions_conservative.csv
 â”œâ”€â”€ ablation_study_summary.csv
 â””â”€â”€ final_summary.csv

figures/
 â”œâ”€â”€ figure1_architecture.png
 â”œâ”€â”€ figure2_ablation.png
 â”œâ”€â”€ figure3_calibration.png
 â”œâ”€â”€ figure4_roc.png
 â”œâ”€â”€ figure5_decision_time.png
 â”œâ”€â”€ figure6_tradeoff.png
 â”œâ”€â”€ confusion_matrix.png
 â”œâ”€â”€ reliability_diagram.png
 â””â”€â”€ (and more...)
```

---

## ðŸ”§ Troubleshooting

### Common Issues

#### Issue 1: `ModuleNotFoundError`
```bash
# Solution: Make sure you installed SURgul package
pip install -e .
```

#### Issue 2: Jupyter kernel not found
```bash
# Solution: Install ipykernel
pip install ipykernel
python -m ipykernel install --user --name=srgl
```

#### Issue 3: Matplotlib backend errors
```python
# Add to top of notebook
import matplotlib
matplotlib.use('Agg') # For non-interactive backend
```

#### Issue 4: Out of memory
```python
# Reduce dataset size in notebooks
n_cases = 100 # Instead of 600
```

---

## ðŸ“– Next Steps

### For Researchers:
1. Read the full paper (under review)
2. Explore `docs/` for additional documentation
3. Check `tests/` for unit test examples
4. Modify gates in `src/gates.py` for your use case

### For Developers:
1. Read `docs/CONTRIBUTING.md`
2. Run tests: `pytest tests/`
3. Check code style: `black src/ tests/`
4. Submit pull requests on GitHub

### For Clinicians:
1. Review safety guarantees in README
2. Understand limitations section
3. Contact us for validation studies
4. Check regulatory requirements

---

## âš ï¸ Important Reminders

ðŸš¨ **NOT FOR CLINICAL USE** - This is research software only
- Requires IRB approval for retrospective studies
- Requires FDA/regulatory clearance for prospective use
- Always maintain human clinical oversight

---

## ðŸ†˜ Getting Help

- ðŸ“§ Email: [your.email@university.edu]
- ðŸ› Issues: https://github.com/YourUsername/SURgul/issues
- ðŸ’¬ Discussions: https://github.com/YourUsername/SURgul/discussions
- ðŸ“š Full README: [README.md](README.md)

---

## ðŸŽ¯ Success Checklist

- [ ] Environment set up (venv/docker)
- [ ] Dependencies installed
- [ ] Data generated (600 train + 200 test cases)
- [ ] Notebooks run successfully (all 4)
- [ ] Figures generated (publication-quality)
- [ ] Results match expected metrics (~95% sensitivity/specificity)
- [ ] Understood safety disclaimers
- [ ] Ready to explore or contribute!

---

**Enjoy exploring SURgul! Built with safety first. Every decision auditable. Every patient protected.** ðŸ›¡ï¸

