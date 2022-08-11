"""Scraped Cargoes API Package.

Classes:
    ScrapedCargoesAPI: Represents Signal's Scraped Cargoes API.
    ScrapedCargo: Scraped Cargo.
"""

from .scraped_cargoes_api import ScrapedCargoesAPI
from .models import ScrapedCargo

__all__ = ["ScrapedCargoesAPI", "ScrapedCargo"]
