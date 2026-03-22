"""Tabular synthetic data generator for packaged SURgul workflows."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_syndx_like_data(
    n_samples: int = 1000,
    base_age: int = 55,
    base_bmi: float = 28.0,
    noise_level: float = 0.5,
) -> pd.DataFrame:
    """Generate a simple synthetic clinical dataset for visualization and testing."""
    np.random.seed(42)

    age = np.random.normal(loc=base_age, scale=10, size=n_samples).astype(int)
    sex = np.random.randint(0, 2, size=n_samples)
    bmi = np.random.normal(loc=base_bmi, scale=5, size=n_samples)

    systolic_bp = (
        120
        + 0.5 * (age - base_age)
        + 1.5 * (bmi - base_bmi)
        + np.random.normal(0, 15 * noise_level, n_samples)
    )
    diastolic_bp = (
        80
        + 0.2 * (age - base_age)
        + 0.5 * (bmi - base_bmi)
        + np.random.normal(0, 10 * noise_level, n_samples)
    )
    cholesterol = (
        200
        + 0.8 * (age - base_age)
        + 2.0 * (bmi - base_bmi)
        + 5 * sex
        + np.random.normal(0, 20 * noise_level, n_samples)
    )

    log_odds = (
        -5
        + 0.05 * (age - base_age)
        + 0.1 * (bmi - base_bmi)
        + 0.01 * (cholesterol - 200)
    )
    probability = 1 / (1 + np.exp(-log_odds))
    adverse_event = np.random.binomial(1, probability, size=n_samples)

    dataframe = pd.DataFrame(
        {
            "patient_id": [f"PID_{index + 1:04d}" for index in range(n_samples)],
            "age": age,
            "sex": sex,
            "bmi": bmi.round(2),
            "systolic_bp": systolic_bp.round(0).astype(int),
            "diastolic_bp": diastolic_bp.round(0).astype(int),
            "cholesterol": cholesterol.round(2),
            "adverse_event": adverse_event,
        }
    )

    dataframe["age"] = dataframe["age"].clip(18, 100)
    dataframe["bmi"] = dataframe["bmi"].clip(15, 60)
    dataframe["systolic_bp"] = dataframe["systolic_bp"].clip(80, 220)
    dataframe["diastolic_bp"] = dataframe["diastolic_bp"].clip(50, 130)
    dataframe["cholesterol"] = dataframe["cholesterol"].clip(100, 400)
    return dataframe
