# Phase 5 Advanced Patterns

**Advanced Usage Patterns for Expert Users**

---

## Table of Contents

1. [Batch Processing Patterns](#batch-processing-patterns)
2. [Automated Pipeline Patterns](#automated-pipeline-patterns)
3. [Error Handling & Recovery](#error-handling--recovery)
4. [Performance Optimization](#performance-optimization)
5. [Custom Validators](#custom-validators)
6. [Custom Exporters](#custom-exporters)
7. [Monitoring & Alerting](#monitoring--alerting)
8. [Multi-Tenancy Patterns](#multi-tenancy-patterns)

---

## Batch Processing Patterns

### Pattern 1: Parallel Batch Processing with Progress Tracking

```python
"""
High-performance batch processing with parallel execution
"""

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from surgul.clinical_case import ClinicalCase
from surgul.trix_pipeline import TRIXPipeline
from surgul.exporters.json_exporter import JSONExporter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParallelBatchProcessor:
 """Process large batches of cases in parallel"""

 def __init__(self, max_workers=4, output_dir="batch_results"):
 self.max_workers = max_workers
 self.output_dir = Path(output_dir)
 self.output_dir.mkdir(exist_ok=True)

 def process_single_case(self, case_data):
 """Process single case (executed in parallel)"""
 try:
 # Create pipeline instance (one per worker)
 pipeline = TRIXPipeline()

 # Process case
 case = ClinicalCase.from_dict(case_data)
 recommendation = pipeline.process(case)

 return {
 'status': 'success',
 'case_id': case.case_id,
 'result': {
 'risk_tier': recommendation.triage_decision.risk_tier.name,
 'confidence': recommendation.triage_decision.confidence,
 'action_state': recommendation.action_state.name
 }
 }

 except Exception as e:
 logger.error(f"Error processing {case_data.get('case_id', 'UNKNOWN')}: {e}")
 return {
 'status': 'error',
 'case_id': case_data.get('case_id', 'UNKNOWN'),
 'error': str(e)
 }

 def process_batch(self, cases_data, chunk_size=100):
 """
 Process large batch with parallel execution and chunking

 Args:
 cases_data: List of case dictionaries
 chunk_size: Process and save in chunks to prevent memory issues
 """
 total_cases = len(cases_data)
 results = []
 errors = []

 logger.info(f"Processing {total_cases} cases with {self.max_workers} workers")

 # Process in chunks
 for chunk_start in range(0, total_cases, chunk_size):
 chunk_end = min(chunk_start + chunk_size, total_cases)
 chunk = cases_data[chunk_start:chunk_end]

 logger.info(f"Processing chunk {chunk_start}-{chunk_end}")

 # Parallel processing with progress bar
 with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
 # Submit all tasks
 futures = {
 executor.submit(self.process_single_case, case_data): case_data
 for case_data in chunk
 }

 # Collect results with progress bar
 with tqdm(total=len(chunk), desc=f"Chunk {chunk_start}-{chunk_end}") as pbar:
 for future in as_completed(futures):
 result = future.result()

 if result['status'] == 'success':
 results.append(result)
 else:
 errors.append(result)

 pbar.update(1)

 # Save chunk results
 chunk_file = self.output_dir / f"chunk_{chunk_start}_{chunk_end}.json"
 self._save_chunk(results[-len(chunk):], chunk_file)

 # Summary
 logger.info(f"Batch complete: {len(results)} succeeded, {len(errors)} failed")

 return {
 'total': total_cases,
 'succeeded': len(results),
 'failed': len(errors),
 'results': results,
 'errors': errors
 }

 def _save_chunk(self, chunk_results, file_path):
 """Save chunk to file"""
 exporter = JSONExporter(pretty=True)
 exporter.export(chunk_results, file_path)
 logger.info(f"Saved chunk to {file_path}")

# Usage example
if __name__ == '__main__':
 # Simulate large dataset
 cases = [
 {'case_id': f'BATCH_{i:05d}', 'age': 50 + (i % 40), 'sex': 'M' if i % 2 == 0 else 'F'}
 for i in range(1000) # 1000 cases
 ]

 processor = ParallelBatchProcessor(max_workers=8)
 batch_result = processor.process_batch(cases, chunk_size=250)

 print(f"\nâœ… Batch Processing Complete")
 print(f" Total: {batch_result['total']}")
 print(f" Succeeded: {batch_result['succeeded']}")
 print(f" Failed: {batch_result['failed']}")
```

### Pattern 2: Streaming Processing for Large Datasets

```python
"""
Stream processing for datasets too large to fit in memory
"""

import json
from pathlib import Path
from surgul.clinical_case import ClinicalCase
from surgul.trix_pipeline import TRIXPipeline
from surgul.exporters.csv_exporter import CSVExporter

class StreamingProcessor:
 """Process cases one at a time from streaming source"""

 def __init__(self):
 self.pipeline = TRIXPipeline()
 self.stats = {'processed': 0, 'errors': 0}

 def process_jsonl_file(self, input_file, output_file):
 """
 Process JSONL file line by line (JSON Lines format)

 Args:
 input_file: Path to .jsonl file (one JSON object per line)
 output_file: Path to output CSV
 """
 csv_exporter = CSVExporter(flatten_nested=True)
 results = []

 with open(input_file, 'r') as f:
 for line_num, line in enumerate(f, 1):
 try:
 # Parse JSON line
 case_data = json.loads(line.strip())

 # Process case
 case = ClinicalCase.from_dict(case_data)
 recommendation = self.pipeline.process(case)

 # Extract result
 results.append({
 'case_id': case.case_id,
 'risk_tier': recommendation.triage_decision.risk_tier.name,
 'confidence': recommendation.triage_decision.confidence
 })

 self.stats['processed'] += 1

 # Save in batches to prevent memory overflow
 if len(results) >= 1000:
 csv_exporter.export(
 results,
 output_file,
 mode='a', # Append mode
 header=(line_num == 1)
 )
 results = [] # Clear memory

 except json.JSONDecodeError:
 print(f"âš  Invalid JSON on line {line_num}")
 self.stats['errors'] += 1
 except Exception as e:
 print(f"âš  Error processing line {line_num}: {e}")
 self.stats['errors'] += 1

 # Save remaining results
 if results:
 csv_exporter.export(results, output_file, mode='a', header=False)

 return self.stats

# Usage
processor = StreamingProcessor()
stats = processor.process_jsonl_file('large_dataset.jsonl', 'results.csv')
print(f"Processed: {stats['processed']}, Errors: {stats['errors']}")
```

---

## Automated Pipeline Patterns

### Pattern 3: Scheduled Compliance Monitoring

```python
"""
Automated compliance monitoring with scheduling
"""

import schedule
import time
from datetime import datetime
from pathlib import Path
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator
from surgul.exporters.json_exporter import JSONExporter
import smtplib
from email.mime.text import MIMEText

class ComplianceMonitor:
 """Automated compliance monitoring system"""

 def __init__(self, metadata, alert_email=None):
 self.metadata = metadata
 self.alert_email = alert_email
 self.nist_validator = NISTAIRMFValidator()
 self.fda_validator = FDAGMLPValidator()
 self.json_exporter = JSONExporter(pretty=True)
 self.history = []

 def run_compliance_check(self):
 """Run compliance validation and alert if needed"""
 print(f"\nðŸ” Running scheduled compliance check: {datetime.now()}")

 # Run validators
 nist_report = self.nist_validator.validate(self.metadata)
 fda_report = self.fda_validator.validate(self.metadata)

 # Record results
 record = {
 'timestamp': datetime.now().isoformat(),
 'nist_score': nist_report.compliance_score,
 'nist_status': nist_report.certification_readiness,
 'fda_score': fda_report.compliance_score,
 'fda_status': fda_report.submission_readiness,
 'nist_critical_gaps': len(nist_report.critical_deficiencies),
 'fda_critical_gaps': len(fda_report.critical_deficiencies)
 }

 self.history.append(record)

 # Check for alerts
 alerts = []

 if nist_report.compliance_score < 0.70:
 alerts.append(f"âš  NIST score dropped below 70%: {nist_report.compliance_score:.1%}")

 if fda_report.compliance_score < 0.65:
 alerts.append(f"âš  FDA score dropped below 65%: {fda_report.compliance_score:.1%}")

 if record['nist_critical_gaps'] > 0:
 alerts.append(f"âš  NIST has {record['nist_critical_gaps']} critical gaps")

 if record['fda_critical_gaps'] > 0:
 alerts.append(f"âš  FDA has {record['fda_critical_gaps']} critical gaps")

 # Send alerts
 if alerts and self.alert_email:
 self.send_alert_email(alerts)

 # Save history
 history_file = Path("compliance_history.json")
 self.json_exporter.export(self.history, history_file)

 # Print summary
 print(f"âœ… Compliance check complete")
 print(f" NIST: {nist_report.compliance_score:.1%} ({nist_report.certification_readiness})")
 print(f" FDA: {fda_report.compliance_score:.1%} ({fda_report.submission_readiness})")

 if alerts:
 print(f"\nâš  {len(alerts)} alerts generated")
 for alert in alerts:
 print(f" {alert}")

 return record

 def send_alert_email(self, alerts):
 """Send alert email"""
 msg = MIMEText(f"Compliance Alert\n\n" + "\n".join(alerts))
 msg['Subject'] = "TRI-X Compliance Alert"
 msg['From'] = "trix-monitor@example.com"
 msg['To'] = self.alert_email

 # Send email (configure your SMTP server)
 # smtp = smtplib.SMTP('smtp.example.com')
 # smtp.send_message(msg)
 # smtp.quit()

 print(f"ðŸ“§ Alert email sent to {self.alert_email}")

 def start_monitoring(self):
 """Start scheduled monitoring"""
 # Run immediately
 self.run_compliance_check()

 # Schedule weekly checks (every Monday at 9 AM)
 schedule.every().monday.at("09:00").do(self.run_compliance_check)

 # Run scheduler
 print("\nðŸ“… Compliance monitoring started")
 print(" Schedule: Every Monday at 9:00 AM")

 while True:
 schedule.run_pending()
 time.sleep(60) # Check every minute

# Usage
if __name__ == '__main__':
 metadata = {
 "system_name": "TRI-X Framework",
 "version": "1.0",
 "validation": {"internal_validation": True}
 }

 monitor = ComplianceMonitor(metadata, alert_email="admin@example.com")
 monitor.start_monitoring()
```

### Pattern 4: CI/CD Integration

```python
"""
GitHub Actions / GitLab CI integration for compliance
"""

import sys
from pathlib import Path
from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator
from surgul.validators.fda_gmlp_validator import FDAGMLPValidator

def ci_compliance_check(min_nist_score=0.70, min_fda_score=0.65):
 """
 CI/CD compliance check - fails build if scores below threshold

 Returns:
 0 if compliant, 1 if not compliant
 """
 print("ðŸ” Running CI/CD Compliance Check")

 # Load metadata
 metadata = {
 "system_name": "TRI-X Framework",
 "version": "1.0",
 # ... load from file or environment
 }

 # Run validators
 nist_validator = NISTAIRMFValidator()
 fda_validator = FDAGMLPValidator()

 nist_report = nist_validator.validate(metadata)
 fda_report = fda_validator.validate(metadata)

 # Check thresholds
 nist_pass = nist_report.compliance_score >= min_nist_score
 fda_pass = fda_report.compliance_score >= min_fda_score

 # Print results
 print(f"\nðŸ“Š Results:")
 print(f" NIST: {nist_report.compliance_score:.1%} (threshold: {min_nist_score:.1%}) {'âœ… PASS' if nist_pass else 'âŒ FAIL'}")
 print(f" FDA: {fda_report.compliance_score:.1%} (threshold: {min_fda_score:.1%}) {'âœ… PASS' if fda_pass else 'âŒ FAIL'}")

 if not (nist_pass and fda_pass):
 print("\nâŒ Compliance check FAILED")
 print("\nCritical Issues:")

 for deficiency in nist_report.critical_deficiencies:
 print(f" â€¢ NIST: {deficiency}")

 for deficiency in fda_report.critical_deficiencies:
 print(f" â€¢ FDA: {deficiency}")

 return 1

 print("\nâœ… Compliance check PASSED")
 return 0

if __name__ == '__main__':
 exit_code = ci_compliance_check()
 sys.exit(exit_code)
```

**GitHub Actions Workflow** (`.github/workflows/compliance.yml`):

```yaml
name: Compliance Check

on: [push, pull_request]

jobs:
 compliance:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v2
 - uses: actions/setup-python@v2
 with:
 python-version: '3.8'
 - name: Install dependencies
 run: pip install -r requirements.txt
 - name: Run compliance check
 run: python ci_compliance_check.py
```

---

## Error Handling & Recovery

### Pattern 5: Robust Error Handling with Retry Logic

```python
"""
Production-grade error handling with retry and fallback
"""

from functools import wraps
import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries=3, initial_delay=1, backoff_factor=2):
 """
 Decorator for retry logic with exponential backoff

 Args:
 max_retries: Maximum number of retry attempts
 initial_delay: Initial delay in seconds
 backoff_factor: Multiply delay by this factor each retry
 """
 def decorator(func: Callable) -> Callable:
 @wraps(func)
 def wrapper(*args, **kwargs) -> Any:
 delay = initial_delay

 for attempt in range(max_retries + 1):
 try:
 return func(*args, **kwargs)

 except Exception as e:
 if attempt == max_retries:
 logger.error(f"Max retries ({max_retries}) reached for {func.__name__}: {e}")
 raise

 logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
 logger.info(f"Retrying in {delay} seconds...")

 time.sleep(delay)
 delay *= backoff_factor

 return None

 return wrapper
 return decorator

class RobustProcessor:
 """Production-grade processor with comprehensive error handling"""

 def __init__(self):
 self.pipeline = None # Lazy initialization
 self.error_log = []

 def _initialize_pipeline(self):
 """Lazy pipeline initialization"""
 if self.pipeline is None:
 try:
 from surgul.trix_pipeline import TRIXPipeline
 self.pipeline = TRIXPipeline()
 except Exception as e:
 logger.error(f"Failed to initialize pipeline: {e}")
 raise

 @retry_with_backoff(max_retries=3, initial_delay=1)
 def process_case_with_retry(self, case_data):
 """Process case with automatic retry on failure"""
 self._initialize_pipeline()

 try:
 from surgul.clinical_case import ClinicalCase

 # Validate input
 if not self._validate_case_data(case_data):
 raise ValueError("Invalid case data")

 # Process
 case = ClinicalCase.from_dict(case_data)
 recommendation = self.pipeline.process(case)

 return {
 'status': 'success',
 'case_id': case.case_id,
 'result': recommendation
 }

 except Exception as e:
 # Log error
 error_record = {
 'case_id': case_data.get('case_id', 'UNKNOWN'),
 'error': str(e),
 'error_type': type(e).__name__,
 'timestamp': time.time()
 }
 self.error_log.append(error_record)

 # Re-raise for retry logic
 raise

 def _validate_case_data(self, case_data):
 """Validate case data before processing"""
 required_fields = ['case_id']

 for field in required_fields:
 if field not in case_data:
 logger.error(f"Missing required field: {field}")
 return False

 return True

 def process_with_fallback(self, case_data, fallback_result=None):
 """
 Process with fallback result on failure

 Args:
 case_data: Input case data
 fallback_result: Result to return if processing fails
 """
 try:
 return self.process_case_with_retry(case_data)

 except Exception as e:
 logger.error(f"All retries failed, using fallback: {e}")

 if fallback_result is None:
 fallback_result = {
 'status': 'failed',
 'case_id': case_data.get('case_id', 'UNKNOWN'),
 'error': 'Processing failed after retries',
 'fallback': True
 }

 return fallback_result

# Usage
processor = RobustProcessor()

# Will retry up to 3 times on failure
result = processor.process_case_with_retry({'case_id': 'TEST001', 'age': 65})

# Or use with fallback
result = processor.process_with_fallback(
 {'case_id': 'TEST002'},
 fallback_result={'status': 'manual_review_required'}
)
```

---

## Performance Optimization

### Pattern 6: Caching for Improved Performance

```python
"""
Intelligent caching to improve performance
"""

from functools import lru_cache
import hashlib
import json
import pickle
from pathlib import Path

class CachedProcessor:
 """Processor with multi-level caching"""

 def __init__(self, cache_dir="cache"):
 self.cache_dir = Path(cache_dir)
 self.cache_dir.mkdir(exist_ok=True)
 self.memory_cache = {}

 def _get_cache_key(self, case_data):
 """Generate cache key from case data"""
 # Convert to JSON string and hash
 data_str = json.dumps(case_data, sort_keys=True)
 return hashlib.md5(data_str.encode()).hexdigest()

 def process_with_cache(self, case_data, use_disk_cache=True):
 """
 Process with multi-level caching

 1. Check memory cache (fastest)
 2. Check disk cache (fast)
 3. Process and cache (slow)
 """
 cache_key = self._get_cache_key(case_data)

 # Level 1: Memory cache
 if cache_key in self.memory_cache:
 print(f"âœ… Memory cache hit: {cache_key[:8]}")
 return self.memory_cache[cache_key]

 # Level 2: Disk cache
 if use_disk_cache:
 cache_file = self.cache_dir / f"{cache_key}.pkl"

 if cache_file.exists():
 print(f"âœ… Disk cache hit: {cache_key[:8]}")
 with open(cache_file, 'rb') as f:
 result = pickle.load(f)

 # Promote to memory cache
 self.memory_cache[cache_key] = result
 return result

 # Level 3: Process (cache miss)
 print(f"âŒ Cache miss, processing: {cache_key[:8]}")

 from surgul.clinical_case import ClinicalCase
 from surgul.trix_pipeline import TRIXPipeline

 pipeline = TRIXPipeline()
 case = ClinicalCase.from_dict(case_data)
 recommendation = pipeline.process(case)

 result = {
 'case_id': case.case_id,
 'risk_tier': recommendation.triage_decision.risk_tier.name,
 'confidence': recommendation.triage_decision.confidence
 }

 # Cache result
 self.memory_cache[cache_key] = result

 if use_disk_cache:
 cache_file = self.cache_dir / f"{cache_key}.pkl"
 with open(cache_file, 'wb') as f:
 pickle.dump(result, f)

 return result

 def clear_cache(self, memory=True, disk=True):
 """Clear cache"""
 if memory:
 self.memory_cache.clear()
 print("âœ… Memory cache cleared")

 if disk:
 for cache_file in self.cache_dir.glob("*.pkl"):
 cache_file.unlink()
 print("âœ… Disk cache cleared")

# Usage
processor = CachedProcessor()

# First call: cache miss, processes
result1 = processor.process_with_cache({'case_id': 'TEST001', 'age': 65})

# Second call: cache hit, instant
result2 = processor.process_with_cache({'case_id': 'TEST001', 'age': 65})

# Clear cache when needed
processor.clear_cache()
```

### Pattern 7: Lazy Loading for Large Systems

```python
"""
Lazy loading to improve startup time
"""

class LazyLoadedSystem:
 """System with lazy-loaded components"""

 def __init__(self):
 self._pipeline = None
 self._nist_validator = None
 self._fda_validator = None
 self._exporters = {}

 @property
 def pipeline(self):
 """Lazy-load TRI-X pipeline"""
 if self._pipeline is None:
 print("â³ Loading TRI-X pipeline...")
 from surgul.trix_pipeline import TRIXPipeline
 self._pipeline = TRIXPipeline()
 print("âœ… Pipeline loaded")

 return self._pipeline

 @property
 def nist_validator(self):
 """Lazy-load NIST validator"""
 if self._nist_validator is None:
 print("â³ Loading NIST validator...")
 from surgul.validators.nist_ai_rmf_validator import NISTAIRMFValidator
 self._nist_validator = NISTAIRMFValidator()
 print("âœ… NIST validator loaded")

 return self._nist_validator

 def get_exporter(self, format_type):
 """Lazy-load exporters on demand"""
 if format_type not in self._exporters:
 print(f"â³ Loading {format_type} exporter...")

 if format_type == 'json':
 from surgul.exporters.json_exporter import JSONExporter
 self._exporters[format_type] = JSONExporter(pretty=True)
 elif format_type == 'csv':
 from surgul.exporters.csv_exporter import CSVExporter
 self._exporters[format_type] = CSVExporter()
 elif format_type == 'fhir':
 from surgul.exporters.fhir_exporter import FHIRExporter
 self._exporters[format_type] = FHIRExporter()
 elif format_type == 'pdf':
 from surgul.exporters.pdf_exporter import PDFExporter
 self._exporters[format_type] = PDFExporter()

 print(f"âœ… {format_type} exporter loaded")

 return self._exporters[format_type]

# Usage
system = LazyLoadedSystem() # Fast initialization

# Components loaded only when needed
recommendation = system.pipeline.process(case) # Loads pipeline
exporter = system.get_exporter('json') # Loads JSON exporter
```

---

## Custom Validators

### Pattern 8: Creating Custom Compliance Validators

```python
"""
Create custom validators for organizational requirements
"""

from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class CustomCheck:
 """Custom compliance check"""
 check_id: str
 category: str
 requirement: str
 status: str # 'PASS', 'FAIL', 'N/A'
 evidence: str = ""
 severity: str = "MEDIUM" # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'

@dataclass
class CustomComplianceReport:
 """Custom compliance report"""
 framework_name: str
 system_name: str
 validation_timestamp: str
 compliance_score: float
 total_checks: int
 checks_passed: int
 checks_failed: int
 all_checks: List[CustomCheck]
 recommendations: List[str]

class OrganizationalValidator:
 """
 Custom validator for organization-specific requirements

 Example: Hospital-specific AI governance requirements
 """

 def __init__(self):
 self.framework_name = "Hospital AI Governance Framework"

 def validate(self, metadata):
 """Validate against organizational requirements"""
 checks = []

 # Check 1: IRB Approval
 checks.append(self._check_irb_approval(metadata))

 # Check 2: Clinical Champion
 checks.append(self._check_clinical_champion(metadata))

 # Check 3: IT Security Review
 checks.append(self._check_security_review(metadata))

 # Check 4: Legal Review
 checks.append(self._check_legal_review(metadata))

 # Check 5: Privacy Impact Assessment
 checks.append(self._check_privacy_assessment(metadata))

 # Check 6: Bias Assessment
 checks.append(self._check_bias_assessment(metadata))

 # Calculate scores
 total = len(checks)
 passed = sum(1 for c in checks if c.status == 'PASS')
 failed = sum(1 for c in checks if c.status == 'FAIL')

 # Generate recommendations
 recommendations = self._generate_recommendations(checks)

 return CustomComplianceReport(
 framework_name=self.framework_name,
 system_name=metadata.get('system_name', 'Unknown'),
 validation_timestamp=datetime.now().isoformat(),
 compliance_score=passed / total if total > 0 else 0,
 total_checks=total,
 checks_passed=passed,
 checks_failed=failed,
 all_checks=checks,
 recommendations=recommendations
 )

 def _check_irb_approval(self, metadata):
 """Check for IRB approval"""
 irb_approved = metadata.get('irb_approval', {}).get('approved', False)

 return CustomCheck(
 check_id="ORG-001",
 category="Ethics",
 requirement="IRB approval obtained for clinical use",
 status='PASS' if irb_approved else 'FAIL',
 evidence=metadata.get('irb_approval', {}).get('approval_number', 'None'),
 severity='CRITICAL'
 )

 def _check_clinical_champion(self, metadata):
 """Check for clinical champion"""
 has_champion = 'clinical_champion' in metadata

 return CustomCheck(
 check_id="ORG-002",
 category="Governance",
 requirement="Clinical champion identified and engaged",
 status='PASS' if has_champion else 'FAIL',
 evidence=metadata.get('clinical_champion', 'None'),
 severity='HIGH'
 )

 def _check_security_review(self, metadata):
 """Check for security review"""
 security_reviewed = metadata.get('security_review', {}).get('completed', False)

 return CustomCheck(
 check_id="ORG-003",
 category="Security",
 requirement="IT security review completed",
 status='PASS' if security_reviewed else 'FAIL',
 evidence=metadata.get('security_review', {}).get('date', 'None'),
 severity='CRITICAL'
 )

 def _check_legal_review(self, metadata):
 """Check for legal review"""
 legal_reviewed = metadata.get('legal_review', {}).get('completed', False)

 return CustomCheck(
 check_id="ORG-004",
 category="Legal",
 requirement="Legal review completed",
 status='PASS' if legal_reviewed else 'FAIL',
 evidence=metadata.get('legal_review', {}).get('date', 'None'),
 severity='HIGH'
 )

 def _check_privacy_assessment(self, metadata):
 """Check for privacy impact assessment"""
 privacy_assessed = metadata.get('privacy_impact_assessment', {}).get('completed', False)

 return CustomCheck(
 check_id="ORG-005",
 category="Privacy",
 requirement="Privacy impact assessment completed",
 status='PASS' if privacy_assessed else 'FAIL',
 evidence=metadata.get('privacy_impact_assessment', {}).get('date', 'None'),
 severity='CRITICAL'
 )

 def _check_bias_assessment(self, metadata):
 """Check for bias assessment"""
 bias_assessed = metadata.get('bias_assessment', {}).get('conducted', False)

 return CustomCheck(
 check_id="ORG-006",
 category="Fairness",
 requirement="Bias and fairness assessment conducted",
 status='PASS' if bias_assessed else 'FAIL',
 evidence="Demographic analysis completed" if bias_assessed else "Not conducted",
 severity='HIGH'
 )

 def _generate_recommendations(self, checks):
 """Generate recommendations based on failed checks"""
 recommendations = []

 for check in checks:
 if check.status == 'FAIL':
 recommendations.append(f"{check.category}: {check.requirement}")

 return recommendations

# Usage
metadata = {
 'system_name': 'TRI-X Framework',
 'irb_approval': {'approved': True, 'approval_number': 'IRB-2026-001'},
 'clinical_champion': 'Dr. John Smith, Chief of Neurology',
 'security_review': {'completed': True, 'date': '2026-01-01'},
 'legal_review': {'completed': False},
 'privacy_impact_assessment': {'completed': True, 'date': '2026-01-05'},
 'bias_assessment': {'conducted': True}
}

validator = OrganizationalValidator()
report = validator.validate(metadata)

print(f"Compliance: {report.compliance_score:.1%}")
print(f"Passed: {report.checks_passed}/{report.total_checks}")

if report.recommendations:
 print("\nRecommendations:")
 for rec in report.recommendations:
 print(f" â€¢ {rec}")
```

---

## Custom Exporters

### Pattern 9: Creating Custom Export Formats

```python
"""
Create custom exporters for specialized formats
"""

from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

class XMLExporter:
 """Custom XML exporter for legacy systems"""

 def export_clinical_case(self, case, output_path):
 """Export clinical case to XML"""
 # Create root
 root = ET.Element('ClinicalCase')
 root.set('version', '1.0')
 root.set('timestamp', datetime.now().isoformat())

 # Demographics
 demographics = ET.SubElement(root, 'Demographics')
 ET.SubElement(demographics, 'CaseID').text = str(case.case_id)
 ET.SubElement(demographics, 'Age').text = str(case.age)
 ET.SubElement(demographics, 'Sex').text = str(case.sex)

 # Vitals
 if case.vitals:
 vitals = ET.SubElement(root, 'VitalSigns')
 ET.SubElement(vitals, 'SystolicBP').text = str(case.vitals.BP_systolic)
 ET.SubElement(vitals, 'DiastolicBP').text = str(case.vitals.BP_diastolic)
 ET.SubElement(vitals, 'HeartRate').text = str(case.vitals.heart_rate)

 # Write to file
 tree = ET.ElementTree(root)
 ET.indent(tree, space=" ")
 tree.write(output_path, encoding='utf-8', xml_declaration=True)

 print(f"âœ… XML exported: {output_path}")

class HL7Exporter:
 """Custom HL7 v2 exporter for healthcare systems"""

 def export_triage_decision(self, recommendation, case, output_path):
 """Export as HL7 ORU^R01 message"""
 timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

 hl7_message = f"""MSH|^~\\&|TRIX|HOSPITAL|EHR|HOSPITAL|{timestamp}||ORU^R01|{case.case_id}|P|2.5
PID|||{case.case_id}||PATIENT^TEST||{self._format_birthdate(case.age)}|{case.sex}
PV1||I|ED^ED01^01
OBR|1||{case.case_id}|TRIX^TRI-X Dizziness Assessment^LN|||{timestamp}
OBX|1|ST|RISK_TIER^Risk Tier^LN||{recommendation.triage_decision.risk_tier.name}||||||F
OBX|2|NM|CONFIDENCE^Confidence Score^LN||{recommendation.triage_decision.confidence:.3f}||||||F
OBX|3|NM|UNCERTAINTY^Uncertainty Mass^LN||{recommendation.triage_decision.uncertainty_mass:.3f}||||||F
OBX|4|ST|ACTION^Recommended Action^LN||{recommendation.action_state.name}||||||F"""

 # Write to file
 with open(output_path, 'w') as f:
 f.write(hl7_message)

 print(f"âœ… HL7 exported: {output_path}")

 def _format_birthdate(self, age):
 """Calculate birthdate from age"""
 birth_year = datetime.now().year - age
 return f"{birth_year}0101"

# Usage
xml_exporter = XMLExporter()
xml_exporter.export_clinical_case(case, "output.xml")

hl7_exporter = HL7Exporter()
hl7_exporter.export_triage_decision(recommendation, case, "output.hl7")
```

---

## Monitoring & Alerting

### Pattern 10: Comprehensive Monitoring System

```python
"""
Production monitoring with metrics, logging, and alerting
"""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from collections import deque, Counter

@dataclass
class PerformanceMetrics:
 """Performance metrics tracker"""
 processing_times: deque = field(default_factory=lambda: deque(maxlen=1000))
 error_count: int = 0
 success_count: int = 0
 total_cases: int = 0
 risk_distribution: Counter = field(default_factory=Counter)
 start_time: float = field(default_factory=time.time)

 @property
 def avg_processing_time(self):
 """Calculate average processing time"""
 return sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0

 @property
 def success_rate(self):
 """Calculate success rate"""
 return self.success_count / self.total_cases if self.total_cases > 0 else 0

 @property
 def uptime_hours(self):
 """Calculate uptime"""
 return (time.time() - self.start_time) / 3600

class MonitoredProcessor:
 """Processor with comprehensive monitoring"""

 def __init__(self, alert_threshold_error_rate=0.05):
 self.metrics = PerformanceMetrics()
 self.alert_threshold = alert_threshold_error_rate

 # Setup logging
 logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 handlers=[
 logging.FileHandler('trix_processor.log'),
 logging.StreamHandler()
 ]
 )
 self.logger = logging.getLogger(__name__)

 def process_with_monitoring(self, case_data):
 """Process case with full monitoring"""
 start_time = time.time()
 case_id = case_data.get('case_id', 'UNKNOWN')

 try:
 # Log start
 self.logger.info(f"Processing started: {case_id}")

 # Process case
 from surgul.clinical_case import ClinicalCase
 from surgul.trix_pipeline import TRIXPipeline

 pipeline = TRIXPipeline()
 case = ClinicalCase.from_dict(case_data)
 recommendation = pipeline.process(case)

 # Record metrics
 processing_time = time.time() - start_time
 self.metrics.processing_times.append(processing_time)
 self.metrics.success_count += 1
 self.metrics.total_cases += 1
 self.metrics.risk_distribution[recommendation.triage_decision.risk_tier.name] += 1

 # Log success
 self.logger.info(
 f"Processing completed: {case_id} | "
 f"Risk: {recommendation.triage_decision.risk_tier.name} | "
 f"Time: {processing_time:.3f}s"
 )

 # Check for alerts
 self._check_alerts()

 return {
 'status': 'success',
 'case_id': case_id,
 'result': recommendation,
 'processing_time': processing_time
 }

 except Exception as e:
 # Record error
 processing_time = time.time() - start_time
 self.metrics.error_count += 1
 self.metrics.total_cases += 1

 # Log error
 self.logger.error(
 f"Processing failed: {case_id} | "
 f"Error: {str(e)} | "
 f"Time: {processing_time:.3f}s",
 exc_info=True
 )

 # Check for alerts
 self._check_alerts()

 return {
 'status': 'error',
 'case_id': case_id,
 'error': str(e),
 'processing_time': processing_time
 }

 def _check_alerts(self):
 """Check if alerts should be triggered"""
 # Alert if error rate too high
 if self.metrics.total_cases >= 10: # Need minimum sample
 error_rate = self.metrics.error_count / self.metrics.total_cases

 if error_rate > self.alert_threshold:
 self.logger.critical(
 f"âš ï¸ ALERT: High error rate detected! "
 f"Rate: {error_rate:.1%} "
 f"(threshold: {self.alert_threshold:.1%})"
 )

 # Alert if avg processing time > 5 seconds
 if self.metrics.avg_processing_time > 5.0:
 self.logger.warning(
 f"âš ï¸ ALERT: Slow processing detected! "
 f"Avg time: {self.metrics.avg_processing_time:.2f}s"
 )

 def get_status_report(self):
 """Generate status report"""
 return {
 'uptime_hours': self.metrics.uptime_hours,
 'total_cases': self.metrics.total_cases,
 'success_count': self.metrics.success_count,
 'error_count': self.metrics.error_count,
 'success_rate': self.metrics.success_rate,
 'avg_processing_time_ms': self.metrics.avg_processing_time * 1000,
 'risk_distribution': dict(self.metrics.risk_distribution),
 'timestamp': datetime.now().isoformat()
 }

# Usage
processor = MonitoredProcessor(alert_threshold_error_rate=0.05)

# Process cases
for case_data in cases:
 result = processor.process_with_monitoring(case_data)

# Get status report
status = processor.get_status_report()
print(f"\nðŸ“Š Status Report:")
print(f" Uptime: {status['uptime_hours']:.2f} hours")
print(f" Cases: {status['total_cases']}")
print(f" Success Rate: {status['success_rate']:.1%}")
print(f" Avg Time: {status['avg_processing_time_ms']:.0f}ms")
```

---

## Multi-Tenancy Patterns

### Pattern 11: Multi-Hospital/Multi-Site System

```python
"""
Multi-tenancy support for running TRI-X across multiple organizations
"""

from pathlib import Path
from typing import Dict
import json

class TenantConfig:
 """Configuration for single tenant (hospital/site)"""

 def __init__(self, tenant_id, config_data):
 self.tenant_id = tenant_id
 self.config = config_data
 self.output_dir = Path(f"tenants/{tenant_id}")
 self.output_dir.mkdir(parents=True, exist_ok=True)

 def get_setting(self, key, default=None):
 """Get tenant-specific setting"""
 return self.config.get(key, default)

class MultiTenantProcessor:
 """Process cases for multiple tenants with isolated configurations"""

 def __init__(self, config_file="tenant_config.json"):
 self.tenants: Dict[str, TenantConfig] = {}
 self.pipelines = {}
 self._load_tenant_configs(config_file)

 def _load_tenant_configs(self, config_file):
 """Load tenant configurations"""
 with open(config_file, 'r') as f:
 configs = json.load(f)

 for tenant_id, config_data in configs.items():
 self.tenants[tenant_id] = TenantConfig(tenant_id, config_data)
 print(f"âœ… Loaded config for tenant: {tenant_id}")

 def get_pipeline(self, tenant_id):
 """Get or create pipeline for tenant"""
 if tenant_id not in self.pipelines:
 from surgul.trix_pipeline import TRIXPipeline

 # Could customize pipeline per tenant here
 self.pipelines[tenant_id] = TRIXPipeline()

 return self.pipelines[tenant_id]

 def process_case(self, tenant_id, case_data):
 """Process case for specific tenant"""
 if tenant_id not in self.tenants:
 raise ValueError(f"Unknown tenant: {tenant_id}")

 tenant = self.tenants[tenant_id]
 pipeline = self.get_pipeline(tenant_id)

 # Process case
 from surgul.clinical_case import ClinicalCase
 case = ClinicalCase.from_dict(case_data)
 recommendation = pipeline.process(case)

 # Export with tenant-specific settings
 export_format = tenant.get_setting('export_format', 'json')
 self._export_result(tenant, recommendation, case, export_format)

 return {
 'tenant_id': tenant_id,
 'case_id': case.case_id,
 'result': recommendation
 }

 def _export_result(self, tenant, recommendation, case, format_type):
 """Export result with tenant-specific settings"""
 output_path = tenant.output_dir / f"{case.case_id}.{format_type}"

 if format_type == 'json':
 from surgul.exporters.json_exporter import JSONExporter
 exporter = JSONExporter(pretty=True)
 exporter.export_care_recommendation(recommendation, output_path)

 elif format_type == 'fhir':
 from surgul.exporters.fhir_exporter import FHIRExporter
 system_url = tenant.get_setting('fhir_system_url', 'http://example.org')
 exporter = FHIRExporter(system_url=system_url)
 exporter.export_care_recommendation(recommendation, case, output_path)

 elif format_type == 'pdf':
 from surgul.exporters.pdf_exporter import PDFExporter
 title = tenant.get_setting('pdf_title', 'Clinical Report')
 exporter = PDFExporter(title=title)
 exporter.export_care_recommendation(recommendation, case, output_path)

 def get_tenant_statistics(self, tenant_id):
 """Get statistics for specific tenant"""
 if tenant_id not in self.tenants:
 return None

 tenant = self.tenants[tenant_id]
 results_dir = tenant.output_dir

 # Count processed cases
 case_count = len(list(results_dir.glob('*')))

 return {
 'tenant_id': tenant_id,
 'cases_processed': case_count,
 'export_format': tenant.get_setting('export_format'),
 'output_dir': str(results_dir)
 }

# Example tenant configuration file (tenant_config.json)
"""
{
 "hospital_a": {
 "name": "General Hospital",
 "export_format": "fhir",
 "fhir_system_url": "http://hospital-a.org/trix",
 "pdf_title": "General Hospital - TRI-X Report"
 },
 "hospital_b": {
 "name": "University Medical Center",
 "export_format": "json",
 "custom_settings": {
 "high_risk_alert": true
 }
 },
 "hospital_c": {
 "name": "Community Clinic",
 "export_format": "pdf",
 "pdf_title": "Community Clinic - Clinical Assessment"
 }
}
"""

# Usage
processor = MultiTenantProcessor('tenant_config.json')

# Process for different tenants
result_a = processor.process_case('hospital_a', {
 'case_id': 'HOSP_A_001',
 'age': 65,
 'sex': 'M'
})

result_b = processor.process_case('hospital_b', {
 'case_id': 'HOSP_B_001',
 'age': 52,
 'sex': 'F'
})

# Get statistics per tenant
stats_a = processor.get_tenant_statistics('hospital_a')
print(f"Hospital A: {stats_a['cases_processed']} cases")
```

---

## Best Practices Summary

### Performance Best Practices

1. **Use Parallel Processing** for large batches (Pattern 1)
2. **Implement Caching** for repeated queries (Pattern 6)
3. **Lazy Load** components to reduce startup time (Pattern 7)
4. **Stream Process** large datasets (Pattern 2)

### Reliability Best Practices

1. **Retry with Backoff** for transient failures (Pattern 5)
2. **Comprehensive Error Handling** with fallbacks (Pattern 5)
3. **Health Monitoring** with alerts (Pattern 10)
4. **Audit Logging** for traceability (Case Study 6)

### Integration Best Practices

1. **CI/CD Integration** for automated compliance (Pattern 4)
2. **Scheduled Monitoring** for continuous validation (Pattern 3)
3. **Multi-Tenant Support** for scalability (Pattern 11)
4. **Custom Validators** for org-specific needs (Pattern 8)

### Code Organization Best Practices

```python
# Recommended project structure for advanced usage

trix_production/
â”œâ”€â”€ config/
â”‚ â”œâ”€â”€ tenant_config.json
â”‚ â”œâ”€â”€ monitoring_config.json
â”‚ â””â”€â”€ export_config.json
â”œâ”€â”€ processors/
â”‚ â”œâ”€â”€ batch_processor.py
â”‚ â”œâ”€â”€ streaming_processor.py
â”‚ â””â”€â”€ monitored_processor.py
â”œâ”€â”€ validators/
â”‚ â”œâ”€â”€ nist_validator.py
â”‚ â”œâ”€â”€ fda_validator.py
â”‚ â””â”€â”€ custom_validators/
â”‚ â””â”€â”€ organizational_validator.py
â”œâ”€â”€ exporters/
â”‚ â”œâ”€â”€ json_exporter.py
â”‚ â”œâ”€â”€ csv_exporter.py
â”‚ â”œâ”€â”€ fhir_exporter.py
â”‚ â””â”€â”€ custom_exporters/
â”‚ â”œâ”€â”€ xml_exporter.py
â”‚ â””â”€â”€ hl7_exporter.py
â”œâ”€â”€ monitoring/
â”‚ â”œâ”€â”€ metrics_collector.py
â”‚ â”œâ”€â”€ alerting.py
â”‚ â””â”€â”€ dashboard_api.py
â”œâ”€â”€ cache/
â”‚ â””â”€â”€ cached_processor.py
â”œâ”€â”€ utils/
â”‚ â”œâ”€â”€ retry_logic.py
â”‚ â”œâ”€â”€ error_handling.py
â”‚ â””â”€â”€ lazy_loading.py
â””â”€â”€ main.py
```

---

## Production Checklist

### Before Deployment

- [ ] Implement error handling with retry logic
- [ ] Set up comprehensive logging
- [ ] Configure monitoring and alerting
- [ ] Enable caching for performance
- [ ] Test with production-scale data
- [ ] Set up CI/CD pipeline
- [ ] Configure backup and recovery
- [ ] Document custom configurations
- [ ] Train operations team
- [ ] Prepare runbook for incidents

### Performance Targets

- [ ] Processing time < 2 seconds per case
- [ ] Error rate < 5%
- [ ] System uptime > 99.5%
- [ ] Cache hit rate > 70%
- [ ] Concurrent users: 100+

### Security Checklist

- [ ] Input validation implemented
- [ ] Output sanitization enabled
- [ ] Audit logging configured
- [ ] Access control enforced
- [ ] Data encryption at rest
- [ ] Secure communication (HTTPS)
- [ ] Regular security reviews
- [ ] Incident response plan

---

## Troubleshooting Advanced Issues

### Issue: Out of Memory with Large Batches

**Solution:** Use streaming processing (Pattern 2) or chunked batch processing (Pattern 1)

```python
# Instead of loading all at once
processor.process_batch(large_dataset) # Memory error!

# Use chunked processing
processor.process_batch(large_dataset, chunk_size=100) # OK
```

### Issue: Slow Performance

**Solutions:**

1. Enable caching (Pattern 6)
2. Use parallel processing (Pattern 1)
3. Lazy load components (Pattern 7)
4. Profile code to find bottlenecks

```python
import cProfile

cProfile.run('processor.process_case(case_data)')
```

### Issue: High Error Rate

**Solutions:**

1. Add retry logic (Pattern 5)
2. Implement comprehensive monitoring (Pattern 10)
3. Check input data quality
4. Review error logs for patterns

### Issue: Integration Failures

**Solutions:**

1. Verify tenant configuration (Pattern 11)
2. Check export format compatibility
3. Validate FHIR compliance
4. Test with small subset first

---

## Advanced Integration Examples

### Example: Kubernetes Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
 name: trix-processor
spec:
 replicas: 3
 selector:
 matchLabels:
 app: trix
 template:
 metadata:
 labels:
 app: trix
 spec:
 containers:
 - name: trix
 image: trix:latest
 resources:
 limits:
 memory: "2Gi"
 cpu: "1000m"
 requests:
 memory: "1Gi"
 cpu: "500m"
 env:
 - name: TENANT_CONFIG
 valueFrom:
 configMapKeyRef:
 name: trix-config
 key: tenant_config.json
 - name: MAX_WORKERS
 value: "4"
```

### Example: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
 trix-processor:
 build: .
 environment:
 - PYTHONUNBUFFERED=1
 - MAX_WORKERS=4
 volumes:
 - ./config:/app/config
 - ./cache:/app/cache
 - ./logs:/app/logs
 restart: unless-stopped

 trix-monitor:
 build: .
 command: python monitoring/dashboard_api.py
 ports:
 - "8000:8000"
 depends_on:
 - trix-processor

 redis:
 image: redis:alpine
 ports:
 - "6379:6379"
 volumes:
 - redis-data:/data

volumes:
 redis-data:
```

---

## Summary

Advanced patterns covered:

1. âœ… **Parallel Batch Processing** - High performance
2. âœ… **Streaming Processing** - Memory efficient
3. âœ… **Automated Monitoring** - Scheduled compliance checks
4. âœ… **CI/CD Integration** - Automated testing
5. âœ… **Error Handling** - Retry with backoff
6. âœ… **Caching** - Performance optimization
7. âœ… **Lazy Loading** - Fast startup
8. âœ… **Custom Validators** - Org-specific requirements
9. âœ… **Custom Exporters** - Special formats
10. âœ… **Monitoring** - Production health tracking
11. âœ… **Multi-Tenancy** - Scale across organizations

These patterns enable production-grade deployment of TRI-X with enterprise features.

---

**Advanced Patterns Complete**

*Last Updated: 2026-01-10*
*Version: 1.0*

