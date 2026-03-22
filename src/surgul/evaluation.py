"""
Statistical Evaluation and Metrics for SRGL

Provides comprehensive evaluation metrics, statistical tests, and confidence intervals
for validating SRGL performance.

Author: PhD Research Team
Date: 2026-01-09
"""

import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from statsmodels.stats.proportion import proportion_confint


class SafetyMetrics:
    """Calculate safety-critical metrics for triage systems"""

    def __init__(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        abstentions: Optional[np.ndarray] = None,
    ):
        """
        Initialize with predictions

        Args:
            y_true: Ground truth risk tiers (0-4)
            y_pred: Predicted risk tiers (0-4, or -1 for abstention)
            abstentions: Boolean array indicating abstentions
        """
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)

        if abstentions is None:
            self.abstentions = y_pred == -1
        else:
            self.abstentions = np.array(abstentions)

        self.non_abstain_mask = ~self.abstentions
        self.y_true_non_abstain = self.y_true[self.non_abstain_mask]
        self.y_pred_non_abstain = self.y_pred[self.non_abstain_mask]

    def sensitivity_critical(self, critical_threshold: int = 3) -> Dict:
        """
        Calculate sensitivity for critical cases (>= threshold)

        Primary safety metric: Must be 100% for SRGL
        """
        critical_mask = self.y_true >= critical_threshold
        n_critical = critical_mask.sum()

        if n_critical == 0:
            return {'sensitivity': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan}

        tp = ((self.y_pred >= critical_threshold) | self.abstentions)[
            critical_mask
        ].sum()
        fn = ((self.y_pred < critical_threshold) & ~self.abstentions)[
            critical_mask
        ].sum()

        sensitivity = tp / n_critical
        ci_lower, ci_upper = proportion_confint(tp, n_critical, method='wilson')

        return {
            'sensitivity': sensitivity,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n_critical': int(n_critical),
            'true_positives': int(tp),
            'false_negatives': int(fn),
        }

    def specificity_safe(self, safe_threshold: int = 1) -> Dict:
        """Calculate specificity for safe cases (< threshold)"""
        safe_mask = self.y_true < safe_threshold
        n_safe = safe_mask.sum()

        if n_safe == 0:
            return {'specificity': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan}

        tn = ((self.y_pred < safe_threshold) & ~self.abstentions)[safe_mask].sum()
        fp = ((self.y_pred >= safe_threshold) | self.abstentions)[safe_mask].sum()

        specificity = tn / n_safe if (tn + fp) > 0 else 0
        ci_lower, ci_upper = proportion_confint(tn, n_safe, method='wilson')

        return {
            'specificity': specificity,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n_safe': int(n_safe),
        }

    def abstention_rate(self) -> Dict:
        """Calculate abstention rate and coverage"""
        n_total = len(self.y_true)
        n_abstain = self.abstentions.sum()

        return {
            'abstention_rate': n_abstain / n_total,
            'n_abstentions': int(n_abstain),
            'n_total': n_total,
            'coverage': 1 - (n_abstain / n_total),
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Convert metrics to DataFrame"""
        metrics = [
            self.sensitivity_critical(),
            self.specificity_safe(),
            self.abstention_rate(),
        ]
        return pd.DataFrame(metrics)
