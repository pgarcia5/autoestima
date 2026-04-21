import requests

url = "https://api.wallapop.com/api/v3/general/search"
params = {
    "keywords": "coche",
    "category_ids": "100",
    "country_code": "ES",
    "start": "0",
    "step": "5"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://es.wallapop.com/",
    "Origin": "https://es.wallapop.com"
}

response = requests.get(url, params=params, headers=headers)
print("Codi:", response.status_code)
print(response.text[:500])