"""Scraped Fixtures API Package.

Classes:
    ScrapedFixturesAPI: Represents Signal's Scraped Fixtures API.
    ScrapedFixture: Scraped Fixture.
"""

from .scraped_fixtures_api import ScrapedFixturesAPI
from .models import ScrapedFixture

__all__ = ["ScrapedFixturesAPI", "ScrapedFixture"]
