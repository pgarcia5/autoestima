"""
test_ml.py
----------
Tests end-to-end del pipeline de Machine Learning d'AutoEstima.
Cobreix SCRUM-24 — Testing.
"""

import pytest
import pandas as pd
import numpy as np
import joblib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ml.preprocess import clean_data, normalize_data, prepare_features
from ml.evaluate import evaluate_model


@pytest.fixture
def sample_df():
    """DataFrame mínim per testejar el pipeline."""
    return pd.DataFrame({
        "price":      [15000, 8000, 25000, 3000, 45000] * 10,
        "make":       ["volkswagen", "seat", "audi", "renault", "bmw"] * 10,
        "model":      ["golf", "ibiza", "a4", "clio", "320"] * 10,
        "fuel_type":  ["diesel", "gasoline", "diesel", "gasoline", "diesel"] * 10,
        "gear_type":  ["manual", "manual", "automatic", "manual", "automatic"] * 10,
        "sale_type":  ["used", "used", "km_0", "used", "almost_new"] * 10,
        "months_old": [36, 24, 12, 72, 18] * 10,
        "power":      [110, 90, 150, 75, 190] * 10,
        "kms":        [45000, 30000, 10000, 90000, 20000] * 10,
        "num_owners": [1, 2, 1, 3, 1] * 10,
    })


class TestPreprocess:

    def test_clean_data_removes_price_outliers(self, sample_df):
        sample_df.loc[0, "price"] = 1
        sample_df.loc[1, "price"] = 999999
        df_clean = clean_data(sample_df)
        assert df_clean["price"].min() >= 500
        assert df_clean["price"].max() <= 200000

    def test_clean_data_removes_km_outliers(self, sample_df):
        sample_df.loc[0, "kms"] = 700000
        df_clean = clean_data(sample_df)
        assert df_clean["kms"].max() <= 600000

    def test_clean_data_fills_nulls(self, sample_df):
        sample_df.loc[0, "num_owners"] = np.nan
        sample_df.loc[1, "gear_type"] = np.nan
        df_clean = clean_data(sample_df)
        assert df_clean["num_owners"].isnull().sum() == 0
        assert df_clean["gear_type"].isnull().sum() == 0

    def test_normalize_data_lowercase(self, sample_df):
        sample_df["make"] = sample_df["make"].str.upper()
        df_norm = normalize_data(sample_df)
        assert df_norm["make"].str.islower().all()

    def test_normalize_data_types(self, sample_df):
        df_norm = normalize_data(sample_df)
        assert df_norm["price"].dtype == int
        assert df_norm["kms"].dtype == int

    def test_prepare_features_shape(self, sample_df):
        X, y = prepare_features(sample_df)
        assert len(X) == len(y)
        assert "months_old" in X.columns
        assert "power" in X.columns
        assert "kms" in X.columns

    def test_prepare_features_no_nulls(self, sample_df):
        X, y = prepare_features(sample_df)
        assert X.isnull().sum().sum() == 0


class TestEvaluate:

    def test_evaluate_model_returns_metrics(self, sample_df):
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        X, y = prepare_features(sample_df)
        pipeline = Pipeline([("scaler", StandardScaler()), ("model", RandomForestRegressor(n_estimators=10, random_state=42))])
        pipeline.fit(X, y)
        metrics = evaluate_model(pipeline, X, y)
        assert "mae" in metrics and "rmse" in metrics and "r2" in metrics
        assert metrics["mae"] >= 0

    def test_evaluate_model_r2_reasonable(self, sample_df):
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        X, y = prepare_features(sample_df)
        pipeline = Pipeline([("scaler", StandardScaler()), ("model", RandomForestRegressor(n_estimators=50, random_state=42))])
        pipeline.fit(X, y)
        metrics = evaluate_model(pipeline, X, y)
        assert metrics["r2"] > 0.5


class TestSavedModel:

    def test_model_file_exists(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'best_model.pkl')
        assert os.path.exists(model_path), "best_model.pkl no trobat!"

    def test_model_predicts_positive_price(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'best_model.pkl')
        if not os.path.exists(model_path):
            pytest.skip("Model no disponible")
        model = joblib.load(model_path)
        data = {"make": "volkswagen", "fuel_type": "diesel", "gear_type": "manual",
                "sale_type": "used", "months_old": 36, "power": 110, "kms": 50000, "num_owners": 1}
        df = pd.DataFrame([data])
        df_enc = pd.get_dummies(df, columns=["make", "fuel_type", "gear_type", "sale_type"])
        for col in model.feature_names_in_:
            if col not in df_enc.columns:
                df_enc[col] = 0
        df_enc = df_enc[model.feature_names_in_]
        pred = model.predict(df_enc)[0]
        assert 0 < pred < 200000


class TestFlaskApp:

    @pytest.fixture
    def client(self):
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web'))
        try:
            from app import app
            app.config["TESTING"] = True
            with app.test_client() as client:
                yield client
        except Exception:
            pytest.skip("No es pot carregar l'app Flask")

    def test_index_loads(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"AutoEstima" in response.data

    def test_predict_valid(self, client):
        response = client.post("/predict", data={
            "make": "volkswagen", "fuel_type": "diesel", "gear_type": "manual",
            "sale_type": "used", "months_old": "36", "power": "110",
            "kms": "50000", "num_owners": "1"
        })
        assert response.status_code == 200
        assert response.get_json()["success"] is True

    def test_predict_missing_fields(self, client):
        response = client.post("/predict", data={"make": "volkswagen"})
        assert response.status_code == 400

    def test_budget_valid(self, client):
        response = client.post("/budget", data={"price_min": "5000", "price_max": "15000"})
        assert response.status_code == 200
        assert response.get_json()["success"] is True

    def test_budget_invalid_range(self, client):
        response = client.post("/budget", data={"price_min": "15000", "price_max": "5000"})
        assert response.status_code == 400

    def test_articles_load(self, client):
        for i in range(1, 5):
            assert client.get(f"/article/{i}").status_code == 200

    def test_article_not_found(self, client):
        assert client.get("/article/99").status_code == 404

    def test_cotxes_load(self, client):
        for i in range(1, 5):
            assert client.get(f"/cotxe/{i}").status_code == 200
