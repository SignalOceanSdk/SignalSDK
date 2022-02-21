
from decimal import Decimal
from typing import Optional, Callable, TypeVar, Tuple, List, Iterable
from datetime import date, datetime
from .._internals import format_iso_date, QueryString


import requests

from .models import ScrapedFixture
from ..connection import Connection
from .._internals import as_decimal

class Pagination:
    """
    Iterator for fixture pagination
    """

    def __init__(self) -> None:
        self.page_number = 1
        
    def __iter__(self):
        return self


class ScrapedFixturesAPI:
    """Represents Signal's Scraped Fixtures API."""

    relative_url = "scraped-fixtures-api/api/public/v1/fixtures"

    page_size = 1000

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Scraped Fixturess API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()
        self.__current_page_number = 1

    def get_fixtures(
        self, 
        received_date_from: date, 
        received_date_to: date,
        vessel_type: int,
        )-> Iterable[ScrapedFixture]:
        
        """
        1. 
        """

        more_fixtues = True
        
        results: List[ScrapedFixture] = []

        while more_fixtues:
            query_string: QueryString = {
                "PageNumber": self.__current_page_number,
                "PageSize": self.page_size,
                "ReceivedDateFrom": format_iso_date(received_date_from),
                "ReceivedDateTo": format_iso_date(received_date_to),
                "VesselType": vessel_type,
            }

            

            self.__current_page_number

    