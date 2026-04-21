# 🚗 AutoEstima

> Predicció del preu de vehicles de segona mà mitjançant Machine Learning.

## Descripció

AutoEstima és un sistema de predicció de preus de cotxes de segona mà entrenat amb dades reals obtingudes de Coches.net. L'usuari pot introduir les característiques d'un vehicle i obtenir una estimació del seu preu de mercat.

## Estructura del projecte

```
autoestima/
├── scraper/        # Scraping de Coches.net
├── data/           # Dades raw i processades
├── ml/             # Entrenament i avaluació del model
├── web/            # Aplicació web Flask
├── notebooks/      # Anàlisi exploratòria (EDA)
└── models/         # Model entrenat serialitzat
```

## Instal·lació

```bash
# Clonar el repositori
git clone https://github.com/el-teu-usuari/autoestima.git
cd autoestima

# Crear entorn virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instal·lar dependències
pip install -r requirements.txt
```

## Ús

```bash
# 1. Executar el scraper
python -m scraper.scraper

# 2. Entrenar el model
python -m ml.train

# 3. Iniciar la web
python web/app.py
```

## Tecnologies

- **Scraping**: requests, BeautifulSoup4
- **Data**: pandas, numpy
- **ML**: scikit-learn
- **Web**: Flask

## Autor

Projecte final — Especialització en Intel·ligència Artificial i Big Data
