# SURgul

## Overview

SURgul implements the safety-first Universal Risk Governance Logic used for the
SRGL contribution in the thesis. The active importable package is `surgul`.

## Installation

```bash
pip install -e .
```

## Quickstart

```python
from surgul.clinical_case import ClinicalCase, TimingPattern, TriggerType, VitalSigns
from surgul.trix_pipeline import TRIXPipeline

case = ClinicalCase(
    case_id="README-001",
    age=62,
    sex="F",
    vitals=VitalSigns(BP_systolic=140, BP_diastolic=86, heart_rate=78),
    timing=TimingPattern.ACUTE,
    trigger=TriggerType.SPONTANEOUS,
)

recommendation = TRIXPipeline().process(case)
print(recommendation.care_pathway.value)
```

## Repository Structure

- `src/surgul/`: active importable package
- `tests/`: automated tests
- `examples/`: example usage
- `notebooks/`: research notebooks

## Tutorials And Demos

- Example scripts:
  - `examples/example_usage.py`: package-level walkthrough
  - `examples/example_enhanced_gates.py`: enhanced gate behavior demo
  - `examples/example_phase5_validators.py`: validator examples
  - `examples/example_phase5_exporters.py`: exporter examples
  - `examples/example_phase5_tutorial_walkthrough.py`: guided phase-5 workflow
- Notebooks:
  - `notebooks/01_data_generation.ipynb`
  - `notebooks/01_statistical_analysis.ipynb`
  - `notebooks/02_statistical_analysis.ipynb`
  - `notebooks/02_visualization.ipynb`
  - `notebooks/03_visualization.ipynb`
  - `notebooks/04_ablation_study.ipynb`

## Cross-Repository Tutorial Charts

- `../tutorial_surface_comparison.png`: scripts vs examples vs notebooks across all repositories
- `../tutorial_asset_density.png`: interactive/tutorial asset density normalized by repository size
- `../tutorial_maturity_report.md`: combined maturity summary

## Package Scope

The package currently includes:

- SRGL core logic in `src/surgul/srgl.py`
- gate implementations in `src/surgul/gates.py`
- conservative merging in `src/surgul/merging.py`
- evaluation, exporters, validators, and visualization helpers

## Source Layout

This repository now uses the recommended `src/<package_name>` layout.
Legacy flat files under `src/` are retained for compatibility work, but the
stable package path is `src/surgul/`.

## Testing

```bash
pytest tests -v
```

## Citation

- cite the associated thesis/manuscript sections covering SURgul and SRGL

## License

- MIT; see `LICENSE`

## Contact

### Contact Author

**Chatchai Tritham** (PhD Candidate)

- Email: [chatchait66@nu.ac.th](mailto:chatchait66@nu.ac.th)
- Department of Computer Science and Information Technology
- Faculty of Science, Naresuan University
- Phitsanulok 65000, Thailand

### Supervisor

**Chakkrit Snae Namahoot**

- Email: [chakkrits@nu.ac.th](mailto:chakkrits@nu.ac.th)
- Department of Computer Science
- Faculty of Science, Naresuan University
- Phitsanulok 65000, Thailand
