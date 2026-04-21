"""
evaluate.py
-----------
Model evaluation and metrics.
"""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(pipeline, X_test, y_test) -> dict:
    """
    Evaluate model performance.

    Args:
        pipeline: Trained sklearn Pipeline.
        X_test: Test features.
        y_test: Test target.

    Returns:
        Dict with MAE, RMSE and R2 scores.
    """
    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    }
