"""
train.py
--------
Model training scripts for AutoEstima.
Trains: Linear Regression, Random Forest, Gradient Boosting.
"""

import logging
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from ml.preprocess import load_data, clean_data, normalize_data, prepare_features
from ml.evaluate import evaluate_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

MODEL_PATH = "models/best_model.pkl"


def get_models() -> dict:
    """
    Define the models to train inside Pipelines.
    Each pipeline scales numerics and then applies the model.

    Returns:
        Dict of model name -> Pipeline.
    """
    return {
        "LinearRegression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "RandomForest": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                n_jobs=-1
            ))
        ]),
        "GradientBoosting": Pipeline([
            ("scaler", StandardScaler()),
            ("model", GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            ))
        ]),
    }


def train_and_evaluate(X, y) -> dict:
    """
    Train and evaluate all models.

    Args:
        X: Feature matrix.
        y: Target vector.

    Returns:
        Dict with results per model.
    """
    # Split 80% train / 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train: {X_train.shape[0]} rows | Test: {X_test.shape[0]} rows")

    models = get_models()
    results = {}

    for name, pipeline in models.items():
        logger.info(f"Training {name}...")
        pipeline.fit(X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test)
        results[name] = {"pipeline": pipeline, "metrics": metrics}
        logger.info(f"{name} → MAE: {metrics['mae']:.0f}€ | RMSE: {metrics['rmse']:.0f}€ | R²: {metrics['r2']:.3f}")

    return results, X_test, y_test


def select_best_model(results: dict) -> tuple:
    """
    Select the best model based on R² score.

    Args:
        results: Dict with model results.

    Returns:
        Tuple (best_name, best_pipeline).
    """
    best_name = max(results, key=lambda k: results[k]["metrics"]["r2"])
    best_pipeline = results[best_name]["pipeline"]
    logger.info(f"Best model: {best_name} (R²={results[best_name]['metrics']['r2']:.3f})")
    return best_name, best_pipeline


def save_model(pipeline, filepath: str = MODEL_PATH) -> None:
    """
    Serialize and save the best model.

    Args:
        pipeline: Trained sklearn Pipeline.
        filepath: Destination path.
    """
    joblib.dump(pipeline, filepath)
    logger.info(f"Model saved to {filepath}")


if __name__ == "__main__":
    # 1. Carregar i preparar dades
    df = load_data()
    df = clean_data(df)
    df = normalize_data(df)
    X, y = prepare_features(df)

    # 2. Entrenar i avaluar
    results, X_test, y_test = train_and_evaluate(X, y)

    # 3. Mostrar resultats comparatius
    print("\n📊 Resultats dels models:")
    print(f"{'Model':<25} {'MAE (€)':>10} {'RMSE (€)':>10} {'R²':>8}")
    print("-" * 55)
    for name, data in results.items():
        m = data["metrics"]
        print(f"{name:<25} {m['mae']:>10.0f} {m['rmse']:>10.0f} {m['r2']:>8.3f}")

    # 4. Guardar el millor model
    best_name, best_pipeline = select_best_model(results)
    save_model(best_pipeline)
    print(f"\n✅ Best model: {best_name} → saved to {MODEL_PATH}")
