# Contributing to SRGL

Thank you for your interest in contributing to SRGL! We welcome contributions from the community.

## ðŸš¨ Important Medical Software Disclaimer

Before contributing, please understand:
- SRGL is research software, NOT production medical software
- Contributions must not enable unsafe clinical use
- All changes must maintain or improve safety guarantees
- Clinical validation is required before any deployment

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, package versions)
- Code snippet demonstrating the issue

### Suggesting Enhancements

For feature requests:
- Describe the enhancement clearly
- Explain why it would be useful
- Consider safety implications for clinical use
- Provide examples of how it would work

### Pull Requests

1. **Fork the repository**
 ```bash
 git clone https://github.com/YourUsername/SRGL.git
 cd SRGL
 ```

2. **Create a branch**
 ```bash
 git checkout -b feature/your-feature-name
 ```

3. **Set up development environment**
 ```bash
 python -m venv venv
 source venv/bin/activate # On Windows: venv\Scripts\activate
 pip install -r requirements-dev.txt
 pip install -e .
 ```

4. **Make your changes**
 - Write clear, documented code
 - Follow PEP 8 style guidelines
 - Add type hints where appropriate
 - Update docstrings

5. **Test your changes**
 ```bash
 # Run tests
 pytest tests/ -v

 # Check code style
 flake8 src/ tests/
 black --check src/ tests/

 # Type checking
 mypy src/

 # Check test coverage
 pytest --cov=src tests/
 ```

6. **Commit your changes**
 ```bash
 git add .
 git commit -m "Add feature: clear description"
 ```

7. **Push and create PR**
 ```bash
 git push origin feature/your-feature-name
 ```
 Then create a Pull Request on GitHub.

## Development Guidelines

### Code Style

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use isort for import sorting
- Add type hints for all functions
- Write comprehensive docstrings

Example:
```python
def calculate_risk_score(
 symptoms: List[str],
 risk_factors: Dict[str, Any],
 threshold: float = 0.8
) -> Tuple[float, str]:
 """
 Calculate risk score based on symptoms and factors.

 Args:
 symptoms: List of patient symptoms
 risk_factors: Dictionary of risk factor values
 threshold: Decision threshold (default: 0.8)

 Returns:
 Tuple of (risk_score, interpretation_text)

 Raises:
 ValueError: If symptoms list is empty

 Example:
 >>> score, text = calculate_risk_score(['vertigo'], {'age': 65})
 >>> print(f"{score:.2f}: {text}")
 """
 # Implementation
 pass
```

### Testing

- Write tests for all new features
- Maintain >90% code coverage
- Use pytest fixtures for common setups
- Test edge cases and error conditions
- Include integration tests

Example:
```python
import pytest
from surgul.gates import Gate_G1_CriticalFlags

@pytest.fixture
def critical_patient():
 return {
 'symptoms': ['sudden_vertigo', 'severe_headache'],
 'red_flags': ['diplopia', 'ataxia'],
 'age': 67
 }

def test_g1_detects_critical_flags(critical_patient):
 gate = Gate_G1_CriticalFlags()
 output = gate.evaluate(critical_patient)

 assert output.tier.value == 1
 assert output.confidence > 0.9
 assert output.enforcement is True
```

### Documentation

- Update README.md if adding user-facing features
- Add docstrings to all functions/classes
- Update notebooks if examples are affected
- Create or update relevant documentation in `docs/`

### Safety-Critical Changes

If your contribution affects:
- Gate logic
- Merging algorithms
- Risk tier assignments
- Safety theorem verification

You MUST:
1. Provide formal justification for changes
2. Update safety proofs if applicable
3. Run ablation studies showing impact
4. Get review from domain experts before merging

## Priority Areas

We especially welcome contributions in:

### ðŸ”¬ Clinical Validation
- Partner with hospitals for data access
- Design prospective study protocols
- Statistical analysis improvements
- Clinical outcome tracking

### ðŸŒ Internationalization
- Multi-language support (Thai, Spanish, Chinese, etc.)
- Cultural adaptation of clinical rules
- Translation of documentation
- Localization of terminology

### ðŸ”Œ EHR Integration
- FHIR API connectors
- HL7 v2/v3 parsers
- Epic/Cerner integration modules
- Real-time data stream processing

### ðŸ“Š Visualization
- Interactive dashboards
- Real-time monitoring tools
- Clinical report generation
- Performance analytics

### ðŸ› Testing & Quality
- Expand test coverage
- Property-based testing
- Stress testing
- Security audits

### ðŸ“š Documentation
- Tutorial improvements
- Use case examples
- Clinical workflow guides
- API documentation

## Code Review Process

All contributions go through:
1. Automated tests (must pass)
2. Code style checks (must pass)
3. Peer review by maintainers
4. Domain expert review (for clinical changes)
5. Final approval by project lead

## Community Guidelines

- Be respectful and professional
- Provide constructive feedback
- Help others learn and improve
- Prioritize patient safety above all else
- Acknowledge uncertainty honestly

## Questions?

- ðŸ“§ Email: [your.email@university.edu]
- ðŸ’¬ GitHub Discussions: https://github.com/YourUsername/SRGL/discussions
- ðŸ› Issues: https://github.com/YourUsername/SRGL/issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

However, note that:
- Clinical deployment requires regulatory approval
- Medical use requires professional oversight
- Contributors share no liability for clinical applications

---

**Thank you for helping make SRGL safer and better! Every contribution matters.** ðŸ™

