# Safety-first Universal Risk Governance Logic (SURgul)

> A reference implementation of the SRGL six-gate triage governor and its conservative merging rule, packaged so a reader can install it, run the behavior tests, and regenerate the architecture diagrams.

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Status](https://img.shields.io/badge/status-preliminary%2Fparked-orange)

## Overview

Clinical triage logic tends to fail in two opposite ways: a single over-confident model discharges a patient it should have escalated, or a committee of weak rules averages a genuine red flag into the background. SURgul packages the governance layer that sits between gate-level evidence and the final triage action, and it resolves that tension by refusing to average safety away.

The package implements SRGL (Safety-first Risk Governance Logic) as six independent gates — critical red flags, moderate risk factors, data quality, TiTrATE pattern matching, uncertainty, and temporal urgency — whose outputs are combined by a conservative merge. The merge keeps three behaviors fixed: any abstaining gate forces the whole decision to abstain, the final risk tier is the maximum across gates rather than a blend, and enforcement actions are taken as a union so no constraint is silently dropped. Two deliberately unsafe baselines (averaging and learned weighting) are included so the contrast with conservative merging can be exercised directly.

This repository is the governance-component slice of a larger clinical decision-support portfolio. The associated conference write-up is parked for a 2027 venue, so the code here is offered as a preliminary, self-contained reference rather than the supporting artifact of a published study. There is no end-to-end experiment driver and no committed metrics; what the code does produce — gate behaviour, merge invariants, and the architecture diagrams — can be inspected and re-run today.

## Key results

This repository is at a preliminary/parked stage and does **not** ship a full experimental pipeline. It does not regenerate manuscript-grade benchmark numbers, and no headline metrics are claimed here. What it does demonstrate:

- The six-gate SRGL governor runs end to end on a single case or a batch and returns a tier, an action, an explanation, and a per-gate audit trail.
- Conservative merging enforces its three design rules at runtime — abstention priority, max-tier escalation, and union of enforcement — checked by `ConservativeMerging.validate_theorems` on each decision and exercised by the test suite.
- The averaging and weighted-merge baselines are present for contrast and are documented as unsafe; they exist for ablation, not for deployment.
- The two architecture figures are reproducible from a single script (see below). They are schematic diagrams of the design, not plots of experimental data.

Anything stated as a quantitative safety guarantee in the source docstrings (for example "100% sensitivity") refers to the design intent and to runtime invariant checks on individual decisions — not to a benchmark that this repository computes.

## Repository structure

```text
src/surgul/        SRGL gates, conservative/average/weighted merging, adapter, pipeline, exporters, validators, visualization
tests/             pytest smoke and behaviour checks (imports, adapter, pipeline, gates, exporters, validators)
scripts/           generate_figures.py (architecture diagrams), manifest generator
examples/          runnable usage demos for gates, exporters, validators, pipeline
notebooks/         exploratory data-generation, analysis, visualization, ablation notebooks
figures/           exported architecture diagrams (PNG + PDF) listed in FIGURE_MANIFEST.csv
data/ results/ outputs/ evaluation/ models/   placeholder directories (no committed artifacts)
pyproject.toml, setup.py, requirements.txt, pytest.ini   package and test configuration
```

## Installation

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Reproducing the results

There is no single-command experiment driver in this repository. The two things that can be reproduced are the test suite and the architecture figures:

```bash
python -m pytest -q            # behaviour and invariant checks for gates + merging
python scripts/generate_figures.py   # rewrites the two diagrams in figures/
```

The synthetic data helper (`surgul.synthetic_data_generator.generate_syndx_like_data`) fixes `numpy` seed 42, so the tabular sample it produces is deterministic across runs. The figure script lays out fixed boxes and arrows, so its output is stable as well. No metric files are written to `results/` or `outputs/`; those directories are placeholders for future work.

## Results and figures

Both committed figures are schematic diagrams of the SRGL design, produced by `scripts/generate_figures.py` with hardcoded box coordinates and labels. They illustrate the architecture; they do not encode experimental measurements, so the script needs no input data and reads nothing from `results/`.

- `figures/surgul_srgl_gate_architecture.png` — the six gates fanning out from the case input into the conservative merge and the audited triage decision; read it as the control-flow map for `SRGL.predict`.
- `figures/surgul_conservative_merging_lattice.png` — the risk-tier lattice from SAFE through CRITICAL plus ABSTAIN, showing how the merge escalates to the maximum tier and how abstention overrides everything else.

## Data

No human-subject data is used and no IRB approval is required. The only dataset is synthetic: `generate_syndx_like_data` draws age, sex, BMI, blood pressure, and related fields from fixed-seed normal distributions for visualization and testing. The clinical examples in the source and tests are illustrative cases, not real patient records.

## Citation

```bibtex
@misc{tritham_surgul,
  author       = {Tritham, Chatchai and Snae Namahoot, Chakkrit},
  title        = {{SURgul}: Safety-first Universal Risk Governance Logic for Clinical Triage},
  year         = {2026},
  note         = {Preliminary reference implementation; conference manuscript in preparation (to appear)}
}
```

## License

Released under the MIT License (see `LICENSE`).

## Contact

**Chatchai Tritham**  
Department of Computer Science and Information Technology, Faculty of Science, Naresuan University, Phitsanulok 65000, Thailand  
Email: chatchait66@nu.ac.th  
ORCID: 0000-0001-7899-228X

**Chakkrit Snae Namahoot**  
Department of Computer Science and Information Technology, Faculty of Science, Naresuan University, Phitsanulok 65000, Thailand  
Email: chakkrits@nu.ac.th  
ORCID: 0000-0003-4660-4590

## Portfolio relationship

| Repository | Role |
|---|---|
| BASICS-CDSS | Beyond-accuracy evaluation methodology |
| TRI-X | Framework-level package |
| ORASR | Routing and safety-action component |
| DRAS-5 | Dynamic risk-state component |
| SAFE-Gate | Safety-gated ensemble framework |
| SynDX | Synthetic validation and explainability evidence |
| SURgul | SRGL/governance reproducibility component |
| TRI-X-CDSS | Integration and implementation package |
| Selective-CDSS | Risk-controlled selective-prediction (abstention) component |
| Causal-CDSS | Causal-inference evaluation component |
| Beyond-Accuracy | Simulation-based safety/calibration evaluation framework |
