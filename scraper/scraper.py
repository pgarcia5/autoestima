"""
scraper.py
----------
Main scraping logic for Coches.net using Selenium.
Extracts: title, brand, price, year, km, fuel type, province.
"""

import re
import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from scraper.utils import random_delay, save_to_csv

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.coches.net/segunda-mano/"


def create_driver() -> webdriver.Chrome:
    """
    Create and configure a headless Chrome WebDriver.

    Returns:
        Configured Chrome WebDriver instance.
    """
    options = Options()
    #options.add_argument("--headless")           # No obrir finestra del navegador
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    # Evitar detecció de bot
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_page_source(driver: webdriver.Chrome, page_num: int) -> str | None:
    """
    Navigate to a listing page and return fully rendered HTML.

    Args:
        driver: Selenium WebDriver instance.
        page_num: Page number to fetch.

    Returns:
        Rendered HTML as string or None if error.
    """
    url = f"{BASE_URL}?pg={page_num}"
    try:
        driver.get(url)
        # Esperar que les targetes de cotxes carreguin
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-CardAd"))
        )
        return driver.page_source
    except Exception as e:
        logger.error(f"Error loading page {page_num}: {e}")
        return None


def parse_listings(html: str) -> list[dict]:
    """
    Parse all car listings from rendered HTML.

    Args:
        html: Fully rendered HTML of the listing page.

    Returns:
        List of dicts with car data.
    """
    listings = []
    soup = BeautifulSoup(html, "lxml")

    cards = soup.select(".mt-CardAd")
    if not cards:
        logger.warning("No cards found on page.")
        return listings

    # Anys des del JSON incrustat
    scripts = soup.find_all("script")
    script_text = " ".join(s.get_text() for s in scripts)
    years = re.findall(r'"year"\s*:\s*(\d{4})', script_text)

    for i, card in enumerate(cards):
        try:
            # Títol
            title_tag = card.select_one(".mt-CardAd-titleHiglight")
            title = title_tag.get_text(strip=True) if title_tag else ""

            # Marca
            brand_tag = card.select_one(".sui-TagChip-link")
            brand = brand_tag.get_text(strip=True) if brand_tag else ""

            # Preu
            price_tag = card.select_one(".mt-CardAdPrice-cashAmount")
            price_text = price_tag.get_text(strip=True) if price_tag else ""
            price = re.sub(r"[^\d]", "", price_text)

            # Quilometratge i combustible
            attrs = card.select(".mt-CardAd-attrItem")
            km_text = attrs[0].get_text(strip=True) if len(attrs) > 0 else ""
            fuel = attrs[1].get_text(strip=True) if len(attrs) > 1 else ""
            km = re.sub(r"[^\d]", "", km_text)

            # Província
            province_tag = card.select_one(".mt-CardAd-location")
            province = province_tag.get_text(strip=True) if province_tag else ""

            # Any
            year = years[i] if i < len(years) else ""

            listings.append({
                "title": title,
                "brand": brand,
                "price": price,
                "year": year,
                "km": km,
                "fuel": fuel,
                "province": province,
            })

        except Exception as e:
            logger.warning(f"Error parsing card {i}: {e}")
            continue

    return listings


def scrape_listings(max_pages: int = 10) -> list[dict]:
    """
    Scrape multiple pages of car listings from Coches.net.

    Args:
        max_pages: Number of pages to scrape.

    Returns:
        List of dicts with all scraped car data.
    """
    all_listings = []
    driver = create_driver()

    try:
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page}/{max_pages}...")

            html = get_page_source(driver, page)
            if html is None:
                logger.warning(f"Skipping page {page}.")
                continue

            listings = parse_listings(html)

            if not listings:
                logger.info(f"No listings on page {page}. Stopping.")
                break

            all_listings.extend(listings)
            logger.info(f"Page {page}: {len(listings)} found. Total: {len(all_listings)}")

            random_delay(2.0, 4.0)

    finally:
        driver.quit()
        logger.info("Browser closed.")

    return all_listings


if __name__ == "__main__":
    data = scrape_listings(max_pages=10)
    save_to_csv(data, "data/raw/coches_raw.csv")
    logger.info(f"✅ Done! {len(data)} listings saved.")
