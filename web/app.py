"""
app.py
------
Flask web application for AutoEstima.
"""

import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MODEL_PATH = "models/best_model.pkl"
DATA_PATH = "data/processed/coches_processed.csv"

model = joblib.load(MODEL_PATH)
df_data = pd.read_csv(DATA_PATH)

FUEL_TYPES = ["diesel", "gasoline", "hybrid", "electric", "LPG"]
GEAR_TYPES = ["manual", "automatic", "semi-automatic"]
SALE_TYPES = ["used", "km_0", "almost_new", "demo", "new"]

MAKES = [
    "audi", "bmw", "chevrolet", "citroen", "dacia", "fiat", "ford",
    "honda", "hyundai", "jaguar", "jeep", "kia", "land rover", "lexus",
    "mazda", "mercedes-benz", "mini", "mitsubishi", "nissan", "opel",
    "peugeot", "porsche", "renault", "seat", "skoda", "smart",
    "subaru", "suzuki", "tesla", "toyota", "volkswagen", "volvo"
]

MOTOS = [
    {"make": "Honda", "model": "CB500F", "year": 2020, "kms": 18500, "price": 5500, "engine": 471, "power": 47, "type": "Naked"},
    {"make": "Yamaha", "model": "MT-07", "year": 2021, "kms": 12000, "price": 7200, "engine": 689, "power": 73, "type": "Naked"},
    {"make": "Kawasaki", "model": "Z650", "year": 2019, "kms": 22000, "price": 5800, "engine": 649, "power": 68, "type": "Naked"},
    {"make": "BMW", "model": "F 800 GS", "year": 2018, "kms": 35000, "price": 6900, "engine": 798, "power": 85, "type": "Adventure"},
    {"make": "Ducati", "model": "Monster 797", "year": 2020, "kms": 9800, "price": 8500, "engine": 803, "power": 73, "type": "Naked"},
    {"make": "Suzuki", "model": "GSX-S750", "year": 2019, "kms": 28000, "price": 6200, "engine": 749, "power": 114, "type": "Naked"},
    {"make": "KTM", "model": "Duke 790", "year": 2021, "kms": 8500, "price": 8900, "engine": 799, "power": 105, "type": "Naked"},
    {"make": "Triumph", "model": "Street Triple", "year": 2020, "kms": 14000, "price": 9500, "engine": 765, "power": 118, "type": "Naked"},
]

NEWS = [
    {
        "category": "Mercat",
        "icon": "🔋",
        "title": "Nou rècord de vendes de vehicles elèctrics",
        "desc": "Les matriculacions de vehicles elèctrics han batut tots els rècords europeus aquest trimestre.",
        "date": "18 Abr 2026",
        "color": "green"
    },
    {
        "category": "Competició",
        "icon": "🏎️",
        "title": "Formula E presenta el nou xassís Gen4",
        "desc": "El nou monoplaces elèctric promet un 30% més de potència i millor aerodinàmica.",
        "date": "17 Abr 2026",
        "color": "blue"
    },
    {
        "category": "Legislació",
        "icon": "🌍",
        "title": "Europa aprova noves normatives d'emissions",
        "desc": "La UE endureix els límits de CO₂ per a vehicles nous a partir del 2027.",
        "date": "15 Abr 2026",
        "color": "orange"
    },
    {
        "category": "Tecnologia",
        "icon": "⚙️",
        "title": "Nissan anuncia inversió en bateries sòlides",
        "desc": "La marca japonesa invertirà 3.000 milions en la nova tecnologia de bateries sòlides.",
        "date": "14 Abr 2026",
        "color": "purple"
    },
]

NEW_CARS = [
    {"name": "BMW M4 Competition", "category": "Esportiu", "year": "2026", "icon": "🏎️"},
    {"name": "Tesla Model Y", "category": "Elèctric", "year": "2026", "icon": "⚡"},
    {"name": "Audi e-tron GT", "category": "Elèctric", "year": "2026", "icon": "🔋"},
    {"name": "Porsche 911 Turbo", "category": "Esportiu", "year": "2026", "icon": "🏁"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        makes=MAKES,
        fuel_types=FUEL_TYPES,
        gear_types=GEAR_TYPES,
        sale_types=SALE_TYPES,
        news=NEWS,
        new_cars=NEW_CARS,
        motos=MOTOS,
    )


import requests as req

@app.route("/img-proxy")
def img_proxy():
    """Proxy per carregar imatges externes evitant bloquejos CORS."""
    url = request.args.get("url")
    if not url:
        return "", 400
    try:
        headers = {"User-Agent": "Mozilla/5.0 AutoEstima/1.0"}
        r = req.get(url, headers=headers, timeout=8, stream=True)
        from flask import Response
        return Response(
            r.content,
            content_type=r.headers.get("Content-Type", "image/jpeg")
        )
    except Exception:
        return "", 404


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = {
            "make": request.form.get("make"),
            "fuel_type": request.form.get("fuel_type"),
            "gear_type": request.form.get("gear_type"),
            "sale_type": request.form.get("sale_type"),
            "months_old": int(request.form.get("months_old")),
            "power": int(request.form.get("power")),
            "kms": int(request.form.get("kms")),
            "num_owners": int(request.form.get("num_owners")),
        }

        df_input = pd.DataFrame([data])
        df_encoded = pd.get_dummies(df_input, columns=["make", "fuel_type", "gear_type", "sale_type"])

        model_features = model.feature_names_in_
        for col in model_features:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[model_features]

        prediction = model.predict(df_encoded)[0]
        prediction = max(0, round(prediction / 100) * 100)

        MAE = 2183
        price_low = max(0, round((prediction - MAE) / 100) * 100)
        price_high = round((prediction + MAE) / 100) * 100

        def fmt(p):
            return f"{int(p):,}".replace(",", ".") + " €"

        return jsonify({
            "success": True,
            "price": int(prediction),
            "price_formatted": fmt(prediction),
            "price_low": fmt(price_low),
            "price_high": fmt(price_high),
            "price_low_raw": int(price_low),
            "price_high_raw": int(price_high),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/similar")
def similar():
    make = request.args.get("make", "")
    fuel = request.args.get("fuel", "")
    price_low = int(request.args.get("price_low", 0))
    price_high = int(request.args.get("price_high", 999999))
    predicted = int(request.args.get("predicted", 0))

    filtered = df_data[
        (df_data["make"] == make.lower()) &
        (df_data["fuel_type"] == fuel.lower()) &
        (df_data["price"] >= price_low) &
        (df_data["price"] <= price_high)
    ].copy()

    if len(filtered) < 6:
        margin = (price_high - price_low)
        filtered = df_data[
            (df_data["make"] == make.lower()) &
            (df_data["price"] >= max(0, price_low - margin)) &
            (df_data["price"] <= price_high + margin)
        ].copy()

    filtered["price_diff"] = abs(filtered["price"] - predicted)
    filtered = filtered.sort_values("price_diff").head(12)
    cars = filtered.to_dict(orient="records")

    return render_template(
        "similar.html",
        cars=cars,
        make=make,
        fuel=fuel,
        predicted=predicted,
        price_low=price_low,
        price_high=price_high,
        count=len(cars),
    )


@app.route("/budget", methods=["POST"])
def budget_search():
    try:
        price_min = int(request.form.get("price_min"))
        price_max = int(request.form.get("price_max"))

        if price_min >= price_max:
            return jsonify({"success": False, "error": "El preu mínim ha de ser menor que el màxim."}), 400

        filtered = df_data[(df_data["price"] >= price_min) & (df_data["price"] <= price_max)]

        if len(filtered) < 5:
            return jsonify({"success": False, "error": "No hi ha prou dades per a aquest rang de preu."}), 400

        top_makes = filtered["make"].value_counts().head(5).to_dict()
        top_fuels = filtered["fuel_type"].value_counts().head(3).to_dict()

        return jsonify({
            "success": True,
            "count": len(filtered),
            "avg_kms": int(filtered["kms"].mean()),
            "avg_months": int(filtered["months_old"].mean()),
            "avg_power": int(filtered["power"].mean()),
            "avg_price": int(filtered["price"].mean()),
            "top_makes": [{"name": k.title(), "count": v} for k, v in top_makes.items()],
            "top_fuels": [{"name": k.title(), "count": v} for k, v in top_fuels.items()],
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
