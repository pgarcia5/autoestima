"""
preprocess.py
-------------
Data cleaning and feature engineering for ML pipeline.
Covers SCRUM-9 (clean) and SCRUM-10 (normalize).
"""

import logging
import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

RAW_PATH = "data/raw/coches_raw.csv"
PROCESSED_PATH = "data/processed/coches_processed.csv"

# Preu màxim i mínim raonables (€)
PRICE_MIN = 500
PRICE_MAX = 200000

# Quilometratge màxim raonable
KMS_MAX = 600000


def load_data(filepath: str = RAW_PATH) -> pd.DataFrame:
    """
    Load raw CSV data.

    Args:
        filepath: Path to the raw CSV file.

    Returns:
        Raw DataFrame.
    """
    df = pd.read_csv(filepath, sep=";", encoding="utf-8", on_bad_lines="skip")
    logger.info(f"Loaded {len(df)} rows from {filepath}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data:
    - Remove irrelevant columns
    - Filter price outliers
    - Filter km outliers
    - Drop rows with too many nulls

    Args:
        df: Raw DataFrame.

    Returns:
        Cleaned DataFrame.
    """
    initial_rows = len(df)

    # 1. Eliminar columnes inútils per al model
    df = df.drop(columns=["ID", "version"], errors="ignore")
    logger.info("Dropped columns: ID, version")

    # 2. Filtrar preus outliers
    df = df[(df["price"] >= PRICE_MIN) & (df["price"] <= PRICE_MAX)]
    logger.info(f"After price filter: {len(df)} rows")

    # 3. Filtrar km outliers
    df = df[df["kms"] <= KMS_MAX]
    logger.info(f"After km filter: {len(df)} rows")

    # 4. Eliminar files sense preu, marca o model (camps crítics)
    df = df.dropna(subset=["price", "make", "model"])
    logger.info(f"After dropping critical nulls: {len(df)} rows")

    # 5. num_owners té molts nulls (71k) — l'omplim amb la mediana
    df["num_owners"] = df["num_owners"].fillna(df["num_owners"].median())

    # 6. gear_type, fuel_type, sale_type: omplir amb la moda
    for col in ["gear_type", "fuel_type", "sale_type"]:
        df[col] = df[col].fillna(df[col].mode()[0])

    # 7. months_old i power: omplir amb la mediana
    for col in ["months_old", "power"]:
        df[col] = df[col].fillna(df[col].median())

    # 8. Eliminar duplicats
    df = df.drop_duplicates()

    removed = initial_rows - len(df)
    logger.info(f"Cleaning complete. Removed {removed} rows. Final: {len(df)} rows")

    return df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize data types:
    - Convert columns to correct types
    - Standardize string values

    Args:
        df: Cleaned DataFrame.

    Returns:
        Normalized DataFrame.
    """
    # Tipus numèrics
    df["price"] = df["price"].astype(int)
    df["kms"] = df["kms"].astype(int)
    df["months_old"] = df["months_old"].astype(int)
    df["power"] = df["power"].astype(int)
    df["num_owners"] = df["num_owners"].astype(int)

    # Strings en minúscules i sense espais
    for col in ["make", "model", "fuel_type", "gear_type", "sale_type"]:
        df[col] = df[col].str.strip().str.lower()

    logger.info("Data types normalized.")
    return df


def save_processed(df: pd.DataFrame, filepath: str = PROCESSED_PATH) -> None:
    """
    Save processed DataFrame to CSV.

    Args:
        df: Processed DataFrame.
        filepath: Destination path.
    """
    df.to_csv(filepath, index=False, encoding="utf-8")
    logger.info(f"Saved {len(df)} rows to {filepath}")


def prepare_features(df: pd.DataFrame):
    """
    Feature engineering for ML:
    - One-Hot Encoding for categorical variables
    - Returns X (features) and y (target)

    Args:
        df: Processed DataFrame.

    Returns:
        Tuple (X, y) ready for ML training.
    """
    # Target
    y = df["price"]

    # Features
    feature_cols = [
        "make", "fuel_type", "gear_type", "sale_type",  # categòriques
        "months_old", "power", "kms", "num_owners"       # numèriques
    ]
    X = df[feature_cols].copy()

    # One-Hot Encoding de les categòriques
    categorical_cols = ["make", "fuel_type", "gear_type", "sale_type"]
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=False)

    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")

    return X, y


if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    df = normalize_data(df)
    save_processed(df)

    X, y = prepare_features(df)

    print("\n✅ Dataset processed!")
    print(f"Shape: {df.shape}")
    print(f"Features: {X.shape[1]} columnes")
    print(f"\nPrice stats:\n{df['price'].describe()}")
    print(f"\nNull values:\n{df.isnull().sum()}")
    print(f"\nSample features:\n{X.head(3)}")
