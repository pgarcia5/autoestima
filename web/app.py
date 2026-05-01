"""
app.py
------
Flask web application for AutoEstima.
"""

import os
import joblib
import pandas as pd
import requests as req
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

# Rutes relatives al directori on s'executa app.py (web/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "processed", "coches_processed.csv")

model   = joblib.load(MODEL_PATH)
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
    {"make": "Honda",   "model": "CB500F",        "year": 2020, "kms": 18500, "price": 5500, "engine": 471, "power":  47, "type": "Naked",     "img": "/static/img/CB500F.jpg"},
    {"make": "Yamaha",  "model": "MT-07",          "year": 2021, "kms": 12000, "price": 7200, "engine": 689, "power":  73, "type": "Naked",     "img": "/static/img/M7-07.jpg"},
    {"make": "Kawasaki","model": "Z650",           "year": 2019, "kms": 22000, "price": 5800, "engine": 649, "power":  68, "type": "Naked",     "img": "/static/img/Z650.jpg"},
    {"make": "BMW",     "model": "F 800 GS",       "year": 2018, "kms": 35000, "price": 6900, "engine": 798, "power":  85, "type": "Adventure", "img": "/static/img/F800.jpg"},
    {"make": "Ducati",  "model": "Monster 797",    "year": 2020, "kms":  9800, "price": 8500, "engine": 803, "power":  73, "type": "Naked",     "img": "/static/img/797.jpg"},
    {"make": "Suzuki",  "model": "GSX-S750",       "year": 2019, "kms": 28000, "price": 6200, "engine": 749, "power": 114, "type": "Naked",     "img": "/static/img/S750.jpg"},
    {"make": "KTM",     "model": "Duke 790",       "year": 2021, "kms":  8500, "price": 8900, "engine": 799, "power": 105, "type": "Naked",     "img": "/static/img/790.jpg"},
    {"make": "Triumph", "model": "Street Triple",  "year": 2020, "kms": 14000, "price": 9500, "engine": 765, "power": 118, "type": "Naked",     "img": "/static/img/765.jpg"},
]

def moto_links(make, model):
    """Genera enllaços de cerca a plataformes de segona mà."""
    query = f"{make} {model}".replace(" ", "+")
    query_wallapop = f"{make}+{model}".replace(" ", "+")
    return {
        "motosnet": f"https://www.motos.net/motos/segunda-mano/?q={query}",
        "milanuncios": f"https://www.milanuncios.com/motos-de-segunda-mano/?q={query}",
        "wallapop": f"https://es.wallapop.com/app/search?keywords={query_wallapop}&category_ids=14000",
    }

for m in MOTOS:
    m["links"] = moto_links(m["make"], m["model"])

NEWS = [
    {
        "id": 1,
        "category": "Mercat",
        "image": "/static/img/noticia1.jpg",
        "title": "Nou rècord de vendes de vehicles elèctrics",
        "desc": "Les matriculacions de vehicles elèctrics han batut tots els rècords europeus aquest trimestre.",
        "date": "18 Abr 2026",
        "color": "green",
        "body": [
            "Les matriculacions de vehicles elèctrics a Europa han assolit un nou rècord històric durant el primer trimestre de 2026, amb un increment del 34% respecte al mateix període de l'any anterior. Segons les dades publicades per l'Associació Europea de Fabricants d'Automòbils (ACEA), s'han registrat més de 850.000 unitats elèctriques en tot el continent.",
            "## Els mercats més dinàmics",
            "Noruega continua liderant la transició elèctrica amb una quota de mercat del 92%, seguida pels Països Baixos amb un 68% i Suècia amb un 54%. Espanya, tot i partir d'una base més baixa, ha registrat un creixement espectacular del 61% interanual, impulsada pels ajuts del Pla MOVES III i la millora de la xarxa de recàrrega.",
            "## Factors clau del creixement",
            "Els experts atribueixen aquest creixement a tres factors principals: la reducció del preu de les bateries, que ha permès als fabricants oferir models elèctrics competitius per sota dels 25.000€; l'ampliació de la xarxa de càrrega ràpida a les autopistes europees; i l'entrada de nous models accessibles per part de marques com Dacia, Citroën i Volkswagen.",
            "## Impacte en el mercat de segona mà",
            "Aquest boom elèctric també comença a notar-se en el mercat de vehicles de segona mà. Els cotxes elèctrics d'ocasió han augmentat un 120% en oferta durant l'últim any, tot i que els preus encara es mantenen per sobre dels vehicles de combustió equivalents. Els analistes preveuen que la paritat de preus en el mercat d'ocasió s'assolirà cap al 2028.",
        ]
    },
    {
        "id": 2,
        "category": "Competició",
        "image": "/static/img/noticia2.jpg",
        "title": "Formula E presenta el nou xassís Gen4",
        "desc": "El nou monoplaces elèctric promet un 30% més de potència i millor aerodinàmica.",
        "date": "17 Abr 2026",
        "color": "blue",
        "body": [
            "La Fórmula E ha presentat oficialment el seu nou monoplaça de quarta generació, el Gen4, que competirà a partir de la temporada 2027. El nou vehicle suposa un salt tecnològic significatiu respecte al seu predecessor, amb una potència màxima de 350 kW en mode atac i una millora del 30% en l'eficiència energètica.",
            "## Especificacions tècniques",
            "El Gen4 incorpora una bateria de nova generació amb una capacitat de 54 kWh, un 20% superior a l'actual, que permetrà completar les curses sense necessitat de canviar de vehicle a meitat de carrera. La velocitat màxima s'eleva fins als 340 km/h.",
            "## Aerodinàmica revolucionària",
            "El disseny aerodinàmic ha estat desenvolupat conjuntament amb la NASA i el Centre de Recerca Aeronàutica Alemany (DLR). Les noves ales actives s'adapten automàticament a les condicions de la pista. El coeficient de resistència aerodinàmica (Cx) s'ha reduït un 18%.",
            "## Resposta dels equips",
            "Tots els equips participants han mostrat el seu entusiasme pel nou reglament tècnic. Porsche, que lidera el campionat actual, ha declarat que el Gen4 representa el futur de la competició elèctrica. Nissan i DS Automobiles ja treballen en els seus nous powertrains específics per al nou xassís.",
        ]
    },
    {
        "id": 3,
        "category": "Legislació",
        "image": "/static/img/noticia3.jpg",
        "title": "Europa aprova noves normatives d'emissions",
        "desc": "La UE endureix els límits de CO₂ per a vehicles nous a partir del 2027.",
        "date": "15 Abr 2026",
        "color": "orange",
        "body": [
            "El Parlament Europeu ha aprovat definitivament el nou reglament d'emissions Euro 7+, que entrarà en vigor el gener de 2027 per als turismes i furgonetes lleugers. La nova normativa redueix els límits de CO₂ fins als 50 g/km de mitjana per a la flota de cada fabricant, la meitat dels 95 g/km actuals del Euro 6.",
            "## Sancions més severes",
            "Un dels canvis més destacats és l'enduriment de les sancions per incompliment. Els fabricants que superin els límits establerts hauran de pagar una multa de 150€ per gram de CO₂ per vehicle venut, enfront dels 95€ actuals. S'estima que les multes podrien superar els 14.000 milions d'euros anuals si la indústria no s'adapta a temps.",
            "## Impacte en els fabricants",
            "Les marques europees han reaccionat de forma diversa. Volkswagen i Stellantis han anunciat acceleració en els seus plans d'electrificació, mentre que alguns fabricants de vehicles de luxe han sol·licitat períodes de transició addicionals per als seus models d'alta gamma.",
            "## Conseqüències per als consumidors",
            "Experts del sector preveuen que la nova normativa accelerarà la reducció de preus dels vehicles elèctrics, ja que els fabricants necessitaran augmentar les seves quotes d'electrificació.",
        ]
    },
    {
        "id": 4,
        "category": "Tecnologia",
        "image": "/static/img/noticia4.jpg",
        "title": "Nissan anuncia inversió en bateries sòlides",
        "desc": "La marca japonesa invertirà 3.000 milions en la nova tecnologia de bateries sòlides.",
        "date": "14 Abr 2026",
        "color": "purple",
        "body": [
            "Nissan ha anunciat una inversió de 3.000 milions d'euros per accelerar el desenvolupament i la producció en massa de bateries d'estat sòlid, una tecnologia que promet revolucionar el sector dels vehicles elèctrics. La companyia japonesa preveu incorporar aquesta tecnologia als seus vehicles de producció a partir de 2028.",
            "## Avantatges de les bateries sòlides",
            "Les bateries d'estat sòlid substitueixen l'electròlit líquid de les bateries d'ions de liti convencionals per un material sòlid. Nissan destaca que els seus prototips aconsegueixen una densitat energètica un 50% superior, temps de càrrega de menys de 15 minuts i una vida útil de més de 1.000 cicles sense degradació significativa.",
            "## Pla d'implementació",
            "La inversió es distribuirà entre tres àrees principals: investigació i desenvolupament a Yokohama, construcció d'una nova planta pilot a Kyushu i col·laboració amb proveïdors de materials sòlids a Europa i Amèrica del Nord.",
            "## Competència tecnològica",
            "Nissan no és l'únic fabricant que aposta per aquesta tecnologia. Toyota ha anunciat que vol ser el primer a comercialitzar-les el 2027. Samsung SDI i CATL també han augmentat significativament les seves inversions en aquest camp.",
        ]
    },
]

NEW_CARS = [
    {
        "id": 1,
        "name": "BMW M4 Competition",
        "category": "Esportiu",
        "year": "2026",
        "icon": "🏎️",
        "img": "/static/img/nou1.jpg",
        "price": "97.800 €",
        "motor": "3.0L Biturbo de 6 cilindres",
        "power": "510 CV",
        "torque": "650 Nm",
        "acceleration": "3,9 s (0-100 km/h)",
        "top_speed": "290 km/h",
        "transmission": "Automàtica 8 velocitats (M Steptronic)",
        "traction": "Tracció posterior (xDrive disponible)",
        "desc": "El BMW M4 Competition 2026 representa la cúspide de la tradició esportiva de BMW. Dissenyat per oferir un equilibri perfecte entre rendiment en circuit i usabilitat diària, incorpora la nova suspensió adaptativa M de tercera generació i el sistema de direcció activa M que transforma cada corba en una experiència memorable.",
        "features": [
            "Sistema de frens de carboni-ceràmica M (opcional)",
            "Diferencial actiu M a l'eix posterior",
            "Panell de control M amb configuració personalitzada",
            "Seients bàquet M en pell Merino",
            "Sistema d'escape M amb mode sport actiu",
            "Pantalla corba de 14,9'' amb sistema iDrive 9",
        ]
    },
    {
        "id": 2,
        "name": "Tesla Model Y",
        "category": "Elèctric",
        "year": "2026",
        "icon": "⚡",
        "img": "/static/img/nou2.jpg",
        "price": "44.990 €",
        "motor": "Motor elèctric dual (Long Range AWD)",
        "power": "393 CV",
        "torque": "493 Nm",
        "acceleration": "4,8 s (0-100 km/h)",
        "top_speed": "217 km/h",
        "transmission": "Monovelocitat automàtica",
        "traction": "Tracció integral (AWD)",
        "desc": "El Tesla Model Y 2026 ha rebut una actualització completa que el situa al capdavant del segment dels SUV elèctrics. Amb la nova bateria de cel·les 4680 de quarta generació, ofereix una autonomia de fins a 600 km i temps de càrrega rècord gràcies a la xarxa Supercharger V4 de Tesla.",
        "features": [
            "Autonomia de fins a 600 km (WLTP)",
            "Càrrega ràpida fins a 250 kW (Supercharger V4)",
            "Pantalla central de 15,4'' amb Tesla Software 16",
            "Pilot automàtic estàndard amb FSD disponible",
            "Interior sense instruments físics (tot digital)",
            "Sostre de vidre panoràmic tèrmic",
        ]
    },
    {
        "id": 3,
        "name": "Audi e-tron GT",
        "category": "Elèctric",
        "year": "2026",
        "icon": "🔋",
        "img": "/static/img/nou3.jpg",
        "price": "108.900 €",
        "motor": "Dos motors elèctrics (plataforma J1)",
        "power": "476 CV (598 CV en mode boost)",
        "torque": "640 Nm",
        "acceleration": "3,3 s (0-100 km/h)",
        "top_speed": "245 km/h",
        "transmission": "Monovelocitat (davant) / 2 velocitats (darrere)",
        "traction": "Tracció integral elèctrica (quattro)",
        "desc": "L'Audi e-tron GT 2026 és la berlina elèctrica d'altes prestacions que demostra que el futur elèctric pot ser emocionant. Compartint plataforma amb el Porsche Taycan, incorpora la nova bateria de 105 kWh amb tecnologia de càrrega de 350 kW, permetent recuperar el 80% en menys de 18 minuts.",
        "features": [
            "Bateria de 105 kWh amb càrrega fins a 350 kW",
            "Suspensió pneumàtica adaptativa de sèrie",
            "Diferencial esportiu actiu a l'eix posterior",
            "Sistema de so Bang & Olufsen 3D de 710 W",
            "Pantalla virtual cockpit plus de 12,3''",
            "Càrrega bidireccional Vehicle-to-Home (V2H)",
        ]
    },
    {
        "id": 4,
        "name": "Porsche 911 Turbo",
        "category": "Esportiu",
        "year": "2026",
        "icon": "🏁",
        "img": "/static/img/nou4.jpg",
        "price": "198.100 €",
        "motor": "3.8L Boxer de 6 cilindres biturbo",
        "power": "580 CV",
        "torque": "750 Nm",
        "acceleration": "2,7 s (0-100 km/h)",
        "top_speed": "320 km/h",
        "transmission": "PDK de 8 velocitats",
        "traction": "Tracció integral (Porsche Traction Management)",
        "desc": "El Porsche 911 Turbo 2026 és la culminació de més de 50 anys d'evolució contínua de l'icònic 911. La nova generació incorpora el sistema híbrid lleuger de 48V que aporta 50 CV addicionals en mode boost, juntament amb la nova aerodinàmica activa que genera 20% més de càrrega aerodinàmica que el seu predecessor.",
        "features": [
            "Sistema híbrid lleuger de 48V (+50 CV en boost)",
            "Aerodinàmica activa amb aleró posterior adaptatiu",
            "Suspensió PASM Sport de sèrie",
            "Frens de carboni-ceràmica PCCB (opcional)",
            "Sistema Porsche Torque Vectoring Plus (PTV+)",
            "Pantalla central tàctil de 10,9'' amb Apple CarPlay",
        ]
    },
]


# ── Routes ────────────────────────────────────────────────

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


@app.route("/cotxe/<int:car_id>")
def cotxe(car_id):
    car = next((c for c in NEW_CARS if c["id"] == car_id), None)
    if not car:
        return "Cotxe no trobat", 404
    return render_template("cotxe.html", car=car)


@app.route("/article/<int:article_id>")
def article(article_id):
    art = next((n for n in NEWS if n["id"] == article_id), None)
    if not art:
        return "Article no trobat", 404
    return render_template("article.html", article=art)


@app.route("/img-proxy")
def img_proxy():
    """Proxy per carregar imatges externes evitant bloquejos CORS."""
    url = request.args.get("url")
    if not url:
        return "", 400
    try:
        headers = {"User-Agent": "Mozilla/5.0 AutoEstima/1.0"}
        r = req.get(url, headers=headers, timeout=8)
        if r.status_code != 200:
            return "", 404
        return Response(r.content, content_type=r.headers.get("Content-Type", "image/jpeg"))
    except Exception:
        return "", 404


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = {
            "make":       request.form.get("make"),
            "fuel_type":  request.form.get("fuel_type"),
            "gear_type":  request.form.get("gear_type"),
            "sale_type":  request.form.get("sale_type"),
            "months_old": int(request.form.get("months_old")),
            "power":      int(request.form.get("power")),
            "kms":        int(request.form.get("kms")),
            "num_owners": int(request.form.get("num_owners")),
        }

        df_input  = pd.DataFrame([data])
        df_encoded = pd.get_dummies(df_input, columns=["make", "fuel_type", "gear_type", "sale_type"])

        for col in model.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[model.feature_names_in_]

        prediction = float(model.predict(df_encoded)[0])
        prediction = max(0, round(prediction / 100) * 100)

        MAE        = 2183
        price_low  = max(0, round((prediction - MAE) / 100) * 100)
        price_high = round((prediction + MAE) / 100) * 100

        def fmt(p):
            return f"{int(p):,}".replace(",", ".") + " €"

        return jsonify({
            "success":       True,
            "price":         int(prediction),
            "price_formatted": fmt(prediction),
            "price_low":     fmt(price_low),
            "price_high":    fmt(price_high),
            "price_low_raw": int(price_low),
            "price_high_raw": int(price_high),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/similar")
def similar():
    make      = request.args.get("make", "")
    fuel      = request.args.get("fuel", "")
    price_low = int(request.args.get("price_low", 0))
    price_high = int(request.args.get("price_high", 999999))
    predicted  = int(request.args.get("predicted", 0))

    filtered = df_data[
        (df_data["make"]      == make.lower()) &
        (df_data["fuel_type"] == fuel.lower()) &
        (df_data["price"]     >= price_low) &
        (df_data["price"]     <= price_high)
    ].copy()

    if len(filtered) < 6:
        margin   = price_high - price_low
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
            "success":    True,
            "count":      len(filtered),
            "avg_kms":    int(filtered["kms"].mean()),
            "avg_months": int(filtered["months_old"].mean()),
            "avg_power":  int(filtered["power"].mean()),
            "avg_price":  int(filtered["price"].mean()),
            "top_makes":  [{"name": k.title(), "count": v} for k, v in top_makes.items()],
            "top_fuels":  [{"name": k.title(), "count": v} for k, v in top_fuels.items()],
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
