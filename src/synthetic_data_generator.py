import numpy as np
import pandas as pd


def generate_syndx_like_data(
    n_samples: int = 1000,
    base_age: int = 55,
    base_bmi: float = 28.0,
    noise_level: float = 0.5,
):
    """
    Generates a synthetic dataset mimicking clinical trial data, based on the conceptual principles of SynDX.

    This function creates a dataset with demographic information, simulated vitals,
    lab results, and a binary outcome. The relationships between variables are
    intentionally modeled to provide a basis for statistical analysis and visualization.

    Args:
    n_samples (int): The number of patients (rows) to generate.
    base_age (int): The mean age of the patient cohort.
    base_bmi (float): The mean BMI of the patient cohort.
    noise_level (float): The amount of random noise to add to the measurements,
    controlling data "messiness".

    Returns:
    pd.DataFrame: A pandas DataFrame containing the synthetic patient data.
    Columns include:
    - 'patient_id': Unique identifier for each patient.
    - 'age': Age of the patient.
    - 'sex': Sex of the patient (0 for female, 1 for male).
    - 'bmi': Body Mass Index.
    - 'systolic_bp': Systolic blood pressure.
    - 'diastolic_bp': Diastolic blood pressure.
    - 'cholesterol': Cholesterol level.
    - 'adverse_event': Binary outcome (e.g., 1 for an adverse event, 0 otherwise).
    """
    np.random.seed(42)  # for reproducibility

    # 1. Generate Demographics
    age = np.random.normal(loc=base_age, scale=10, size=n_samples).astype(int)
    sex = np.random.randint(0, 2, size=n_samples)  # 0: Female, 1: Male
    bmi = np.random.normal(loc=base_bmi, scale=5, size=n_samples)

    # 2. Generate Vitals and Labs with controlled relationships
    # Blood pressure is slightly correlated with age and BMI
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

    # Cholesterol is correlated with age, bmi, and sex
    cholesterol = (
        200
        + 0.8 * (age - base_age)
        + 2.0 * (bmi - base_bmi)
        + 5 * sex
        + np.random.normal(0, 20 * noise_level, n_samples)
    )

    # 3. Generate a Binary Outcome
    # The probability of an adverse event increases with age, BMI, and cholesterol
    log_odds = (
        -5
        + 0.05 * (age - base_age)
        + 0.1 * (bmi - base_bmi)
        + 0.01 * (cholesterol - 200)
    )
    probability = 1 / (1 + np.exp(-log_odds))
    adverse_event = np.random.binomial(1, probability, size=n_samples)

    # 4. Assemble DataFrame
    df = pd.DataFrame(
        {
            'patient_id': [f'PID_{{i+1:04d}}' for i in range(n_samples)],
            'age': age,
            'sex': sex,
            'bmi': bmi.round(2),
            'systolic_bp': systolic_bp.round(0).astype(int),
            'diastolic_bp': diastolic_bp.round(0).astype(int),
            'cholesterol': cholesterol.round(2),
            'adverse_event': adverse_event,
        }
    )

    # Clip to realistic values
    df['age'] = df['age'].clip(18, 100)
    df['bmi'] = df['bmi'].clip(15, 60)
    df['systolic_bp'] = df['systolic_bp'].clip(80, 220)
    df['diastolic_bp'] = df['diastolic_bp'].clip(50, 130)
    df['cholesterol'] = df['cholesterol'].clip(100, 400)

    return df


if __name__ == '__main__':
    # Example of how to use the generator
    synthetic_data = generate_syndx_like_data(n_samples=50)
    print("Generated Synthetic Data (First 5 Rows):")
    print(synthetic_data.head())
    print("\nData Info:")
    synthetic_data.info()
    print("\nData Description:")
    print(synthetic_data.describe())
