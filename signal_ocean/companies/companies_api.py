"""The companies api."""
from typing import Optional, Tuple
from urllib.parse import urljoin

from signal_ocean import Connection
from signal_ocean.companies.models import Company
from signal_ocean.util.request_helpers import get_single, get_multiple


class CompaniesAPI:
    """Represents Signal's Companies API."""

    relative_url = "companies-api/v1/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes CompaniesAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_company(self, company_id: int) -> Optional[Company]:
        """Retrieves a company by its id.

        Args:
            company_id: Unique id of the company to retrieve.

        Returns:
            A company or None if no company with the specified id has
            been found.
        """
        url = urljoin(CompaniesAPI.relative_url, f"companies/{company_id}")
        return get_single(self.__connection, url, Company)

    def get_companies(self, name: Optional[str] = None) -> Tuple[Company, ...]:
        """Retrieves all available companies.

        Args:
            name: String to filter and return only companies the name
                of which contains the provided string. If None, all
                companies are returned.

        Returns:
            A tuple of all available companies.
        """
        endpoint = (
            "companies/all"
            if name is None
            else f"companies/searchByName/{name}"
        )
        url = urljoin(CompaniesAPI.relative_url, endpoint)
        return get_multiple(self.__connection, url, Company)
