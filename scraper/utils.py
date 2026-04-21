"""
utils.py
--------
Helper functions for the scraper (headers, delays, CSV saving).
"""

import csv
import time
import random
import logging

logger = logging.getLogger(__name__)


def get_headers() -> dict:
    """Return HTTP headers to mimic a real browser."""
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }


def random_delay(min_s: float = 1.5, max_s: float = 3.5) -> None:
    """Wait a random amount of time to avoid being blocked."""
    delay = random.uniform(min_s, max_s)
    logger.debug(f"Waiting {delay:.1f}s...")
    time.sleep(delay)


def save_to_csv(data: list[dict], filepath: str) -> None:
    """
    Save a list of dicts to a CSV file.

    Args:
        data: List of dicts to save.
        filepath: Destination path for the CSV.
    """
    if not data:
        logger.warning("No data to save.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"💾 Saved {len(data)} rows to {filepath}")
