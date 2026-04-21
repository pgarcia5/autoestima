import requests
from bs4 import BeautifulSoup

url = "https://www.coches.net/segunda-mano/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Guardem l'HTML complet en un fitxer per inspeccionar-lo
with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("✅ Fitxer pagina.html creat!")
print("Total caràcters:", len(response.text))