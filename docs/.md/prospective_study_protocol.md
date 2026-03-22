# Evaluation Protocol for a Prospective Observational Study

**Version:** 1.0
**Date:** 2026-01-09

---

### 1. Study Title

A Prospective, Multi-center, Observational Study to Validate the [Your Model/Framework Name] for Predicting Adverse Events in Patients with [Specify Condition].

### 2. Background and Rationale

Retrospective analyses using synthetic and historical data have shown that the [Your Model/Framework Name] has potential in identifying patients at high risk of adverse events. However, its performance and clinical utility have not yet been evaluated in a real-world, prospective setting.

This study is designed to bridge that gap by assessing the model's predictive accuracy and its impact on clinical decision-making in real-time.

### 3. Objectives

#### 3.1. Primary Objective
- To evaluate the predictive performance (e.g., AUC-ROC, sensitivity, specificity) of the [Your Model/Framework Name] for predicting the occurrence of a composite adverse event endpoint within 30 days of patient admission.

#### 3.2. Secondary Objectives
- To assess the calibration of the model's risk predictions.
- To compare the model's performance against existing risk scoring systems (e.g., [Name of a standard score like SOFA or APACHE II]).
- To collect physician feedback on the usability and interpretability of the model's output.
- To analyze the incidence of specific adverse events within the cohort.

### 4. Study Design

This will be a prospective, multi-center, non-interventional, observational cohort study. A cohort of eligible patients will be enrolled, and data will be collected at baseline and during follow-up. The [Your Model/Framework Name] will be run in a "silent mode," where its predictions are recorded but not shown to the treating clinicians, to avoid influencing patient care.

- **Study Population:** Patients aged 18 years and older admitted to [Specify Ward, e.g., Intensive Care Units, General Medicine Wards] at participating hospitals.
- **Sample Size:** A sample size of approximately 2,000 patients is targeted, which will provide adequate statistical power to evaluate the primary endpoint. This will be confirmed with a formal power calculation.

### 5. Patient Inclusion and Exclusion Criteria

#### 5.1. Inclusion Criteria
- Adult patients (≥ 18 years of age).
- Admitted to a participating study center.
- Expected length of stay > 48 hours.
- Written informed consent provided by the patient or their legal representative.

#### 5.2. Exclusion Criteria
- Patients participating in another interventional clinical trial.
- Patients with a terminal condition where palliative care is the primary goal.
- Inability to obtain baseline data within 24 hours of admission.

### 6. Data Collection

Data will be collected from the Electronic Health Record (EHR) system.

- **Baseline Data:**
 - Demographics: Age, sex, ethnicity.
 - Vitals: Blood pressure, heart rate, respiratory rate, temperature.
 - Laboratory values: [Specify key labs, e.g., CBC, metabolic panel, inflammatory markers].
 - Comorbidities and admission diagnosis.
- **Follow-up Data (up to 30 days):**
 - Occurrence of the composite adverse event endpoint (e.g., mortality, ICU transfer, need for mechanical ventilation).
 - Length of hospital stay.
 - Discharge disposition.

### 7. Statistical Analysis Plan

- **Primary Endpoint Analysis:** The primary objective will be assessed by calculating the Area Under the Receiver Operating Characteristic Curve (AUC-ROC) for the model's prediction of the 30-day composite adverse event. A 95% confidence interval will be calculated.
- **Secondary Endpoint Analysis:**
 - Model calibration will be assessed using a calibration plot and the Hosmer-Lemeshow test.
 - The AUC-ROC of the [Your Model/Framework Name] will be compared to the standard risk score using the DeLong test.
 - Descriptive statistics will be used to summarize patient characteristics and outcomes.
 - Physician feedback will be analyzed qualitatively.

All analyses will be performed using Python or R. The full statistical analysis plan will be finalized before the database is locked.

---
*This document serves as a template. Specific details should be filled in based on the actual model and clinical context.*
