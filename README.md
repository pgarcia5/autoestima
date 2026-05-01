# 🚗 AutoEstima

> Sistema de predicció del preu de vehicles de segona mà mitjançant Machine Learning.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.2-green)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.1-orange)](https://scikit-learn.org)
[![Dataset](https://img.shields.io/badge/Dataset-82.372%20cotxes-yellow)](https://www.kaggle.com)

## Descripció

AutoEstima és una aplicació web que permet als usuaris estimar el valor de mercat d'un cotxe de segona mà. L'usuari introdueix les característiques del vehicle (marca, combustible, quilometres, antiguitat, etc.) i el sistema retorna una predicció de preu basada en un model de **Random Forest** entrenat amb dades reals del mercat espanyol.

## Característiques

- 🔮 **Predicció ML** amb rang de confiança (±2.183 €)
- 🚗 **Cotxes similars** del dataset per comparar
- 💰 **Cerca per pressupost** amb estadístiques del mercat
- 🏍️ **Secció de motos** amb preus reals de mercat
- 📰 **Articles de notícies** del sector automobilístic
- 🌙 **Mode clar / fosc**

## Estructura del projecte

```
autoestima/
├── scraper/            # Mòdul de scraping (Coches.net)
│   ├── scraper.py
│   └── utils.py
├── data/
│   ├── raw/            # Dataset original (Kaggle)
│   └── processed/      # Dataset net i preparat
├── ml/                 # Pipeline de Machine Learning
│   ├── preprocess.py   # Neteja i transformació de dades
│   ├── train.py        # Entrenament dels models
│   └── evaluate.py     # Avaluació i mètriques
├── models/             # Model entrenat (best_model.pkl)
├── notebooks/
│   └── eda.ipynb       # Anàlisi Exploratòria de Dades
├── web/                # Aplicació web Flask
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── similar.html
│   │   └── article.html
│   └── static/
│       ├── style.css
│       ├── main.js
│       └── images.js
├── requirements.txt
└── README.md
```

## Resultats del Model

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Linear Regression | 3.814 € | 6.725 € | 0.760 |
| **Random Forest** | **2.183 €** | **4.315 €** | **0.901** |
| Gradient Boosting | 2.312 € | 4.419 € | 0.897 |

**Model escollit: Random Forest** — millor R² (0.901) i menor MAE (2.183 €).

## Dataset

- **Font**: [Kaggle — Online Ads of Used Cars (Spain)](https://www.kaggle.com/datasets/harturo123/online-adds-of-used-cars)
- **Registres originals**: 93.991
- **Registres nets**: 82.372
- **Variables**: marca, combustible, canvi, estat, antiguitat, potència, quilometres, propietaris

## Instal·lació

```bash
# Clonar el repositori
git clone https://github.com/el-teu-usuari/autoestima.git
cd autoestima

# Crear entorn virtual
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Instal·lar dependències
pip install -r requirements.txt
```

## Ús

```bash
# Entrenar el model (opcional, ja inclou best_model.pkl)
python -m ml.train

# Iniciar l'aplicació web
cd web
python app.py
```

Obre el navegador a `http://localhost:5000`

## Tecnologies

| Categoria | Tecnologies |
|---|---|
| Scraping | requests, BeautifulSoup4, Selenium |
| Dades | pandas, numpy |
| ML | scikit-learn (Random Forest, GradientBoosting, LinearRegression) |
| Web | Flask, HTML5, CSS3, JavaScript |
| Visualització | matplotlib, seaborn |

## Autor

Projecte Final d'Especialització — Intel·ligència Artificial i Big Data
